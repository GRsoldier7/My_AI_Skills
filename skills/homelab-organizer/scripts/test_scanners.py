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


DOC = Path(__file__).resolve().parent.parent / 'references' / 'audit-procedure.md'


def doc_schema(output_file: str) -> dict:
    """The JSON example that follows "Output `<output_file>`" in audit-procedure.md."""
    found = re.search(rf'Output `{re.escape(output_file)}`[^\n]*\n```json\n(.*?)```', DOC.read_text(), re.DOTALL)
    if found is None:
        raise AssertionError(f'no {output_file} schema block in {DOC}')
    return json.loads(found.group(1))


def entry_keys(entries: list) -> list[str]:
    """Keys of the first non-empty entry; the emitters write "" placeholders into empty arrays."""
    return sorted(next(e for e in entries if e))


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
        # The guest seams must name readable files (an unreadable one stops the scan), so they start empty
        for seam in ('ct-refs', 'ct-config'):
            (self.sys / seam).touch()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_script(self, name: str, roots: list[Path] | None = None, /, **env_extra: str) -> tuple[int, dict | None]:
        env = {**os.environ, 'ORGANIZER_ROOTS': ' '.join(map(str, roots or [self.root])), 'SCAN_ROOT_TOP': '0',
               'ORGANIZER_DIR': str(self.organizer), 'AUDIT_DIR': str(self.organizer / 'AUDIT-test'),
               'ORGANIZER_SYMLINK_DIRS': str(self.linkhome),
               'ORGANIZER_INUSE_FILES': str(self.sys / 'MEMORY.md'), 'ORGANIZER_INUSE_DIRS': str(self.sys / 'inuse'),
               'ORGANIZER_SYS_REF_FILES': str(self.sys / 'cron'),
               # Fixture files stand in for the guests' unit/cron dumps and for /etc/pve/lxc/*.conf: without
               # them every scan in this suite would pct exec the live guests of the host it runs on
               'ORGANIZER_CT_REF_FILES': str(self.sys / 'ct-refs'), 'ORGANIZER_CT_CONFIG_FILES': str(self.sys / 'ct-config'),
               # Pinned to the defaults so a floor exported in the operator's shell cannot move a fixture's bucket
               'STALE_DAYS': '90', 'SAFE_DAYS': '7', **env_extra}
        proc = subprocess.run(['bash', str(SCRIPTS / name)], capture_output=True, text=True,
                              env=env, timeout=120, check=False)
        self.last_stderr = proc.stderr
        try:
            return proc.returncode, json.loads(proc.stdout)
        except json.JSONDecodeError:
            return proc.returncode, None

    def scan(self, roots: list[Path] | None = None, **env_extra: str) -> dict:
        rc, data = self.run_script('scan-files.sh', roots, **env_extra)
        self.assertEqual(rc, 0)
        if data is None:
            self.fail('scan-files.sh did not emit valid JSON')
        return data

    def bucket_of(self, data: dict, path: Path) -> str | None:
        for name, entries in data['categorized'].items():
            if any(e and e['path'] == str(path) for e in entries):
                return name
        return None

    def entry_in(self, data: dict, bucket: str, path: Path) -> dict:
        """The row for `path`, failing the test when the file landed in any other bucket."""
        self.assertEqual(self.bucket_of(data, path), bucket)
        return next(e for e in data['categorized'][bucket] if e and e['path'] == str(path))

    def stub_path(self, name: str, body: str) -> str:
        """PATH with an executable fixture `name` first, so the script under test never reaches the real one."""
        bindir = Path(self._tmp.name) / 'bin'
        bindir.mkdir(exist_ok=True)
        (bindir / name).write_text(body)
        (bindir / name).chmod(0o755)
        return f'{bindir}:{os.environ["PATH"]}'


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
                    'ORGANIZER_INUSE_DIRS', 'ORGANIZER_SYS_REF_FILES', 'ORGANIZER_CT_REF_FILES',
                    'ORGANIZER_CT_CONFIG_FILES', 'SCAN_ROOT_TOP=0'):
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

    def test_doc_schema_matches_emit(self) -> None:
        # Pins the Phase B schema fixed in dbd1bba: the doc said content_hash (8 chars), the scanner emits hash (12)
        write(self.root / 'zq-safe.md', 'u1\n')
        write(self.root / 'zq-cited.md', 'u2\n')
        write(self.root / 'zq-citer.md', 'see zq-cited.md\n')
        write(self.root / '20250101 - Zq Dated.md', 'u3\n')
        write(self.root / 'a' / 'zq-d.md', 'same\n')
        write(self.root / 'b' / 'zq-d.md', 'same\n')
        data, schema = self.scan(), doc_schema('files.json')
        self.assertEqual(sorted(data), sorted(schema))
        self.assertEqual(sorted(data['totals']), sorted(schema['totals']))
        for bucket, entries in data['categorized'].items():
            with self.subTest(bucket):
                documented = schema['categorized'][bucket] or schema['categorized']['SAFE_QUARANTINE']
                self.assertEqual(entry_keys(entries), entry_keys(documented))

    def test_package_marker_is_in_use(self) -> None:
        # #28: __init__.py is kept out of the ref index as over-common, so by name it always read as
        # unreferenced, and a non-empty 90-day-old marker in a live package went SAFE
        marker = write(self.root / 'pkg' / '__init__.py', '__version__ = "1"\n')
        self.assertEqual(self.entry_in(self.scan(), 'WATCHLIST', marker)['in_use_signals'], 'package_marker')

    def test_zero_byte_files_are_never_duplicates_or_safe(self) -> None:
        # #23: every empty file is hash-equal, so unrelated empties came out as DUPLICATE pairs and the
        # first-seen one SAFE. An empty file carries no evidence either way: hold it, and keep any signal
        empties = {write(self.root / 'a' / 'zq-empty.md', ''): 'zero_byte;',
                   write(self.root / 'b' / 'zq-other-empty.md', ''): 'zero_byte;',
                   write(self.root / 'pkg' / '__init__.py', ''): 'package_marker;zero_byte;'}
        data = self.scan()
        self.assertEqual([d for d in data['categorized']['DUPLICATE'] if d], [])
        for path, reason in empties.items():
            with self.subTest(path.name):
                self.assertEqual(self.entry_in(data, 'WATCHLIST', path)['reason'], reason)

    def test_credential_shaped_content_is_never_proposed(self) -> None:
        # A script with a hardcoded secret sat in SAFE_QUARANTINE, and the archive is pushed to another node,
        # so quarantine would spread it. Shapes are assembled at runtime so none lands in this public repo
        pem = '-----BEGIN ' + 'RSA PRIVATE' + ' KEY-----'
        cloud = 'AK' + 'IA' + 'EXAMPLEKEY012345'
        pw = 'hunter2' + 'hunter2'
        bare = 'zqbare' + 'value0123'
        cases = {
            'pem block in a conf': (self.root / 'zq-tls.conf', f'cert\n{pem}\nMIIB\n'),
            'cloud key in yaml': (self.root / 'zq-cloud.yaml', f'access: {cloud}\n'),
            'quoted password in a script': (self.root / 'zq-deploy.sh', f'#!/bin/sh\nDB_PASSWORD="{pw}"\n'),
            'json token field': (self.root / 'zq-app.json', '{"token": "' + 'tok' * 5 + '"}\n'),
            'bare key before a separator': (self.root / 'zq-env.sh', f'export API_KEY={bare}; run\n'),
        }
        paths = {name: write(p, text) for name, (p, text) in cases.items()}
        copy = write(self.root / 'copy' / 'zq-deploy.sh', cases['quoted password in a script'][1])
        data = self.scan()
        for name, p in paths.items():
            with self.subTest(name):
                self.assertIn('credential_shaped;', self.entry_in(data, 'WATCHLIST', p)['reason'])
        # A same-content copy must not surface as a DUPLICATE of a held file
        self.assertEqual(self.bucket_of(data, copy), 'WATCHLIST')
        # Flag only: the matched text never reaches stdout or stderr
        for value in (pem, cloud, pw, bare):
            self.assertNotIn(value, json.dumps(data) + self.last_stderr)

    def test_reference_style_values_are_not_credential_shaped(self) -> None:
        # The gate must not hold a reference ($VAR, <placeholder>, a lookup) or a call result assigned to a
        # token-named variable, or it quietly holds most of the tree
        code = write(self.root / 'zq-settings.py', 'PASSWORD = settings.lookup("DB_PASSWORD")\nTOKEN_BUDGET = 200000\n'
                                                   'token = generate_access_token(user)\nself.token = tokenizer_for_model(name)\n')
        shell = write(self.root / 'zq-run.sh', '#!/bin/sh\nPASSWORD="$DB_PASSWORD"\nAPI_KEY=${API_KEY:-<your-key>}\n')
        data = self.scan()
        for f in (code, shell):
            with self.subTest(f.name):
                self.assertEqual(self.bucket_of(data, f), 'SAFE_QUARANTINE')

    def test_quoted_passphrase_with_spaces_is_credential_shaped(self) -> None:
        # The quoted-value class excluded whitespace, so a passphrase of several words went SAFE and could
        # be copied into the archive
        phrase = write(self.root / 'zq-phrase.conf', 'password = "' + 'correct horse ' + 'battery staple"\n')
        self.assertIn('credential_shaped;', self.entry_in(self.scan(), 'WATCHLIST', phrase)['reason'])

    def test_file_under_ct_mount_point_is_in_use(self) -> None:
        # #26: safety-rules.md promises container mount points as an in-use signal. A bound host dir or a
        # single bound file is live inside the guest; a volume-backed mp names no host path and binds nothing
        bound = write(self.root / 'shared' / 'zq-bound.conf', 'k=v\n')
        single = write(self.root / 'zq-single-bind.sh', '#!/bin/sh\n')
        plain = write(self.root / 'zq-unbound.md')
        write(self.sys / 'ct-config', f'arch: amd64\nmp0: {self.root / "shared"},mp=/data\n'
                                      f'lxc.mount.entry: {single} usr/local/bin/zq none bind,create=file\n'
                                      'mp1: local-lvm:vm-999-disk-1,mp=/vol\n')
        data = self.scan()
        for f in (bound, single):
            with self.subTest(f.name):
                self.assertEqual(self.entry_in(data, 'WATCHLIST', f)['in_use_signals'], 'ct_mount')
        self.assertEqual(self.bucket_of(data, plain), 'SAFE_QUARANTINE')

    def test_ct_mount_of_host_root_or_dotted_path_still_binds(self) -> None:
        # #26 review: the mount parser needed a character after "/", so a bind of host / was dropped whole,
        # and a non-canonical source (<dir>/.) never prefix-matched the files under it
        for name, source in (('host root', '/'), ('dotted dir', f'{self.root / "shared"}/.')):
            with self.subTest(name):
                f = write(self.root / 'shared' / 'zq-under-mount.md')
                write(self.sys / 'ct-config', f'mp0: {source},mp=/host,ro=1\n')
                self.assertEqual(self.entry_in(self.scan(), 'WATCHLIST', f)['in_use_signals'], 'ct_mount')

    def test_ct_mount_matches_a_root_reached_through_a_symlink(self) -> None:
        # #26 review: the mount source is canonical but find emits paths under the root as given, so a root
        # reached through a symlinked ancestor never prefix-matched its own canonical mount
        real = Path(self._tmp.name) / 'real'
        f = write(real / 'sub' / 'zq-mounted.md')
        (Path(self._tmp.name) / 'link').symlink_to(real)
        write(self.sys / 'ct-config', f'mp0: {real / "sub"},mp=/data\n')
        data = self.scan([Path(self._tmp.name) / 'link' / 'sub'])
        walked = Path(self._tmp.name) / 'link' / 'sub' / f.name
        self.assertEqual(self.entry_in(data, 'WATCHLIST', walked)['in_use_signals'], 'ct_mount')

    def test_unreadable_safety_seam_stops_the_scan(self) -> None:
        # #26 review: a guest seam naming a missing file silently dropped every guest ref; the stderr notice
        # did not stop the phase, so a guest-run script could still go SAFE
        for seam in ('ORGANIZER_CT_REF_FILES', 'ORGANIZER_CT_CONFIG_FILES'):
            # A second path after a newline was neither checked nor read
            for value in (str(self.sys / 'zq-missing'), f'{self.sys / "ct-refs"}\n{self.sys / "zq-missing"}'):
                with self.subTest(seam=seam, value=value):
                    rc, data = self.run_script('scan-files.sh', **{seam: value})
                    self.assertNotEqual(rc, 0)
                    self.assertIsNone(data)
                    self.assertIn(seam, self.last_stderr)

    def test_ct_mount_covering_a_scan_root_is_announced(self) -> None:
        # #26: a bind of a whole scan root makes every file under it read in use. Held is the safe
        # direction, but an audit that silently proposes nothing has gone blind without saying so
        write(self.sys / 'ct-config', f'mp0: {self.root},mp=/host\n')
        self.scan()
        self.assertIn(str(self.root), self.last_stderr)

    def test_file_named_by_ct_unit_is_in_use(self) -> None:
        # #26: a repo script copied into a guest and run there by a timer read as SAFE; the guest's unit
        # names only the copy's path, so its basename is the signal
        job = write(self.root / 'deploy' / 'zq-ct-backup.sh', '#!/bin/sh\n')
        write(self.sys / 'ct-refs', '[Service]\nExecStart=/root/zq-ct-backup.sh\n')
        self.assertEqual(self.bucket_of(self.scan(), job), 'WATCHLIST')

    def test_in_ct_path_never_makes_a_host_tree_live(self) -> None:
        # #26 guard: a guest's paths are the guest's. WorkingDirectory=<dir> inside a guest must not mark
        # everything under the host's same-named dir in use, or the organizer goes blind
        plain = write(self.root / 'zq-plain-stale.md')
        write(self.sys / 'ct-refs', f'[Service]\nWorkingDirectory={self.root}\n')
        self.assertEqual(self.bucket_of(self.scan(), plain), 'SAFE_QUARANTINE')

    def test_guest_units_and_drop_ins_are_read_from_running_cts(self) -> None:
        # #26, live branch against a stub pct: a script named only by a unit drop-in inside a running guest
        # is in use. The stopped guest is never exec'd (the stub refuses it, which would list it unreadable)
        job = write(self.root / 'deploy' / 'zq-dropin-job.sh', '#!/bin/sh\n')
        guest = Path(self._tmp.name) / 'guest'
        write(guest / 'etc' / 'systemd' / 'system' / 'zq.service.d' / 'override.conf',
              '[Service]\nExecStart=/root/zq-dropin-job.sh\n')
        data = self.scan(ORGANIZER_CT_REF_FILES='', GUEST_ROOT=str(guest), PATH=self.stub_path('pct', GUEST_PCT_STUB))
        self.assertEqual(self.entry_in(data, 'WATCHLIST', job)['in_use_signals'], 'cron_systemd_or_symlink_ref')
        self.assertEqual(data['ct_refs_unreadable'], [])

    def test_guest_units_outside_etc_system_are_read(self) -> None:
        # #26 review: the dump read only /etc/systemd/system *.service/*.timer/*.path and drop-ins, so a unit
        # in the package unit dir, or a socket hook, still left the script it runs SAFE
        cases = {
            'package unit dir': ('usr/lib/systemd/system/zq-pkg.service', 'ExecStart=/root/zq-usrlib-job.sh\n', 'zq-usrlib-job.sh'),
            'socket unit': ('etc/systemd/system/zq.socket', 'ExecStartPre=/root/zq-socket-hook.sh\n', 'zq-socket-hook.sh'),
            'cron.daily script': ('etc/cron.daily/zq-daily', '#!/bin/sh\n/root/zq-daily-step.sh\n', 'zq-daily-step.sh'),
            'package unit drop-in': ('usr/lib/systemd/system/zq-pkg.service.d/override.conf',
                                     'ExecStart=/root/zq-pkg-dropin.sh\n', 'zq-pkg-dropin.sh'),
        }
        guest = Path(self._tmp.name) / 'guest'
        jobs = {name: write(self.root / 'deploy' / script, f'#!/bin/sh\n# {name}\n') for name, (_, _, script) in cases.items()}
        for rel, text, _ in cases.values():
            write(guest / rel, text)
        data = self.scan(ORGANIZER_CT_REF_FILES='', GUEST_ROOT=str(guest), PATH=self.stub_path('pct', GUEST_PCT_STUB))
        for name, job in jobs.items():
            with self.subTest(name):
                self.assertEqual(self.entry_in(data, 'WATCHLIST', job)['in_use_signals'], 'cron_systemd_or_symlink_ref')

    def test_failed_guest_listing_stops_the_scan(self) -> None:
        # #26 review: a failed `pct list` read as "no guests", so no guest was asked and every script they run
        # could go SAFE. Without a listing there is no safe result, so the scan stops instead of emitting one
        rc, data = self.run_script('scan-files.sh', ORGANIZER_CT_REF_FILES='', PATH=self.stub_path('pct', GUEST_PCT_LIST_FAILS_STUB))
        self.assertNotEqual(rc, 0)
        self.assertIsNone(data)
        self.assertIn('pct list', self.last_stderr)

    def test_path_with_spaces_is_named_in_full(self) -> None:
        # #26 review: path tokens stopped at the first space, so ExecStart="/root/zq guest backup.sh" named
        # only /root/zq. Quoted and backslash-escaped paths are taken whole, on the host and in a guest
        for seam in ('cron', 'ct-refs'):
            with self.subTest(seam):
                quoted = write(self.root / f'zq {seam} quoted job.sh', f'#!/bin/sh\n# {seam} q\n')
                escaped = write(self.root / f'zq {seam} escaped job.sh', f'#!/bin/sh\n# {seam} e\n')
                write(self.sys / seam, f'ExecStart="/root/{quoted.name}"\nExecStartPost=/root/zq\\ {seam}\\ escaped\\ job.sh\n')
                data = self.scan()
                for f in (quoted, escaped):
                    self.assertEqual(self.entry_in(data, 'WATCHLIST', f)['in_use_signals'], 'cron_systemd_or_symlink_ref')
                (self.sys / seam).unlink()

    def test_unreadable_guest_is_reported(self) -> None:
        # #26: a guest whose dump fails leaves the scripts it runs unprotected. That must show in the data and
        # on stderr, never read as "this guest names nothing"
        data = self.scan(ORGANIZER_CT_REF_FILES='', PATH=self.stub_path('pct', GUEST_PCT_FAIL_STUB))
        self.assertEqual(data['ct_refs_unreadable'], ['101'])
        self.assertIn('CT 101', self.last_stderr)

    def test_cited_duplicate_is_never_proposed(self) -> None:
        # #30: DUPLICATE is a proposed bucket, but a copy entered it without the refs/in-use check every other
        # proposal gets, so only a triage rule stood between a cited copy and quarantine
        copies = [write(self.root / d / 'zq-dup-cited.md', 'same\n') for d in ('a', 'b')]
        write(self.root / 'zq-dup-citer.md', 'see zq-dup-cited.md\n', old=False)
        data = self.scan()
        self.assertEqual([d for d in data['categorized']['DUPLICATE'] if d], [])
        reasons = sorted(self.entry_in(data, 'WATCHLIST', c)['reason'] for c in copies)
        self.assertEqual(reasons, ['has_inbound_refs;', 'has_inbound_refs;duplicate;'])

    def test_proposal_names_the_files_it_would_orphan(self) -> None:
        # #27: quarantining X dropped to 0 the refs of files only X cited, so they surfaced as new SAFE next
        # run with no trail. The approver now sees them on X's own row before approving X
        parent = write(self.root / 'zq-orphan-parent.md', 'see zq-orphan-child.md\n')
        child = write(self.root / 'zq-orphan-child.md')
        self.assertEqual(self.entry_in(self.scan(), 'SAFE_QUARANTINE', parent)['would_orphan'], [str(child)])

    def test_second_citer_clears_would_orphan(self) -> None:
        # #27 guard: a file that another live file still cites is not orphaned by the proposal
        parent = write(self.root / 'zq-orphan-parent.md', 'see zq-orphan-child.md\n')
        write(self.root / 'zq-orphan-child.md')
        write(self.root / 'zq-other-citer.md', 'also zq-orphan-child.md\n', old=False)
        self.assertEqual(self.entry_in(self.scan(), 'SAFE_QUARANTINE', parent)['would_orphan'], [])


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
        # ORGANIZER_DIR narrows the walk too (#24): exported by mistake it hides a whole tree's links
        self.links()
        for var in ('ORGANIZER_ROOTS', 'ORGANIZER_DIR'):
            with self.subTest(var):
                self.assertIn(var, self.last_stderr)

    def test_percent_encoded_target_is_decoded(self) -> None:
        # #19: only %20 was decoded, so a target holding %28 %29 %2B (either case) read as missing
        write(self.root / 'zq (x) + y.md')
        write(self.root / 'doc.md', 'see [a](zq%20%28x%29%20%2B%20y.md) [b](zq%20%28x%29%20%2b%20y.md)\n')
        self.assertEqual(self.broken_targets(), [])

    def test_decoder_leaves_bare_percent_and_nul_alone(self) -> None:
        # #19: a bare % (no two hex digits after it) and %00 (a NUL fits no path) stay literal, a target's
        # own backslash is never re-read as an escape, and the row reports the target as written
        write(self.root / 'zq 100% done.md')
        write(self.root / 'doc.md', 'see [a](zq%20100%%20done.md) [b](zq%00.md) [c](zq\\_x.md)\n')
        self.assertEqual(self.broken_targets(), ['zq%00.md', 'zq\\_x.md'])

    def test_decoded_control_and_non_ascii_bytes_stay_literal(self) -> None:
        # #19 review: decoding %0A or %FF put a raw newline or an invalid UTF-8 byte into the "resolved" field,
        # and the whole links.json stopped parsing. Only printable ASCII is decoded; the rest stays as written
        write(self.root / 'doc.md', '[a](zq%0Aname.md) [b](zq%FFname.md) [c](zq%7Fdel.md)\n')
        self.assertEqual(self.broken_targets(), ['zq%0Aname.md', 'zq%FFname.md', 'zq%7Fdel.md'])

    def test_file_url_target_resolves_locally(self) -> None:
        # #20: file:///abs had the .md's directory prepended, so every file:// link read as missing.
        # file:///abs, file:/abs and file://localhost/abs are local; any other authority is a remote
        # host, skipped like https
        real = write(self.root / 'zq-real.md')
        nope = self.root / 'zq-nope.md'
        write(self.root / 'sub' / 'doc.md', f'[a](file://{real}) [b](file://localhost{real}) [c](file:{real}) '
                                            f'[d](file://{nope}) [e](file://203.0.113.9{real})\n')
        self.assertEqual(self.broken_targets(), [f'file://{nope}'])

    def test_balanced_parens_in_target(self) -> None:
        # #21: the link regex stopped at the first ")", so "(Mid).md" lost its tail and read as missing;
        # a missing target is reported whole
        write(self.root / 'zq (Mid).md')
        write(self.root / 'doc.md', 'see [a](zq%20(Mid).md) and [b](zq%20(Nope).md)\n')
        self.assertEqual(self.broken_targets(), ['zq%20(Nope).md'])

    def test_each_link_is_reported_once(self) -> None:
        # #21: the post-match strip ran through the first ")" on the line, not the end of the match, so a
        # ")" before a link re-scanned it and its row came out twice, inflating the raw counts
        write(self.root / 'doc.md', '(see) [x](zq-gone.md)\n[a](zq-a.md) text) [b](zq-b.md)\n')
        self.assertEqual(sorted(self.broken_targets()), ['zq-a.md', 'zq-b.md', 'zq-gone.md'])

    def test_organizer_reports_are_not_link_sources(self) -> None:
        # #24: the organizer's own reports quote every broken link they found, so each finding was
        # re-reported from the report forever (scan-files.sh excludes the same dir as a ref source)
        write(self.organizer / 'AUDIT-old.md', 'see [x](./zq-reported.md)\n')
        self.assertNotIn('./zq-reported.md', self.broken_targets())

    def test_link_in_inline_code_is_ignored(self) -> None:
        # #24: only fenced blocks were skipped, so a row quoting `[x](./nope.md)` as inline code was a
        # finding. CommonMark: a code span binds before a link. The real link on the line still counts
        write(self.root / 'doc.md', '| row | `[x](./zq-inline.md)` |\n[y](./zq-real-missing.md) `` `[z](./zq-double.md)` ``\n')
        self.assertEqual(self.broken_targets(), ['./zq-real-missing.md'])

    def test_link_in_plain_double_backtick_span_is_ignored(self) -> None:
        # #24: pairing backticks singly read each `` as an empty span, which left the link inside exposed
        write(self.root / 'doc.md', '``[x](./zq-double-plain.md)`` and [y](./zq-real-missing.md)\n')
        self.assertEqual(self.broken_targets(), ['./zq-real-missing.md'])

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

    def test_doc_schema_matches_emit(self) -> None:
        # The doc listed a "reason" field check-links never emitted; it writes "resolved"
        write(self.root / 'doc.md', 'see [x](./zq-missing.md)\n```\n')
        write(self.root / 'run.sh', 'source ./zq-missing.sh\n')
        (self.root / 'zq-dangling').symlink_to(self.root / 'zq-nowhere')
        data, schema = self.links(), doc_schema('links.json')
        self.assertEqual(sorted(data), sorted(schema))
        for key in ('broken_md_links', 'dangling_symlinks', 'broken_sources', 'unclosed_fences'):
            with self.subTest(key):
                self.assertEqual(entry_keys(data[key]), entry_keys(schema[key]))


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
# Running CT whose `pct exec` runs the probe on this host, against an apt that lists nothing upgradable
PCT_RUNNING_STUB = """#!/bin/sh
case "$1" in
  list) printf 'VMID       Status     Lock         Name\\n101        running                 ct-a\\n' ;;
  status) echo 'status: running' ;;
  config) printf 'hostname: ct-a\\nmemory: 512\\n' ;;
  exec) shift 3; exec "$@" ;;
esac
"""
APT_NONE_UPGRADABLE_STUB = "#!/bin/sh\necho 'Listing... Done'\n"
# One running and one stopped guest. `pct exec` runs the scanner's real guest command with each top-level
# path (/etc /var /lib /usr, space-anchored so /usr/lib is rewritten once) moved under $GUEST_ROOT, so the
# command's own file list is exercised and nothing on this host is read
GUEST_PCT_STUB = """#!/bin/sh
case "$1" in
  list) printf 'VMID       Status     Lock         Name\\n101        running                 ct-a\\n102        stopped                 ct-b\\n' ;;
  exec) [ "$2" = 101 ] || exit 7
        shift 3; [ "$1" = sh ] && [ "$2" = -c ] || exit 9
        exec sh -c "$(printf '%s' "$3" | sed "s# /etc/# $GUEST_ROOT/etc/#g; s# /var/# $GUEST_ROOT/var/#g; s# /lib/# $GUEST_ROOT/lib/#g; s# /usr/# $GUEST_ROOT/usr/#g")" ;;
esac
"""
GUEST_PCT_LIST_FAILS_STUB = "#!/bin/sh\n[ \"$1\" = list ] && exit 1\nexit 0\n"
GUEST_PCT_FAIL_STUB = """#!/bin/sh
case "$1" in
  list) printf 'VMID       Status     Lock         Name\\n101        running                 ct-a\\n' ;;
  exec) exit 1 ;;
esac
"""


