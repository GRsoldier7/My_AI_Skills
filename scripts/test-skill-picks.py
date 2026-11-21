"""Exercise the public selection and export commands in disposable directories."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import importlib
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

picks = importlib.import_module("skill-picks")
ROOT = picks.ROOT
SIZES = {
    "faith-personal": 3, "faith-teaching": 4, "faith-publishing": 3,
    "work-bi": 2, "consulting": 2, "business-web": 2, "govcon": 2,
    "home": 1, "deep-research": 1,
}
FOUNDATION = "skills/faith/bible-study-theologian/references/faith-foundation.md"


class SkillPicksTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.temp = Path(tmp.name).resolve()
        self.catalog = picks.config(ROOT)

    def copy_selected(self, profile):
        fixture = self.temp / "checkout"
        _, entries = picks.select(ROOT, self.catalog, profile)
        sources = ["registry/skills.json", f"{picks.SETS}/profiles.json", f"{picks.SETS}/{profile}.txt",
                   *picks.shared_documents(self.catalog[0], entries)]
        for source in sources:
            (fixture / source).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / source, fixture / source)
        for row in entries:
            shutil.copytree(ROOT / row["path"], fixture / row["path"])
        return fixture

    def test_all_manual_profile_and_tool_pairs_have_complete_reproducible_receipts(self):
        pairs = 0
        catalog = self.catalog
        self.assertEqual(set(catalog[0]["profiles"]), set(SIZES))
        for profile, count in SIZES.items():
            settings, entries = picks.select(ROOT, catalog, profile)
            self.assertEqual(len(entries), count)
            expected = {"chatgpt", "copilot"} if profile == "work-bi" else set(picks.HOSTS)
            self.assertEqual(set(settings["platforms"]), expected)
            for host in sorted(expected):
                with self.subTest(profile=profile, host=host):
                    target = self.temp / f"{profile}-{host}"
                    with redirect_stdout(io.StringIO()):
                        picks.main(["export", profile, "--platform", host, "--output", str(target)])
                    receipt = {}
                    for line in (target / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
                        digest, path = line.split("  ", 1)
                        self.assertNotIn(path, receipt)
                        receipt[path] = digest
                    self.assertEqual(list(receipt), sorted(receipt))
                    actual = {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()}
                    self.assertEqual(set(receipt) | {"SHA256SUMS"}, actual)
                    for path, digest in receipt.items():
                        content = (target / path).read_bytes()
                        self.assertEqual(hashlib.sha256(content).hexdigest(), digest)
                        if path.startswith("skills/"):
                            self.assertEqual((ROOT / path).read_bytes(), content)
                    reading = (target / "INSTRUCTIONS.md").read_text(encoding="utf-8")
                    self.assertIn(settings["context"], reading)
                    for row in entries:
                        self.assertIn(f"## Source section: {row['path']}/SKILL.md", reading)
                    if profile.startswith("faith-"):
                        self.assertIn(FOUNDATION, receipt)
                        self.assertIn(f"## Source section: {FOUNDATION}", reading)
                    if profile == "work-bi":
                        self.assertIn("skills/CONNECTORS.md", receipt)
                        self.assertIn("skills/engineering/validate-data/LICENSE", receipt)
                        self.assertIn("TERMS AND CONDITIONS FOR USE", reading)
                        self.assertIn("Two synthetic groups", reading)
                    if profile in ("business-web", "consulting", "govcon"):
                        self.assertIn("skills/THIRD-PARTY-NOTICES.md", receipt)
                        self.assertIn("Copyright (c) 2026", reading)
                    if profile == "business-web":
                        self.assertIn("supplied measurements", reading)
                    pairs += 1
        self.assertEqual(pairs, 50)
        for name in ("faith-personal", "work-bi"):
            first = self.temp / f"{name}-chatgpt"
            expected = picks.assemble(ROOT, catalog, name, "chatgpt")
            self.assertEqual((first / "SHA256SUMS").read_bytes(), expected["SHA256SUMS"])

    def test_cli_list_inspect_and_read_only_failures(self):
        for args, phrase in [
            (["list", "--platform", "claude"], "faith-personal (3)"),
            (["inspect", "faith-publishing"], "skills/faith/social-media-apologetics/SKILL.md"),
        ]:
            out = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/skill-picks.py"), *args],
                                 cwd=self.temp, capture_output=True, text=True, check=True)
            self.assertIn(phrase, out.stdout)
            if "list" in args:
                self.assertNotIn("work-bi", out.stdout)
        for args in [
            ["export", "work-bi", "--platform", "codex", "--output", "bad"],
            ["export", "../home", "--platform", "chatgpt", "--output", "bad"],
        ]:
            out = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/skill-picks.py"), *args],
                                 cwd=self.temp, capture_output=True)
            self.assertNotEqual(0, out.returncode)
        self.assertEqual([], list(self.temp.iterdir()))

    def test_ineligible_duplicate_and_unknown_registrations(self):
        fixture = self.copy_selected("home")
        real = "skills/core/personal-productivity"
        entry = next(row for row in self.catalog[1] if row["path"] == real)
        for values in ({"portable": False}, {"status": "review"}, {"name": "alias"}, {"dir": "anything"}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                picks.select(fixture, (self.catalog[0], [dict(entry, **values)]), "home")
        for records in ([], [entry, entry], [entry, dict(entry, path="skills/other/personal-productivity")]):
            with self.subTest(count=len(records)), self.assertRaises(ValueError):
                picks.select(fixture, (self.catalog[0], records), "home")
        for text in (real + "\n" + real, "../private/notes", "skills/../private", "skills/core/wrapup",
                     "agents/grok-bot/skills/skill-scout"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                (fixture / picks.SETS / "home.txt").write_text(text, encoding="utf-8")
                picks.select(fixture, self.catalog, "home")
        (fixture / picks.SETS / "home.txt").write_text(real, encoding="utf-8")
        (fixture / real / "SKILL.md").unlink()
        with self.assertRaises(ValueError):
            picks.select(fixture, self.catalog, "home")

    def test_private_extra_and_missing_sibling_fail_before_output(self):
        fixture = self.copy_selected("faith-personal")
        skill = fixture / "skills/faith/prayer-and-reflection"
        private = skill / "private-notes.md"
        private.write_text("Private fixture", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            picks.assemble(fixture, self.catalog, "faith-personal", "chatgpt")
        private.unlink()
        set_path = fixture / picks.SETS / "faith-personal.txt"
        text = set_path.read_text(encoding="utf-8")
        set_path.write_text(text.replace("skills/faith/bible-study-theologian\n", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unbundled reference"):
            picks.assemble(fixture, self.catalog, "faith-personal", "chatgpt")

    def test_malformed_profile_and_resource_data(self):
        settings = self.catalog[0]["profiles"]["work-bi"]
        for changes in ({"platforms": ["chatgpt", "codex"]}, {"purpose": ""}, {"platforms": ["muse", "muse"]},
                        {"platforms": None}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                manifest = deepcopy(self.catalog[0])
                manifest["profiles"]["work-bi"] = dict(settings, **changes)
                picks.select(ROOT, (manifest, self.catalog[1]), "work-bi")
        manifest = deepcopy(self.catalog[0])
        manifest["resources"]["skills/microsoft/power-bi"].append("../private.md")
        with self.assertRaisesRegex(ValueError, "resource"):
            picks.select(ROOT, (manifest, self.catalog[1]), "work-bi")

    def test_existing_linked_and_traversing_targets_are_preserved(self):
        target = self.temp / "existing"
        target.mkdir()
        sentinel = target / "owner.txt"
        sentinel.write_bytes(b"owner")
        for path in (target, target / ".." / "new", self.temp / "missing-parent" / "new"):
            with self.subTest(path=path), self.assertRaises((ValueError, OSError)):
                picks.output_path(str(path), ROOT)
        self.assertEqual(sentinel.read_bytes(), b"owner")
        new = self.temp / "new"
        self.assertEqual(new, picks.output_path(str(new), ROOT))
        reviewed = self.temp / ".bundle-cache" / "reviewed"
        reviewed.mkdir(parents=True)
        self.assertEqual(reviewed / "new", picks.output_path(str(reviewed / "new"), reviewed))
        with self.assertRaisesRegex(ValueError, "source directories"):
            picks.output_path(str(reviewed / "SKILLS" / "new"), reviewed)
        alias = self.temp / "alias"
        try:
            alias.symlink_to(target, target_is_directory=True)
        except OSError as exc:
            self.skipTest(str(exc))
        with self.assertRaises(ValueError):
            picks.output_path(str(alias / "new"), ROOT)
        self.assertFalse((target / "new").exists())
        dangling = self.temp / "dangling"
        dangling.symlink_to(self.temp / "missing")
        with self.assertRaises(ValueError):
            picks.output_path(str(dangling), ROOT)

    def test_linked_source_is_rejected(self):
        fixture = self.copy_selected("faith-personal")
        reference = fixture / FOUNDATION
        shadow = self.temp / "unrelated.md"
        shadow.write_text("private fixture", encoding="utf-8")
        reference.unlink()
        try:
            reference.symlink_to(shadow)
        except OSError as exc:
            self.skipTest(str(exc))
        with self.assertRaises(ValueError):
            picks.assemble(fixture, self.catalog, "faith-personal", "chatgpt")

    def test_interrupted_export_keeps_a_concurrently_replaced_file(self):
        target = self.temp / "pack"
        owner_file = self.temp / "owner.md"
        owner_file.write_bytes(b"owner version")
        original = Path.open
        def replace_during_export(path, *args, **kwargs):
            if path.name == "SHA256SUMS":
                owner_file.replace(target / "README.md")
                raise OSError("interrupted")
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", replace_during_export), self.assertRaisesRegex(OSError, "interrupted"):
            picks.write_pack(target, {"README.md": b"guide", "SHA256SUMS": b"receipt"})
        self.assertEqual((target / "README.md").read_bytes(), b"owner version")

    def test_failed_write_and_concurrent_export_preserve_data(self):
        target = self.temp / "pack"
        content = {"skills/test/SKILL.md": b"read", "README.md": b"guide", "SHA256SUMS": b"receipt"}
        original = Path.open
        def unavailable(path, *args, **kwargs):
            if path.name == "SHA256SUMS":
                raise OSError("injected full disk")
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", unavailable), self.assertRaisesRegex(OSError, "full disk"):
            picks.write_pack(target, content)
        self.assertFalse(target.exists())
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(picks.write_pack, target, content) for _ in range(2)]
        self.assertEqual(sum(f.exception() is None for f in futures), 1)
        self.assertTrue(any(isinstance(f.exception(), FileExistsError) for f in futures))
        self.assertEqual((target / "README.md").read_bytes(), b"guide")


if __name__ == "__main__":
    unittest.main()
