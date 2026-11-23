#!/usr/bin/env python3
"""Read-only checker for a clean-project optimizeproject.md register (schema 1 or 2).
Python 3.10+, stdlib only; reads one file, never writes, runs project code, or uses the network.
check [PATH]: one JSON object, exit 0 valid / 1 errors / 2 missing or unreadable. next-id [PATH]: next CP ID."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

STATUSES = {"open", "approved", "in-progress", "blocked", "implemented-unverified",
            "resolved", "accepted-risk", "false-positive"}
CLOSED = {"resolved", "accepted-risk", "false-positive"}
SEVERITIES = {"critical", "high", "medium", "low", "informational"}
CONFIDENCES = {"verified", "probable", "uncertain"}
OUTCOMES = {"clean", "findings", "could-not-assess"}
ID_RE = re.compile(r"CP-\d{4}")
ANY_ID_RE = re.compile(r"\bCP-(\d{4})\b")
TS_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?[+-]\d{2}:\d{2}")
TS_LIKE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?")
SECRET_RES = [re.compile(p) for p in (
    r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY", r"ghp_[A-Za-z0-9]{36}", r"xox[baprs]-",
    r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*\S{16,}")]
SECTION_RE = re.compile(r"^##\s+(\d+)\.", re.M)
DETAIL_RE = re.compile(r"^###\s+(\S+)\s+—\s+", re.M)
SEPARATOR_RE = re.compile(r"\|(?:\s*:?-+:?\s*\|)+")
EMPTY = ("", "not completed", "not assigned")


def cells(line: str) -> list[str]:
    parts = re.split(r"(?<!\\)\|", line.strip())[1:-1]
    return [p.strip().strip("`").strip() for p in parts]


def table_rows(block: str) -> list[list[str]]:
    """Data rows of every pipe table in block; header and separator rows are skipped."""
    rows: list[list[str]] = []
    in_table = False
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
        elif SEPARATOR_RE.fullmatch(stripped):
            in_table = True
        elif in_table:
            rows.append(cells(stripped))
    return rows


def split_marks(text: str, pattern: re.Pattern[str]) -> list[tuple[str, str]]:
    marks = list(pattern.finditer(text))
    return [(m.group(1), text[m.end():marks[n + 1].start() if n + 1 < len(marks) else len(text)])
            for n, m in enumerate(marks)]


def shown(value: object) -> str | None:  # echo-safe: redact secret-shaped values, cap at 200
    return None if value is None else "<redacted>" if any(p.search(str(value)) or p.search(str(value).upper()) for p in SECRET_RES) else str(value)[:200]


def norm(value: str | None) -> str:
    return (value or "").strip().rstrip(".").strip().lower()


def blank_result() -> dict:
    return {"ok": False, "schema": None, "findings": 0, "open": 0, "next_id": "CP-0001",
            "by_status": {}, "last_assessed": None, "revision": None, "outcome": None,
            "errors": [], "warnings": []}


def next_id(text: str) -> str:
    numbers = [int(n) for n in ANY_ID_RE.findall(text)]
    return f"CP-{max(numbers, default=0) + 1:04d}"


def check(text: str) -> dict:
    result = blank_result()
    errors, warnings = result["errors"], result["warnings"]
    match = re.search(r"^Report schema version:\s*(\d+)\s*$", text, re.M)
    schema = int(match.group(1)) if match else None
    if schema is None:
        errors.append("schema version line missing")
    elif schema == 1:
        warnings.append("schema 1: migrate to 2")
    elif schema != 2:
        errors.append(f"unsupported schema {schema}")

    sections = {int(k): v for k, v in split_marks(text, SECTION_RE)}
    current = sections.get(1, "").split("\n### ")[0]
    summary = {row[0]: row[1] for row in table_rows(current) if len(row) >= 2}
    last = next((v for k, v in summary.items() if k.lower().startswith("last assessment")), None)
    outcome = summary.get("Outcome")
    if schema == 2:
        if not (last and TS_RE.fullmatch(last)):
            errors.append("Last assessment is not ISO-8601 with a local offset")
        if outcome not in OUTCOMES:
            errors.append(f"Outcome must be clean, findings, or could-not-assess (got {shown(outcome)!r})")

    index: dict[str, str] = {}
    for row in table_rows(sections.get(2, "")):
        if len(row) < 8:
            errors.append(f"§2 row has {len(row)} cells, expected 8: {[shown(c) for c in row[:1]]}")
            continue
        fid, severity, confidence, status = row[0], norm(row[3]), norm(row[4]), norm(row[5])
        if not ID_RE.fullmatch(fid):
            errors.append(f"§2 ID {shown(fid)!r} is not CP-####")
        if fid in index:
            errors.append(f"duplicate ID {shown(fid)} in §2")
        index.setdefault(fid, status)
        for label, value, allowed in (("severity", severity, SEVERITIES),
                                      ("confidence", confidence, CONFIDENCES), ("status", status, STATUSES)):
            if value not in allowed:
                errors.append(f"{shown(fid)}: {label} {shown(value)!r} not in enum")

    seen: set[str] = set()
    for fid, body in split_marks(sections.get(3, ""), DETAIL_RE):
        fields = {row[0]: row[1] for row in table_rows(body) if len(row) >= 2}
        if fid in seen:
            errors.append(f"duplicate §3 heading {shown(fid)}")
        seen.add(fid)
        if not ID_RE.fullmatch(fid):
            errors.append(f"§3 heading ID {shown(fid)!r} is not CP-####")
        if fid not in index:
            errors.append(f"§3 {shown(fid)} has no §2 row")
        detail_status = norm(fields.get("Status"))
        if detail_status and detail_status not in STATUSES:
            errors.append(f"{shown(fid)}: §3 status {shown(detail_status)!r} not in enum")
        statuses = {index.get(fid), detail_status}
        if "resolved" in statuses and norm(fields.get("Completion evidence")) in EMPTY:
            errors.append(f"{shown(fid)}: resolved without completion evidence")
        if "accepted-risk" in statuses and norm(fields.get("Review date")) in EMPTY:
            errors.append(f"{shown(fid)}: accepted-risk without a review date")
    errors.extend(f"§2 {shown(fid)} has no '### {shown(fid)} —' heading in §3" for fid in index if fid not in seen)

    for number, line in enumerate(text.splitlines(), 1):
        if any(p.search(line) for p in SECRET_RES):
            errors.append(f"line {number}: secret-shaped value (redact it; value not shown)")
        for stamp in TS_LIKE_RE.findall(line):
            if stamp.endswith("Z"):
                warnings.append(f"line {number}: Z-suffixed timestamp; use a local offset")
            if schema == 2 and not TS_RE.fullmatch(stamp):
                errors.append(f"line {number}: timestamp {shown(stamp)} is not ISO-8601 with a local offset")

    result.update({
        "ok": not errors, "schema": schema, "findings": len(index),
        "open": sum(1 for s in index.values() if s not in CLOSED), "next_id": next_id(text),
        "by_status": dict(sorted(Counter(shown(s) for s in index.values()).items())), "last_assessed": shown(last),
        "revision": shown(summary.get("Revision and branch")), "outcome": shown(outcome)})
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("check", "next-id"))
    parser.add_argument("path", nargs="?", default="optimizeproject.md", type=Path)
    args = parser.parse_args(argv)
    text, reason = None, "missing"
    try:
        text = args.path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pass
    except (OSError, UnicodeDecodeError) as error:
        reason = f"unreadable ({error.__class__.__name__})"
    if args.command == "next-id":
        if text is None and reason != "missing":
            print(f"register.py: {args.path}: {reason}", file=sys.stderr)
            return 2
        print(next_id(text or ""))
        return 0
    result = check(text) if text is not None else blank_result()
    if text is None:
        result["errors"].append(f"{args.path}: {reason}")
    print(json.dumps(result))
    return 2 if text is None else 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
