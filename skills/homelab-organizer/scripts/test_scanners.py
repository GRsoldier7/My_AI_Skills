"""Regression tests for the homelab-organizer scanners.

Each test pins one defect found in the 2026-10-05 / 2026-10-14 audits. Run against
another copy of the scripts (e.g. the pre-fix ones) with SCRIPTS_DIR=<dir>.

    python3 -m unittest -v test_scanners.py
"""

import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

SCRIPTS = Path(os.environ.get('SCRIPTS_DIR', Path(__file__).resolve().parent))
OLD = time.time() - 200 * 86400


def write(path: Path, text: str = 'x\n', old: bool = True) -> Path:
    """Create a fixture file, back-dated past the 90-day stale threshold unless old=False."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if old:
        os.utime(path, (OLD, OLD))
    return path


class ScannerCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / 'root'
        self.root.mkdir()
        self.organizer = self.root / 'docs' / 'organizer'
        # Stands in for ~/.claude/skills: symlinks OUTSIDE the scanned roots that point into them
        self.linkhome = Path(self._tmp.name) / 'linkhome'
        self.linkhome.mkdir()
        # Stands in for operator memory, runbook dirs and the cron/systemd homes: no test reads the live ones
        self.sys = Path(self._tmp.name) / 'sys'
        (self.sys / 'inuse').mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_script(self, name: str, roots: list[Path] | None = None, /, **env_extra: str) -> tuple[int, dict | None]:
        env = {**os.environ, 'ORGANIZER_ROOTS': ' '.join(map(str, roots or [self.root])), 'SCAN_ROOT_TOP': '0',
               'ORGANIZER_DIR': str(self.organizer), 'AUDIT_DIR': str(self.organizer / 'AUDIT-test'),
               'ORGANIZER_SYMLINK_DIRS': str(self.linkhome),
               'ORGANIZER_INUSE_FILES': str(self.sys / 'MEMORY.md'), 'ORGANIZER_INUSE_DIRS': str(self.sys / 'inuse'),
               'ORGANIZER_SYS_REF_FILES': str(self.sys / 'cron'),
               # Pinned to the defaults so a floor exported in the operator's shell cannot move a fixture's bucket
               'STALE_DAYS': '90', 'SAFE_DAYS': '7', **env_extra}
        proc = subprocess.run(['bash', str(SCRIPTS / name)], capture_output=True, text=True,
                              env=env, timeout=120, check=False)
        self.last_stderr = proc.stderr
        try:
            return proc.returncode, json.loads(proc.stdout)
        except json.JSONDecodeError:
            return proc.returncode, None

    def scan(self, roots: list[Path] | None = None) -> dict:
        rc, data = self.run_script('scan-files.sh', roots)
        self.assertEqual(rc, 0)
        if data is None:
            self.fail('scan-files.sh did not emit valid JSON')
        return data

    def bucket_of(self, data: dict, path: Path) -> str | None:
        for name, entries in data['categorized'].items():
            if any(e and e['path'] == str(path) for e in entries):
                return name
        return None


class ScanFilesTest(ScannerCase):
    def test_empty_buckets_emit_valid_json(self) -> None:
        # #7: `declare -a` + set -u crashed the emit when any bucket was empty
        write(self.root / 'fresh.md', old=False)
        data = self.scan()
        self.assertEqual(data['categorized']['SAFE_QUARANTINE'], [])

    def test_prior_audit_output_is_not_a_reference(self) -> None:
        # #15: AUDIT-*/files.json names every candidate, so each audit hid the next one's findings
        orphan = write(self.root / 'zq-orphan-note.md')
        write(self.organizer / 'AUDIT-old' / 'files.json', json.dumps({'path': str(orphan)}))
        self.assertEqual(self.bucket_of(self.scan(), orphan), 'SAFE_QUARANTINE')

    def test_house_date_prefix_is_dated(self) -> None:
        # #9: only YYYY-MM-DD was recognised; the house convention is "YYYYMMDD - Description"
        report = write(self.root / '20250101 - Zq Old Report.md')
        self.assertEqual(self.bucket_of(self.scan(), report), 'DATED_HISTORICAL')

    def test_python_module_imported_by_name_is_in_use(self) -> None:
        # #11: "from pkg.zq_helper_mod import x" never contains the string "zq_helper_mod.py"
        helper = write(self.root / 'pkg' / 'zq_helper_mod.py', 'def thing():\n    return 1\n')
        write(self.root / 'pkg' / 'zq_app.py', 'from pkg.zq_helper_mod import thing\n')
        data = self.scan()
        self.assertNotEqual(self.bucket_of(data, helper), 'SAFE_QUARANTINE')

    def test_generated_cache_is_not_walked(self) -> None:
        # #12: .mypy_cache alone produced 2,669 false SAFE entries
        cached = write(self.root / '.mypy_cache' / 'zq.json', '{}')
        self.assertIsNone(self.bucket_of(self.scan(), cached))

    def test_credential_paths_are_never_read(self) -> None:
        # #5: the ref index grepped every walked file before the per-file floor ran. A read is
        # observable: if any credential-class file is indexed, its mention gives the target a ref.
        target = write(self.root / 'zq-plain-target.md')
        in_dir = write(self.root / 'Secrets' / 'zq-notes.md', 'zq-plain-target.md\n')
        by_name = write(self.root / 'zq_api_token.json', '"zq-plain-target.md"\n')
        by_pw = write(self.root / 'zq-db-password.yaml', 'x: zq-plain-target.md\n')
        data = self.scan()
        self.assertEqual(self.bucket_of(data, target), 'SAFE_QUARANTINE')
        for f in (in_dir, by_name, by_pw):
            self.assertIsNone(self.bucket_of(data, f))

    def test_token_named_code_is_still_a_reference_source(self) -> None:
        # F2: a name filter meant for credential DATA files also dropped tokenizer.py-style code and
        # docs as reference sources, so the files they cite looked unreferenced
        cited = write(self.root / 'zq-cited-by-doc.md')
        write(self.root / 'zq-token-budget.md', 'see zq-cited-by-doc.md\n')
        self.assertEqual(self.bucket_of(self.scan(), cited), 'WATCHLIST')

    def test_parenthesised_import_is_in_use(self) -> None:
        # F1: "from pkg.mod import (" has no name after import, so the import regex skipped it
        mod = write(self.root / 'pkg' / 'zq_paren_mod.py', 'def thing():\n    return 1\n')
        write(self.root / 'pkg' / 'zq_app2.py', 'from pkg.zq_paren_mod import (\n    thing,\n)\n')
        self.assertNotEqual(self.bucket_of(self.scan(), mod), 'SAFE_QUARANTINE')

    def test_file_inside_symlinked_dir_is_in_use(self) -> None:
        # F5: ~/.claude/skills/<x> -> My_AI_Skills/skills/<x>; every file in a linked dir is live
        inside = write(self.root / 'skillx' / 'scripts' / 'zq-live-script.sh', '#!/bin/sh\n')
        (self.linkhome / 'skillx').symlink_to(self.root / 'skillx')
        self.assertEqual(self.bucket_of(self.scan(), inside), 'WATCHLIST')

    def test_regex_metachar_in_name_still_counts_refs(self) -> None:
        # F6: count_refs used the basename as a regex; "[" made grep error out -> refs 0 -> SAFE
        bracket = write(self.root / 'zq[1].md')
        write(self.root / 'zq-citer.md', 'see zq[1].md\n')
        self.assertEqual(self.bucket_of(self.scan(), bracket), 'WATCHLIST')

    def test_quote_in_path_keeps_json_valid(self) -> None:
        # F4: paths were interpolated into JSON unescaped; audit.sh now aborts on invalid JSON
        write(self.root / 'zq"quoted\\name.md')
        self.scan()

    def test_duplicate_carries_refs_and_in_use(self) -> None:
        # #10: duplicates skipped the ref + in-use checks, so a cited copy was proposed for quarantine
        write(self.root / 'a' / 'zq-dup.md', 'same\n')
        write(self.root / 'b' / 'zq-dup.md', 'same\n')
        dups = [d for d in self.scan()['categorized']['DUPLICATE'] if d]
        self.assertEqual(len(dups), 1)
        self.assertIn('refs', dups[0])
        self.assertIn('in_use_signals', dups[0])

    def test_symlink_target_is_in_use(self) -> None:
        # #13: safety-rules.md lists symlink targets as in-use; the scanner never checked
        target = write(self.root / 'zq-linked-target.sh', '#!/bin/sh\n')
        (self.root / 'zq-link').symlink_to(target)
        self.assertEqual(self.bucket_of(self.scan(), target), 'WATCHLIST')

    def test_file_named_by_cron_is_in_use(self) -> None:
        # safety-rules.md: a path named by cron or a systemd unit is in use. Only the override seam is
        # pinned: the live crontab/systemd branch is untested by design, since no test reads live sources
        job = write(self.root / 'zq-nightly-job.sh', '#!/bin/sh\n')
        write(self.sys / 'cron', f'0 3 * * * root {job}\n')
        self.assertEqual(self.bucket_of(self.scan(), job), 'WATCHLIST')

    def test_file_named_in_operator_memory_is_in_use(self) -> None:
        note = write(self.root / 'zq-remembered-note.md')
        write(self.sys / 'MEMORY.md', '- see zq-remembered-note.md\n')
        self.assertEqual(self.bucket_of(self.scan(), note), 'WATCHLIST')

    def test_file_named_in_runbook_dir_is_in_use(self) -> None:
        script = write(self.root / 'zq-runbook-step.sh', '#!/bin/sh\n')
        write(self.sys / 'inuse' / 'restore.md', 'run zq-runbook-step.sh\n')
        self.assertEqual(self.bucket_of(self.scan(), script), 'WATCHLIST')

    def test_ref_index_covers_every_walked_file(self) -> None:
        # #6: past 5,000 walked files the ref index kept only the first 2,000, so anything in a
        # later root read as 0 refs -> SAFE. Fresh filler stays under the SAFE_DAYS floor (cheap)
        bulk = Path(self._tmp.name) / 'bulk'
        for i in range(5001):
            write(bulk / f'f{i}.md', old=False)
        cited = write(self.root / 'zq-cited-late.md')
        write(self.root / 'zq-late-citer.md', 'see zq-cited-late.md\n')
        self.assertEqual(self.bucket_of(self.scan([bulk, self.root]), cited), 'WATCHLIST')

    def test_active_override_is_announced(self) -> None:
        # A seam left exported in the operator's shell narrows the walk or the in-use sources — the
        # false-SAFE direction — so every run that uses one must say so
        self.scan()
        for var in ('ORGANIZER_ROOTS', 'ORGANIZER_SYMLINK_DIRS', 'ORGANIZER_DIR', 'ORGANIZER_INUSE_FILES',
                    'ORGANIZER_INUSE_DIRS', 'ORGANIZER_SYS_REF_FILES', 'SCAN_ROOT_TOP=0'):
            with self.subTest(var):
                self.assertIn(var, self.last_stderr)

    def test_unset_override_is_not_announced(self) -> None:
        # Positive control in the same run: a set seam is named, an empty one is not
        self.run_script('scan-files.sh', ORGANIZER_DIR='')
        self.assertIn('ORGANIZER_ROOTS', self.last_stderr)
        self.assertNotIn('ORGANIZER_DIR', self.last_stderr)
        self.assertNotIn('_DAYS', self.last_stderr)

    def test_tuned_day_floor_is_announced(self) -> None:
        # A tuned floor changes which files can go SAFE as much as a narrowed root does
        self.run_script('scan-files.sh', STALE_DAYS='30', SAFE_DAYS='3')
        self.assertIn('STALE_DAYS=30', self.last_stderr)
        self.assertIn('SAFE_DAYS=3', self.last_stderr)

    def test_malformed_day_floor_aborts(self) -> None:
        # "7d" made the (( )) age test error out, which reads as false: a 30-day-old file went SAFE.
        # "090" fails the same way (bash reads a leading 0 as octal); "-5" parses but leaves no floor;
        # 2**63 wraps negative in 64-bit (( )) and also leaves no floor
        young = write(self.root / 'zq-young.md', old=False)
        month = time.time() - 30 * 86400
        os.utime(young, (month, month))
        for var, value in (('STALE_DAYS', '7d'), ('STALE_DAYS', '090'), ('STALE_DAYS', '-5'),
                           ('STALE_DAYS', '9223372036854775808'), ('SAFE_DAYS', '1w')):
            with self.subTest(f'{var}={value}'):
                rc, data = self.run_script('scan-files.sh', **{var: value})
                self.assertNotEqual(rc, 0)
                self.assertIsNone(data)


class CheckLinksTest(ScannerCase):
    def links(self) -> dict:
        rc, data = self.run_script('check-links.sh')
        self.assertEqual(rc, 0)
        if data is None:
            self.fail('check-links.sh did not emit valid JSON')
        return data

    def broken_targets(self) -> list[str]:
        return [b['target'] for b in self.links()['broken_md_links'] if b]

    def test_missing_relative_link_is_reported(self) -> None:
        # #1: the inline [[ =~ ]] regex never matched — the md check was dead since creation
        write(self.root / 'doc.md', 'see [x](./zq-missing.md)\n')
        self.assertIn('./zq-missing.md', self.broken_targets())

    def test_existing_absolute_link_is_not_reported(self) -> None:
        # #2: absolute targets had the .md's directory prepended
        real = write(self.root / 'real.md')
        write(self.root / 'sub' / 'doc.md', f'see [x]({real})\n')
        self.assertNotIn(str(real), self.broken_targets())

    def test_link_inside_code_fence_is_ignored(self) -> None:
        # #17: fenced examples were reported as broken links
        write(self.root / 'doc.md', 'text\n```\n[x](./zq-fenced.md)\n```\n')
        self.assertNotIn('./zq-fenced.md', self.broken_targets())

    def test_fence_closes_only_on_its_own_marker(self) -> None:
        # Any ``` or ~~~ line toggled the fence, so a nested marker closed it early and the real
        # closer reopened it — every link after the block was hidden
        cases = {
            'tilde inside backticks': '```\n~~~\n```\n',
            'short run inside long run': '````\n```\n````\n',
            'info string is not a closer': '```\n```python\n```\n',
        }
        for name, fenced in cases.items():
            with self.subTest(name):
                write(self.root / 'doc.md', f'{fenced}[x](./zq-after-fence.md)\n')
                self.assertIn('./zq-after-fence.md', self.broken_targets())

    def test_inline_triple_backticks_do_not_open_a_fence(self) -> None:
        # CommonMark: a backtick fence's info string cannot hold a backtick, so ```x``` is inline code
        write(self.root / 'doc.md', '```x``` is inline\n[y](./zq-after-inline.md)\n')
        self.assertIn('./zq-after-inline.md', self.broken_targets())

    def test_unclosed_fence_is_reported(self) -> None:
        # A stray opener hides every later link (CommonMark-correct), so the hidden region must surface
        write(self.root / 'doc.md', 'text\n```\n[x](./zq-hidden.md)\n')
        unclosed = self.links().get('unclosed_fences') or []
        self.assertEqual([(Path(u['in_file']).name, u['line']) for u in unclosed if u], [('doc.md', 2)])

    def test_closed_fence_is_not_reported_unclosed(self) -> None:
        write(self.root / 'doc.md', '```\n[x](./zq-fenced.md)\n```\n')
        self.assertEqual(self.links().get('unclosed_fences'), [])

    def test_active_root_override_is_announced(self) -> None:
        self.links()
        self.assertIn('ORGANIZER_ROOTS', self.last_stderr)

    def test_backslash_in_link_keeps_json_valid(self) -> None:
        # F4: markdown-escaped "\_" in a broken link target produced an illegal JSON escape
        write(self.root / 'doc.md', 'see [x](zq\\_missing.md)\n')
        self.assertIn('zq\\_missing.md', self.broken_targets())

    def test_credential_dirs_not_walked_for_links(self) -> None:
        # F7: check-links read .md files under credential-class dirs
        write(self.root / 'secrets' / 'doc.md', 'see [x](./zq-in-secrets.md)\n')
        self.assertNotIn('./zq-in-secrets.md', self.broken_targets())

    def test_unimplemented_import_check_is_null_not_clean(self) -> None:
        # #4: broken_imports was never implemented but reported [] — a clean result it never earned
        write(self.root / 'doc.md', 'nothing\n')
        self.assertIsNone(self.links()['broken_imports'])

    def test_every_md_file_and_link_line_is_checked(self) -> None:
        # #3: head -500 capped both the .md file list and the link lines per file, silently
        for i in range(510):
            write(self.root / 'many' / f'd{i}.md', f'[x](./zq-m{i}.md)\n')
        write(self.root / 'long.md', ''.join(f'[x](./zq-l{i}.md)\n' for i in range(510)))
        self.assertEqual(len(self.broken_targets()), 1020)

    def test_every_sh_file_and_source_line_is_checked(self) -> None:
        # #3: head -300 capped the .sh file list and head -50 the source lines per file
        for i in range(310):
            write(self.root / 'many' / f's{i}.sh', f'source ./zq-s{i}.sh\n')
        write(self.root / 'long.sh', ''.join(f'source ./zq-t{i}.sh\n' for i in range(60)))
        self.assertEqual(len([b for b in self.links()['broken_sources'] if b]), 370)


PCT_STUB = """#!/bin/sh
case "$1" in
  list) printf 'VMID       Status     Lock         Name\\n101        stopped                 ct-a\\n' ;;
  status) echo 'status: stopped' ;;
  config) printf 'hostname: ct-a\\nmemory: 512\\n' ;;
