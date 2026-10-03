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
import fnmatch
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


def is_vendored(skill_path: Path, patterns: list[str]) -> bool:
    """True if this skill came from an upstream pack we re-sync rather than author."""
    try:
        rel = skill_path.relative_to(REPO_DIR).as_posix()
    except ValueError:
        return False
    # Match the skill DIRECTORY as well as the SKILL.md path. A prefix glob like
    # "skills/engineering/ce-*" only ever matched because fnmatch's `*` spans `/`;
    # an exact directory entry — the natural way to vendor one skill that shares no
    # name prefix with a pack — would otherwise silently never match.
    candidates = (rel, rel.rsplit("/", 1)[0])
    return any(fnmatch.fnmatch(c, pat) for c in candidates for pat in patterns)


def build_skill_index() -> tuple[set[str], dict[str, list[str]]]:
    """Every valid skill reference token, plus any token claimed by two skills.

    A reference resolves against either the directory name or the frontmatter
    `name:`. Both are real identifiers: generate-skill-registry.py writes the
    frontmatter name into the registry, so directory-only matching reported
    every aliased skill as a phantom reference.

    Accepting aliases can mask a genuine collision, so callers get the
    collision map back and surface it as its own finding.
    """
    owners: dict[str, list[str]] = {}
    for p in SKILLS_DIR.rglob("SKILL.md"):
        tokens = {p.parent.name}
        fm_text, _ = extract_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if fm_text:
            fm_name = (parse_simple_yaml(fm_text).get("name") or "").strip()
            if fm_name:
                tokens.add(fm_name)
        for tok in tokens:
            owners.setdefault(tok, []).append(p.parent.name)

    collisions = {tok: sorted(set(dirs)) for tok, dirs in owners.items() if len(set(dirs)) > 1}
    return set(owners), collisions


# ──────────────────────────────────────────────────────────────────────────────
# Linters
# ──────────────────────────────────────────────────────────────────────────────

def lint_frontmatter(skill_path: Path, fm: dict, required_meta: list[str],
                     vendored: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    skill_name = skill_path.parent.name

    if not fm:
        findings.append(Finding(
            "FAIL", skill_name, str(skill_path), 1, "frontmatter-missing",
            "No frontmatter block found.",
            fix="Add a `---` … `---` YAML block at the top of SKILL.md.",
        ))
        return findings

    # name must equal directory — upstream packs name themselves, so this and the
    # metadata requirements below are ours to enforce only on skills we author.
    fm_name = fm.get("name", "").strip()
    if fm_name != skill_name and not vendored:
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
    if not vendored:
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
    # issue-tracker triage labels used by the vendored mattpocock engineering skills
    "needs-triage", "needs-info", "ready-for-agent", "ready-for-human",
}


