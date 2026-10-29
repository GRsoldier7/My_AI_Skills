"""Curated profile contracts; fixtures never install into a real user directory."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('skill_sets', Path(__file__).with_name('skill-sets.py'))
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
ROOT = Path(__file__).resolve().parents[1]


class SkillSetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'platform-configs/skill-sets').mkdir(parents=True)
        self.entries = []
        for name in ('alpha', 'beta'):
            folder = self.root / 'skills/core' / name
            folder.mkdir(parents=True)
            (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Use when testing {name}.\n---\n# {name}\n')
            self.entries.append(dict(id=name, name=name, path=f'skills/core/{name}',
                                     aliases=[], status='trial', dependencies=[],
                                     provenance={'kind': 'owner-authored'},
                                     package_sha256=M.package_hash(folder)))
        self.manifest = dict(schema_version=1, skills=self.entries, profiles={
            'base': dict(skills=['alpha'], includes=[], allow_trial=True),
            'combined': dict(skills=['beta', 'alpha'], includes=['base'], allow_trial=True)})

    def test_inheritance_and_dependencies_deduplicate(self):
        self.entries[1]['dependencies'] = ['alpha']
        self.assertEqual([e['id'] for e in M.resolve_profile(self.manifest, 'combined')], ['alpha', 'beta'])

    def test_reference_and_trial_are_not_implicitly_active(self):
        self.manifest['profiles']['base']['allow_trial'] = False
        with self.assertRaises(ValueError):
            M.resolve_profile(self.manifest, 'base')
        self.manifest['profiles']['base']['allow_trial'] = True
        self.entries[0]['status'] = 'reference'
        with self.assertRaises(ValueError):
            M.resolve_profile(self.manifest, 'base')

    def test_dependency_and_profile_cycles_fail(self):
        self.entries[0]['dependencies'] = ['beta']
        self.entries[1]['dependencies'] = ['alpha']
        with self.assertRaises(ValueError):
            M.resolve_profile(self.manifest, 'base')
        self.entries[0]['dependencies'] = []
        self.entries[1]['dependencies'] = []
        self.manifest['profiles']['base']['includes'] = ['combined']
        with self.assertRaises(ValueError):
            M.resolve_profile(self.manifest, 'base')

    def test_missing_dependency_fails(self):
        self.entries[0]['dependencies'] = ['missing']
        with self.assertRaises(ValueError):
            M.resolve_profile(self.manifest, 'base')

    def test_declared_name_and_alias_collisions_fail(self):
        self.entries[1]['aliases'] = ['alpha']
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_duplicate_stable_id_fails(self):
        self.entries[1]['id'] = 'alpha'
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_example_links_in_code_are_not_live_dependencies(self):
        folder = self.root / self.entries[0]['path']
        with (folder / 'SKILL.md').open('a') as f:
            f.write('\nExample: `See [rules](references/X.md)`\n\n```markdown\n[example](missing.md)\n```\n')
        self.entries[0]['package_sha256'] = M.package_hash(folder)
        M.validate(self.root, self.manifest)

    def test_same_effective_name_at_two_paths_fails(self):
        self.entries[1]['name'] = 'alpha'
        (self.root / self.entries[1]['path'] / 'SKILL.md').write_text('---\nname: alpha\ndescription: Beta\n---\n')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest, check_hashes=False)

    def test_hash_covers_resources_and_detects_tampering(self):
        folder = self.root / self.entries[0]['path']
        (folder / 'extra.md').write_text('new resource')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_missing_reference_fails_even_with_fresh_hash(self):
        folder = self.root / self.entries[0]['path']
        with (folder / 'SKILL.md').open('a') as f:
            f.write('\nRead [rules](references/missing.md).\n')
        self.entries[0]['package_sha256'] = M.package_hash(folder)
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def write_resource(self, skill_id, relative, content):
        entry = next(entry for entry in self.entries if entry['id'] == skill_id)
        folder = self.root / entry['path']
        path = folder / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        entry['package_sha256'] = M.package_hash(folder)
        return path

    def test_declared_dependency_reference_is_allowed(self):
        self.entries[1]['dependencies'] = ['alpha']
        self.write_resource('alpha', 'references/foundation.md', '# Foundation\n')
        self.write_resource('beta', 'references/guide.md',
                            '[Foundation](../../alpha/references/foundation.md#foundation)\n')
        M.validate(self.root, self.manifest)

    def test_transitive_dependency_reference_is_allowed(self):
        folder = self.root / 'skills/core/gamma'
        folder.mkdir()
        (folder / 'SKILL.md').write_text('---\nname: gamma\n---\n# Gamma\n')
        self.entries.append(dict(id='gamma', name='gamma', path='skills/core/gamma',
                                 aliases=[], status='trial', dependencies=['beta'],
                                 provenance={'kind': 'owner-authored'},
                                 package_sha256=M.package_hash(folder)))
        self.entries[1]['dependencies'] = ['alpha']
        self.write_resource('gamma', 'guide.md', '[Foundation](../alpha/SKILL.md)\n')
        M.validate(self.root, self.manifest)

    def test_profile_membership_does_not_authorize_sibling_reference(self):
        self.write_resource('beta', 'guide.md', '[Undeclared](../alpha/SKILL.md)\n')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_missing_file_in_declared_dependency_is_rejected(self):
        self.entries[1]['dependencies'] = ['alpha']
        self.write_resource('beta', 'guide.md', '[Missing](../alpha/missing.md)\n')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_absolute_reference_inside_own_package_is_rejected(self):
        target = self.root / self.entries[0]['path'] / 'SKILL.md'
        self.write_resource('alpha', 'guide.md', f'[Absolute]({target})\n')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_windows_absolute_reference_is_rejected(self):
        self.write_resource('alpha', 'guide.md', '[Absolute](C:/skills/alpha/SKILL.md)\n')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_reference_outside_repository_is_rejected(self):
        outside = tempfile.TemporaryDirectory(dir=self.root.parent)
        self.addCleanup(outside.cleanup)
        (Path(outside.name) / 'outside.md').write_text('Outside repository\n')
        target = '../../../../' + Path(outside.name).name + '/outside.md'
        self.write_resource('alpha', 'guide.md', f'[Outside]({target})\n')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_reference_outside_allowed_packages_is_rejected(self):
        (self.root / 'README.md').write_text('Repository guide\n')
        self.entries[1]['dependencies'] = ['alpha']
        self.write_resource('beta', 'guide.md', '[Outside](../../../README.md)\n')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_symlink_component_in_dependency_reference_is_rejected(self):
        self.entries[1]['dependencies'] = ['alpha']
        (self.root / 'skills/core/redirect').symlink_to(self.root / self.entries[0]['path'])
        for target in ('../redirect/SKILL.md', '../redirect/../alpha/SKILL.md'):
            with self.subTest(target=target):
                self.write_resource('beta', 'guide.md', f'[Redirect]({target})\n')
                with self.assertRaises(ValueError):
                    M.validate(self.root, self.manifest)

    def test_dependency_cycles_are_rejected_without_profile_selection(self):
        self.manifest['profiles'] = {}
        self.entries[0]['dependencies'] = ['beta']
        self.entries[1]['dependencies'] = ['alpha']
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_unknown_dependencies_are_rejected_without_profile_selection(self):
        self.manifest['profiles'] = {}
        self.entries[0]['dependencies'] = ['missing']
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)

    def test_path_escape_and_symlink_fail(self):
        original = self.entries[0]['path']
        self.entries[0]['path'] = '../outside'
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest)
        self.entries[0]['path'] = original
        (self.root / original / 'redirect.md').symlink_to(self.root / self.entries[1]['path'] / 'SKILL.md')
        with self.assertRaises(ValueError):
            M.validate(self.root, self.manifest, check_hashes=False)

    def test_generation_is_idempotent_preserves_unmanaged_sets_and_readme(self):
        base = self.root / 'platform-configs/skill-sets'
        (base / 'manifest.json').write_text(json.dumps(self.manifest))
        (base / 'README.md').write_text('# Existing guide\nKeep this.\n')
        (base / 'global.txt').write_text('keep-global\n')
        M.generate(self.root, write=True)
        first = {p.name: p.read_bytes() for p in base.iterdir()}
        M.generate(self.root, write=True)
        self.assertEqual(first, {p.name: p.read_bytes() for p in base.iterdir()})
        self.assertEqual((base / 'global.txt').read_text(), 'keep-global\n')
        self.assertIn('Keep this.', (base / 'README.md').read_text())
        M.generate(self.root)

    def test_drift_check_is_read_only(self):
        base = self.root / 'platform-configs/skill-sets'
        (base / 'manifest.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            M.generate(self.root)
        self.assertFalse((base / 'base.txt').exists())

    def test_output_symlink_rejected_before_any_write(self):
        base = self.root / 'platform-configs/skill-sets'
        (base / 'manifest.json').write_text(json.dumps(self.manifest))
        victim = self.root / 'untouched.txt'
        victim.write_text('keep')
        (base / 'combined.txt').symlink_to(victim)
        with self.assertRaises(ValueError):
            M.generate(self.root, write=True)
        self.assertEqual(victim.read_text(), 'keep')
        self.assertFalse((base / 'base.txt').exists())

    def test_global_name_is_reserved_and_preserves_default_set(self):
        base = self.root / 'platform-configs/skill-sets'
        (base / 'global.txt').write_bytes(b'user-owned-default\n')
        self.manifest['profiles']['global'] = self.manifest['profiles']['base']
        (base / 'manifest.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            M.generate(self.root, write=True)
        self.assertEqual((base / 'global.txt').read_bytes(), b'user-owned-default\n')
        self.assertFalse((base / 'base.txt').exists())

    def test_unmanaged_named_set_collision_fails_before_writes(self):
        base = self.root / 'platform-configs/skill-sets'
        (base / 'combined.txt').write_bytes(b'manual-selection\n')
        (base / 'manifest.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            M.generate(self.root, write=True)
        self.assertEqual((base / 'combined.txt').read_bytes(), b'manual-selection\n')
        self.assertFalse((base / 'base.txt').exists())

    def test_removed_generated_profile_is_reported_and_preserved(self):
        base = self.root / 'platform-configs/skill-sets'
        manifest_path = base / 'manifest.json'
        manifest_path.write_text(json.dumps(self.manifest))
        M.generate(self.root, write=True)
        old = (base / 'combined.txt').read_bytes()
        del self.manifest['profiles']['combined']
        manifest_path.write_text(json.dumps(self.manifest))
        for write in (False, True):
            with self.assertRaises(ValueError):
                M.generate(self.root, write=write)
        self.assertEqual((base / 'combined.txt').read_bytes(), old)

    def test_renamed_generated_profile_requires_explicit_retirement(self):
        base = self.root / 'platform-configs/skill-sets'
        manifest_path = base / 'manifest.json'
        manifest_path.write_text(json.dumps(self.manifest))
        M.generate(self.root, write=True)
        self.manifest['profiles']['renamed'] = self.manifest['profiles'].pop('combined')
        manifest_path.write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            M.generate(self.root, write=True)
        self.assertFalse((base / 'renamed.txt').exists())

    def test_fresh_autocrlf_checkout_preserves_exact_package_hashes(self):
        for entry in self.entries:
            folder = self.root / entry['path']
            (folder / 'LICENSE').write_text('License line one\nLicense line two\n')
            (folder / 'LICENSE.upstream').write_text('Upstream first\nUpstream second\n')
            entry['package_sha256'] = M.package_hash(folder)
        (self.root / '.gitattributes').write_bytes((ROOT / '.gitattributes').read_bytes())
        (self.root / 'platform-configs/skill-sets/manifest.json').write_text(json.dumps(self.manifest))
        M.generate(self.root, write=True)
        def git(*args):
            subprocess.run(['git', *args], cwd=self.root, capture_output=True, check=True)
        git('init', '-q')
        git('add', '.')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=' + str(self.root / 'no-hooks'),
            'commit', '-qm', 'Synthetic checkout fixture')
        clone = self.root / 'checkout'
        git('-c', 'core.autocrlf=true', 'clone', '-q', '--no-hardlinks', str(self.root), str(clone))
        M.generate(clone)

    def test_repository_manifest_and_generated_sets_are_current(self):
        M.generate(ROOT)

    def test_repository_profiles_install_in_isolated_project_and_repeat(self):
        manifest = json.loads((ROOT / 'platform-configs/skill-sets/manifest.json').read_text())
        for profile in manifest['profiles']:
            target = self.root / profile
            target.mkdir()
            command = ['bash', str(ROOT / 'scripts/install-skills.sh'), '--project', str(target),
                       '--set', str(ROOT / 'platform-configs/skill-sets' / f'{profile}.txt')]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 3)
            self.assertFalse((target / '.agents').exists())
            self.assertEqual(subprocess.run(command + ['--apply'], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(len(list((target / '.agents/skills').iterdir())), len(M.resolve_profile(manifest, profile)))


if __name__ == '__main__':
    unittest.main()
