"""Regression tests for registry checks and cross-platform generation."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "skill_registry", Path(__file__).with_name("generate-skill-registry.py")
)
REGISTRY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REGISTRY)


class RegistryPortabilityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve() / "repo with spaces"
        self.root.mkdir()
        self.git("init", "-q")
        self.git("config", "core.symlinks", "false")
        self.git("config", "core.autocrlf", "false")

        self.old = "skills/old/compat"
        self.new = "skills/new/current"
        self.target = b"../new/current"
        self.link = self.root / self.old
        self.link.parent.mkdir(parents=True)
        self.destination = self.root / self.new
        self.destination.mkdir(parents=True)
        self.manifest = self.root / "moved.json"
        self.write_move(self.old, self.new)
        settings = patch.multiple(
            REGISTRY, REPO_DIR=self.root, MOVED_FILE=self.manifest,
            GLOBAL_SET=self.root / "global.txt",
        )
        settings.start()
        self.addCleanup(settings.stop)

    def git(self, *args, input=None):
        return subprocess.run(
            ["git", *args], cwd=self.root, input=input, capture_output=True, check=True
        ).stdout

    def write_move(self, old, new):
        self.manifest.write_text(json.dumps({"moved": {old: new}}), encoding="utf-8")

    def checkout_placeholder(self, target=None):
        target = self.target if target is None else target
        oid = self.git("hash-object", "-w", "--stdin", input=target).decode("ascii").strip()
        self.git("update-index", "--add", "--cacheinfo", f"120000,{oid},{self.old}")
        self.git("checkout-index", "--force", "--", self.old)
        self.assertFalse(self.link.is_symlink())
        self.assertEqual(self.link.read_bytes(), target)

    def failures(self):
        fails, _ = REGISTRY.registry_checks([], {})
        return fails

    def test_exact_tracked_placeholder_is_a_compatibility_link(self):
        self.checkout_placeholder()
        self.assertEqual(self.failures(), [])

    def test_ordinary_tracked_file_is_not_a_compatibility_link(self):
        self.link.write_bytes(self.target)
        self.git("add", "--", self.old)
        self.assertTrue(self.failures())

    def test_alternate_index_cannot_disguise_an_ordinary_tracked_file(self):
        self.link.write_bytes(self.target)
        self.git("add", "--", self.old)
        alternate = self.root / ".git" / "alternate-index"
        with patch.dict(os.environ, {"GIT_INDEX_FILE": str(alternate)}):
            self.checkout_placeholder()
            self.assertTrue(self.git("ls-files", "--stage", "--", self.old).startswith(b"120000 "))
            self.assertTrue(self.failures())

    def test_altered_placeholder_is_rejected_even_when_it_resolves_correctly(self):
        self.checkout_placeholder()
        for altered in (b"../new/./current", self.target + b"\n", b"..\\new\\current"):
            with self.subTest(altered=altered):
                self.link.write_bytes(altered)
                self.assertTrue(self.failures())

    def test_wrong_case_cannot_borrow_a_tracked_index_entry(self):
        self.checkout_placeholder()
        self.write_move(self.old.upper(), self.new)
        self.assertTrue(self.failures())

    def test_tracked_placeholder_must_resolve_to_the_mapped_destination(self):
        (self.destination.parent / "unrelated").mkdir()
        self.checkout_placeholder(b"../new/unrelated")
        self.assertTrue(self.failures())

    def test_tracked_placeholder_cannot_leave_and_reenter_repository(self):
        self.checkout_placeholder(f"../../../{self.root.name}/{self.new}".encode("utf-8"))
        self.assertTrue(self.failures())

    def test_tracked_placeholder_cannot_leave_and_reenter_through_symlinks(self):
        alias = self.destination.parent / "alias"
        outside = self.root.parent / "outside"
        try:
            alias.symlink_to(Path("current"), target_is_directory=True)
        except OSError as error:
            if getattr(error, "winerror", None) == 1314:
                self.skipTest(f"Windows does not allow creating native links here ({error})")
            raise
        self.checkout_placeholder(b"../new/alias")
        self.assertEqual(self.failures(), [])
        alias.unlink()
        outside.symlink_to(Path(self.root.name) / self.new, target_is_directory=True)
        alias.symlink_to(Path("../../../outside"), target_is_directory=True)
        self.assertEqual(alias.resolve(strict=True), self.destination)
        self.assertTrue(self.failures())

    def test_tracked_placeholder_and_mapped_destination_cannot_escape(self):
        outside = self.root.parent / "outside"
        outside.mkdir()
        self.checkout_placeholder(b"../../../outside")
        self.write_move(self.old, "../outside")
        self.assertTrue(self.failures())

    def test_target_must_exist(self):
        self.checkout_placeholder()
        self.destination.rmdir()
        self.assertIn(f"moved target missing: {self.new}", self.failures())

    def test_native_relative_symlink_and_wrong_targets(self):
        try:
            self.link.symlink_to(Path(self.target.decode("ascii")), target_is_directory=True)
        except OSError as error:
            if getattr(error, "winerror", None) == 1314:
                self.skipTest(f"Windows does not allow creating native links here ({error})")
            raise
        self.assertTrue(self.link.exists())
        self.assertEqual(self.failures(), [])
        for bad in ("../wrong", self.destination, f"../../../{self.root.name}/{self.new}"):
            with self.subTest(target=bad):
                self.link.unlink()
                self.link.symlink_to(Path(bad), target_is_directory=True)
                self.assertTrue(self.failures())

    def test_discovery_order_uses_portable_case_sensitive_paths(self):
        skills = self.root / "skills"
        for name in ("a-last", "Z-first"):
            skill = skills / name
            skill.mkdir()
            (skill / "SKILL.md").touch()
        lower_case = skills / "lower-case-only"
        lower_case.mkdir()
        (lower_case / "skill.md").touch()
        files = REGISTRY.find_skill_files(skills)
        self.assertEqual([p.parent.name for p in files], ["Z-first", "a-last"])

    def test_license_order_uses_portable_case_sensitive_names(self):
        skill = self.destination
        (skill / "license-a.txt").write_text("Apache License", encoding="utf-8")
        (skill / "LICENSE-Z.txt").write_text("MIT License", encoding="utf-8")
        self.assertEqual(REGISTRY._detect_license(skill, {}, {}, ""), "MIT")

    def test_vendored_patterns_match_portable_path_case(self):
        skill = self.root / "skills" / "Domain" / "External"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").touch()
        curation = self.root / "curation.json"
        curation.write_text("{}", encoding="utf-8")
        config = self.root / "lint-config.json"
        config.write_text('{"vendored_paths": ["skills/domain/*"]}', encoding="utf-8")
        with patch.multiple(
            REGISTRY, SKILLS_ROOT=self.root / "skills", CURATION_FILE=curation, LINT_CONFIG=config
        ):
            entries, _ = REGISTRY.build_registry()
        self.assertEqual(entries[0]["origin"], "library")

    def test_registry_regeneration_writes_lf_and_check_accepts_git_crlf(self):
        agents = self.root / "agents"
        agents.mkdir()
        agent = agents / "test.md"
        agent.write_bytes(b"# Agent\r\n\r\nExisting notes.\r\n")
        registry = self.root / "skills.json"
        curation = {"agents": {"test": {}}}
        self.manifest.unlink()
        with (
            patch.multiple(REGISTRY, REGISTRY_JSON=registry, AGENTS_DIR=agents),
            patch.object(REGISTRY, "build_registry", return_value=([], curation)),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(REGISTRY.registry_main(write=True), 0)
            for path in (agent, registry):
                content = path.read_bytes()
                self.assertNotIn(b"\r", content)
                path.write_bytes(content.replace(b"\n", b"\r\n"))
            self.assertEqual(REGISTRY.registry_main(write=False), 0)
            self.assertEqual(REGISTRY.registry_main(write=True), 0)
        self.assertNotIn(b"\r", agent.read_bytes())
        self.assertNotIn(b"\r", registry.read_bytes())
        self.assertIn(b"Existing notes.\n", agent.read_bytes())


if __name__ == "__main__":
    unittest.main()
