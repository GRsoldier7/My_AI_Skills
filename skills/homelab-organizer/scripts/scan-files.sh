#!/usr/bin/env bash
# Phase B — File audit
# Walks tracked roots, applies hard-skip floor, computes mtime + ref count + in-use signals.
# Outputs JSON to stdout.
set -uo pipefail

AUDIT_DIR="${AUDIT_DIR:-/root/homelab/docs/organizer/AUDIT-$(date +%Y-%m-%d)}"
STALE_DAYS="${STALE_DAYS:-90}"
SAFE_DAYS="${SAFE_DAYS:-7}"   # never act on anything modified within N days

ROOTS=(
  "/root/homelab"
  "/opt/echelon/Biohacking_Optimization"
  "/root/.claude/sessions"
  "/root/.claude/todos"
  "/root/.claude/file-history"
  "/root/My_AI_Skills"
)
# /root top-level scratch (depth-1 only) handled specially below

# Hard-skip patterns — pruned during walk
PRUNE_NAMES=(.git .planning .venv venv node_modules __pycache__ target dist build .archive backups)
PRUNE_REGEX=$(IFS='|'; echo "${PRUNE_NAMES[*]}")

# In-use signal sources — we grep these for filename mentions
INUSE_FILES=(
  "/root/.claude/projects/-root/memory/MEMORY.md"
  "/root/homelab/docs/memory/MEMORY_INDEX.md"
  "/root/homelab/docs/memory/LESSONS_LEARNED.md"
  "/root/homelab/docs/memory/SELF_HEALING.md"
  "/root/homelab/CLAUDE.md"
  "/root/My_AI_Skills/CLAUDE.md"
)
INUSE_DIRS=("/root/homelab/docs/runbooks" "/root/homelab/docs/living")

# Build inbound-reference index — scan tracked roots once for filename mentions
# This is the "reference graph" — we cache it later in state.yaml
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
INDEX_FILE="$TMP/refs.txt"
: > "$INDEX_FILE"

walk_file_list() {
  for root in "${ROOTS[@]}"; do
    [[ -d "$root" ]] || continue
    find "$root" -type f \
      \( -name '.git' -o -name '.planning' -o -name '.venv' -o -name 'venv' -o -name 'node_modules' -o -name '__pycache__' -o -name 'target' -o -name 'dist' -o -name 'build' -o -name '.archive' -o -name 'backups' \) -prune \
      -o -type f \
      \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.yaml' -o -name '*.yml' -o -name '*.json' -o -name '*.tf' -o -name '*.toml' -o -name '*.ini' -o -name '*.cfg' -o -name '*.conf' -o -name '*.service' \) \
      -print 2>/dev/null
  done
  # /root top-level scratch (depth-1 only)
  find /root -maxdepth 1 -type f 2>/dev/null
}

# Build reference index: filename -> list of files mentioning it
build_ref_index() {
  while IFS= read -r f; do
    base=$(basename "$f")
    # skip super-common names that would over-match
    case "$base" in
      README.md|CLAUDE.md|index.md|__init__.py|setup.py|main.py|test.py|test.sh|run.sh|build.sh) continue ;;
    esac
    echo "$base"
  done | sort -u > "$TMP/basenames.txt"

  # Build a single grep over all tracked content
  while IFS= read -r src; do
    [[ -f "$src" ]] || continue
    grep -Hof "$TMP/basenames.txt" "$src" 2>/dev/null | head -200
  done > "$INDEX_FILE"
}

# Optimisation: for first run, skip reference building if too many files (fall back to lighter heuristic)
all_files=$(walk_file_list)
file_count=$(echo "$all_files" | wc -l)

if (( file_count > 5000 )); then
  # Large repo — use a subset for the ref index
  echo "$all_files" | head -2000 > "$TMP/refs_input.txt"
else
  echo "$all_files" > "$TMP/refs_input.txt"
fi

build_ref_index < "$TMP/refs_input.txt"

