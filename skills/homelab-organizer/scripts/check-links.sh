#!/usr/bin/env bash
# Phase C — Link integrity
# Checks markdown links, dangling symlinks, shell sources, project-internal Python imports.
set -uo pipefail

ROOTS=("/root/homelab" "/opt/echelon/Biohacking_Optimization" "/root/My_AI_Skills")

declare -a broken_md dangling_symlinks broken_sources broken_imports

# Markdown links — [text](path) where path is relative and not a URL
check_md_links() {
  local md="$1"
  while IFS=: read -r line content; do
    # Extract every [..](..) pair on the line
    while [[ "$content" =~ \[[^]]*\]\(([^\)\#]+)(\#[^\)]*)?\) ]]; do
      target="${BASH_REMATCH[1]}"
      content="${content#*\)}"
      # Skip URLs and anchors
      [[ "$target" =~ ^https?:// ]] && continue
      [[ "$target" =~ ^mailto: ]] && continue
      [[ "$target" =~ ^# ]] && continue
      # Resolve relative to the .md's directory
      dir=$(dirname "$md")
      resolved=$(realpath -m "$dir/$target" 2>/dev/null)
      if [[ ! -e "$resolved" ]]; then
        broken_md+=("{\"in_file\":\"$md\",\"line\":$line,\"target\":\"$target\",\"resolved\":\"$resolved\"}")
      fi
    done
  done < <(grep -nE '\[[^]]*\]\([^\)]+\)' "$md" 2>/dev/null | head -500)
}

for root in "${ROOTS[@]}"; do
  [[ -d "$root" ]] || continue
  while IFS= read -r md; do
    check_md_links "$md"
  done < <(find "$root" -type f -name '*.md' \
    -not -path '*/.git/*' -not -path '*/.archive/*' -not -path '*/node_modules/*' \
    -not -path '*/.venv/*' -not -path '*/__pycache__/*' 2>/dev/null | head -500)

  # Dangling symlinks
  while IFS= read -r link; do
    target=$(readlink "$link" 2>/dev/null || echo "?")
    dangling_symlinks+=("{\"path\":\"$link\",\"points_to\":\"$target\"}")
  done < <(find "$root" -type l ! -exec test -e {} \; -print 2>/dev/null)

  # Shell sources
  while IFS= read -r sh; do
    while IFS=: read -r line content; do
      target=$(echo "$content" | grep -oE '(source|\. )\s+[^ ;|&]+' | awk '{print $NF}')
      [[ -z "$target" ]] && continue
      # Strip quotes
      target=${target//\"/}
      target=${target//\'/}
      # Variable substitution — skip
      [[ "$target" == *'$'* ]] && continue
      # Skip runtime-only files that legitimately don't exist at audit time
      case "$target" in
        .env|.env.*|*/.env|*/.env.*) continue ;;
        venv/bin/activate|.venv/bin/activate|*/venv/bin/activate|*/.venv/bin/activate) continue ;;
      esac
      # Resolve
      if [[ "$target" == /* ]]; then
        resolved="$target"
      else
        resolved=$(realpath -m "$(dirname "$sh")/$target" 2>/dev/null)
      fi
      if [[ ! -f "$resolved" ]]; then
        broken_sources+=("{\"in_file\":\"$sh\",\"line\":$line,\"target\":\"$target\"}")
      fi
    done < <(grep -nE '^\s*(source\s+|\.\s+)[^ ;|&]+' "$sh" 2>/dev/null | head -50)
  done < <(find "$root" -type f -name '*.sh' \
    -not -path '*/.git/*' -not -path '*/.archive/*' 2>/dev/null | head -300)
done

join_arr() { local IFS=,; echo "$*"; }

cat <<JSON
{
  "audit_date": "$(date +%Y-%m-%d)",
  "broken_md_links": [$(join_arr "${broken_md[@]:-}")],
  "dangling_symlinks": [$(join_arr "${dangling_symlinks[@]:-}")],
  "broken_sources": [$(join_arr "${broken_sources[@]:-}")],
  "broken_imports": [$(join_arr "${broken_imports[@]:-}")]
}
JSON
