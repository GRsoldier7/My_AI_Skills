#!/usr/bin/env bash
# Install a skill set from this repo into Claude Code and Codex as symlinks, so the
# repo stays the single source of truth: `git pull` updates every installed skill in place.
#
# Usage:
#   ./scripts/install-skills.sh                   # dry run: report state, change nothing
#   ./scripts/install-skills.sh --apply           # create or repair the symlinks
#   ./scripts/install-skills.sh --apply --prune   # also remove managed links not in the set (incl. NAME installs)
#   ./scripts/install-skills.sh --project DIR     # target DIR/.claude/skills and DIR/.agents/skills
#   ./scripts/install-skills.sh --tool codex      # one tool only: claude | codex
#   ./scripts/install-skills.sh --set FILE        # another set file (default: platform-configs/skill-sets/global.txt)
#   ./scripts/install-skills.sh NAME...           # named skills (directory names) instead of a set file
#
# User-scope targets: Claude Code ~/.claude/skills, Codex ~/.agents/skills.
# A real directory or file, or a symlink pointing outside this repo, is never touched (SKIP).
# Managed link = an absolute symlink into this repo's skills/, however made; relative links are left alone.
# Exit: 0 in sync or applied · 1 bad entry · 2 bad usage · 3 dry run with changes pending.

set -eo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
SET_FILE="$REPO_DIR/platform-configs/skill-sets/global.txt"
APPLY=false
PRUNE=false
BASE="$HOME"
TOOLS="claude codex"
NAMES=""
need_arg() { [[ $# -ge 2 && -n "$2" ]] || { echo "Missing value for $1" >&2; exit 2; }; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --apply) APPLY=true; shift ;;
        --prune) PRUNE=true; shift ;;
        --project) need_arg "$@"; [[ -d "$2" ]] || { echo "Not a directory: $2" >&2; exit 2; }; BASE="$(cd "$2" && pwd -P)"; shift 2 ;;
        --tool) need_arg "$@"; TOOLS="$2"; shift 2 ;;
        --set) need_arg "$@"; SET_FILE="$2"; shift 2 ;;
        -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
        -*) echo "Unknown option: $1" >&2; exit 2 ;;
        *) NAMES="$NAMES $1"; shift ;;
    esac
done
[[ -n "$BASE" ]] || { echo "HOME is not set; set it or pass --project DIR" >&2; exit 2; }
if [[ -n "$NAMES" && "$PRUNE" == true ]]; then
    echo "--prune needs a set file, not skill names (it would remove every other managed link)" >&2
    exit 2
fi
for tool in $TOOLS; do
    case "$tool" in claude|codex) ;; *) echo "Unknown tool: $tool (claude|codex)" >&2; exit 2 ;; esac
done

# Entries: repo-relative skill directories, one per line.
ENTRIES=""
if [[ -n "$NAMES" ]]; then
    for n in $NAMES; do
        hits="$(cd "$REPO_DIR" && find skills -maxdepth 3 -path "*/$n/SKILL.md" | sed 's|/SKILL.md$||')"
        count="$(grep -c . <<< "$hits" || true)"
        if [[ "$count" -ne 1 ]]; then echo "ERROR: '$n' matches $count skill directories" >&2; exit 1; fi
        ENTRIES="$ENTRIES$hits"$'\n'
    done
else
    [[ -f "$SET_FILE" ]] || { echo "ERROR: set file not found: $SET_FILE" >&2; exit 1; }
    ENTRIES="$(sed -e 's/#.*//' -e 's/^[[:space:]]*//' -e 's|^\./||' -e 's/[[:space:]]*$//' -e 's|/*$||' "$SET_FILE" | grep -v '^$' || true)"
fi
[[ -n "$ENTRIES" ]] || { echo "ERROR: no skills to install (the set lists none)" >&2; exit 1; }

