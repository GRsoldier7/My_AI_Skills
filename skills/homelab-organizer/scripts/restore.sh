#!/usr/bin/env bash
# Restore a quarantined file from a manifest entry.
# Usage: restore.sh <archive_path>
#   or:  restore.sh --by-original <original_path>
set -uo pipefail

ARCHIVE_ROOT="${ARCHIVE_ROOT:-/root/homelab/.archive}"

usage() {
  cat <<EOF
Usage:
  $0 <archive_path>                  Restore a specific archived file to its original location
  $0 --by-original <original_path>   Find and restore by the original path
  $0 --list [date]                   List all archived files (optionally filter by date YYYY-MM-DD)
EOF
  exit 2
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
    found=$(find "$ARCHIVE_ROOT" -path "*/$rel" -type f 2>/dev/null | head -1)
    [[ -z "$found" ]] && { echo "Not found in archive: $orig"; exit 1; }
    mkdir -p "$(dirname "$orig")"
    mv "$found" "$orig" && echo "Restored: $found → $orig"
    ;;
  *)
    src="$1"
    [[ ! -f "$src" ]] && { echo "Not a file: $src"; exit 1; }
    [[ "$src" != "$ARCHIVE_ROOT"/* ]] && { echo "Not under archive root: $ARCHIVE_ROOT"; exit 1; }
    # Recover original path: strip ARCHIVE_ROOT/<date>/ prefix, prepend /
    rest="${src#$ARCHIVE_ROOT/}"
    rest="${rest#*/}"   # strip date dir
    orig="/$rest"
    mkdir -p "$(dirname "$orig")"
    mv "$src" "$orig" && echo "Restored: $src → $orig"
    ;;
esac
