#!/usr/bin/env python3
"""
generate-skill-registry.py

Auto-generates the skill registry table inside
`/root/My_AI_Skills/skills/core/master-orchestrator/SKILL.md`
from the frontmatter of every `SKILL.md` under
`/root/My_AI_Skills/skills/` (plus each skill's `agents/openai.yaml`
invocation policy, which marks manual-only rows).

Idempotent: replaces only the content between
`<!-- AUTO-GENERATED-REGISTRY:START -->` and
`<!-- AUTO-GENERATED-REGISTRY:END -->`. If the markers
don't exist, the script wraps the existing
`## The Skill Registry` section after creating a backup.

Stdlib only — does not require PyYAML.

Usage:
    python3 generate-skill-registry.py            # dry-run (default)
    python3 generate-skill-registry.py --dry-run  # explicit dry-run
    python3 generate-skill-registry.py --inject   # apply
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SKILLS_ROOT = Path("/root/My_AI_Skills/skills")
TARGET_SKILL = SKILLS_ROOT / "core" / "master-orchestrator" / "SKILL.md"
BACKUP_DIR = Path("/root/My_AI_Skills/.backup")
BACKUP_FILE = BACKUP_DIR / "master-orchestrator-pre-autogen.md"

START_MARKER = "<!-- AUTO-GENERATED-REGISTRY:START -->"
END_MARKER = "<!-- AUTO-GENERATED-REGISTRY:END -->"
SECTION_HEADING = "## The Skill Registry"

# Trigger-phrase keywords we'll harvest from descriptions.
TRIGGER_HINT_PATTERNS = [
    r"AUTO-TRIGGER[^.]*",
    r"EXPLICIT TRIGGER[^.]*",
    r"Use when[^.]*",
    r"Use this skill (?:when|whenever)[^.]*",
    r"Trigger(?:s)? on[^.]*",
    r"Triggers?:[^.]*",
    r"Activates? (?:on|when|for)[^.]*",
    r"Also trigger[^.]*",
]

# Friendly category display names — fallback to title-case of the dirname
CATEGORY_DISPLAY = {
    "aarons-latest": "Aaron's Latest Skills",
    "core": "Core (Meta-Layer)",
    "engineering": "Engineering",
    "faith": "Faith",
    "growth": "Growth & Marketing",
    "homelab": "Homelab",
    "legal-financial": "Legal-Financial",
    "microsoft": "Microsoft Power Platform",
    "product": "Product",
    "strategy": "Strategy & Business",
}

# ---------------------------------------------------------------------------
# Minimal hand-rolled YAML-ish frontmatter parser
# ---------------------------------------------------------------------------


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse the first `---\\n...\\n---` block. Supports:
    - flat scalars: `key: value`
    - quoted scalars: `key: "value"`
    - block scalars: `key: |` and `key: >`  (multiline, dedented)
    - one level of nested mapping under a parent key (e.g. `metadata:`)
    - nested list items (`- item`)

    The parser is intentionally minimal — it covers the conventions used
    across the SKILL.md library and nothing else.
    """
    if not text.startswith("---"):
        return {}

    # Locate the closing fence
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}

    body = lines[1:end_idx]
    return _parse_block(body, base_indent=0)


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_block(lines: list[str], base_indent: int) -> dict[str, Any]:
    """Parse a list of lines all sharing the same base indent into a mapping."""
    result: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue

        indent = _indent_of(raw)
        if indent < base_indent:
            # Out of our block
            break
        if indent > base_indent:
            # Should have been swallowed by a parent — skip defensively
            i += 1
            continue

        line = raw[base_indent:]
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2)

        # Block scalar (| or >)
        if rest.strip() in ("|", ">", "|-", ">-", "|+", ">+"):
            style = rest.strip()[0]
            i += 1
            collected: list[str] = []
            child_indent: int | None = None
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    collected.append("")
                    i += 1
                    continue
                ind = _indent_of(nxt)
                if ind <= base_indent:
                    break
                if child_indent is None:
                    child_indent = ind
                collected.append(nxt[child_indent:] if ind >= child_indent else nxt.lstrip())
                i += 1
            if style == ">":
                # Folded — join non-empty consecutive lines with spaces, blank line = paragraph
                paragraphs: list[list[str]] = [[]]
                for ln in collected:
                    if ln == "":
                        paragraphs.append([])
                    else:
                        paragraphs[-1].append(ln)
                value = "\n\n".join(" ".join(p).strip() for p in paragraphs if p)
            else:
                # Literal
                value = "\n".join(collected).rstrip()
            result[key] = value
            continue

        # Empty value → either nested mapping/list, or genuinely empty
        if rest == "":
            # Look ahead — if next non-blank line is more indented, recurse
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and _indent_of(lines[j]) > base_indent:
                child_indent = _indent_of(lines[j])
                # Determine list vs map by first non-blank child line
                if lines[j].lstrip().startswith("- "):
                    items: list[Any] = []
                    while i + 1 < len(lines):
                        nxt = lines[i + 1]
                        if not nxt.strip():
                            i += 1
                            continue
                        if _indent_of(nxt) < child_indent:
                            break
                        stripped = nxt[child_indent:]
                        if stripped.startswith("- "):
                            items.append(_strip_quotes(stripped[2:]))
                        i += 1
                    result[key] = items
                else:
                    # Nested mapping — collect child lines, recurse
                    child_lines: list[str] = []
                    while i + 1 < len(lines):
                        nxt = lines[i + 1]
                        if not nxt.strip():
                            child_lines.append(nxt)
                            i += 1
                            continue
                        if _indent_of(nxt) < child_indent:
                            break
                        child_lines.append(nxt)
                        i += 1
                    result[key] = _parse_block(child_lines, child_indent)
                i += 1
                continue
            else:
                result[key] = ""
                i += 1
                continue

        # Inline scalar (possibly comma-list for adjacent-skills)
        result[key] = _strip_quotes(rest)
        i += 1
    return result


