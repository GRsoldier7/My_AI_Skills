#!/usr/bin/env bash
# Phase C — Link integrity
# Checks markdown links, dangling symlinks, shell sources.
# Python imports are NOT checked — broken_imports is emitted as null, never as a clean [].
set -uo pipefail

# A seam left exported in the operator's shell silently narrows the audit, so every run that uses
# one says so. Read before any default is assigned
overrides=()
for v in ORGANIZER_ROOTS ORGANIZER_DIR; do [[ -n "${!v:-}" ]] && overrides+=("$v"); done
if (( ${#overrides[@]} )); then echo "check-links.sh: override active: ${overrides[*]}" >&2; fi

ROOTS=("/root/homelab" "/opt/echelon/Biohacking_Optimization" "/root/My_AI_Skills" "/root/.claude/projects/-root/memory")
# Space-separated override, used by the self-test
if [[ -n "${ORGANIZER_ROOTS:-}" ]]; then read -ra ROOTS <<<"$ORGANIZER_ROOTS"; fi
# The organizer's own reports quote every broken link they found, so checking them re-reports each
# finding forever (scan-files.sh excludes the same dir as a reference source)
ORGANIZER_DIR="${ORGANIZER_DIR:-/root/homelab/docs/organizer}"

declare -a broken_md dangling_symlinks broken_sources unclosed_fences

# Held in a variable: written inline in [[ =~ ]], bash's quoting of \( \] made this regex never match.
# A destination may hold one level of balanced parens (CommonMark): "(Mid).md" is part of the target
MD_LINK_RE='\[[^]]*\]\((([^()#[:space:]]|\([^()#[:space:]]*\))+)(#[^)]*)?\)'
# Interpolated into JSON — a markdown-escaped "\_" in a target was an illegal JSON escape
json_esc() { local s=${1//\\/\\\\}; printf '%s' "${s//\"/\\\"}"; }
# Credential-class dirs are never opened, same as scan-files.sh
CRED_DIR_EXCL=(-not -ipath '*/credentials/*' -not -ipath '*/secrets/*' -not -ipath '*/keys/*' -not -path '*/.ssh/*')

# Percent-decoding, into REPLY. Only %XX for a printable ASCII byte (20-7E) is decoded, rightmost first
# so a bare % never blocks a later escape; one pass, so %2520 yields %20. Anything else stays literal: a
# control byte or an invalid UTF-8 byte in "resolved" made the whole JSON unparseable, and %00 fits no
# path. Not printf %b: that re-reads a target's own backslashes (\_) and \c truncates
pct_decode() {
  local s="$1" tail="" c
  while [[ "$s" =~ ^(.*)%(2[0-9A-Fa-f]|[3-6][0-9A-Fa-f]|7[0-9A-Ea-e])(.*)$ ]]; do
    printf -v c "\\x${BASH_REMATCH[2]}"
    tail="$c${BASH_REMATCH[3]}$tail"; s="${BASH_REMATCH[1]}"
  done
  REPLY="$s$tail"
}

# Markdown links — [text](path) where path is local and not a remote URL
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
      # Strip through the whole match: stripping through the first ")" re-scanned the same link
      # whenever a ")" preceded it on the line, and the row came out twice
      content="${content#*"${BASH_REMATCH[0]}"}"
      path="$target"
      # Skip anchors and remote URLs. file:///abs, file:/abs and file://localhost/abs are local
      # paths; any other authority is a remote host, as uncheckable as https
      [[ "$path" =~ ^# ]] && continue
      [[ "$path" =~ ^https?:// ]] && continue
      [[ "$path" =~ ^mailto: ]] && continue
      if [[ "$path" == file:* ]]; then
        path="${path#file:}"
        if [[ "$path" == //* ]]; then
          path="${path#//}"
          [[ "$path" == localhost/* ]] && path="${path#localhost}"
          [[ "$path" == /* ]] || continue
        fi
      fi
      pct_decode "$path"; path="$REPLY"
      # Absolute targets resolve as-is; relative ones against the .md's directory
      if [[ "$path" == /* ]]; then
        resolved=$(realpath -m "$path" 2>/dev/null)
      else
        resolved=$(realpath -m "$(dirname "$md")/$path" 2>/dev/null)
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
    # Inline code is not a link (CommonMark: code spans bind before links). Stripped here, after the
    # fence check, so NR is still the line in the file. Plain ``…`` spans go first, then backticks pair
    # singly: a longer run or an escaped \` can still pair wrongly (link findings only)
    !open && /\]\(/ { s2 = $0; gsub(/``[^`]*``/, "", s2); gsub(/`[^`]*`/, "", s2); if (s2 ~ /\]\(/) print NR ":" s2 }
    END { if (open) print "U:" start }' "$md" 2>/dev/null)
}

for root in "${ROOTS[@]}"; do
  [[ -d "$root" ]] || continue
  while IFS= read -r md; do
    check_md_links "$md"
  done < <(find "$root" -type f -name '*.md' \
    -not -path '*/.git/*' -not -path '*/.archive/*' -not -path '*/node_modules/*' \
    -not -path '*/.venv/*' -not -path '*/__pycache__/*' -not -path "$ORGANIZER_DIR/*" "${CRED_DIR_EXCL[@]}" 2>/dev/null)

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
    -not -path '*/.git/*' -not -path '*/.archive/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path "$ORGANIZER_DIR/*" "${CRED_DIR_EXCL[@]}" 2>/dev/null)
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
