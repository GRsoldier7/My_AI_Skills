#!/usr/bin/env python3
"""
lint-skills.py — Catch the categories of issues found in the 2026-05-09 audit
so they don't return.

Scans /root/My_AI_Skills/skills/**/SKILL.md for:
  * Missing/empty frontmatter fields (name, description, metadata.{version,
    domain-category, last-reviewed})
  * `last-reviewed` older than --max-age days (default 90)
  * Stale tokens defined in lint-config.json (claude-opus-4-6, 192.168.1.240, etc.)
  * Phantom skill references — backticked tokens that look like skill names but
    don't match any directory under skills/
  * Windows-only paths in description sections (Scripts/activate, %USERPROFILE%, Z:/)
  * Deprecated APIs (datetime.utcnow(), etc.)

Stdlib only — no pip install required (works on /usr/bin/python3 3.10+).

Exit codes:
  0  — all checks PASS (warnings allowed)
  1  — one or more FAIL findings
  2  — usage / config error

Usage:
  ./lint-skills.py                     # full repo
  ./lint-skills.py --category core     # one category
  ./lint-skills.py --max-age 60        # tighter staleness threshold
  ./lint-skills.py --json              # machine-readable
  ./lint-skills.py --fix-suggestions   # print sed commands for common fixes
  ./lint-skills.py --files a/SKILL.md b/SKILL.md  # specific files (pre-commit)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_DIR = Path("/root/My_AI_Skills")
SKILLS_DIR = REPO_DIR / "skills"
DEFAULT_CONFIG = REPO_DIR / "scripts" / "lint-config.json"

# Categories that contain SKILL.md children (vs. homelab-organizer which IS a skill)
CATEGORY_DIRS = {
    "core", "engineering", "faith", "growth", "legal-financial",
    "microsoft", "product", "strategy",
}

# Severity ranking for sorting/exit code
SEV_RANK = {"FAIL": 0, "WARN": 1, "INFO": 2}


@dataclass
class Finding:
    severity: str          # FAIL | WARN | INFO
    skill: str             # skill name (or "<repo>")
    file: str              # absolute path
    line: int              # 0 if file-level
    rule: str              # short rule id
    message: str           # human-readable
    fix: str = ""          # suggested fix (sed or note)


# ──────────────────────────────────────────────────────────────────────────────
# Frontmatter parsing (no PyYAML — minimal extractor)
# ──────────────────────────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(text: str) -> tuple[str, int]:
    """Return (frontmatter_block, line_offset_of_block_end). Empty string if none."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", 0
    fm = m.group(1)
    end_line = text[: m.end()].count("\n")
    return fm, end_line


def parse_simple_yaml(fm: str) -> dict:
    """
    Tiny YAML-ish parser — only what we need: top-level scalars and a one-level
    'metadata:' block. Multi-line `description: |` blocks are concatenated.
    """
    out: dict = {}
    metadata: dict = {}
    in_metadata = False
    in_block_scalar = None  # field name receiving block-scalar lines
    block_indent = None

    for raw in fm.splitlines():
        # Block-scalar continuation
        if in_block_scalar is not None:
            if raw.strip() == "":
                # empty lines inside a block scalar — keep going
                target = metadata if in_metadata else out
                target[in_block_scalar] = (target.get(in_block_scalar, "") + "\n").rstrip() + "\n"
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            if block_indent is None:
                block_indent = indent
            if indent >= block_indent and raw.strip() != "":
                target = metadata if in_metadata else out
                target[in_block_scalar] = (target.get(in_block_scalar, "") + raw[block_indent:] + "\n")
                continue
            else:
                in_block_scalar = None
                block_indent = None
                # fall through to handle this line normally

        if not raw.strip():
            continue

        # Detect leaving metadata block
        if in_metadata and not raw.startswith(" ") and not raw.startswith("\t"):
            in_metadata = False

        if raw.rstrip() == "metadata:":
            in_metadata = True
            continue

        # key: value
        m = re.match(r"^(\s*)([a-zA-Z][a-zA-Z0-9_-]*)\s*:\s*(.*)$", raw)
        if not m:
            continue
        indent_str, key, val = m.group(1), m.group(2), m.group(3).rstrip()

        # Block scalar?
        if val in ("|", ">", "|-", ">-"):
            target = metadata if in_metadata else out
            target[key] = ""
            in_block_scalar = key
            block_indent = None
            continue

        # Strip surrounding quotes
        val_clean = val.strip()
        if (val_clean.startswith('"') and val_clean.endswith('"')) or (
            val_clean.startswith("'") and val_clean.endswith("'")
        ):
            val_clean = val_clean[1:-1]

        if in_metadata and indent_str:
            metadata[key] = val_clean
        else:
            out[key] = val_clean

    if metadata:
        out["metadata"] = metadata
    return out