class InventoryContainersTest(unittest.TestCase):
    # Stubbed pct/qm: CT 101 has no doc; VM 110's doc sits in lxc/ (misfiled); vms/ is empty
    def inventory(self, pct_stub: str = PCT_STUB, docs: dict[str, str] | None = None) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            stubs = Path(tmp) / 'bin'
            stubs.mkdir()
            for name, body in (('pct', pct_stub), ('qm', QM_STUB), ('hostname', '#!/bin/sh\necho node-a\n'),
                               ('apt', APT_NONE_UPGRADABLE_STUB)):
                (stubs / name).write_text(body)
                (stubs / name).chmod(0o755)
            (Path(tmp) / 'lxc' / '110-misfiled').mkdir(parents=True)
            (Path(tmp) / 'vms').mkdir()
            (Path(tmp) / 'containers').mkdir()
            for rel, text in (docs or {}).items():
                write(Path(tmp) / rel, text)
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

    def test_fully_patched_ct_keeps_json_valid(self) -> None:
        # #25: grep -c prints 0 AND exits 1 on no match, so `|| echo 0` emitted "0\n0" and broke the whole
        # file the first time a CT had nothing to upgrade (2026-10-23)
        ct = next(c for c in self.inventory(PCT_RUNNING_STUB)['containers'] if c['id'] == '101')
        self.assertEqual(ct['probe']['pkgs_outdated'], 0)

    def test_prose_mention_does_not_document_a_guest(self) -> None:
        # #22: any "CT <id>" mention counted as documentation, so a guest named only in another guest's
        # README as a cross-reference read as documented
        docs = {'containers/zq-other/README.md': '# Other (CT 150)\n\nUpstream proxy is NPM (CT 101).\n'}
        self.assertIn('101', self.inventory(docs=docs)['drift_summary']['undocumented_lxc'])

    def test_fenced_comment_does_not_document_a_guest(self) -> None:
        # #22: a shell comment inside a code fence looks like a heading line, and a live README had one
        # naming a guest ("# Run with ... (matches CT <id> production)")
        for fence in ('```', '~~~'):
            with self.subTest(fence):
                docs = {'containers/zq-proj/README.md': f'# Proj\n{fence}bash\n# Matches CT 101 production\n{fence}\n'}
                self.assertIn('101', self.inventory(docs=docs)['drift_summary']['undocumented_lxc'])

    def test_heading_mention_documents_a_guest(self) -> None:
        # #22 control: a heading naming the guest (any level, any line) or a yaml id: key still documents it
        cases = {
            'title line': {'containers/zq-ct-a/README.md': '# Ct-a (CT 101)\n'},
            'later section': {'containers/zq-proj/README.md': '# Proj\n' + 'text\n' * 60 + '## Production Deployment (CT 101)\n'},
            'yaml id': {'containers/zq-ct-a/ct.yaml': 'id: 101\nname: ct-a\n'},
        }
        for name, docs in cases.items():
            with self.subTest(name):
                self.assertNotIn('101', self.inventory(docs=docs)['drift_summary']['undocumented_lxc'])

    def test_indented_heading_documents_a_guest(self) -> None:
        # #22: CommonMark allows a heading up to 3 spaces in, but the match ran on the unstripped line
        docs = {'containers/zq-proj/README.md': '# Proj\n\n   ## Production (CT 101)\n'}
        self.assertNotIn('101', self.inventory(docs=docs)['drift_summary']['undocumented_lxc'])

    def test_four_space_indent_is_not_a_heading(self) -> None:
        # #22 guard: 4 spaces or a tab is an indented code block, so its "# ..." is a shell comment
        for indent in ('    ', '\t'):
            with self.subTest(repr(indent)):
                docs = {'containers/zq-proj/README.md': f'# Proj\n\n{indent}# Matches CT 101 production\n'}
                self.assertIn('101', self.inventory(docs=docs)['drift_summary']['undocumented_lxc'])

    def test_doc_schema_matches_emit(self) -> None:
        # The doc promised current/baseline_delta/drift per guest; the script emits none of them
        data, schema = self.inventory(), doc_schema('containers.json')
        self.assertEqual(sorted(data), sorted(schema))
        self.assertEqual(entry_keys(data['containers']), entry_keys(schema['containers']))
        self.assertEqual(sorted(data['drift_summary']), sorted(schema['drift_summary']))


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

    def test_bare_pipe_in_name_is_part_of_the_path(self) -> None:
        # The reason split took the first "|" anywhere, so "zq|pipe.md" read as the path ".../zq"
        src = write(self.tmp / 'src' / 'zq|pipe.md')
        manifest = self.quarantine(f'{src} | test')
        self.assertTrue(self.archived(src).exists())
        self.assertIn('- reason: test\n', manifest)

    def test_existing_archive_entry_is_never_overwritten(self) -> None:
        # A second same-day quarantine of one path replaced the first archived copy
        src = write(self.tmp / 'src' / 'zq-again.md', 'first\n')
        self.quarantine(str(src))
        write(src, 'second\n')
        self.quarantine(str(src))
        self.assertEqual(self.archived(src).read_text(), 'first\n')
        self.assertEqual(src.read_text(), 'second\n')

    def test_crlf_input_line_still_names_the_file(self) -> None:
        # Review Focus: an approved list saved with CRLF endings leaves "\r" on every line — on the path when
        # there is no reason, on the reason when there is one
        bare = write(self.tmp / 'src' / 'zq-crlf.md')
        reasoned = write(self.tmp / 'src' / 'zq-crlf-why.md')
        manifest = self.quarantine(f'{bare}\r', f'{reasoned} | test\r')
        self.assertTrue(self.archived(bare).exists())
        self.assertTrue(self.archived(reasoned).exists())
        self.assertIn('- reason: test\n', manifest)

    def test_reason_may_contain_the_separator(self) -> None:
        # Review Focus: only the FIRST " | " splits, so free-text reasons keep their own pipes
        src = write(self.tmp / 'src' / 'zq-why.md')
        manifest = self.quarantine(f'{src} | stale | no refs')
        self.assertIn('- reason: stale | no refs\n', manifest)


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

    def test_by_original_rejects_dot_dot_and_relative_paths(self) -> None:
        # --by-original had no ".." guard: "/../../live/x" resolved through the archive to a live file outside it
        self.archived('d1', self.tmp / 'src' / 'zq-any.md')
        live = write(self.tmp / 'live' / 'zq-decoy.md', 'live\n')
        for orig in (f'/../../live/{live.name}', 'src/zq-rel.md'):
            with self.subTest(orig):
                proc = self.restore('--by-original', orig)
                self.assertEqual(proc.returncode, 1)
                self.assertIn('Not an archived entry', proc.stderr)
        self.assertEqual(live.read_text(), 'live\n')

    def test_trailing_slash_does_not_skip_the_overwrite_guard(self) -> None:
        # -e "file/" is false, so a trailing slash on a directory entry skipped REFUSE(exists)
        original = write(self.tmp / 'lxc' / 'zq-dir', 'live file\n')
        self.archived('d1', original / 'README.md', 'doc\n')
        proc = self.restore(str(self.archive / 'd1' / str(original).lstrip('/')) + '/')
        self.assertEqual(proc.returncode, 1)
        self.assertIn('REFUSE(exists)', proc.stderr)
        self.assertEqual(original.read_text(), 'live file\n')

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

    def test_repeated_slash_after_date_dir_is_not_an_entry(self) -> None:
        # "d1//" slipped past the <date>/<path> guard and was stopped only because "//" (root) exists
        copy = self.archived('d1', self.tmp / 'src' / 'zq-slashes.md')
        proc = self.restore(str(self.archive / 'd1') + '//')
        self.assertEqual(proc.returncode, 1)
        self.assertIn('Not an archived entry', proc.stderr)
        self.assertTrue(copy.exists())


if __name__ == '__main__':
    unittest.main()
