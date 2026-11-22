"""Replay the work pack's synthetic examples and verify pinned upstream files."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "skills/engineering/analytics-code-workbench/references"


def example(name, language):
    text = (CODE / (name + ".md")).read_text(encoding="utf-8")
    return re.search(r"^~~~" + language + r"\n(.+?)^~~~", text.replace(chr(96) * 3, "~~~"), re.M | re.S)[1]


class WorkSkillsTests(unittest.TestCase):
    def test_upstream_files_and_licenses_match_their_recorded_git_objects(self):
        records = json.loads((ROOT / "registry/curation.json").read_bytes())["reference_sources"]
        resources = json.loads((ROOT / "platform-configs/skill-sets/profiles.json").read_bytes())["resources"]
        for path, record in records.items():
            with self.subTest(path=path):
                family = "/".join(path.split("/")[:3])
                self.assertIn(path[len(family) + 1:], resources[family])
                data = (ROOT / path).read_bytes()
                header = f"blob {len(data)}\0".encode()
                self.assertEqual(hashlib.sha1(header + data).hexdigest(), record["blob"])
                self.assertRegex(record["source"], r"^https://github\.com/[\w.-]+/[\w.-]+/blob/[a-f0-9]{40}/[^?#]+$")
                self.assertIn(record["license"], {"MIT", "Apache-2.0"})
                project = record["source"].partition("/blob/")[0]
                self.assertTrue(any(p.startswith(family + "/LICENSE") and
                                    r["source"].startswith(project + "/blob/") and r["license"] == record["license"]
                                    for p, r in records.items()))
        self.assertGreaterEqual(len(set(r["source"].partition("/blob/")[0] for r in records.values())), 6)

    def test_python_handles_replay_zero_and_invalid_input(self):
        scope = {}
        exec(compile(example("python", "python"), "completion-rate-example", "exec"), scope)
        rate = scope["completion_rate"]
        self.assertAlmostEqual(rate([("A", 1, 2), ("B", 2, 8), ("A", 1, 2)]), .30)
        self.assertEqual(rate([("B", 2, 8)]), .25)
        for rows in ([], [("C", 0, 0)]):
            self.assertIsNone(rate(rows))
        for rows in ([("A", 1, 2), ("A", 0, 2)], [("A", 3, 2)], [("A", True, 2)], [("", 0, 1)]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                rate(rows)

    def test_sql_arithmetic_fixture_with_local_sqlite(self):
        query = example("tsql", "sql")
        with sqlite3.connect(":memory:") as conn:
            self.assertAlmostEqual(conn.execute(query).fetchone()[0], .30)
            zero = query.replace("1 AS completed, 2 AS eligible", "0 AS completed, 0 AS eligible").replace("'B', 2, 8", "'B', 0, 0")
            self.assertIsNone(conn.execute(zero).fetchone()[0])

    def test_powershell_inventory_literal_path_empty_sorted_and_missing(self):
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            self.skipTest("PowerShell is unavailable")
        with tempfile.TemporaryDirectory() as path:
            base = Path(path)
            reports = base / "quarter[1]"
            reports.mkdir()
            script = base / "example.ps1"
            script.write_text("param([string]$Fixture)\n" + example("powershell", "powershell") + """
$ErrorActionPreference = 'Stop'
if (@(Get-ReportInventory $Fixture).Count -ne 0) { throw 'Empty input' }
foreach ($name in 'B.csv','notes.txt','A.csv') { [IO.File]::WriteAllText([IO.Path]::Combine($Fixture, $name), 'x') }
$result = @(Get-ReportInventory $Fixture)
if (($result.Name -join ',') -ne 'A.csv,B.csv' -or $result[0].Length -ne 1) { throw 'Inventory mismatch' }
$failed = $false
try { Get-ReportInventory ([IO.Path]::Combine($Fixture, 'absent')) } catch { $failed = $true }
if (-not $failed) { throw 'Missing directory must fail' }
""", encoding="utf-8")
            proc = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(script), str(reports)],
                                  capture_output=True, text=True, timeout=30)
            self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
