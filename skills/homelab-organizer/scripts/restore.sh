#!/usr/bin/env bash
# Restore a quarantined file or directory from the archive. Never overwrites: if anything exists at the
# original path, it refuses and leaves the archived copy where it is.
# Usage: restore.sh <archive_path>
#   or:  restore.sh --by-original <original_path>
set -uo pipefail

ARCHIVE_ROOT="${ARCHIVE_ROOT:-/root/homelab/.archive}"

usage() {
  cat <<EOF
Usage:
  $0 <archive_path>                  Restore a specific archived file or directory to its original location
  $0 --by-original <original_path>   Find and restore by the original path
  $0 --list [date]                   List all archived files (optionally filter by date YYYY-MM-DD)
EOF
  exit 2
}

# mv onto an existing path would destroy whatever was written there since the quarantine
restore_to() {
  local from="$1" to="$2"
  if [[ -e "$to" || -L "$to" ]]; then
    echo "REFUSE(exists): $to — move it aside first; the archived copy stays at $from" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$to")"
  mv "$from" "$to" && echo "Restored: $from → $to"
}

case "${1:-}" in
  ""|-h|--help) usage ;;
  --list)
    date="${2:-}"
    if [[ -n "$date" ]]; then
      ls -la "$ARCHIVE_ROOT/$date" 2>/dev/null || { echo "No archive for date: $date"; exit 1; }
    else
      ls -la "$ARCHIVE_ROOT"/ 2>/dev/null || { echo "No archive root: $ARCHIVE_ROOT"; exit 1; }
    fi
    ;;
  --by-original)
    orig="${2:?missing original path}"
    rel="${orig#/}"
    # Literal lookup in each date dir: find -path read the name as a glob, so "zq[1].md" found "zq1.md"
    matches=()
    for d in "$ARCHIVE_ROOT"/*/; do
      [[ -e "$d$rel" || -L "$d$rel" ]] && matches+=("$d$rel")
    done
    (( ${#matches[@]} )) || { echo "Not found in archive: $orig"; exit 1; }
    if (( ${#matches[@]} > 1 )); then
      echo "Archived more than once — restore one by its archive path:" >&2
      printf '  %s\n' "${matches[@]}" >&2
      exit 1
    fi
    restore_to "${matches[0]}" "$orig"
    ;;
  *)
    src="$1"
    [[ -e "$src" || -L "$src" ]] || { echo "Not in archive: $src"; exit 1; }
    [[ "$src" != "$ARCHIVE_ROOT"/* ]] && { echo "Not under archive root: $ARCHIVE_ROOT"; exit 1; }
    # Strip ARCHIVE_ROOT/<date>/ and prepend /. Quoted: the root is a literal path, not a pattern
    rest="${src#"$ARCHIVE_ROOT"/}"
    # An archived entry is <date>/<path>: a bare date dir would move the whole day, and ".." walks out of the archive
    case "/$rest/" in */../*|*/./*) echo "Not an archived entry: $src" >&2; exit 1 ;; esac
    [[ "$rest" =~ ^[^/]+/[^/] ]] || { echo "Not an archived entry (need <date>/<path>): $src" >&2; exit 1; }
    rest="${rest#*/}"
    restore_to "$src" "/$rest"
    ;;
esac
