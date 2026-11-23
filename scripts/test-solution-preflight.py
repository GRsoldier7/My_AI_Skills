#!/usr/bin/env python3
"""Exercise the offline solution checker through its public CLI with synthetic files."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


CHECK = Path(__file__).resolve().parents[1] / "skills/microsoft/power-automate/scripts/check-solution.py"
CONNECTOR = "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
FLOW = "e24993dd-817e-4c8b-b0ff-261823e538a4"
APP = "ex_requestapp"
TEMPLATE = {
    "EnvironmentVariables": [
        {"SchemaName": "ex_Count", "Value": "", "DefaultValue": "42", "IsRequired": False},
        {"SchemaName": "ex_Enabled", "Value": "", "TypeId": 100000002},
    ],
    "ConnectionReferences": [{"LogicalName": "ex_SharePoint", "ConnectionId": "", "ConnectorId": CONNECTOR}],
    "CopilotAgents": [],
}
PRIVATE = "synthetic-private-DO-NOT-PRINT"


class PreflightTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        self.zip = root / "solution.zip"
        self.template = root / "template.json"
        self.settings = root / "settings.json"
        self.target = copy.deepcopy(TEMPLATE)
        self.target["EnvironmentVariables"][0]["Value"] = 0
        self.target["EnvironmentVariables"][1]["Value"] = False
        self.target["ConnectionReferences"][0]["ConnectionId"] = PRIVATE
        self.template.write_text(json.dumps(TEMPLATE), encoding="utf-8-sig")
        self.write_target()
        self.make_archive()

    def make_archive(self, managed="1", name="DemoContract", version="1.2.3.4",
                     roots=True, payloads=True, modern=True, with_customizations=True):
        root_entries = (f'<RootComponent type="300" schemaName="{APP}"/><RootComponent type="29" id="{{{FLOW.upper()}}}"/>'
                        if roots else "")
        manifest = (f"<ImportExportXml><SolutionManifest><Managed>{managed}</Managed>"
                    f"<UniqueName>{name}</UniqueName><Version>{version}</Version><RootComponents>{root_entries}"
                    "</RootComponents></SolutionManifest></ImportExportXml>")
        with zipfile.ZipFile(self.zip, "w") as archive:
            archive.writestr("solution.xml", manifest)
            if with_customizations:
                archive.writestr("customizations.xml", "<ImportExportXml/>")
            archive.writestr("[Content_Types].xml", "<Types/>")
            if payloads:
                archive.writestr(f"CanvasApps/{APP}_DocumentUri.msapp", "synthetic-presence-only")
                definition = {"properties": {"definition": {"triggers": {}, "actions": {}}}} if modern else {}
                archive.writestr(f"Workflows/RunRequest-{FLOW.upper()}.json", json.dumps(definition))

    def write_target(self):
        self.settings.write_text(json.dumps(self.target), encoding="utf-8")

    def run_cli(self, *extra, error=None):
        result = subprocess.run(
            [sys.executable, str(CHECK), "--solution", str(self.zip), "--name", "DemoContract",
             "--version", "1.2.3.4", "--template", str(self.template), "--settings", str(self.settings), *extra],
            capture_output=True, text=True, check=False,
        )
        self.assertNotIn(PRIVATE, result.stderr + result.stdout)
        self.assertEqual(result.returncode, 0 if error is None else 1, result.stderr + result.stdout)
        self.assertIn("PASS" if error is None else error, result.stdout if error is None else result.stderr)

    def test_explicit_bindings_and_approved_artifacts(self):
        # Zero and false, a BOM and extra PAC fields all survive.
        hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in (self.zip, self.template, self.settings)]
        self.run_cli("--sha256", hashes[0], "--template-sha256", hashes[1], "--settings-sha256", hashes[2],
                     "--canvas-app", APP.upper(), "--cloud-flow", "{" + FLOW.upper() + "}")

    def test_mismatched_fingerprints(self):
        for switch in ("--sha256", "--template-sha256", "--settings-sha256"):
            with self.subTest(switch=switch):
                self.run_cli(switch, "a" * 64, error="SHA-256 mismatch")

    def test_wrong_solution_wrong_version_and_unmanaged(self):
        for key, value, field in (("managed", "0", "Managed"), ("name", "Other", "UniqueName"),
                                  ("version", "1.2.3.5", "Version"), ("version", "1.2.3", "Version")):
            with self.subTest(key=key, value=value):
                self.make_archive(**{key: value})
                self.run_cli(error=field + " mismatch")

    def test_standalone_archive(self):
        with zipfile.ZipFile(self.zip, "w") as archive:
            archive.writestr("manifest.json", "{}")
        self.run_cli(error="root solution.xml")
        self.make_archive(with_customizations=False)
        self.run_cli(error="root customizations.xml")

    def test_component_presence(self):
        for flag, name in (("--canvas-app", APP), ("--cloud-flow", FLOW)):
            for missing in ("roots", "payloads"):
                with self.subTest(flag=flag, missing=missing):
                    self.make_archive(**{missing: False})
                    self.run_cli(flag, name, error="Expected")
        self.make_archive(modern=False)
        self.run_cli("--cloud-flow", FLOW, error="cloud flow definition")
        self.run_cli("--canvas-app", "ex_unrelated", error="Expected canvas app")
        self.run_cli("--cloud-flow", "00000000-0000-0000-0000-000000000001", error="Expected cloud flow")

    def test_optional_default_requires_manual_review_when_not_explicit(self):
        self.target["EnvironmentVariables"][0].pop("Value")
        self.write_target()
        self.run_cli(error="Unresolved Value for ex_Count")

    def test_missing_extra_duplicate_rows_and_json_keys(self):
        rows = self.target["EnvironmentVariables"]
        original = copy.deepcopy(rows)
        for bad, message in ((rows[:1], "Missing EnvironmentVariables"),
                             (rows + [{"SchemaName": "ex_Extra", "Value": True}], "Unexpected"),
                             (rows + [dict(rows[0], SchemaName="EX_COUNT")], "Duplicate SchemaName")):
            self.target["EnvironmentVariables"] = bad
            self.write_target()
            self.run_cli(error=message)
        self.target["EnvironmentVariables"] = original
        self.target["ConnectionReferences"] *= 2
        self.write_target()
        self.run_cli(error="Duplicate LogicalName")
        self.settings.write_text('{"EnvironmentVariables": [], "EnvironmentVariables": []}', encoding="utf-8")
        self.run_cli(error="Duplicate JSON property")

    def test_unresolved_values_and_connector_mismatch(self):
        for value in (None, "", "   ", {}, [], "<target>", "prefix/{{replace}}", "TODO", {"site": "$(SITE)"}):
            with self.subTest(value=value):
                self.target["EnvironmentVariables"][0]["Value"] = value
                self.write_target()
                self.run_cli(error="Unresolved Value")
        self.target["EnvironmentVariables"][0]["Value"] = {"items": [0, False, None]}
        self.target["ConnectionReferences"][0]["ConnectorId"] = PRIVATE
        self.write_target()
        self.run_cli(error="ConnectorId mismatch")
        self.target["ConnectionReferences"][0].update(ConnectorId=CONNECTOR, ConnectionId="   ")
        self.write_target()
        self.run_cli(error="Unresolved ConnectionId")

    def test_intentional_no_mappings(self):
        empty = {"EnvironmentVariables": [], "ConnectionReferences": [], "CopilotAgents": []}
        for file in (self.template, self.settings):
            file.write_text(json.dumps(empty), encoding="utf-8")
        self.run_cli()

    def test_reviewed_target_binding_changed(self):
        approved = hashlib.sha256(self.settings.read_bytes()).hexdigest()
        self.target["ConnectionReferences"][0]["ConnectionId"] = "different-syntactically-valid-id"
        self.write_target()
        self.run_cli("--settings-sha256", approved, error="target settings SHA-256 mismatch")


if __name__ == "__main__":
    unittest.main()
