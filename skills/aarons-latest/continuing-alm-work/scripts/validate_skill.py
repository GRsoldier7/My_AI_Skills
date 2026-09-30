#!/usr/bin/env python3
"""Dependency-free static validator for the continuing-alm-work skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_TOP_LEVEL = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME)\b|<placeholder>", re.IGNORECASE)


class ValidationError(Exception):
    pass


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_simple_frontmatter(text: str) -> tuple[dict[str, object], str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        raise ValidationError("SKILL.md must begin with YAML frontmatter on line 1")
    marker = normalized.find("\n---\n", 4)
    if marker < 0:
        raise ValidationError("SKILL.md frontmatter is not closed with ---")

    raw = normalized[4:marker]
    body = normalized[marker + 5 :]
    data: dict[str, object] = {}
    current_map: str | None = None

    for number, line in enumerate(raw.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current_map != "metadata":
                raise ValidationError(f"Unsupported nested frontmatter at line {number}")
            match = re.match(r"^\s{2,}([A-Za-z0-9_-]+):\s*(.*)$", line)
            if not match:
                raise ValidationError(f"Invalid metadata entry at line {number}")
            metadata = data.setdefault("metadata", {})
            assert isinstance(metadata, dict)
            metadata[match.group(1)] = unquote(match.group(2))
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            raise ValidationError(f"Invalid frontmatter line {number}: {line}")
        key, value = match.groups()
        current_map = key if not value else None
        data[key] = {} if not value else unquote(value)

    return data, body


def validate_frontmatter(root: Path, text: str) -> list[str]:
    data, body = parse_simple_frontmatter(text)
    errors: list[str] = []

    unknown = sorted(set(data) - ALLOWED_TOP_LEVEL)
    if unknown:
        errors.append(f"Unsupported top-level frontmatter fields: {', '.join(unknown)}")

    name = data.get("name")
    if not isinstance(name, str) or not name:
        errors.append("Frontmatter name is required")
    else:
        if not NAME_RE.fullmatch(name):
            errors.append("Name must be lowercase kebab-case")
        if len(name) > 64:
            errors.append("Name exceeds 64 characters")
        if name != root.name:
            errors.append(f"Name '{name}' does not match folder '{root.name}'")

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("Description is required")
    else:
        if not description.startswith("Use when"):
            errors.append("Description should begin with 'Use when'")
        if len(description) > 1024:
            errors.append("Description exceeds 1024 characters")
        if "<" in description or ">" in description:
            errors.append("Description contains angle brackets")

    compatibility = data.get("compatibility", "")
    if not isinstance(compatibility, str):
        errors.append("Compatibility must be a string")
    elif len(compatibility) > 500:
        errors.append("Compatibility exceeds 500 characters")

    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        errors.append("Metadata must be a YAML map")
    elif not metadata.get("version"):
        errors.append("metadata.version is required for this package")

    if len(text.replace("\r\n", "\n").splitlines()) > 500:
        errors.append("SKILL.md exceeds the 500-line progressive-disclosure limit")
    if not body.strip():
        errors.append("SKILL.md body is empty")

    return errors


def validate_links(root: Path, files: list[Path]) -> list[str]:
    errors: list[str] = []
    for file_path in files:
        text = file_path.read_text(encoding="utf-8-sig")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            resolved = (file_path.parent / relative).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{file_path.relative_to(root)} links outside the skill: {target}")
                continue
            if not resolved.exists():
                errors.append(f"Broken link in {file_path.relative_to(root)}: {target}")
    return errors


def validate_evals(root: Path) -> list[str]:
    path = root / "evals" / "evals.json"
    if not path.is_file():
        return ["Missing evals/evals.json"]
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return [f"Invalid evals JSON: {exc}"]

    if data.get("skill_name") != root.name:
        errors.append("evals.skill_name must match the skill folder name")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        return errors + ["evals must be a non-empty array"]

    seen: set[int] = set()
    for index, case in enumerate(evals, start=1):
        label = f"eval #{index}"
        if not isinstance(case, dict):
            errors.append(f"{label} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, int) or case_id <= 0:
            errors.append(f"{label} id must be a positive integer")
        elif case_id in seen:
            errors.append(f"Duplicate eval id: {case_id}")
        else:
            seen.add(case_id)
        for field in ("prompt", "expected_output"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{label} requires a non-empty {field}")
        files = case.get("files", [])
        if not isinstance(files, list):
            errors.append(f"{label} files must be an array")
        expectations = case.get("expectations")
        if not isinstance(expectations, list) or not expectations:
            errors.append(f"{label} expectations must be a non-empty array")
        elif not all(isinstance(item, str) and item.strip() for item in expectations):
            errors.append(f"{label} expectations must contain non-empty strings")
    return errors


def validate_placeholders(root: Path, files: list[Path]) -> list[str]:
    errors: list[str] = []
    for file_path in files:
        text = file_path.read_text(encoding="utf-8-sig")
        match = PLACEHOLDER_RE.search(text)
        if match:
            errors.append(f"Placeholder '{match.group(0)}' found in {file_path.relative_to(root)}")
    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["Missing SKILL.md"]

    skill_text = skill.read_text(encoding="utf-8-sig")
    errors.extend(validate_frontmatter(root, skill_text))

    markdown_files = [skill, *sorted((root / "references").glob("*.md"))]
    errors.extend(validate_links(root, markdown_files))
    errors.extend(validate_placeholders(root, markdown_files))
    errors.extend(validate_evals(root))
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}")
        return 2
    errors = validate(root)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID")
    print(f"- skill: {root.name}")
    print(f"- files: {sum(1 for path in root.rglob('*') if path.is_file())}")
    print(f"- evals: {len(json.loads((root / 'evals/evals.json').read_text(encoding='utf-8-sig'))['evals'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