count_refs() {
  local base="$1"
  grep -c ":$base$\|/$base$\|/$base[^a-zA-Z0-9_-]" "$INDEX_FILE" 2>/dev/null | head -1
}

check_inuse() {
  local path="$1" base
  base=$(basename "$path")
  for f in "${INUSE_FILES[@]}"; do
    [[ -f "$f" ]] || continue
    grep -qF "$base" "$f" 2>/dev/null && { echo "mentioned_in_$(basename "$f")"; return; }
  done
  for d in "${INUSE_DIRS[@]}"; do
    [[ -d "$d" ]] || continue
    grep -rqF "$base" "$d" 2>/dev/null && { echo "mentioned_in_$(basename "$d")"; return; }
  done
  echo ""
}

# Build candidate list
declare -a safe_q watchlist dated_hist duplicates
declare -A hash_seen
total_scanned=0
total_skipped_floor=0

while IFS= read -r f; do
  [[ -f "$f" ]] || continue
  total_scanned=$((total_scanned+1))
  # Floor: modified within SAFE_DAYS
  mtime_days=$(( ( $(date +%s) - $(stat -c %Y "$f" 2>/dev/null || echo 0) ) / 86400 ))
  if (( mtime_days < SAFE_DAYS )); then
    total_skipped_floor=$((total_skipped_floor+1))
    continue
  fi
  # Floor: candidate must be > STALE_DAYS old
  if (( mtime_days <= STALE_DAYS )); then
    continue
  fi
  base=$(basename "$f")
  refs=$(count_refs "$base")
  refs=${refs:-0}
  inuse=$(check_inuse "$f")
  hash=$(sha256sum "$f" 2>/dev/null | cut -c1-12)
  size=$(stat -c %s "$f" 2>/dev/null || echo 0)
  is_dated=false
  if [[ "$base" =~ [0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
    is_dated=true
  fi

  # Duplicate detection
  if [[ -n "${hash_seen[$hash]:-}" ]]; then
    duplicates+=("{\"path\":\"$f\",\"duplicate_of\":\"${hash_seen[$hash]}\",\"hash\":\"$hash\",\"mtime_days\":$mtime_days,\"size\":$size}")
    continue
  fi
  hash_seen[$hash]="$f"

  # Categorize
  entry="{\"path\":\"$f\",\"mtime_days\":$mtime_days,\"size\":$size,\"hash\":\"$hash\",\"refs\":$refs,\"in_use_signals\":\"$inuse\""
  if (( refs == 0 )) && [[ -z "$inuse" ]]; then
    if [[ "$is_dated" == "true" ]]; then
      dated_hist+=("$entry,\"reason\":\"dated_artifact_no_refs\"}")
    else
      safe_q+=("$entry,\"reason\":\"mtime_gt_${STALE_DAYS}d_no_refs\"}")
    fi
  else
    reason=""
    (( refs > 0 )) && reason="${reason}has_inbound_refs;"
    [[ -n "$inuse" ]] && reason="${reason}${inuse};"
    watchlist+=("$entry,\"reason\":\"$reason\"}")
  fi
done <<< "$all_files"

# Emit JSON
join_arr() {
  local IFS=,
  echo "$*"
}

cat <<JSON
{
  "audit_date": "$(date +%Y-%m-%d)",
  "totals": {"scanned": $total_scanned, "skipped_floor": $total_skipped_floor, "candidates_safe_quarantine": ${#safe_q[@]}, "candidates_watchlist": ${#watchlist[@]}, "candidates_dated": ${#dated_hist[@]}, "candidates_duplicates": ${#duplicates[@]}},
  "categorized": {
    "SAFE_QUARANTINE": [$(join_arr "${safe_q[@]:-}")],
    "WATCHLIST": [$(join_arr "${watchlist[@]:-}")],
    "DATED_HISTORICAL": [$(join_arr "${dated_hist[@]:-}")],
    "DUPLICATE": [$(join_arr "${duplicates[@]:-}")]
  }
}
JSON