# ---------------------------------------------------------------------------
# Skill extraction
# ---------------------------------------------------------------------------


def first_sentence(text: str, max_chars: int = 220) -> str:
    """Return a single-sentence, single-line summary of the description."""
    if not text:
        return ""
    flat = re.sub(r"\s+", " ", text).strip()
    # Cut at the first sentence-ender that's followed by a space or end
    m = re.search(r"(.+?[.!?])(?:\s|$)", flat)
    summary = m.group(1) if m else flat
    if len(summary) > max_chars:
        summary = summary[: max_chars - 1].rstrip() + "…"
    return summary


def extract_triggers(description: str) -> str:
    """Pull out trigger-like phrases from the description and join into one line."""
    if not description:
        return ""
    flat = re.sub(r"\s+", " ", description).strip()
    hits: list[str] = []
    for pat in TRIGGER_HINT_PATTERNS:
        for m in re.finditer(pat, flat, flags=re.IGNORECASE):
            chunk = m.group(0).strip().rstrip(",;")
            # Truncate each chunk to keep the row narrow
            if len(chunk) > 120:
                chunk = chunk[:117] + "…"
            hits.append(chunk)
            if len(hits) >= 2:
                break
        if len(hits) >= 2:
            break
    if not hits:
        # Fallback — use the first sentence as a soft trigger hint
        return first_sentence(flat, max_chars=120)
    return " | ".join(hits)


def adjacent_value(meta: dict[str, Any]) -> str:
    raw = meta.get("adjacent-skills")
    if raw is None:
        return ""
    if isinstance(raw, list):
        return ", ".join(str(x) for x in raw)
    return str(raw)


def find_skill_files() -> list[Path]:
    return sorted(SKILLS_ROOT.rglob("SKILL.md"))


