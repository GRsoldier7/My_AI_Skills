#!/usr/bin/env python3
"""Find a small curated skill set and export one local, manually usable reading pack."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import posixpath
import re
import stat
import sys
from urllib.parse import unquote, urlsplit

from checked_paths import directory, existing_file, metadata

ROOT = Path(__file__).resolve().parents[1]
SETS = "platform-configs/skill-sets"
HOSTS = {
    "chatgpt": "Attach the reading copy to the intended chat or use its relevant sections in an approved project. Keep standing instructions short.",
    "copilot": "Provide the reading copy or the relevant sections as context in the approved Copilot workspace.",
    "claude": "Read the relevant workflow in Claude. For native Claude Code discovery, follow the repository's device guide separately.",
    "codex": "Point Codex at the selected source file and its references. The repository installer owns native installation.",
    "muse": "Give Muse the selected instructions as context and try the example in the intended profile.",
    "hermes": "Give the intended Hermes session the selected instructions and try the example with that agent's available tools.",
}
PUBLIC_DOCUMENTS = {"skills/CONNECTORS.md", "skills/THIRD-PARTY-NOTICES.md"}
PACKAGE = re.compile(r"skills/[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*")
RESOURCE = re.compile(r"(?:agents/openai\.yaml|references/[a-z0-9]+(?:-[a-z0-9]+)*\.md|LICENSE(?:\.txt)?)")
LINK = re.compile(r"\[([^\]\n]+)\]\(([^()\s]+)\)")
FIELDS = {"purpose", "context", "example", "platforms"}


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_source(root, relative):
    path = root / relative
    directory(path.parent)
    body = existing_file(path)
    if body is None:
        raise ValueError(f"Missing required file: {relative}")
    return body


def config(root):
    manifest = json.loads(read_source(root, f"{SETS}/profiles.json"), object_pairs_hook=unique_keys)
    registry = json.loads(read_source(root, "registry/skills.json"), object_pairs_hook=unique_keys)
    if (not isinstance(manifest, dict) or manifest.get("schema") != 1 or
            not all(isinstance(manifest.get(k), dict) for k in ("profiles", "resources", "shared_documents"))):
        raise ValueError("Invalid skill selection manifest")
    if not isinstance(registry, dict) or registry.get("schema") != 1 or not isinstance(registry.get("skills"), list):
        raise ValueError("Unsupported skill registry")
    for path, packages in manifest["shared_documents"].items():
        if (path not in PUBLIC_DOCUMENTS or not isinstance(packages, list) or not packages or
                any(not isinstance(item, str) or item not in manifest["resources"] for item in packages)
                or len(packages) != len(set(packages))):
            raise ValueError(f"Invalid shared resource declaration: {path}")
    return manifest, registry["skills"]


def select(root, catalog, profile):
    manifest, registry = catalog
    if not isinstance(profile, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", profile) or profile not in manifest["profiles"]:
        raise ValueError(f"Unknown profile: {profile}")
    settings = manifest["profiles"][profile]
    if (not isinstance(settings, dict) or set(settings) != FIELDS or
            not all(isinstance(settings[key], str) and settings[key].strip() for key in ("purpose", "context", "example"))):
        raise ValueError(f"Invalid purpose, context or example for {profile}")
    hosts = settings["platforms"]
    if (not isinstance(hosts, list) or not hosts or any(not isinstance(host, str) or host not in HOSTS for host in hosts)
            or len(set(hosts)) != len(hosts) or (profile == "work-bi" and set(hosts) - {"chatgpt", "copilot"})):
        raise ValueError(f"Invalid receiving platforms for {profile}")
    entries = []
    lines = read_source(root, f"{SETS}/{profile}.txt").decode("utf-8").splitlines()
    paths = [part for line in lines if (part := line.partition("#")[0].strip())]
    if not 1 <= len(paths) <= 4 or len(paths) != len(set(paths)):
        raise ValueError(f"Choose 1–4 distinct canonical packages for {profile}")
    for path in paths:
        if not PACKAGE.fullmatch(path) or path not in manifest["resources"]:
            raise ValueError(f"Unreviewed or invalid public package: {path}")
        name = path.rsplit("/", 1)[1]
        matches = [r for r in registry if isinstance(r, dict) and
                   (r.get("path") == path or r.get("name") == name or r.get("dir") == name)]
        if len(matches) != 1:
            raise ValueError(f"Expected one registry entry for {path}")
        row = matches[0]
        if (row.get("portable") is not True or row.get("status") not in ("core", "optional") or
                row.get("name") != name or row.get("dir") != name or row.get("path") != path):
            raise ValueError(f"Ineligible status, identity or portability: {path}")
        extras = manifest["resources"][path]
        if (not isinstance(extras, list) or any(not isinstance(item, str) or not RESOURCE.fullmatch(item) for item in extras)
                or len(set(extras)) != len(extras)):
            raise ValueError(f"Invalid reviewed resource list for {path}")
        if not read_source(root, f"{path}/SKILL.md"):
            raise ValueError(f"Empty skill source: {path}")
        entries.append(row)
    return settings, entries


def package_files(root, row, extras):
    relative = row["path"]
    base = root / relative
    directory(base)
    allowed = {"SKILL.md", *extras}
    # Walk only explicit directories. A private overlay, a new resource or a link
    # is a reason to review the package before copying any part of it.
    folders = {Path(item).parent.as_posix() for item in allowed}
    actual = set()
    for folder in sorted(folders):
        parent = base / folder
        directory(parent)
        for child in parent.iterdir():
            name = child.relative_to(base).as_posix()
            mode = metadata(child).st_mode
            if stat.S_ISDIR(mode) and name in folders:
                continue
            if not stat.S_ISREG(mode) or name not in allowed:
                raise ValueError(f"Unreviewed package entry: {relative}/{name}")
            actual.add(name)
    if actual != allowed:
        raise ValueError(f"Missing reviewed resources in {relative}: {', '.join(sorted(allowed - actual))}")
    files = {f"{relative}/{name}": read_source(root, f"{relative}/{name}") for name in sorted(allowed)}
    source = files[f"{relative}/SKILL.md"].decode("utf-8").splitlines()
    if not source or source[0] != "---" or "---" not in source[1:]:
        raise ValueError(f"Missing skill frontmatter: {relative}")
    front = source[1:source.index("---", 1)]
    if f"name: {row['name']}" not in front:
        raise ValueError(f"Source and registry name differ: {relative}")
    if row.get("origin") == "vendored" and not any(name.startswith("LICENSE") for name in allowed):
        raise ValueError(f"Missing vendored license: {relative}")
    return files


def reading_text(path, body, files):
    text = body.decode("utf-8")
    if path.endswith("/SKILL.md"):
        lines = text.splitlines()
        text = "\n".join(lines[lines.index("---", 1) + 1:]).strip()

    def root_link(match):
        label, url = match.groups()
        target = urlsplit(url)
        if target.scheme in {"https", "http", "mailto"} or (not target.path and not target.netloc):
            return match[0]
        raw = unquote(target.path)
        if target.scheme or target.netloc or raw.startswith("/") or "\\" in raw or ":" in raw:
            raise ValueError(f"Unsupported link in {path}: {url}")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), raw))
        if resolved not in files:
            raise ValueError(f"Unbundled reference in {path}: {url}")
        suffix = f"#{target.fragment}" if target.fragment else ""
        return f"[{label}]({resolved}{suffix})"

    return LINK.sub(root_link, text).strip()


def shared_documents(manifest, entries):
    selected = {row["path"] for row in entries}
    return [path for path, packages in manifest["shared_documents"].items() if selected.intersection(packages)]


def assemble(root, catalog, profile, host):
    settings, entries = select(root, catalog, profile)
    if host not in settings["platforms"]:
        raise ValueError(f"Unsupported platform {host} for {profile}")
    files = {}
    for row in entries:
        files.update(package_files(root, row, catalog[0]["resources"][row["path"]]))
    for path in shared_documents(catalog[0], entries):
        files[path] = read_source(root, path)
    entrypoints = [row["path"] + "/SKILL.md" for row in entries]
    workflow_links = [f"- [`{r['name']}`]({r['path']}/SKILL.md) ({r['status']})" for r in entries]
    intro = [
        f"# {profile} for {host}", settings["purpose"], settings["context"],
        HOSTS[host], "Choose the workflow that matches the request. Use referenced sections when needed. "
        "The current project determines which information and actions are authorized.",
    ]
    example = "Example task\n\n> " + settings["example"]
    readme = intro + ["## First use", "Open [INSTRUCTIONS.md](INSTRUCTIONS.md) for the self-contained reading copy. "
                      "It includes the workflows and the text of their shared references. For a shorter prompt, "
                      "use one workflow and its required sections. The canonical package files are also provided.",
                      example, "## Source entry points", "\n".join(workflow_links),
                      "## Verification", "SHA256SUMS identifies the exact bytes of each exported file. "
                      "This local export prepares material for manual use. Native activation, "
                      "connectors and live results need a separate trial on the receiving tool."]
    reading = intro + [example, "## Contents", "\n".join(workflow_links)]
    references = sorted(p for p in files if p.endswith(".md") and p not in entrypoints
                        and p != "skills/THIRD-PARTY-NOTICES.md")
    for path in [*entrypoints, *references]:
        reading.extend([f"## Source section: {path}", reading_text(path, files[path], files)])
    for path in sorted(files):
        if path == "skills/THIRD-PARTY-NOTICES.md" or path.rsplit("/", 1)[-1].startswith("LICENSE"):
            reading.extend([f"## Attribution and license: {path}", files[path].decode("utf-8").strip()])
    if "skills/THIRD-PARTY-NOTICES.md" in files:
        readme.append("See the [third-party notices](skills/THIRD-PARTY-NOTICES.md) for attributions and license text.")
    files["README.md"] = ("\n\n".join(readme) + "\n").encode()
    files["INSTRUCTIONS.md"] = ("\n\n".join(reading) + "\n").encode()
    files["SHA256SUMS"] = "".join(
        f"{hashlib.sha256(files[path]).hexdigest()}  {path}\n" for path in sorted(files)
    ).encode()
    return files


def output_path(raw, root):
    path = Path(raw)
    if not raw.strip() or ".." in path.parts or not path.name:
        raise ValueError("Choose a new output folder under an existing directory")
    # os.path.isreserved is available on Windows from Python 3.13.
    reserved = getattr(os.path, "isreserved", lambda name: PureWindowsPath(name).is_reserved())
    if os.name == "nt" and (path.drive.startswith(("\\\\?\\", "\\\\.\\")) or
                            (path.anchor and not path.is_absolute()) or
                            any(p.endswith((" ", ".")) or ":" in p or reserved(p)
                                for p in path.parts if p != path.anchor)):
        raise ValueError("Unsupported output folder")
    path = Path.cwd() / path
    protected = {".git", ".github", ".claude", ".agents", ".codex", ".config", ".ssh", ".aws"}
    if any(p.casefold() in protected for p in path.relative_to(path.anchor).parts):
        raise ValueError("Choose an output outside tool, account and Git configuration directories")
    if path.is_relative_to(root) and path != root and path.relative_to(root).parts[0].casefold() in {
            "skills", "registry", "platform-configs", "agents", "scripts"}:
        raise ValueError("Choose an output outside the library's source directories")
    directory(path.parent)
    try:
        metadata(path)
    except FileNotFoundError:
        return path
    raise ValueError(f"Output already exists: {path}")


def write_pack(target, files):
    # Exclusive creation protects an existing destination even across concurrent exporters.
    target.mkdir()
    folders = {target: metadata(target)}
    created = []
    try:
        for relative, data in files.items():
            path = target / relative
            for parent in reversed(path.parents):
                if parent.is_relative_to(target) and parent not in folders:
                    directory(parent.parent)
                    parent.mkdir()
                    folders[parent] = metadata(parent)
            directory(path.parent)
            with path.open("xb") as dest:
                created.append((path, os.fstat(dest.fileno()), data))
                dest.write(data)
    except BaseException:
        for path, original, expected in reversed(created):
            try:
                directory(path.parent)
                if os.path.samestat(original, metadata(path)):
                    # A failed write can leave a prefix. Keep concurrently replaced or edited files.
                    current = existing_file(path)
                    if current is not None and expected.startswith(current):
                        path.unlink()
            except (OSError, ValueError):
                pass
        for folder, original in reversed(folders.items()):
            try:
                directory(folder.parent)
                if os.path.samestat(original, metadata(folder)):
                    folder.rmdir()
            except (OSError, ValueError):
                pass  # Keep any unrelated entry created concurrently.
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    choices = commands.add_parser("list", help="list the profiles, optionally for one receiving tool")
    choices.add_argument("--platform", choices=HOSTS)
    detail = commands.add_parser("inspect", help="show scope, eligibility and canonical paths")
    detail.add_argument("profile")
    export = commands.add_parser("export", help="write one self-contained manual reading pack")
    export.add_argument("profile")
    export.add_argument("--platform", required=True, choices=HOSTS)
    export.add_argument("--output", required=True, help="new folder with an existing parent")
    args = parser.parse_args(argv)
    try:
        catalog = config(ROOT)
        if args.command == "list":
            for name in catalog[0]["profiles"]:
                settings, entries = select(ROOT, catalog, name)
                if not args.platform or args.platform in settings["platforms"]:
                    print(f"{name} ({len(entries)})  {settings['purpose']}")
        elif args.command == "inspect":
            settings, entries = select(ROOT, catalog, args.profile)
            print(f"{args.profile} ({len(entries)} skills)\n{settings['purpose']}\n{settings['context']}")
            checked = assemble(ROOT, catalog, args.profile, settings["platforms"][0])
            print(f"{len(checked) - 3} source and notice files checked. Verify live behavior on the receiving tool.")
            print("Manual reading packs: " + ", ".join(settings["platforms"]))
            for row in entries:
                print(f"  {row['name']} [{row['status']}]  {row['path']}/SKILL.md")
            print("Example: " + settings["example"])
        else:
            files = assemble(ROOT, catalog, args.profile, args.platform)
            target = output_path(args.output, ROOT)
            write_pack(target, files)
            print(f"Created {target} ({len(files)} files). Start with README.md.")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
