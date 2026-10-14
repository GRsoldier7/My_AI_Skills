#!/usr/bin/env bash
# Phase C — Link integrity
# Checks markdown links, dangling symlinks, shell sources.
# Python imports are NOT checked — broken_imports is emitted as null, never as a clean [].
set -uo pipefail

ROOTS=("/root/homelab" "/opt/echelon/Biohacking_Optimization" "/root/My_AI_Skills" "/root/.claude/projects/-root/memory")
# Space-separated override, used by the self-test
if [[ -n "${ORGANIZER_ROOTS:-}" ]]; then
  read -ra ROOTS <<<"$ORGANIZER_ROOTS"
  # Left exported in the operator's shell, it silently narrows the audit
  echo "check-links.sh: override active: ORGANIZER_ROOTS" >&2
fi

declare -a broken_md dangling_symlinks broken_sources unclosed_fences

# Held in a variable: written inline in [[ =~ ]], bash's quoting of \( \] made this regex never match
MD_LINK_RE='\[[^]]*\]\(([^)#[:space:]]+)(#[^)]*)?\)'
# Interpolated into JSON — a markdown-escaped "\_" in a target was an illegal JSON escape
json_esc() { local s=${1//\\/\\\\}; printf '%s' "${s//\"/\\\"}"; }
# Credential-class dirs are never opened, same as scan-files.sh
CRED_DIR_EXCL=(-not -ipath '*/credentials/*' -not -ipath '*/secrets/*' -not -ipath '*/keys/*' -not -path '*/.ssh/*')

# Markdown links — [text](path) where path is relative and not a URL
check_md_links() {
  local md="$1"
  while IFS=: read -r line content; do
    # "U:<opener line>" — a fence still open at EOF hides every later link, so surface it
    if [[ "$line" == U ]]; then
      unclosed_fences+=("{\"in_file\":\"$(json_esc "$md")\",\"line\":$content}")
      continue
    fi
    # Extract every [..](..) pair on the line
    while [[ "$content" =~ $MD_LINK_RE ]]; do
      target="${BASH_REMATCH[1]}"
      content="${content#*\)}"
      # Skip URLs and anchors
      [[ "$target" =~ ^https?:// ]] && continue
      [[ "$target" =~ ^mailto: ]] && continue
      [[ "$target" =~ ^# ]] && continue
      # Absolute targets resolve as-is; relative ones against the .md's directory
      if [[ "$target" == /* ]]; then
        resolved=$(realpath -m "${target//%20/ }" 2>/dev/null)
      else
        resolved=$(realpath -m "$(dirname "$md")/${target//%20/ }" 2>/dev/null)
      fi
      if [[ ! -e "$resolved" ]]; then
        broken_md+=("{\"in_file\":\"$(json_esc "$md")\",\"line\":$line,\"target\":\"$(json_esc "$target")\",\"resolved\":\"$(json_esc "$resolved")\"}")
      fi
    done
  # Lines inside ``` / ~~~ fences are examples, not links. A fence closes only on a bare run of its
  # own character at least as long as the opener (CommonMark) — a nested marker must not reopen it
  done < <(awk '
    { s = $0; sub(/^[[:space:]]+/, "", s); c = substr(s, 1, 1) }
    (c == "`" || c == "~") && match(s, "^" c "+") && RLENGTH >= 3 {
      if (!open) {
        # A backtick fence info string cannot hold a backtick: ```x``` is inline code, not an opener
        if (!(c == "`" && index(substr(s, RLENGTH + 1), "`"))) { open = c; len = RLENGTH; start = NR; next }
      } else if (c == open && RLENGTH >= len && substr(s, RLENGTH + 1) ~ /^[[:space:]]*$/) { open = ""; next }
    }
    !open && /\]\(/ { print NR ":" $0 }
    END { if (open) print "U:" start }' "$md" 2>/dev/null)
}

for root in "${ROOTS[@]}"; do
  [[ -d "$root" ]] || continue
  while IFS= read -r md; do
    check_md_links "$md"
  done < <(find "$root" -type f -name '*.md' \
    -not -path '*/.git/*' -not -path '*/.archive/*' -not -path '*/node_modules/*' \
    -not -path '*/.venv/*' -not -path '*/__pycache__/*' "${CRED_DIR_EXCL[@]}" 2>/dev/null)

  # Dangling symlinks
  while IFS= read -r link; do
    target=$(readlink "$link" 2>/dev/null || echo "?")
    dangling_symlinks+=("{\"path\":\"$(json_esc "$link")\",\"points_to\":\"$(json_esc "$target")\"}")
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
        broken_sources+=("{\"in_file\":\"$(json_esc "$sh")\",\"line\":$line,\"target\":\"$(json_esc "$target")\"}")
      fi
    done < <(grep -nE '^\s*(source\s+|\.\s+)[^ ;|&]+' "$sh" 2>/dev/null)
  done < <(find "$root" -type f -name '*.sh' \
    -not -path '*/.git/*' -not -path '*/.archive/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' "${CRED_DIR_EXCL[@]}" 2>/dev/null)
done

join_arr() { local IFS=,; echo "$*"; }

cat <<JSON
{
  "audit_date": "$(date +%Y-%m-%d)",
  "broken_md_links": [$(join_arr "${broken_md[@]:-}")],
  "dangling_symlinks": [$(join_arr "${dangling_symlinks[@]:-}")],
  "broken_sources": [$(join_arr "${broken_sources[@]:-}")],
  "unclosed_fences": [$(join_arr "${unclosed_fences[@]:-}")],
  "broken_imports": null
}
JSON
