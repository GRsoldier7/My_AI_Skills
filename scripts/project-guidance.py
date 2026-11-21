#!/usr/bin/env python3
"""Compose project instructions, verify the committed copies, or preview a local deployment."""
import argparse
import os
from pathlib import Path
import sys
import tempfile

from checked_paths import directory, existing_file

CONFIG = Path(__file__).resolve().parents[1] / "platform-configs"
FRAGMENTS = ("identity.md", "conventions.md", "tech-stack.md")
# Source template, project filename (None means manual delivery), tool-specific instruction.
PLATFORMS = {
    "claude": ("claude/CLAUDE.md.template", "CLAUDE.md", "Read the project's applicable contributor guidance."),
    "codex": ("codex/AGENTS.md.template", "AGENTS.md", "Apply the repository and directory instructions for the files you touch."),
    "cursor": ("cursor/cursorrules.template", ".cursorrules", "Use for projects that consume .cursorrules. Respect scoped rules in the project."),
    "gemini": ("gemini/GEMINI.md.template", "GEMINI.md", "Use the project context and tools available in this session."),
    "chatgpt": ("chatgpt/custom-instructions.md", None, "Review this starter before placing it in the intended ChatGPT project's instructions."),
}

def render(config):
    shared = config / "shared"
    directory(shared)
    pieces = []
    for name in FRAGMENTS:
        data = existing_file(shared / name)
        if not data or not data.strip():
            raise ValueError(f"Missing or empty guidance fragment: {name}")
        pieces.append(data.decode("utf-8").replace("\r\n", "\n").strip())
    return {name: ("\n\n".join([f"# Project guidance for {name}", "<!-- Generated from platform-configs/shared by scripts/project-guidance.py. -->", intro, *pieces]) + "\n").encode("utf-8")
            for name, (_, _, intro) in PLATFORMS.items()}

def generate(config, write):
    updates = []
    for name, data in render(config).items():
        path = config / PLATFORMS[name][0]
        directory(path.parent)
        if existing_file(path) != data:
            updates.append((path, data))
    if updates and not write:
        raise ValueError("Generated guidance needs regeneration with --write: " + ", ".join(p.name for p, _ in updates))
    for path, data in updates:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            staged = Path(handle.name)
            try:
                handle.write(data)
                handle.close()
                os.replace(staged, path)
            finally:
                staged.unlink(missing_ok=True)
    print(f"Guidance current for {len(PLATFORMS)} tools.")

def deploy(config, raw, platforms, apply):
    names = [name.strip() for name in platforms.split(",")]
    if any(name not in PLATFORMS or PLATFORMS[name][1] is None for name in names) or len(set(names)) != len(names):
        raise ValueError("Choose distinct project platforms from claude,codex,cursor,gemini.")
    target = Path(raw)
    if not raw.strip() or ".." in target.parts:
        raise ValueError("Choose the existing project directory directly.")
    if os.name == "nt" and (target.drive.startswith(("\\\\?\\", "\\\\.\\")) or
                            (target.anchor and not target.is_absolute()) or
                            any(p.endswith((" ", ".")) or ":" in p for p in target.parts if p != target.anchor)):
        raise ValueError("Choose a normal project path.")
    target = Path.cwd() / target
    directory(target)
    outputs = render(config)
    pending = []
    for name in names:
        path = target / PLATFORMS[name][1]
        current = existing_file(path)
        if current is None:
            pending.append((path, outputs[name]))
        elif current != outputs[name]:
            raise ValueError(f"Project instructions already differ at {path}. Review and merge them manually.")
    for path, data in pending:
        if apply:
            with path.open("xb") as file:
                file.write(data)
        print(f"{'Created' if apply else 'Would create'} {path}")
    if not pending:
        print("Selected files already match.")
    elif not apply:
        print("Preview complete. Pass --apply to create these files.")

def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--write", action="store_true", help="regenerate the repository templates")
    subs = parser.add_subparsers(dest="command")
    subs.add_parser("check", help="check template freshness (default)")
    project = subs.add_parser("deploy", help="preview instructions for an existing project", allow_abbrev=False)
    project.add_argument("--target", required=True)
    project.add_argument("--platforms", required=True, help="comma-separated claude,codex,cursor,gemini")
    project.add_argument("--apply", action="store_true", help="create absent files after validation")
    args = parser.parse_args()
    if args.write and args.command:
        parser.error("use --write by itself")
    try:
        if args.command == "deploy":
            deploy(CONFIG, args.target, args.platforms, args.apply)
        else:
            generate(CONFIG, args.write)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")

if __name__ == "__main__":
    main()