esac
"""
QM_STUB = """#!/bin/sh
case "$1" in
  list) printf '      VMID NAME     STATUS     MEM(MB)    BOOTDISK(GB) PID\\n       110 vm-b     stopped    2048       32.00        0\\n' ;;
  status) echo 'status: stopped' ;;
  config) printf 'name: vm-b\\nmemory: 2048\\n' ;;
esac
"""


class InventoryContainersTest(unittest.TestCase):
    # Stubbed pct/qm: CT 101 has no doc; VM 110's doc sits in lxc/ (misfiled); vms/ is empty
    def inventory(self) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            stubs = Path(tmp) / 'bin'
            stubs.mkdir()
            for name, body in (('pct', PCT_STUB), ('qm', QM_STUB), ('hostname', '#!/bin/sh\necho node-a\n')):
                (stubs / name).write_text(body)
                (stubs / name).chmod(0o755)
            (Path(tmp) / 'lxc' / '110-misfiled').mkdir(parents=True)
            (Path(tmp) / 'vms').mkdir()
            (Path(tmp) / 'containers').mkdir()
            env = {**os.environ, 'PATH': f'{stubs}:{os.environ["PATH"]}', 'STATE_FILE': f'{tmp}/state.yaml',
                   'HOMELAB_LXC_DOC': f'{tmp}/lxc', 'HOMELAB_VM_DOC': f'{tmp}/vms', 'HOMELAB_CT_DOC': f'{tmp}/containers'}
            proc = subprocess.run(['bash', str(SCRIPTS / 'inventory-containers.sh')], capture_output=True,
                                  text=True, env=env, timeout=60, check=False)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        # Guard: the stubs, never the live node, answered
        self.assertEqual(sorted(c['id'] for c in data['containers']), ['101', '110'])
        return data

    def test_vm_hostname_comes_from_name_field(self) -> None:
        # #14: qm config says name:, not hostname:, so every VM hostname was blank
        vm = next(c for c in self.inventory()['containers'] if c['id'] == '110')
        self.assertEqual(vm['hostname'], 'vm-b')

    def test_misfiled_doc_is_reported(self) -> None:
        # #14: naming_mismatches was a hardcoded [] although the loop above it filled the array
        self.assertEqual(len(self.inventory()['drift_summary']['naming_mismatches']), 1)

    def test_empty_drift_list_is_an_empty_array(self) -> None:
        # #14: printf over an empty array emitted [""] — one phantom orphaned doc
        self.assertEqual(self.inventory()['drift_summary']['orphaned_docs'], [])

    def test_drift_names_the_nodes_it_checked(self) -> None:
        # Unclustered nodes: a peer node's guest doc folder read as orphaned here, and only a hand check on
        # the peer stopped the archive. The scope has to travel in the data, not only in prose
        self.assertEqual(self.inventory()['drift_summary']['checked_nodes'], ['node-a'])


class AuditOrchestratorTest(unittest.TestCase):
    def test_crashed_phase_stops_the_audit(self) -> None:
        # #8: audit.sh printed "Intermediates ready" over a phase that crashed
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / 'scripts'
            scripts.mkdir()
            (scripts / 'audit.sh').write_text((SCRIPTS / 'audit.sh').read_text())
            (scripts / 'scan-files.sh').write_text('echo "{"\nexit 3\n')
            proc = subprocess.run(['bash', str(scripts / 'audit.sh'), 'files'], capture_output=True,
                                  text=True, env={**os.environ, 'ORGANIZER_DIR': tmp}, timeout=60, check=False)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('FAILED', proc.stderr)


class QuarantineTest(unittest.TestCase):
    """quarantine.sh must move exactly the path named on stdin and record a paste-safe restore."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.archive = self.tmp / 'archive'

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def quarantine(self, *lines: str) -> str:
        env = {**os.environ, 'ARCHIVE_ROOT': str(self.archive), 'AUDIT_DATE': 'test'}
        proc = subprocess.run(['bash', str(SCRIPTS / 'quarantine.sh')], input=''.join(f'{x}\n' for x in lines),
                              capture_output=True, text=True, env=env, timeout=60, check=False)
        self.assertEqual(proc.returncode, 0)
        manifest = self.archive / 'test' / 'MANIFEST.md'
        return manifest.read_text() if manifest.exists() else ''

    def archived(self, src: Path) -> Path:
        return self.archive / 'test' / str(src).lstrip('/')

    def test_backslash_name_moves_that_file_not_its_lookalike(self) -> None:
        # xargs, used as a trim, ate the backslash: "zq\b.md" became "zqb.md" and the lookalike moved
        target = write(self.tmp / 'src' / 'zq\\b.md', 'target\n')
        lookalike = write(self.tmp / 'src' / 'zqb.md', 'lookalike\n')
        self.quarantine(f'{target} | test')
        self.assertTrue(self.archived(target).exists())
        self.assertTrue(lookalike.exists())

    def test_quote_and_space_runs_survive_the_trim(self) -> None:
        # xargs aborted on an unmatched quote and collapsed runs of spaces, so both names read as missing
        for name in ("zq it's.md", 'zq  two  spaces.md'):
            with self.subTest(name):
                src = write(self.tmp / 'src' / name)
                manifest = self.quarantine(f'  {src}  |  test  ')
                self.assertTrue(self.archived(src).exists())
                self.assertIn('- reason: test\n', manifest)

    def test_manifest_hash_is_the_content_digest(self) -> None:
        # sha256sum prefixes its output with "\" when the NAME holds a backslash
        src = write(self.tmp / 'src' / 'zq\\h.md', 'payload\n')
        digest = hashlib.sha256(b'payload\n').hexdigest()[:12]
        self.assertIn(f'- hash: {digest}\n', self.quarantine(str(src)))

    def test_restore_command_is_paste_safe(self) -> None:
        # The restore line put names inside double quotes, so a "$(...)" in a name ran on paste
        src = write(self.tmp / 'src' / 'zq$(touch pwned) "q".md', 'r\n')
        found = re.search(r'^- restore: `(.*)`$', self.quarantine(str(src)), re.MULTILINE)
        if found is None:
            self.fail('manifest has no restore line')
        subprocess.run(['bash', '-c', found.group(1)], cwd=self.tmp, capture_output=True, timeout=30, check=False)
        self.assertFalse((self.tmp / 'pwned').exists())
        self.assertTrue(src.exists())