# Token-local context patterns for phantom-ref detection. Each is anchored to the
# token's edge ($ for text before it, ^ for text after) so it can only ever describe
# the token being tested — never a neighbour that happens to share the line.
INVOKE_BEFORE_RE = re.compile(
    r"(?:\b(?:invoke|invokes|load|loads|run|runs|call|calls|use|uses|using|see|"
    r"route|redirect|delegate|handoff|hand\s*off|compose|chain|escalate|defer|"
    r"apply|applies|execute|executes|trigger|triggers|launch|launches|"
    r"dispatch|dispatches)"
    r"(?:\s+(?:to|with|on|off))?"
    r"|\brequires?|\bdepends\s+on|\b(?:adjacent[-\s])?skills?)"
    r"\s*[:=|,-]?\s*(?:the\s+|a\s+|to\s+)?$"
)
# "the `todo-triage` skill handles X". Singular only, and not "`x` skill names …":
# plural and descriptive-noun continuations are prose ABOUT skills, not invocations.
INVOKE_AFTER_RE = re.compile(
    r"^\s*skill\b(?!\s+(?:name|names|file|files|director(?:y|ies)|id|ids|author|authors"
    r"|description|descriptions|instruction|instructions|trigger|triggers|metadata"
    r"|frontmatter|prompt|prompts|registry|version|versions)\b)"
)
# A noun immediately after the token names what the token IS, and none of these are
# skills: "`project-standards` persona", "`review-fixer` reviewer". This has to beat
# the invocation patterns, because "Pass the path list to the `x` persona" is a real
# verb-object-preposition shape aimed at something that is not a skill.
EXCLUDE_AFTER_RE = re.compile(
    r"^\s*(?:persona|personas|reviewer|reviewers|sub-?agent|sub-?agents|agent|agents"
    r"|role|roles|owner|owners|label|labels|verdict|verdicts|enum|value|values"
    r"|server|servers|endpoint|endpoints|namespace|namespaces|column|columns"
    r"|table|tables|field|fields|key|keys|block|blocks|persona's)\b"
)
# "Route image tasks to `x`" — an object sits between the verb and the preposition,
# so the verb is not adjacent to the token and INVOKE_BEFORE_RE alone would miss it.
INVOKE_BEFORE_OBJ_RE = re.compile(
    r"\b(?:route|routes|delegate|delegates|hand\s*offs?|handoffs?|escalate|escalates"
    r"|defer|defers|pass|passes|forward|forwards|send|sends|dispatch|dispatches"
    r"|hand)\b[^`]{0,40}?"
    r"\s(?:to|with)\s+(?:the\s+|a\s+)?$"
)
# A guard must be opened by a conditional, either immediately before the token
# ("If the `x` skill is available") or immediately after it ("`x` if available").
# Bare availability wording is a statement, not a guard: "Use `x` skill is available"
# still fails, because nothing there makes the reference conditional.
GUARD_BEFORE_RE = re.compile(r"\b(?:if|when|where|unless)\s+(?:the\s+|a\s+)?$")
GUARD_AFTER_RE = re.compile(
    r"^\s*(?:skills?\s+)?(?:only\s+)?(?:if|when|unless|where)\s+"
    r"(?:it\s+|they\s+|the\s+skill\s+)?(?:is\s+|are\s+)?"
    r"(?:available|present|installed|enabled)\b"
)
# "e.g. `x`" marks x hypothetical; "such as package.json ... invoke `x`" does not.
EXAMPLE_BEFORE_RE = re.compile(
    r"\b(?:e\.g\.|eg\.|for\s+example|such\s+as|hypothetical|imagined|would-be|"
    r"split\s+into|would\s+create)\s*[,:]?\s*(?:the\s+|a\s+)?$"
)


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
            # Every test below is TOKEN-LOCAL: it reads only the text hugging this
            # token, never the whole line. Line-level tests are what made this rule
            # both noisy and blind — noisy because a routing-owner label or a "Supply
            # Chain" table row counted as an invocation, blind because an unrelated
            # "(e.g. ...)" later in the sentence suppressed a real dangling ref. With
            # a line-level guard, a valid "if available" on ONE token would also
            # excuse a genuinely broken DIFFERENT token on the same line.
            before = line[:m.start()].lower()
            after = line[m.end():].lower()
            before_tail, after_head = before[-48:], after[:48]

            if EXCLUDE_AFTER_RE.match(after_head):
                continue
            if not (
                INVOKE_BEFORE_RE.search(before_tail)
                or INVOKE_BEFORE_OBJ_RE.search(before_tail)
                or INVOKE_AFTER_RE.match(after_head)
                or f"/{tok}" in line
            ):
                continue
            # A guarded reference is a contract, not a defect: the skill documents its
            # own fallback for when the target is absent ("If the `ralph-loop` skill is
            # available..."), so a missing target is the documented path, not a break.
            # The guard must grammatically wrap THIS token to count.
            if GUARD_BEFORE_RE.search(before_tail) or GUARD_AFTER_RE.match(after_head):
                continue
            # Hypothetical/example contexts are not real refs, but only when the marker
            # introduces THIS token ("e.g. `foo`"). "When files such as package.json
            # change, invoke `missing-skill`" is a real invocation and must still fail.
            if EXAMPLE_BEFORE_RE.search(before_tail):
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

    vendored = is_vendored(skill_path, cfg.get("vendored_paths", []))

    findings: list[Finding] = []
    findings.extend(lint_frontmatter(skill_path, fm, cfg.get("required_metadata_fields", []), vendored))
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
    known_skills, alias_collisions = build_skill_index()

    if args.files:
        skill_paths = [Path(p) for p in args.files if Path(p).name == "SKILL.md" and Path(p).is_file()]
    else:
        skill_paths = discover_skills(args.category)

    if not skill_paths:
        print(f"No SKILL.md files found (category={args.category}, files={args.files}).", file=sys.stderr)
        return 2

    all_findings: list[Finding] = []
    for tok, dirs in sorted(alias_collisions.items()):
        all_findings.append(Finding(
            "FAIL", dirs[0], str(SKILLS_DIR), 1, f"alias-collision:{tok}",
            f"Reference `{tok}` is claimed by {len(dirs)} skills: {', '.join(dirs)}.",
            fix="Rename one skill's directory or frontmatter `name:` so the token is unique.",
        ))
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
