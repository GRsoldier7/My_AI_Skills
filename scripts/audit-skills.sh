#!/usr/bin/env bash
# audit-skills.sh — full skills-library audit driver.
#
# Two layers:
#   (a) Mechanical lint — runs lint-skills.py against the whole repo.
#   (b) Deep parallel-agent audit — Claude Code only. We can't invoke other
#       agents from a shell script, so this prints the prompt template the
#       user can paste into a Claude Code session for the deep pass.
#
# Outputs land in /root/My_AI_Skills/audits/YYYY-MM-DD-HHMM/.
# Compares against the previous audit and exits non-zero if NEW failing
# rules appear (so this is safe to run from CI / pre-commit).
#
# Usage:
#   ./audit-skills.sh                   # full repo audit
#   ./audit-skills.sh --category core   # one category
#   ./audit-skills.sh --skip-deep       # don't print the deep-audit prompt

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
AUDITS_DIR="$REPO_DIR/audits"
LINT="$SCRIPT_DIR/lint-skills.py"

CATEGORY=""
SKIP_DEEP=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --category) CATEGORY="$2"; shift 2 ;;
        --skip-deep) SKIP_DEEP=true; shift ;;
        -h|--help)
            sed -n '2,16p' "$0"
            exit 0
            ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
done

STAMP="$(date +%Y-%m-%d-%H%M)"
OUT_DIR="$AUDITS_DIR/$STAMP"
mkdir -p "$OUT_DIR"

# ──────────────────────────────────────────────────────────────────────────
# Layer (a): mechanical lint
# ──────────────────────────────────────────────────────────────────────────
LINT_ARGS=()
[[ -n "$CATEGORY" ]] && LINT_ARGS+=(--category "$CATEGORY")

echo "Running lint-skills.py …"
LINT_EXIT=0
"$LINT" "${LINT_ARGS[@]}" --fix-suggestions \
    > "$OUT_DIR/lint.txt" 2>&1 || LINT_EXIT=$?
"$LINT" "${LINT_ARGS[@]}" --json \
    > "$OUT_DIR/lint.json" 2>/dev/null || true

echo "  → $OUT_DIR/lint.txt"
echo "  → $OUT_DIR/lint.json"

# ──────────────────────────────────────────────────────────────────────────
# Layer (b): deep parallel-agent audit prompt template
# ──────────────────────────────────────────────────────────────────────────
DEEP_PROMPT="$OUT_DIR/deep-audit-prompt.md"
cat > "$DEEP_PROMPT" <<'PROMPT_EOF'
# Deep Skills Audit — Parallel Agent Prompt Template

The lint pass catches mechanical regressions. This deeper pass requires Claude
Code reasoning to catch routing collisions, scope overlaps, content currency,
and subjective quality issues. Run it with parallel agents — one per category.

## How to run

In a Claude Code session, dispatch 5 parallel Task() calls (one per group):

| Group | Categories | Skill count |
|---|---|---|
| 1 | core | 11 |
| 2 | engineering | 8 |
| 3 | growth + product | 15 |
| 4 | strategy + faith | 12 |
| 5 | microsoft + legal-financial + homelab-organizer | 11 |

## Per-agent prompt (template)

```
You are auditing the My_AI_Skills sub-library at /root/My_AI_Skills/skills/<CATEGORY>/.

For EACH SKILL.md in that category, evaluate against these axes:

1. ROUTING COLLISIONS — does this skill auto-trigger on requests that another
   skill in the library also auto-triggers on, with no precedence rule?
2. SCOPE OVERLAP — does this skill cover ground already covered by a native
   plugin skill (e.g. context7, supabase, cloudflare)? If so, does the SKILL.md
   explicitly say when to prefer this one vs the plugin?
3. CONTENT CURRENCY — are claims, model names, IPs, URLs, and version numbers
   current as of $(date +%Y-%m-%d)? Flag any "(coming soon)" or stale dates.
4. INTENT CLARITY — does the description tell the model precisely WHEN to fire
   AND when NOT to fire? Faith skills are the gold standard ("Do NOT use for X").
5. PHANTOM REFERENCES — does this skill reference skills that don't exist?
   (Lint catches the obvious ones; you catch the cross-skill mismatches.)
6. COMPOSABILITY — does the skill have a Composability Contract (input,
   output, hands-off-to)?

Output: per-skill JSON entry to a file at
  /tmp/aiskills_audit/<group>.json
with shape:
  { "skill": "name", "tier": "CRITICAL|HIGH|MEDIUM|LOW",
    "axes": ["routing","scope",...], "finding": "...", "fix": "..." }

End with a 1-paragraph executive summary listing only CRITICAL + HIGH.
```