class RestoreTest(unittest.TestCase):
    """restore.sh must put back exactly the archived entry it was asked for, and never overwrite."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.archive = self.tmp / 'archive'

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def archived(self, date: str, original: Path, text: str = 'archived\n') -> Path:
        """Place a fixture where quarantine.sh would have archived `original` on `date`."""
        return write(self.archive / date / str(original).lstrip('/'), text)

    def restore(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(['bash', str(SCRIPTS / 'restore.sh'), *args], capture_output=True, text=True,
                              env={**os.environ, 'ARCHIVE_ROOT': str(self.archive)}, timeout=60, check=False)

    def test_by_original_matches_the_name_literally(self) -> None:
        # find -path read the name as a glob: "zq[1] \b.md" found the archived "zq1 b.md" and restored it
        target = self.tmp / 'src' / 'zq[1] \\b.md'
        lookalike = self.tmp / 'src' / 'zq1 b.md'
        self.archived('d1', target, 'target\n')
        kept = self.archived('d1', lookalike, 'lookalike\n')
        proc = self.restore('--by-original', str(target))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(target.read_text(), 'target\n')
        self.assertTrue(kept.exists())

    def test_restore_never_overwrites_a_live_file(self) -> None:
        # mv replaced whatever had been written at the original path since the quarantine
        original = write(self.tmp / 'src' / 'zq-live.md', 'newer\n')
        copy = self.archived('d1', original)
        for args in (('--by-original', str(original)), (str(copy),)):
            with self.subTest(args[0]):
                proc = self.restore(*args)
                self.assertEqual(proc.returncode, 1)
                self.assertIn('REFUSE(exists)', proc.stderr)
                self.assertEqual(original.read_text(), 'newer\n')
                self.assertTrue(copy.exists())

    def test_by_original_refuses_an_entry_archived_twice(self) -> None:
        # find | head -1 picked one copy in directory order, so which version came back was luck
        original = self.tmp / 'src' / 'zq-twice.md'
        first = self.archived('d1', original, 'first\n')
        second = self.archived('d2', original, 'second\n')
        proc = self.restore('--by-original', str(original))
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(original.exists())
        self.assertIn(str(first), proc.stderr)
        self.assertIn(str(second), proc.stderr)

    def test_archived_directory_is_restorable(self) -> None:
        # Approved D actions archive whole doc folders; restore.sh accepted regular files only
        original = self.tmp / 'lxc' / '999-gone'
        self.archived('d1', original / 'README.md', 'doc\n')
        proc = self.restore(str(self.archive / 'd1' / str(original).lstrip('/')))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual((original / 'README.md').read_text(), 'doc\n')

    def test_glob_chars_in_archive_root_still_strip(self) -> None:
        # ${src#$ARCHIVE_ROOT/} was an unquoted pattern: "[1]" in the root never matched itself
        self.archive = self.tmp / 'arch[1]'
        original = self.tmp / 'src' / 'zq-root.md'
        copy = self.archived('d1', original)
        proc = self.restore(str(copy))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(original.read_text(), 'archived\n')

    def test_by_original_on_empty_archive_is_not_found(self) -> None:
        # Review Focus: with no date dirs the "$ARCHIVE_ROOT"/*/ glob stays literal and must match nothing
        self.archive.mkdir()
        proc = self.restore('--by-original', str(self.tmp / 'src' / 'zq-none.md'))
        self.assertEqual(proc.returncode, 1)
        self.assertIn('Not found in archive', proc.stdout)

    def test_bare_date_dir_is_not_an_entry(self) -> None:
        # Accepting directories made the date dir itself restorable: the whole day moved to /<date>
        copy = self.archived('d1', self.tmp / 'src' / 'zq-day.md')
        proc = self.restore(str(self.archive / 'd1'))
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(copy.exists())

    def test_dot_dot_cannot_walk_out_of_the_archive(self) -> None:
        # "$ARCHIVE_ROOT/../x" passed the prefix check and moved a live file outside the archive to /x
        live = write(self.tmp / 'zq-live-outside.md', 'live\n')
        self.archive.mkdir()
        proc = self.restore(str(self.archive / '..' / live.name))
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(live.read_text(), 'live\n')


if __name__ == '__main__':
    unittest.main()
