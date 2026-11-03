#!/usr/bin/env python3
"""Verify pinned design package bytes and local Markdown references without execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-root", type=Path, help="Directory containing the three upstream Git clones")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "platform-configs/skill-sets/design-sources.json").read_text())
    checked = 0
    for package in manifest["packages"]:
        folder = ROOT / package["path"]
        assert folder.resolve().is_relative_to(ROOT), "Package escaped repository"
        assert re.fullmatch(r"[0-9a-f]{40}", package["commit"]), "Incomplete commit pin"
        expected = {f["path"] for f in package["files"]}
        actual = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()}
        assert actual == expected, f"File inventory changed: {package['name']}: {actual ^ expected}"
        assert "SKILL.md" in actual and "UPSTREAM_LICENSE" in actual
        for item in package["files"]:
            path = folder / item["path"]
            assert path.resolve().is_relative_to(folder.resolve()) and not path.is_symlink()
            assert digest(path.read_bytes()) == item["sha256"], f"Changed bytes: {path}"
            if args.upstream_root:
                upstream = args.upstream_root / package["repository"].rsplit("/", 1)[1].removesuffix(".git")
                original = subprocess.check_output(["git", "-C", str(upstream), "show", f"{package['commit']}:{item['source_path']}"])
                assert digest(original) == item["upstream_sha256"], f"Upstream mismatch: {path}"
            if item["sha256"] != item["upstream_sha256"]:
                assert package["name"] == "ui-ux-pro-max" and item["path"] == "SKILL.md"
                assert package["adaptations"], "Undocumented adaptation"
            checked += 1
        for md in folder.rglob("*.md"):
            for link in re.findall(r"\]\(([^\s)#]+)(?:#[^)]*)?\)", md.read_text()):
                if ":" in link or link.startswith(("#", "/")) or "<" in link:
                    continue
                assert (md.parent / unquote(link)).exists(), f"Missing reference: {md}: {link}"
    selected = [line.strip() for line in (ROOT / "platform-configs/skill-sets/design.txt").read_text().splitlines()
                if line.strip() and not line.startswith("#")]
    assert selected == [p["path"] for p in manifest["packages"]]
    print(f"Verified {len(manifest['packages'])} packages, {checked} files, exact inventories, pins, licenses and local Markdown references.")
    print("Integrity validation does not grant security intake approval or confirm global installation.")


if __name__ == "__main__":
    main()