## After the parallel pass

Aggregate the 5 per-group files into AUDIT.md following the structure used
on 2026-05-09 at /tmp/aiskills_audit/AUDIT.md.

## Tier definitions
- CRITICAL — wrong info, broken paths, will misroute users
- HIGH     — routing collisions, scope overlaps, stale claims with evidence
- MEDIUM   — quality improvements, missing gold-standard patterns
- LOW      — polish, minor inconsistencies
PROMPT_EOF

if [[ "$SKIP_DEEP" == false ]]; then
    echo ""
    echo "Deep parallel-agent audit prompt template:"
    echo "  → $DEEP_PROMPT"
    echo "  (open in Claude Code, dispatch 5 Task() calls per the table inside)"
fi

# ──────────────────────────────────────────────────────────────────────────
# Compare to previous audit — flag NEW failing rules
# ──────────────────────────────────────────────────────────────────────────
NEW_FAILS=0
PREV_DIR=""
# Find the most recent prior audit dir (excluding the one we just made)
if [[ -d "$AUDITS_DIR" ]]; then
    PREV_DIR="$(find "$AUDITS_DIR" -maxdepth 1 -mindepth 1 -type d \
        ! -path "$OUT_DIR" 2>/dev/null | sort | tail -n 1 || true)"
fi

if [[ -n "$PREV_DIR" && -f "$PREV_DIR/lint.json" ]]; then
    echo ""
    echo "Comparing to previous audit: $PREV_DIR"
    DIFF_FILE="$OUT_DIR/diff-vs-previous.txt"
    /usr/bin/python3 - "$PREV_DIR/lint.json" "$OUT_DIR/lint.json" \
        > "$DIFF_FILE" <<'PYEOF'
import json, sys
prev = json.load(open(sys.argv[1]))
curr = json.load(open(sys.argv[2]))

def key(f):
    # Identity ignoring line numbers (lines drift on edits)
    return (f["skill"], f["rule"], f["severity"])

prev_keys = {key(f) for f in prev["findings"]}
curr_keys = {key(f) for f in curr["findings"]}

new_fails = [f for f in curr["findings"]
             if key(f) not in prev_keys and f["severity"] == "FAIL"]
fixed     = [f for f in prev["findings"]
             if key(f) not in curr_keys and f["severity"] == "FAIL"]

print(f"NEW failing findings: {len(new_fails)}")
for f in new_fails:
    print(f"  + [{f['severity']}] {f['skill']}::{f['rule']} — {f['message']}")
print()
print(f"FIXED since previous: {len(fixed)}")
for f in fixed:
    print(f"  - [{f['severity']}] {f['skill']}::{f['rule']}")

# Encode count for shell to read
print(f"::NEW_FAIL_COUNT={len(new_fails)}")
PYEOF
    NEW_FAILS=$(grep -oE '::NEW_FAIL_COUNT=[0-9]+' "$DIFF_FILE" | tail -1 | cut -d= -f2)
    NEW_FAILS=${NEW_FAILS:-0}
    echo "  → $DIFF_FILE"
else
    echo ""
    echo "(No previous audit to diff against — this is the baseline.)"
fi

# ──────────────────────────────────────────────────────────────────────────
# Summary + exit
# ──────────────────────────────────────────────────────────────────────────
FAIL_COUNT=$(/usr/bin/python3 -c "import json; print(json.load(open('$OUT_DIR/lint.json'))['fail_count'])" 2>/dev/null || echo 0)
WARN_COUNT=$(/usr/bin/python3 -c "import json; print(json.load(open('$OUT_DIR/lint.json'))['warn_count'])" 2>/dev/null || echo 0)

echo ""
echo "════════════════════════════════"
echo "  Audit summary — $STAMP"
echo "  FAIL:        $FAIL_COUNT"
echo "  WARN:        $WARN_COUNT"
echo "  NEW FAILS:   $NEW_FAILS  (vs. previous audit)"
echo "  Output dir:  $OUT_DIR"
echo "════════════════════════════════"

# Exit non-zero only if NEW critical issues introduced (regression).
# A baseline run with pre-existing fails is informational, not a hard fail —
# unless we have no prior audit at all and FAIL_COUNT > 0.
if [[ "$NEW_FAILS" -gt 0 ]]; then
    echo "REGRESSION: $NEW_FAILS new FAIL findings introduced. Block merge." >&2
    exit 1
fi

# If baseline (no previous audit) and there are FAIL findings, propagate lint exit.
if [[ -z "$PREV_DIR" ]]; then
    exit "$LINT_EXIT"
fi

exit 0
