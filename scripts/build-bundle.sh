#!/bin/bash
# Build packed markdown bundles of all SKILL.md files for NotebookLM upload.
#
# Produces 3 files in OUT_DIR:
#   01_skills_core_engineering_faith_homelab_legal.md  (~280K)
#   02_skills_growth_microsoft_product_strategy.md     (~470K)
#   03_skills_top_level_docs.md                        (~45K)
#
# Idempotent: overwrites existing files. Safe to run repeatedly.

set -euo pipefail

REPO="/root/My_AI_Skills"
OUT_DIR="/root/My_AI_Skills/.bundle-cache"
DATE=$(date +%Y-%m-%d)

mkdir -p "$OUT_DIR"

write_bundle() {
    local out_file="$1"
    local title="$2"
    shift 2
    local categories=("$@")

    {
        echo "# $title"
        echo ""
        echo "> Generated $DATE from $REPO"
        echo ""
        for cat in "${categories[@]}"; do
            for skill_md in "$REPO/skills/$cat"/*/SKILL.md "$REPO/skills/$cat/SKILL.md"; do
                [ -f "$skill_md" ] || continue
                rel="${skill_md#$REPO/}"
                echo "---"
                echo ""
                echo "## $rel"
                echo ""
                cat "$skill_md"
                echo ""
            done
        done
    } > "$out_file"
    echo "Wrote $out_file ($(wc -c < "$out_file") bytes)"
}

# Bundle 1: core + engineering + faith + homelab-organizer + legal-financial
write_bundle "$OUT_DIR/01_skills_core_engineering_faith_homelab_legal.md" \
    "My_AI_Skills Bundle 1 — Core / Engineering / Faith / Homelab / Legal" \
    core engineering faith homelab-organizer legal-financial

# Bundle 2: growth + microsoft + product + strategy
write_bundle "$OUT_DIR/02_skills_growth_microsoft_product_strategy.md" \
    "My_AI_Skills Bundle 2 — Growth / Microsoft / Product / Strategy" \
    growth microsoft product strategy

# Bundle 3: top-level docs (README + repo CLAUDE.md + index)
{
    echo "# My_AI_Skills — Top-Level Documentation"
    echo ""
    echo "> Generated $DATE from $REPO"
    echo ""
    echo "Repo: https://github.com/GRsoldier7/My_AI_Skills"
    echo ""
    echo "---"
    echo ""
    echo "## README.md"
    echo ""
    [ -f "$REPO/README.md" ] && cat "$REPO/README.md"
    echo ""
    echo "---"
    echo ""
    echo "## CLAUDE.md (repo-level)"
    echo ""
    [ -f "$REPO/CLAUDE.md" ] && cat "$REPO/CLAUDE.md"
    echo ""
    echo "---"
    echo ""
    echo "## Skill Index"
    echo ""
    cd "$REPO"
    for skill_md in $(find skills -name "SKILL.md" | sort); do
        skill_dir=$(dirname "$skill_md")
        skill_name=$(basename "$skill_dir")
        # Extract description from frontmatter
        desc=$(awk '/^description:/{sub(/^description: */,""); print; exit}' "$skill_md" | head -c 200)
        echo "- **$skill_dir** — $desc"
    done
} > "$OUT_DIR/03_skills_top_level_docs.md"
echo "Wrote $OUT_DIR/03_skills_top_level_docs.md ($(wc -c < "$OUT_DIR/03_skills_top_level_docs.md") bytes)"

ls -lh "$OUT_DIR"/
