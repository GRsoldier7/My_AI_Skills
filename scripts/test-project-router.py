"""Installer/package regression tests. These do not test agent routing behavior."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SPEC = importlib.util.spec_from_file_location('project_router', Path(__file__).with_name('project-router.py'))
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

class RouterDistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'home'
        self.home.mkdir()
        self.source = Path(__file__).resolve().parents[1]
        self.files = M.runtime_files(self.source)

    def test_seven_complete_skills(self):
        self.assertEqual(len([p for p in self.files if p.endswith('/SKILL.md')]), 7)
        self.assertIn('continuing-alm-work/references/approval-boundaries.md', self.files)

    def test_build_archive(self):
        target = self.root / 'plugin.zip'
        M.build(self.source, target)
        with zipfile.ZipFile(target) as archive:
            self.assertIsNone(archive.testzip())
            data = json.loads(archive.read('project-router/plugin.json'))
            self.assertEqual(data['name'], 'project-router')
            self.assertIn('project-router/skills/project-router/SKILL.md', archive.namelist())
            self.assertFalse(any('/tests/' in n or '/evals/' in n for n in archive.namelist()))

    def test_dry_run_no_writes(self):
        M.install(self.source, self.home, apply=False, guidance=True)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_install_idempotent(self):
        M.install(self.source, self.home, apply=True, guidance=True)
        before = {str(p.relative_to(self.home)): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.home.rglob('*') if p.is_file()}
        M.install(self.source, self.home, apply=True, guidance=True)
        after = {str(p.relative_to(self.home)): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.home.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_preflight_preserves_different_skill(self):
        dest = self.home / '.agents/skills/workbetter'
        dest.mkdir(parents=True)
        (dest / 'SKILL.md').write_text('user version')
        with self.assertRaises(FileExistsError):
            M.install(self.source, self.home, apply=True, guidance=True)
        self.assertEqual((dest / 'SKILL.md').read_text(), 'user version')
        self.assertFalse((self.home / '.agents/skills/project-router').exists())
        self.assertFalse((self.home / '.codex').exists())

    def test_unrelated_instructions_preserved(self):
        p = self.home / '.codex/AGENTS.md'
        p.parent.mkdir()
        original = b'# My rules\r\nKeep my settings.\r\n'
        p.write_bytes(original)
        M.install(self.source, self.home, apply=True, guidance=True)
        self.assertTrue(p.read_bytes().startswith(original))
        self.assertEqual(p.read_text().count(M.START), 1)

    def test_symlink_destination_rejected(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (self.home / '.agents').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            M.install(self.source, self.home, apply=True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_conflicting_guidance_preflight(self):
        p = self.home / '.codex/AGENTS.md'
        p.parent.mkdir()
        p.write_text(M.START + '\nlocal custom text\n' + M.END)
        with self.assertRaises(FileExistsError):
            M.install(self.source, self.home, apply=True, guidance=True)
        self.assertFalse((self.home / '.agents').exists())

    def test_missing_skill_fails_before_writes(self):
        with self.assertRaises(FileNotFoundError):
            M.install(self.root, self.home, apply=True)
        self.assertEqual(list(self.home.iterdir()), [])

if __name__ == '__main__':
    unittest.main()
