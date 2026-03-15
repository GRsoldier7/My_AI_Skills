#!/usr/bin/env bash
# Validate all SKILL.md files against naming conventions and required fields.
# Uses built-in checks since skills-ref may not be installed. Install it with:
#   npm install -g @agentskills/skills-ref
#
# Usage:
#   ./scripts/validate-skills.sh                   # Validate all skills
#   ./scripts/validate-skills.sh --category core   # Validate one category
#   ./scripts/validate-skills.sh --fix             # Show fix suggestions for failures

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

CATEGORY=""
FIX_MODE=false
PASS=0
FAIL=0
WARN=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --category) CATEGORY="$2"; shift 2 ;;
        --fix) FIX_MODE=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "  ${GREEN}✓${NC} $1"; PASS=$((PASS+1)); }
fail() { echo -e "  ${RED}✗${NC} $1"; FAIL=$((FAIL+1)); }
warn() { echo -e "  ${YELLOW}!${NC} $1"; WARN=$((WARN+1)); }

validate_skill() {
    local skill_file="$1"
    local skill_dir="$(dirname "$skill_file")"
    local skill_name="$(basename "$skill_dir")"
    local issues=0

    echo ""
    echo "── $skill_name"

    # Rule 1: name field must match directory name
    local name_field
    name_field="$(grep -m1 '^name:' "$skill_file" | sed 's/name: *//' | tr -d '"' | tr -d "'" | tr -d ' ' || true)"
    if [[ "$name_field" == "$skill_name" ]]; then
        pass "name field matches directory ($skill_name)"
    else
        fail "name field '$name_field' does not match directory '$skill_name'"
        issues=$((issues+1))
    fi

    # Rule 2: name must be lowercase kebab-case only
    if echo "$skill_name" | grep -qE '^[a-z0-9][a-z0-9-]*[a-z0-9]$'; then
        pass "name is valid kebab-case"
    else
        fail "name '$skill_name' contains invalid characters (uppercase or special chars)"
        issues=$((issues+1))
    fi

    # Rule 3: description field must exist and not be empty
    if grep -q '^description:' "$skill_file"; then
        pass "description field present"
    else
        fail "description field missing"
        issues=$((issues+1))
    fi

    # Rule 4: check description length (approximate)
    local desc_length
    desc_length="$(awk '/^description:/,/^[a-zA-Z_-]+:/' "$skill_file" | wc -c)"
    if [[ "$desc_length" -lt 100 ]]; then
        warn "description may be too short (<100 chars) — should be 200-1024 chars"
    else
        pass "description length looks adequate"
    fi

    # Rule 5: metadata block should exist
    if grep -q 'metadata:' "$skill_file"; then
        pass "metadata block present"
    else
        fail "metadata block missing — add: author, version, domain-category, adjacent-skills, last-reviewed, review-trigger"
        issues=$((issues+1))
    fi

    # Rule 6: version field
    if grep -q 'version:' "$skill_file"; then
        pass "version field present"
    else
        warn "version field missing in metadata"
    fi

    # Rule 7: last-reviewed field
    if grep -q 'last-reviewed:' "$skill_file"; then
        pass "last-reviewed field present"
    else
        warn "last-reviewed field missing"
    fi

    # Rule 8: review-trigger field
    if grep -q 'review-trigger:' "$skill_file"; then
        pass "review-trigger field present"
    else
        warn "review-trigger field missing"
    fi

    # Rule 9: adjacent-skills field
    if grep -q 'adjacent-skills:' "$skill_file"; then
        pass "adjacent-skills field present"
    else
        warn "adjacent-skills field missing"
    fi

    # Rule 10: line count (warn if >500)
    local line_count
    line_count="$(wc -l < "$skill_file")"
    if [[ "$line_count" -le 500 ]]; then
        pass "SKILL.md body within 500 lines ($line_count lines)"
    else
        warn "SKILL.md is $line_count lines — consider moving heavy content to references/"
    fi

    # Rule 11: anti-patterns section
    if grep -qi 'anti.pattern' "$skill_file"; then
        pass "anti-patterns section present"
    else
        warn "anti-patterns section missing — add ≥3 named anti-patterns"
    fi

    # Rule 12: failure modes section
    if grep -qi 'failure mode\|failure:' "$skill_file"; then
        pass "failure modes section present"
    else
        warn "failure modes section missing"
    fi

    # Rule 13: composability section
    if grep -qi 'composab\|hands off\|adjacent' "$skill_file"; then
        pass "composability section present"
    else
        warn "composability section missing"
    fi

    if [[ "$FIX_MODE" == true && "$issues" -gt 0 ]]; then
        echo ""
        echo "  Fix suggestions for $skill_name:"
        echo "  1. Ensure 'name: $skill_name' is in frontmatter"
        echo "  2. Add metadata block with: author, version, domain-category, adjacent-skills, last-reviewed, review-trigger"
        echo "  See: skills/core/skill-builder/references/skill-template.md"
    fi
}

# Run validation
search_dir="$SKILLS_DIR"
[[ -n "$CATEGORY" ]] && search_dir="$SKILLS_DIR/$CATEGORY"

echo "Validating skills in $search_dir..."
echo ""

while IFS= read -r skill_file; do
    validate_skill "$skill_file"
done < <(find "$search_dir" -name "SKILL.md" -type f | sort)

# Summary
echo ""
echo "════════════════════════════════"
echo "Validation Summary"
echo "────────────────────────────────"
echo -e "  ${GREEN}PASS${NC}:  $PASS checks"
echo -e "  ${YELLOW}WARN${NC}:  $WARN checks"
echo -e "  ${RED}FAIL${NC}:  $FAIL checks"
echo "────────────────────────────────"

if [[ "$FAIL" -gt 0 ]]; then
    echo -e "  ${RED}RESULT: FAILED${NC}"
    echo "  Fix FAIL items before merging. Run with --fix for suggestions."
    exit 1
elif [[ "$WARN" -gt 0 ]]; then
    echo -e "  ${YELLOW}RESULT: PASSED WITH WARNINGS${NC}"
    echo "  WARN items are quality improvements, not blockers."
    exit 0
else
    echo -e "  ${GREEN}RESULT: PASSED${NC}"
    exit 0
fi
