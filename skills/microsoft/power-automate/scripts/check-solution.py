#!/usr/bin/env python3
"""Offline structural check for a managed Dataverse solution and explicit target bindings."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import uuid
from xml.etree import ElementTree as ET
import zipfile
import zlib

MIB = 1024 * 1024
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,255}")
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
MARKER = re.compile(
    r"\{\{[^{}\n]+\}\}|\$\{[^{}\n]+\}|\$\([A-Za-z_][\w.:-]*\)|__[\w-]+__|"
    r"<[A-Za-z][\w -]*>|(?:^|[/=])(?:TODO|TBD|CHANGEME|REPLACE[_ -]?ME)(?:$|[/&])",
    re.IGNORECASE,
)


class Invalid(ValueError):
    pass


class ManifestParser(ET.TreeBuilder):
    def doctype(self, name, public_id, system_id):
        raise Invalid("Manifest contains a document type. Use the original solution export.")


def check_hash(actual, expected, label):
    if expected is not None:
        if not re.fullmatch(r"[0-9A-Fa-f]{64}", expected):
            raise Invalid(f"Supply the complete 64-character {label} SHA-256.")
        if actual != expected.lower():
            raise Invalid(f"{label} SHA-256 mismatch. Retrieve the exact reviewed artifact for this target.")


def workflow_id(value):
    try:
        return str(uuid.UUID(value.strip("{}")))
    except (AttributeError, ValueError):
        raise Invalid("Supply a workflow GUID from the approved component inventory.") from None


def check_components(args, manifest, archive):
    root_components = manifest.findall("SolutionManifest/RootComponents/RootComponent")
    app_names = {(item.get("schemaName") or "").casefold() for item in root_components if item.get("type") == "300"}
    flow_ids = {(item.get("id") or "").strip("{}").casefold() for item in root_components if item.get("type") == "29"}
    members = archive.infolist()
    for app in args.canvas_app:
        if not IDENTIFIER.fullmatch(app):
            raise Invalid("Supply the canvas app schema name from the approved component inventory.")
        filename = f"canvasapps/{app}_documenturi.msapp".casefold()
        matches = [item for item in members if item.filename.casefold() == filename and item.file_size]
        if app.casefold() not in app_names or len(matches) != 1:
            raise Invalid(f"Expected canvas app {app}: check its root component and packaged .msapp, or review the layout manually.")
    for raw_id in args.cloud_flow:
        guid = workflow_id(raw_id)
        pattern = re.compile(r"Workflows/[^/]+-" + re.escape(guid) + r"\.json", re.IGNORECASE)
        matches = [item for item in members if pattern.fullmatch(item.filename)]
        if guid not in flow_ids or len(matches) != 1 or not 0 < matches[0].file_size <= 8 * MIB:
            raise Invalid(f"Expected cloud flow {guid}: check its root component and workflow JSON, or review the layout manually.")
        body = json.loads(archive.read(matches[0]), object_pairs_hook=unique_properties, parse_constant=invalid_constant)
        properties = body.get("properties") if isinstance(body, dict) else None
        definition = properties.get("definition") if isinstance(properties, dict) else None
        if not isinstance(definition, dict) or not all(isinstance(definition.get(k), dict) for k in ("triggers", "actions")):
            raise Invalid(f"Expected cloud flow definition for {guid}. Review the packaged workflow format.")


def archive_check(args):
    if not args.solution.is_file() or args.solution.stat().st_size > 512 * MIB:
        raise Invalid("Use a local solution ZIP of at most 512 MiB or arrange a separate package review.")
    with args.solution.open("rb") as handle:
        digest = hashlib.sha256()
        for chunk in iter(lambda: handle.read(MIB), b""):
            digest.update(chunk)
        fingerprint = digest.hexdigest()
        check_hash(fingerprint, args.sha256, "solution ZIP")
        with zipfile.ZipFile(handle) as archive:
            items = archive.infolist()
            if len(items) > 50000:
                raise Invalid("Package exceeds the 50,000-member review limit.")
            for name in ("solution.xml", "customizations.xml", "[Content_Types].xml"):
                matches = [item for item in items if item.filename.casefold() == name.casefold()]
                if len(matches) != 1 or matches[0].filename != name or not matches[0].file_size:
                    raise Invalid(f"Expected one nonempty root {name}. Select the managed solution export.")
            entry = archive.getinfo("solution.xml")
            if entry.file_size > 8 * MIB:
                raise Invalid("Manifest exceeds 8 MiB. Arrange a separate package review.")
            manifest = ET.fromstring(archive.read(entry), parser=ET.XMLParser(target=ManifestParser()))
            if args.canvas_app or args.cloud_flow:
                check_components(args, manifest, archive)
    sections = manifest.findall("SolutionManifest")
    if manifest.tag != "ImportExportXml" or len(sections) != 1:
        raise Invalid("Expected one SolutionManifest within the Dataverse ImportExportXml manifest.")
    for tag, expected in (("Managed", "1"), ("UniqueName", args.name), ("Version", args.version)):
        fields = sections[0].findall(tag)
        if len(fields) != 1 or (fields[0].text or "").strip() != expected:
            raise Invalid(f"Manifest {tag} mismatch. Check the release identity and managed export option.")
    return fingerprint


def unique_properties(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid("Duplicate JSON property. Regenerate the template or correct the settings.")
        result[key] = value
    return result


def invalid_constant(_):
    raise Invalid("Use standard JSON values in the deployment files.")


def load_settings(path, label, approved_hash):
    if not path.is_file() or path.stat().st_size > 4 * MIB:
        raise Invalid(f"Use a local {label} JSON file of at most 4 MiB.")
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    check_hash(digest, approved_hash, label)
    try:
        value = json.loads(data, object_pairs_hook=unique_properties, parse_constant=invalid_constant)
    except (UnicodeError, json.JSONDecodeError):
        raise Invalid(f"Invalid {label} JSON. Use the native PAC deployment settings format.") from None
    if not isinstance(value, dict):
        raise Invalid(f"Expected a JSON object in {label}.")
    return value, digest


def indexed(document, section, key, label):
    rows = document.get(section)
    if not isinstance(rows, list):
        raise Invalid(f"{label} requires the PAC {section} array. Regenerate or copy the template.")
    result = {}
    seen = set()
    for position, row in enumerate(rows, start=1):
        name = row.get(key) if isinstance(row, dict) else None
        if not isinstance(name, str) or not IDENTIFIER.fullmatch(name):
            raise Invalid(f"Check {key} at {label} {section} row {position}.")
        if name.casefold() in seen:
            raise Invalid(f"Duplicate {key} in {label}: {name}. Keep one mapping.")
        seen.add(name.casefold())
        result[name] = row
    return result


def has_marker(value):
    if isinstance(value, str):
        return bool(MARKER.search(value))
    if isinstance(value, dict):
        return any(has_marker(item) for item in value.values())
    if isinstance(value, list):
        return any(has_marker(item) for item in value)
    return False


def unresolved(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return True
    return (isinstance(value, (list, dict)) and not value) or has_marker(value)


def bindings(template, settings):
    counts = []
    for section, key, field in (
        ("EnvironmentVariables", "SchemaName", "Value"),
        ("ConnectionReferences", "LogicalName", "ConnectionId"),
    ):
        expected = indexed(template, section, key, "PAC template")
        supplied = indexed(settings, section, key, "target settings")
        missing = sorted(expected.keys() - supplied.keys())
        extra = sorted(supplied.keys() - expected.keys())
        if missing:
            raise Invalid(f"Missing {section} mapping: {missing[0]}. Copy the row from the fresh PAC template.")
        if extra:
            raise Invalid(f"Unexpected {section} mapping: {extra[0]}. Check the template and target file.")
        for name, row in supplied.items():
            binding = row.get(field)
            if unresolved(binding) or (field == "ConnectionId" and not isinstance(binding, str)):
                raise Invalid(f"Unresolved {field} for {name}. Supply the reviewed target binding.")
            if field == "ConnectionId":
                connector = expected[name].get("ConnectorId")
                if not isinstance(connector, str) or unresolved(connector) or row.get("ConnectorId") != connector:
                    raise Invalid(f"ConnectorId mismatch or missing for {name}. Restore the PAC connector ID.")
        counts.append(len(expected))
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solution", required=True, type=Path, help="Original managed solution ZIP")
    parser.add_argument("--name", required=True, help="Approved solution unique name")
    parser.add_argument("--version", required=True, help="Approved four-part solution version")
    parser.add_argument("--template", required=True, type=Path, help="Fresh PAC settings template from that ZIP")
    parser.add_argument("--settings", required=True, type=Path, help="Reviewed target-specific PAC JSON")
    parser.add_argument("--canvas-app", action="append", default=[], help="Expected canvas app schema name (repeatable)")
    parser.add_argument("--cloud-flow", action="append", default=[], help="Expected solution cloud workflow GUID (repeatable)")
    parser.add_argument("--sha256", help="Digest of the QA-tested solution ZIP")
    parser.add_argument("--template-sha256", help="Digest of the PAC template recorded with the tested ZIP")
    parser.add_argument("--settings-sha256", help="Digest of settings independently approved for this target")
    args = parser.parse_args()
    try:
        if not IDENTIFIER.fullmatch(args.name) or not VERSION.fullmatch(args.version):
            raise Invalid("Supply a solution unique name and a four-part numeric version (e.g. 1.2.0.0).")
        digest = archive_check(args)
        template, template_hash = load_settings(args.template, "PAC template", args.template_sha256)
        settings, settings_hash = load_settings(args.settings, "target settings", args.settings_sha256)
        variables, connections = bindings(template, settings)
    except Invalid as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError, RecursionError,
            RuntimeError, NotImplementedError, EOFError, zlib.error, LookupError):
        print("BLOCKED: Cannot read the ZIP, manifest or JSON. Check format, access and integrity.", file=sys.stderr)
        return 1
    print(f"PASS (offline structure and explicit mappings): {args.name} {args.version} managed")
    print(f"Mapped environment variables: {variables}. Connection references: {connections}.")
    print(f"Requested component matches: {len(args.canvas_app)} canvas apps, {len(args.cloud_flow)} cloud flows.")
    print(f"ZIP SHA-256: {digest}\nTemplate SHA-256: {template_hash}\nTarget settings SHA-256: {settings_hash}")
    print("Operator verifies template origin, target identity, binding values, extension metadata and runtime import.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
