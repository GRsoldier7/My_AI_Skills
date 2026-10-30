"""Focused admission and sandbox configuration checks; no candidate execution."""
import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location("gate", Path(__file__).with_name("scan.py"))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.package = self.root / "skills/example"
        self.package.mkdir(parents=True)
        (self.package / "SKILL.md").write_text("---\nname: example\n---\nText.\n")

    def args(self, paths=None, manifest=None):
        return argparse.Namespace(package=paths or [], packages_file=manifest, repo_root=self.root)

    def test_enumeration_over_32_packages_is_not_truncated(self):
        paths = []
        for number in range(40):
            package = self.root / f"skills/s{number}"
            package.mkdir()
            (package / "SKILL.md").write_text("Example")
            paths.append(str(package.relative_to(self.root)))
        self.assertEqual(40, len(gate.enumerate_packages(self.args(paths))))

    def test_record_manifest_accepted(self):
        path = self.root / "packages.json"
        path.write_text(json.dumps({"skills": [{"path": "skills/example"}]}))
        self.assertEqual([self.package], gate.enumerate_packages(self.args(manifest=path)))

    def test_duplicates_fail(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            gate.enumerate_packages(self.args(["skills/example", "skills/example"]))

    def test_missing_package_fails(self):
        with self.assertRaisesRegex(ValueError, "Missing"):
            gate.enumerate_packages(self.args(["skills/missing"]))

    def test_parent_escape_fails(self):
        with self.assertRaisesRegex(ValueError, "within"):
            gate.enumerate_packages(self.args(["../outside"]))

    def test_nested_symlink_fails(self):
        (self.package / "link").symlink_to("/etc/passwd")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            gate.enumerate_packages(self.args(["skills/example"]))

    def test_empty_list_fails(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            gate.enumerate_packages(self.args())

    def test_missing_isolation_has_no_fallback(self):
        with mock.patch.object(gate.shutil, "which", return_value=None):
            with self.assertRaisesRegex(ValueError, "no unsandboxed fallback"):
                gate.sandbox_command(self.root, self.package, self.root, True)

    def test_sandbox_has_no_home_mount_and_network_isolation(self):
        with mock.patch.object(gate.shutil, "which", return_value="/usr/bin/bwrap"):
            command = gate.sandbox_command(self.root, self.package, self.root, False)
        self.assertIn("--unshare-all", command)
        self.assertIn("--clearenv", command)
        self.assertNotIn("--share-net", command)
        self.assertNotIn(str(Path.home()), command)
        self.assertEqual(command[command.index(str(self.package))-1], "--ro-bind")


if __name__ == "__main__":
    unittest.main()