bad=0
while IFS= read -r e; do
    [[ -n "$e" ]] || continue
    if [[ "$e" != skills/* || "$e" == *..* || -z "${e##*/}" || ! -f "$REPO_DIR/$e/SKILL.md" ]]; then
        echo "ERROR: not a skill directory in this repo: $e" >&2
        bad=1
    fi
done <<< "$ENTRIES"
dups="$(grep -v '^$' <<< "$ENTRIES" | sed 's|.*/||' | sort | uniq -d || true)"
if [[ -n "$dups" ]]; then echo "ERROR: two entries share a skill name: $dups" >&2; bad=1; fi
[[ "$bad" -eq 0 ]] || exit 1

in_set() { grep -qxF "$1" <<< "$ENTRIES"; }
pending=0
skipped=0
note() {
    echo "  $1"
    case "$1" in
        ADD*|RELINK*|REMOVE*) pending=$((pending + 1)) ;;
        SKIP*) skipped=$((skipped + 1)) ;;
    esac
}

[[ "$APPLY" == true ]] || echo "DRY RUN: nothing will change. Re-run with --apply."
for tool in $TOOLS; do
    if [[ "$tool" == claude ]]; then dir="$BASE/.claude/skills"; else dir="$BASE/.agents/skills"; fi
    echo "== $tool: $dir"
    if [[ "$APPLY" == true ]]; then mkdir -p "$dir"; fi
    while IFS= read -r e; do
        [[ -n "$e" ]] || continue
        name="${e##*/}"
        src="$REPO_DIR/$e"
        dst="$dir/$name"
        if [[ "$tool" == codex && "$e" == skills/aarons-latest/* ]]; then
            if [[ -L "$dst" && "$(readlink "$dst")" == "$REPO_DIR/"* ]]; then
                note "SKIP    $name (managed by scripts/project-router.py; remove the stale link $dst first)"
            else
                note "SKIP    $name (the Codex copy is managed by scripts/project-router.py)"
            fi
            continue
        fi
        if [[ -L "$dst" ]]; then
            cur="$(readlink "$dst")"
            if [[ "$cur" == "$src" ]]; then
                note "OK      $name"
            elif [[ "$cur" == "$REPO_DIR/"* ]]; then
                note "RELINK  $name (was $cur)"
                if [[ "$APPLY" == true ]]; then ln -sfn "$src" "$dst"; fi
            else
                if [[ -e "$dst" ]]; then gone=""; else gone=", dangling"; fi
                note "SKIP    $name (symlink to $cur$gone, not managed by this repo)"
            fi
        elif [[ -e "$dst" ]]; then
            if diff -rq "$src" "$dst" >/dev/null 2>&1; then
                state="same content as repo; safe to replace: move it away, then --apply"
            else
                state="DIFFERS from repo"
            fi
            note "SKIP    $name (existing directory, not managed by this repo; $state)"
        else
            note "ADD     $name"
            if [[ "$APPLY" == true ]]; then ln -s "$src" "$dst"; fi
        fi
    done <<< "$ENTRIES"
    if [[ "$PRUNE" == true && -d "$dir" ]]; then
        for link in "$dir"/*; do
            [[ -L "$link" ]] || continue
            cur="$(readlink "$link")"
            [[ "$cur" == "$REPO_DIR/skills/"* ]] || continue
            if ! in_set "${cur#"$REPO_DIR"/}"; then
                note "REMOVE  ${link##*/} (no longer in the set)"
                if [[ "$APPLY" == true ]]; then rm -- "$link"; fi
            fi
        done
    fi
done

extra=""
if [[ "$skipped" -gt 0 ]]; then extra=" ($skipped skipped: see SKIP lines)"; fi
if [[ "$APPLY" == true ]]; then
    echo "Applied$extra. Claude Code picks up skill changes live; restart Codex sessions to see them."
elif [[ "$pending" -gt 0 ]]; then
    echo "$pending change(s) pending$extra."
    exit 3
else
    echo "In sync$extra."
fi
