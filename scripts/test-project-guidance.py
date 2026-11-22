"""Project guidance regressions. Uses disposable project directories only."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("guidance", Path(__file__).with_name("project-guidance.py"))
guidance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guidance)

class ProjectGuidanceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.project = self.root / "project"
        self.project.mkdir()
        self.config = self.root / "config"
        shutil.copytree(guidance.CONFIG / "shared", self.config / "shared")
        for relative, _, _ in guidance.PLATFORMS.values():
            (self.config / relative).parent.mkdir(exist_ok=True)
    def test_generation_tracks_shared_source_and_stale_outputs(self):
        guidance.generate(self.config, True)
        first = guidance.render(self.config)
        fragment = self.config / "shared" / "identity.md"
        fragment.write_bytes(b"Updated policy.\r\n")
        with self.assertRaisesRegex(ValueError, "regeneration"):
            guidance.generate(self.config, False)
        guidance.generate(self.config, True)
        for name, data in guidance.render(self.config).items():
            self.assertNotEqual(first[name], data)
            self.assertIn(b"Updated policy.", data)
            self.assertNotIn(b"\r", data)
            self.assertEqual(data, (self.config / guidance.PLATFORMS[name][0]).read_bytes())

    def test_preview_and_repeated_apply(self):
        guidance.deploy(self.config, str(self.project), "codex,claude", False)
        self.assertEqual([], list(self.project.iterdir()))
        guidance.deploy(self.config, str(self.project), "codex,claude", True)
        before = {p.name:(p.read_bytes(),p.stat().st_mtime_ns) for p in self.project.iterdir()}
        self.assertEqual(set(before), {"AGENTS.md","CLAUDE.md"})
        guidance.deploy(self.config, str(self.project), "codex,claude", True)
        self.assertEqual(before, {p.name:(p.read_bytes(),p.stat().st_mtime_ns) for p in self.project.iterdir()})

    def test_conflicts_and_invalid_requests_preserve_project(self):
        (self.project / "CLAUDE.md").write_text("owner's instructions", encoding="utf-8")
        for kinds in ["codex,claude", "codex,unknown", "codex,codex", "chatgpt"]:
            with self.subTest(kinds=kinds), self.assertRaises(ValueError):
                guidance.deploy(self.config, str(self.project), kinds, True)
        self.assertEqual(["CLAUDE.md"], [p.name for p in self.project.iterdir()])
        self.assertEqual("owner's instructions", (self.project/"CLAUDE.md").read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            guidance.deploy(self.config, str(self.project / ".." / "project"), "codex", True)

    def test_git_checkout_preserves_resource_bytes(self):
        repo = self.root / "line endings"
        repo.mkdir()
        shutil.copyfile(guidance.CONFIG.parent / ".gitattributes", repo / ".gitattributes")
        samples = {name: b"first line\nsecond line\n" for name in
                   ("source.ts", "fixture.csv", "view.html", "package-lock.json", "LICENSE", "readme.md")}
        samples["binary.fixture"] = b"\0\r\n\xff\n"
        for name, data in samples.items():
            (repo / name).write_bytes(data)
        def git(*args):
            subprocess.run(["git", "-c", "core.autocrlf=true", *args], cwd=repo, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        git("init", "-q")
        git("add", "--", ".")
        for name in samples:
            (repo / name).unlink()
        git("checkout-index", "-a")
        for name, data in samples.items():
            self.assertEqual(data, (repo / name).read_bytes(), name)

    def test_link_target_rejected_before_writes(self):
        other = self.root / "other"
        other.mkdir()
        alias = self.root / "alias"
        try:
            alias.symlink_to(other, target_is_directory=True)
        except OSError as exc:
            self.skipTest(str(exc))
        with self.assertRaises(ValueError):
            guidance.deploy(self.config, str(alias), "codex", True)
        dest = self.project / "CLAUDE.md"
        dest.symlink_to(other / "absent")
        with self.assertRaises(ValueError):
            guidance.deploy(self.config, str(self.project), "codex,claude", True)
        self.assertFalse((self.project/"AGENTS.md").exists())
        self.assertFalse(list(other.iterdir()))

if __name__ == "__main__":
    unittest.main()
