#!/usr/bin/env bash
# Git pre-commit hook template for My_AI_Skills.
#
# Install:
#   cp /root/My_AI_Skills/scripts/git-pre-commit-hook.sh \
#      /root/My_AI_Skills/.git/hooks/pre-commit
#   chmod +x /root/My_AI_Skills/.git/hooks/pre-commit
#
# Or use the .pre-commit-config.yaml at the repo root with:
#   pip install pre-commit && pre-commit install
#
# This hook lints only staged SKILL.md files — fast and focused.

set -euo pipefail

REPO_DIR="$(git rev-parse --show-toplevel)"
LINT="$REPO_DIR/scripts/lint-skills.py"

# Collect staged SKILL.md files (added/modified, not deleted)
mapfile -t staged < <(git diff --cached --name-only --diff-filter=AM \
    | grep -E '^skills/.*/SKILL\.md$' || true)

if [[ ${#staged[@]} -eq 0 ]]; then
    exit 0
fi

# Convert to absolute paths
abs_paths=()
for p in "${staged[@]}"; do
    abs_paths+=("$REPO_DIR/$p")
done

echo "Linting ${#abs_paths[@]} staged SKILL.md file(s)…"
"$LINT" --files "${abs_paths[@]}" --fix-suggestions