def load_skill(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    name = fm.get("name") or path.parent.name
    description = fm.get("description") or ""
    domain = (
        (meta or {}).get("domain-category")
        or _infer_category_from_path(path)
        or "uncategorized"
    )
    last_reviewed = (meta or {}).get("last-reviewed") or ""
    version = (meta or {}).get("version") or ""
    return {
        "path": str(path),
        "name": str(name),
        "description": str(description),
        "domain-category": str(domain),
        "version": str(version),
        "last-reviewed": str(last_reviewed),
        "adjacent-skills": adjacent_value(meta or {}),
        "manual-only": is_manual_only(path, fm),
        "summary": first_sentence(str(description)),
        "triggers": extract_triggers(str(description)),
    }


def _yaml_scalar(value: str) -> str:
    """Normalize a YAML scalar: drop an inline comment and quotes, lower-case."""
    return re.split(r"[ \t]#", value, maxsplit=1)[0].strip().strip("\"'").lower()


def is_manual_only(path: Path, fm: dict[str, Any]) -> bool:
    """True when Claude (`disable-model-invocation: true`) or Codex
    (`agents/openai.yaml` `policy.allow_implicit_invocation: false`) blocks model
    invocation. Host-local overrides (settings.json `skillOverrides`) are not read:
    mirror such a choice into the skill's agents/openai.yaml."""
    if _yaml_scalar(str(fm.get("disable-model-invocation", ""))) == "true":
        return True
    codex = path.parent / "agents" / "openai.yaml"
    if not codex.is_file():
        return False
    in_policy = False  # line scan, linear time: only `policy:`'s indented block counts
    for line in codex.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            in_policy = line.split("#", 1)[0].strip() == "policy:"
        elif in_policy and line.strip().startswith("allow_implicit_invocation:"):
            return _yaml_scalar(line.split(":", 1)[1]) == "false"
    return False


def _infer_category_from_path(path: Path) -> str:
    """Fallback: directory layout is skills/<category>/<skill>/SKILL.md
    (or skills/<skill>/SKILL.md for a top-level skill)."""
    try:
        rel = path.relative_to(SKILLS_ROOT)
    except ValueError:
        return ""
    parts = rel.parts
    if len(parts) >= 3:
        return parts[0]
    if len(parts) == 2:
        # Top-level skill (e.g. homelab-organizer/SKILL.md) — bucket under "homelab"
        return "homelab"
    return ""


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _md_escape(value: str) -> str:
    """Escape pipes for table cells and strip newlines."""
    if not value:
        return ""
    return value.replace("|", "\\|").replace("\n", " ").strip()


def render_registry_block(skills: list[dict[str, Any]], generated_at: str) -> str:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in skills:
        grouped[s["domain-category"]].append(s)

    # Stable category ordering — known categories first, then alphabetical
    known_order = [
        "core",
        "engineering",
        "faith",
        "strategy",
        "legal-financial",
        "growth",
        "product",
        "microsoft",
        "homelab",
    ]
    ordered_categories: list[str] = []
    for c in known_order:
        if c in grouped:
            ordered_categories.append(c)
    for c in sorted(grouped.keys()):
        if c not in ordered_categories:
            ordered_categories.append(c)

    out: list[str] = []
    out.append(START_MARKER)
    out.append("")
    out.append(
        f"<!-- Generated by scripts/generate-skill-registry.py at {generated_at} — do not edit by hand. -->"
    )
    out.append(f"<!-- Total skills: {len(skills)} -->")
    out.append("")

    for cat in ordered_categories:
        rows = sorted(grouped[cat], key=lambda s: s["name"].lower())
        display = CATEGORY_DISPLAY.get(cat, cat.replace("-", " ").title())
        out.append(f"### {display} ({len(rows)})")
        out.append("")
        out.append("| Skill | Domain | Description | last-reviewed | Triggers |")
        out.append("|-------|--------|-------------|---------------|----------|")
        for s in rows:
            out.append(
                "| `{name}`{flag} | {domain} | {summary} | {last_reviewed} | {triggers} |".format(
                    name=_md_escape(s["name"]),
                    flag=" (manual-only)" if s["manual-only"] else "",
                    domain=_md_escape(s["domain-category"]),
                    summary=_md_escape(s["summary"]) or "_(no description)_",
                    last_reviewed=_md_escape(s["last-reviewed"]) or "—",
                    triggers=_md_escape(s["triggers"]) or "—",
                )
            )
        out.append("")

    out.append(END_MARKER)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# File injection
# ---------------------------------------------------------------------------


def _replace_between_markers(content: str, new_block: str) -> str | None:
    """Return updated content if both markers exist, else None."""
    if START_MARKER not in content or END_MARKER not in content:
        return None
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    return pattern.sub(new_block, content, count=1)


def _wrap_existing_registry_section(content: str, new_block: str) -> str:
    """First-time injection: replace the existing manual `## The Skill Registry`
    section (up to the next top-level `---` separator or `## ` heading) with
    a heading + the auto-generated block.

    Falls back to appending if the section can't be found.
    """
    lines = content.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == SECTION_HEADING:
            start = i
            break
    if start is None:
        # Append a new section at the end
        suffix = ["", SECTION_HEADING, "", new_block, ""]
        return content.rstrip() + "\n\n" + "\n".join(suffix).lstrip() + "\n"

    # Find the end of the section: next `## ` heading OR a stand-alone `---`
    # separator line that signals a new top-level section.
    end = len(lines)
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if s.startswith("## ") and j != start:
            end = j
            break
        if s == "---":
            end = j
            break

    new_section = [SECTION_HEADING, "", new_block, ""]
    rebuilt = lines[:start] + new_section + lines[end:]
    return "\n".join(rebuilt) + ("\n" if not content.endswith("\n") else "")


def inject(content: str, new_block: str) -> tuple[str, str]:
    """Return (new_content, mode) where mode is 'replace' or 'wrap'."""
    replaced = _replace_between_markers(content, new_block)
    if replaced is not None:
        return replaced, "replace"
    return _wrap_existing_registry_section(content, new_block), "wrap"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate(content: str) -> list[str]:
    """Sanity-check the post-injection content. Returns list of warnings."""
    warnings: list[str] = []
    if not content.startswith("---\n"):
        warnings.append("File no longer starts with frontmatter fence.")
    # Frontmatter must close
    fm_close = content.find("\n---\n", 4)
    if fm_close == -1:
        warnings.append("Frontmatter does not appear to close.")
    if content.count(START_MARKER) != 1:
        warnings.append(
            f"Expected exactly 1 START_MARKER, found {content.count(START_MARKER)}."
        )
    if content.count(END_MARKER) != 1:
        warnings.append(
            f"Expected exactly 1 END_MARKER, found {content.count(END_MARKER)}."
        )
    # Duplicate `## The Skill Registry`
    if content.count(f"\n{SECTION_HEADING}\n") > 1:
        warnings.append(f"Duplicate '{SECTION_HEADING}' headings detected.")
    return warnings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the change diff without writing (default).",
    )
    group.add_argument(
        "--inject",
        action="store_true",
        help="Apply the change to master-orchestrator/SKILL.md.",
    )
    args = parser.parse_args()

    write = bool(args.inject)
    # Default = dry-run

    if not TARGET_SKILL.exists():
        print(f"ERROR: target file not found: {TARGET_SKILL}", file=sys.stderr)
        return 2

    skill_files = find_skill_files()
    skills = [load_skill(p) for p in skill_files]

    print(f"Found {len(skills)} SKILL.md files under {SKILLS_ROOT}")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in skills:
        grouped[s["domain-category"]].append(s)
    for cat in sorted(grouped.keys()):
        rows = sorted(grouped[cat], key=lambda s: s["name"].lower())
        print(f"\n  [{cat}]  ({len(rows)} skills)")
        for s in rows:
            print(f"    - {s['name']}  (last-reviewed: {s['last-reviewed'] or '—'})")

    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    new_block = render_registry_block(skills, generated_at)

    original = TARGET_SKILL.read_text(encoding="utf-8")
    new_content, mode = inject(original, new_block)

    print(
        f"\nInjection mode: {mode!r}  ('replace' = markers existed, 'wrap' = first-time wrap)"
    )

    warnings = validate(new_content)
    if warnings:
        print("\nVALIDATION WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("\nValidation: OK")

    if write:
        # Always back up before writing
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TARGET_SKILL, BACKUP_FILE)
        print(f"\nBackup written: {BACKUP_FILE}")
        TARGET_SKILL.write_text(new_content, encoding="utf-8")
        print(f"Updated:        {TARGET_SKILL}")
        # Halt with non-zero on validation warnings to alert pre-commit hooks
        return 0 if not warnings else 1

    # dry-run preview
    print("\n" + "=" * 70)
    print("DRY-RUN PREVIEW (first 80 lines of generated block):")
    print("=" * 70)
    for ln in new_block.splitlines()[:80]:
        print(ln)
    if len(new_block.splitlines()) > 80:
        print(f"... ({len(new_block.splitlines()) - 80} more lines truncated)")
    print("=" * 70)
    print("\nDry-run only — no files modified. Re-run with --inject to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
