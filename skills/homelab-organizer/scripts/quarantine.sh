#!/usr/bin/env bash
# Action executor — moves approved files to .archive/<date>/<rel-path>/ and writes a manifest entry.
# Never deletes. Idempotent. Refuses any path that hits the hard-skip floor.
set -uo pipefail

ARCHIVE_ROOT="${ARCHIVE_ROOT:-/root/homelab/.archive}"
AUDIT_DATE="${AUDIT_DATE:-$(date +%Y-%m-%d)}"
ARCHIVE_DIR="$ARCHIVE_ROOT/$AUDIT_DATE"
MANIFEST="$ARCHIVE_DIR/MANIFEST.md"

mkdir -p "$ARCHIVE_DIR"

# Hard-skip floor — paths that must NEVER be quarantined regardless of approval
floor_check() {
  local p="$1"
  case "$p" in
    /etc/*|/usr/*|/sys/*|/proc/*|/boot/*|/var/lib/docker/*|/var/lib/lxc/*) return 1 ;;
    */.git/*|*/.git) return 1 ;;
    /root/.claude/settings*.json) return 1 ;;
    /root/.ssh/*|/etc/ssh/*) return 1 ;;
    "$ARCHIVE_ROOT"/*) return 1 ;;
  esac
  # 7-day floor
  local mtime_days
  mtime_days=$(( ( $(date +%s) - $(stat -c %Y "$p" 2>/dev/null || echo 0) ) / 86400 ))
  (( mtime_days < 7 )) && return 1
  return 0
}

ensure_manifest_header() {
  if [[ ! -f "$MANIFEST" ]]; then
    cat > "$MANIFEST" <<EOF
# Quarantine Manifest — $AUDIT_DATE

Each entry below is a quarantine action. To restore a file, copy the
\`restore\` command and run it.

EOF
  fi
}

quarantine_one() {
  local src="$1" reason="${2:-unspecified}"
  if [[ ! -e "$src" ]]; then
    echo "skip(missing): $src" >&2
    return 0
  fi
  if ! floor_check "$src"; then
    echo "REJECT(floor): $src" >&2
    return 2
  fi
  ensure_manifest_header

  # Compute archive path: preserve the source's leading directory tree under ARCHIVE_DIR
  # e.g., /root/homelab/scratch/foo.md → $ARCHIVE_DIR/root/homelab/scratch/foo.md
  local rel="${src#/}"
  local dst="$ARCHIVE_DIR/$rel"
  local dst_dir
  dst_dir=$(dirname "$dst")
  mkdir -p "$dst_dir"

  # Capture metadata before move
  local mtime size hash
  mtime=$(stat -c %y "$src" 2>/dev/null)
  size=$(stat -c %s "$src" 2>/dev/null)
  hash=$(sha256sum "$src" 2>/dev/null | cut -c1-12)

  # Perform move (atomic on same filesystem)
  if mv "$src" "$dst"; then
    # Append manifest entry
    cat >> "$MANIFEST" <<EOF

## $(date -Iseconds) — $rel

- original: \`$src\`
- archived: \`$dst\`
- mtime: $mtime
- size: $size bytes
- hash: $hash
- reason: $reason
- restore: \`mkdir -p "$(dirname "$src")" && mv "$dst" "$src"\`

EOF
    echo "OK: $src → $dst"
    return 0
  else
    echo "FAIL(mv): $src" >&2
    return 1
  fi
}

# Read paths from stdin: one path per line, optionally followed by | <reason>
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  [[ "$line" == \#* ]] && continue
  src="${line%%|*}"
  reason="${line#*|}"
  [[ "$src" == "$reason" ]] && reason="unspecified"
  src=$(echo "$src" | xargs)
  reason=$(echo "$reason" | xargs)
  quarantine_one "$src" "$reason" || true
done

echo "Manifest: $MANIFEST" >&2