# ──────────────────────────────────────────────────────────────────────────────
# Skill discovery
# ──────────────────────────────────────────────────────────────────────────────

def discover_skills(category: str | None = None) -> list[Path]:
    """Find every SKILL.md under skills/. Optionally filtered by category."""
    if category:
        root = SKILLS_DIR / category
    else:
        root = SKILLS_DIR
    if not root.exists():
        return []
    return sorted(p for p in root.rglob("SKILL.md") if p.is_file())


def all_skill_names() -> set[str]:
    """Set of every skill directory name (= every valid skill reference token)."""
    names: set[str] = set()
    for p in SKILLS_DIR.rglob("SKILL.md"):
        names.add(p.parent.name)
    return names


# ──────────────────────────────────────────────────────────────────────────────
# Linters
# ──────────────────────────────────────────────────────────────────────────────

def lint_frontmatter(skill_path: Path, fm: dict, required_meta: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    skill_name = skill_path.parent.name

    if not fm:
        findings.append(Finding(
            "FAIL", skill_name, str(skill_path), 1, "frontmatter-missing",
            "No frontmatter block found.",
            fix="Add a `---` … `---` YAML block at the top of SKILL.md.",
        ))
        return findings

    # name must equal directory
    fm_name = fm.get("name", "").strip()
    if fm_name != skill_name:
        findings.append(Finding(
            "FAIL", skill_name, str(skill_path), 1, "name-mismatch",
            f"name field '{fm_name}' does not match directory '{skill_name}'.",
            fix=f"Set `name: {skill_name}` in frontmatter.",
        ))

    # description must exist and be non-trivial
    desc = (fm.get("description") or "").strip()
    if not desc:
        findings.append(Finding(
            "FAIL", skill_name, str(skill_path), 1, "description-missing",
            "description field missing or empty.",
        ))
    elif len(desc) < 100:
        findings.append(Finding(
            "WARN", skill_name, str(skill_path), 1, "description-short",
            f"description is {len(desc)} chars — should be 200-1024.",
        ))

    # metadata block + required fields
    meta = fm.get("metadata") or {}
    if not meta:
        findings.append(Finding(
            "FAIL", skill_name, str(skill_path), 1, "metadata-missing",
            "metadata block missing.",
            fix="Add `metadata:` block with version, domain-category, last-reviewed.",
        ))
    else:
        for fld in required_meta:
            if not str(meta.get(fld, "")).strip():
                findings.append(Finding(
                    "FAIL", skill_name, str(skill_path), 1, f"metadata-missing-{fld}",
                    f"metadata.{fld} missing or empty.",
                ))

    return findings


def lint_last_reviewed(skill_path: Path, fm: dict, max_age_days: int, today: date) -> list[Finding]:
    findings: list[Finding] = []
    skill_name = skill_path.parent.name
    meta = fm.get("metadata") or {}
    raw = str(meta.get("last-reviewed", "")).strip()
    if not raw:
        return findings  # already covered by required-field check
    try:
        reviewed = datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        findings.append(Finding(
            "WARN", skill_name, str(skill_path), 1, "last-reviewed-format",
            f"last-reviewed '{raw}' is not YYYY-MM-DD.",
        ))
        return findings

    age = (today - reviewed).days
    if age < 0:
        findings.append(Finding(
            "WARN", skill_name, str(skill_path), 1, "last-reviewed-future",
            f"last-reviewed is {abs(age)} days in the future ({raw}).",
        ))
    elif age > max_age_days:
        findings.append(Finding(
            "WARN", skill_name, str(skill_path), 1, "last-reviewed-stale",
            f"last-reviewed {raw} is {age} days old (>{max_age_days}).",
            fix=f"Update `last-reviewed: \"{today.isoformat()}\"` after re-validating content.",
        ))
    return findings


def lint_stale_tokens(skill_path: Path, lines: list[str], cfg: dict) -> list[Finding]:
    findings: list[Finding] = []
    skill_name = skill_path.parent.name
    for entry in cfg.get("stale_tokens", []):
        tok = entry["token"]
        for i, line in enumerate(lines, 1):
            if tok in line:
                findings.append(Finding(
                    entry.get("severity", "WARN"), skill_name, str(skill_path), i,
                    f"stale-token:{tok}",
                    f"{entry.get('reason', 'Stale token')}: '{tok}' on line {i}.",
                    fix=entry.get("fix", ""),
                ))
    return findings


def lint_deprecated_apis(skill_path: Path, lines: list[str], cfg: dict) -> list[Finding]:
    findings: list[Finding] = []
    skill_name = skill_path.parent.name
    for entry in cfg.get("deprecated_apis", []):
        tok = entry["token"]
        for i, line in enumerate(lines, 1):
            if tok in line:
                findings.append(Finding(
                    entry.get("severity", "WARN"), skill_name, str(skill_path), i,
                    f"deprecated-api:{tok}",
                    f"{entry.get('reason', 'Deprecated API')}: '{tok}' on line {i}.",
                    fix=entry.get("fix", ""),
                ))
    return findings


def lint_windows_paths(skill_path: Path, fm_text: str, fm_end_line: int, cfg: dict) -> list[Finding]:
    """
    Scan ONLY the description (in frontmatter) for Windows-only paths.
    Description is where they hurt most because that's what the model sees first.
    We detect by scanning the frontmatter block raw text up to fm_end_line.
    """
    findings: list[Finding] = []
    skill_name = skill_path.parent.name
    for entry in cfg.get("windows_only_paths", []):
        tok = entry["token"]
        for i, line in enumerate(fm_text.splitlines(), 1):
            if tok in line:
                findings.append(Finding(
                    "FAIL", skill_name, str(skill_path), i,
                    f"windows-path:{tok}",
                    f"Windows-only path '{tok}' in description (line {i}). {entry.get('reason', '')}",
                    fix=entry.get("fix", ""),
                ))
    return findings


# Phantom skill reference detection
# We look for backticked `tokens` that match a kebab-case skill-name shape AND
# are referenced as skills (e.g. mentioned in routing/composability/handoff text)
# but don't exist as a skill directory.
SKILL_REF_PATTERN = re.compile(r"`([a-z][a-z0-9-]{2,40})`")
# Skill-shape: lowercase-kebab, 3-41 chars, contains at least one hyphen so we
# don't flag every short backticked word like `name` or `bash`.
SKILL_SHAPE_RE = re.compile(r"^[a-z][a-z0-9]+(-[a-z0-9]+)+$")
# Words that look skill-shaped but should NEVER be flagged as phantom refs.
SKILL_REF_ALLOWLIST = {
    # cli tools / common identifiers
    "claude-code", "agent-sdk", "claude-agent-sdk", "claude-api",
    "anthropic-sdk", "openai-sdk", "agent-skills",
    # frameworks/libs frequently named in skills
    "next-js", "create-react-app", "tailwind-css", "shadcn-ui",
    "fast-api", "react-server-components", "agent-skill",
    # ports/ids
    "claude-3-5-sonnet", "claude-3-opus", "claude-opus-4-7",
    "claude-sonnet-4", "claude-haiku-4",
    # cli sub-commands / file names (kebab-cased in backticks)
    "docker-compose", "node-modules", "package-json", "tsconfig-json",
    "pre-commit", "venv-bin-activate",
    # common phrases used in code blocks
    "best-practices", "domain-category", "last-reviewed", "review-trigger",
    "adjacent-skills", "auto-trigger", "explicit-trigger",
    # external plugin skills + user-level skills referenced for plugin-overlap routing
    "karpathy-guidelines", "pytest-async-testing-patterns",
    "docker-compose-production", "n8n-mcp",
}


def lint_phantom_refs(skill_path: Path, lines: list[str], known_skills: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    skill_name = skill_path.parent.name
    seen: set[tuple[str, int]] = set()  # dedupe per (token, line)
    for i, line in enumerate(lines, 1):
        for m in SKILL_REF_PATTERN.finditer(line):
            tok = m.group(1)
            if tok in known_skills:
                continue
            if tok in SKILL_REF_ALLOWLIST:
                continue
            if not SKILL_SHAPE_RE.match(tok):
                continue
            # Heuristic: only flag tokens that look like skill names AND appear in
            # a "skill-y" context — namely, the line mentions skill/route/chain/handoff/adjacent
            # OR the token appears in the frontmatter (description/metadata).
            ctx = line.lower()
            looks_skilly = any(
                kw in ctx for kw in (
                    "skill", "route", "chain", "handoff", "adjacent",
                    "compose", "delegate", "invoke", "use ", "see ",
                    "trigger", "redirect",
                )
            )
            if not looks_skilly:
                continue
            # Skip hypothetical/example contexts — these are not real refs.
            if any(marker in ctx for marker in (
                "e.g.,", "e.g. ", "for example", "such as", "hypothetical",
                "imagined", "would-be", "split into", "would create",
            )):
                continue
            # Skip hypothetical/example contexts — these are not real refs.
            if any(marker in ctx for marker in (
                "e.g.,", "e.g. ", "for example", "such as", "hypothetical",
                "imagined", "would-be", "split into", "would create",
            )):
                continue
            key = (tok, i)
            if key in seen:
                continue
            seen.add(key)
            findings.append(Finding(
                "FAIL", skill_name, str(skill_path), i, f"phantom-ref:{tok}",
                f"Reference to `{tok}` does not match any skill directory.",
                fix=(
                    f"Either create skills/<category>/{tok}/ or change the reference "
                    "to an existing skill name."
                ),
            ))
    return findings


# ──────────────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────────────

def lint_one(skill_path: Path, cfg: dict, known_skills: set[str], today: date,
             max_age_days: int) -> list[Finding]:
    text = skill_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    fm_text, fm_end = extract_frontmatter(text)
    fm = parse_simple_yaml(fm_text) if fm_text else {}

    findings: list[Finding] = []
    findings.extend(lint_frontmatter(skill_path, fm, cfg.get("required_metadata_fields", [])))
    findings.extend(lint_last_reviewed(skill_path, fm, max_age_days, today))
    findings.extend(lint_stale_tokens(skill_path, lines, cfg))
    findings.extend(lint_deprecated_apis(skill_path, lines, cfg))
    findings.extend(lint_windows_paths(skill_path, fm_text, fm_end, cfg))
    findings.extend(lint_phantom_refs(skill_path, lines, known_skills))
    return findings


def render_human(findings: list[Finding], scanned: int, fix_suggestions: bool) -> str:
    by_skill: dict[str, list[Finding]] = {}
    for f in findings:
        by_skill.setdefault(f.skill, []).append(f)

    out: list[str] = []
    out.append(f"Scanned {scanned} SKILL.md files. {len(findings)} findings.\n")

    if not findings:
        out.append("All checks passed.\n")
        return "\n".join(out)

    color = sys.stdout.isatty()
    def c(s: str, code: str) -> str:
        return f"\033[{code}m{s}\033[0m" if color else s

    sev_color = {"FAIL": "0;31", "WARN": "1;33", "INFO": "0;36"}

    for skill, items in sorted(by_skill.items()):
        out.append(f"── {skill}")
        for f in sorted(items, key=lambda x: (SEV_RANK[x.severity], x.line)):
            tag = c(f"[{f.severity}]", sev_color.get(f.severity, "0"))
            loc = f"{f.file}:{f.line}" if f.line else f.file
            out.append(f"  {tag} {f.rule}: {f.message}")
            out.append(f"        at {loc}")
            if fix_suggestions and f.fix:
                out.append(f"        fix: {f.fix}")
        out.append("")

    fails = sum(1 for f in findings if f.severity == "FAIL")
    warns = sum(1 for f in findings if f.severity == "WARN")
    out.append("════════════════════════════════")
    out.append(f"  FAIL: {fails}    WARN: {warns}    SCANNED: {scanned}")
    out.append("════════════════════════════════")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lint My_AI_Skills SKILL.md files.")
    ap.add_argument("--category", default=None, help="Limit to one category (core, engineering, ...).")
    ap.add_argument("--max-age", type=int, default=None,
                    help="Days before last-reviewed is stale (default from lint-config.json).")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to lint-config.json.")
    ap.add_argument("--json", dest="json_out", action="store_true", help="Machine-readable JSON output.")
    ap.add_argument("--fix-suggestions", action="store_true",
                    help="Print suggested sed commands / notes alongside findings.")
    ap.add_argument("--files", nargs="*", default=None,
                    help="Lint only these SKILL.md files (overrides --category). For pre-commit hooks.")
    args = ap.parse_args(argv)

    try:
        cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: config not found: {args.config}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"ERROR: config is not valid JSON: {e}", file=sys.stderr)
        return 2

    max_age_days = args.max_age if args.max_age is not None else int(cfg.get("max_age_days", 90))
    today = date.today()
    known_skills = all_skill_names()

    if args.files:
        skill_paths = [Path(p) for p in args.files if Path(p).name == "SKILL.md" and Path(p).is_file()]
    else:
        skill_paths = discover_skills(args.category)

    if not skill_paths:
        print(f"No SKILL.md files found (category={args.category}, files={args.files}).", file=sys.stderr)
        return 2

    all_findings: list[Finding] = []
    for sp in skill_paths:
        all_findings.extend(lint_one(sp, cfg, known_skills, today, max_age_days))

    if args.json_out:
        print(json.dumps({
            "scanned": len(skill_paths),
            "max_age_days": max_age_days,
            "findings": [asdict(f) for f in all_findings],
            "fail_count": sum(1 for f in all_findings if f.severity == "FAIL"),
            "warn_count": sum(1 for f in all_findings if f.severity == "WARN"),
        }, indent=2))
    else:
        print(render_human(all_findings, len(skill_paths), args.fix_suggestions))

    return 1 if any(f.severity == "FAIL" for f in all_findings) else 0


if __name__ == "__main__":
    sys.exit(main())
