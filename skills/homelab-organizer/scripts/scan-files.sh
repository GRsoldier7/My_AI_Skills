#!/usr/bin/env bash
# Phase B — File audit
# Walks tracked roots, applies hard-skip floor, computes mtime + ref count + in-use signals.
# Outputs JSON to stdout.
set -uo pipefail

AUDIT_DIR="${AUDIT_DIR:-/root/homelab/docs/organizer/AUDIT-$(date +%Y-%m-%d)}"
STALE_DAYS="${STALE_DAYS:-90}"
SAFE_DAYS="${SAFE_DAYS:-7}"   # never act on anything modified within N days
# A non-integer made the (( )) age tests error out, which reads as false: the floors stopped
# applying and young files went SAFE. Bash reads a leading 0 as octal, so "090" fails the same way,
# and 19+ digits wrap negative in 64-bit (( )). Six digits is ~2,700 years
for v in STALE_DAYS SAFE_DAYS; do
  [[ "${!v}" =~ ^(0|[1-9][0-9]{0,5})$ ]] || { echo "scan-files.sh: $v must be an integer 0-999999, got '${!v}'" >&2; exit 2; }
done

# A seam left exported in the operator's shell narrows the walk or the in-use sources — the
# false-SAFE direction — so every run that uses one says so. Read before any default is assigned
overrides=()
for v in ORGANIZER_ROOTS ORGANIZER_SYMLINK_DIRS ORGANIZER_DIR ORGANIZER_INUSE_FILES ORGANIZER_INUSE_DIRS ORGANIZER_SYS_REF_FILES; do
  [[ -n "${!v:-}" ]] && overrides+=("$v")
done
[[ "${SCAN_ROOT_TOP:-1}" != 1 ]] && overrides+=("SCAN_ROOT_TOP=$SCAN_ROOT_TOP")
# A tuned floor moves files in or out of SAFE as surely as a narrowed root
[[ "$STALE_DAYS" != 90 ]] && overrides+=("STALE_DAYS=$STALE_DAYS")
[[ "$SAFE_DAYS" != 7 ]] && overrides+=("SAFE_DAYS=$SAFE_DAYS")
if (( ${#overrides[@]} )); then echo "scan-files.sh: override active: ${overrides[*]}" >&2; fi

ROOTS=(
  "/root/homelab"
  "/opt/echelon/Biohacking_Optimization"
  "/root/.claude/sessions"
  "/root/.claude/todos"
  "/root/.claude/file-history"
  "/root/My_AI_Skills"
)
# Space-separated override, used by the self-test
if [[ -n "${ORGANIZER_ROOTS:-}" ]]; then read -ra ROOTS <<<"$ORGANIZER_ROOTS"; fi
# /root top-level scratch (depth-1 only) handled specially below
SCAN_ROOT_TOP="${SCAN_ROOT_TOP:-1}"
# Prior AUDIT-*/files.json lists every candidate path; indexing it gives each stale file a fake ref
ORGANIZER_DIR="${ORGANIZER_DIR:-/root/homelab/docs/organizer}"
# Upstream code checked out inside a tracked root — never ours to quarantine
VENDORED_PATHS=("/root/homelab/containers/home-assistant/external" "/root/homelab/projects/caveman")
# Depth-1 symlink homes OUTSIDE the roots whose targets are live (space-separated override for the self-test)
read -ra SYMLINK_DIRS <<<"${ORGANIZER_SYMLINK_DIRS:-/root/.claude/skills /root/.claude/commands /root/.claude/hooks /root}"

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
  "/root/.claude/CLAUDE.md"
  "/root/AGENTS.md"
)
INUSE_DIRS=("/root/homelab/docs/runbooks" "/root/homelab/docs/living" "/root/.claude/projects/-root/memory")
# Space-separated overrides, used by the self-test so it never reads live operator memory
if [[ -n "${ORGANIZER_INUSE_FILES:-}" ]]; then read -ra INUSE_FILES <<<"$ORGANIZER_INUSE_FILES"; fi
if [[ -n "${ORGANIZER_INUSE_DIRS:-}" ]]; then read -ra INUSE_DIRS <<<"$ORGANIZER_INUSE_DIRS"; fi

# Build inbound-reference index — scan tracked roots once for filename mentions
# This is the "reference graph" — we cache it later in state.yaml
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
INDEX_FILE="$TMP/refs.txt"
: > "$INDEX_FILE"

# Credential-shaped names. Applied to DATA files only (json/yaml/conf/...): a tokenizer.py or a
# token-budget.md is code/docs, and dropping it from the walk also drops it as a reference source
CRED_NAME_EXCL=(! -iname '*secret*' ! -iname '*credential*' ! -iname '*token*' ! -iname '*password*' ! -iname '*passwd*'
  ! -iname '*creds*' ! -iname '*apikey*' ! -iname '*api_key*' ! -iname '*private*' ! -name 'rclone.conf' ! -name 'wg*.conf')

walk_file_list() {
  local vendored_prune=() v
  for v in "${VENDORED_PATHS[@]}"; do vendored_prune+=(-o -path "$v"); done
  for root in "${ROOTS[@]}"; do
    [[ -d "$root" ]] || continue
    # Prune by directory name (NOT -type f — that breaks descent prevention).
    # Credential-class dirs and names are pruned HERE, before anything reads them:
    # the ref index greps every walked file, so a later floor check is too late.
    find "$root" \
      \( -type d \( -name '.git' -o -name '.planning' -o -name '.venv' -o -name 'venv' -o -name 'node_modules' -o -name '__pycache__' -o -name 'target' -o -name 'dist' -o -name 'build' -o -name '.archive' -o -name 'backups' -o -name '.cache' -o -name '.local' -o -name '.config' -o -name '.gnupg' \
          -o -iname 'credentials' -o -iname 'secrets' -o -iname 'keys' -o -name '.ssh' -o -name '.docker' -o -name '.kube' -o -name '.aws' -o -name '.gcloud' -o -name '.password-store' \
          -o -name '.mypy_cache' -o -name '.pytest_cache' -o -name '.ruff_cache' -o -name '.next' -o -name '.turbo' "${vendored_prune[@]}" \) -prune \) \
      -o \( -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.tf' -o -name '*.service' -o -name '*.socket' -o -name '*.timer' \) -print \) \
      -o \( -type f "${CRED_NAME_EXCL[@]}" \
        \( -name '*.yaml' -o -name '*.yml' -o -name '*.json' -o -name '*.toml' -o -name '*.ini' -o -name '*.cfg' -o -name '*.conf' \) -print \) 2>/dev/null
  done
  # /root top-level scratch (depth-1 only) — exclude /root dotfiles by mindepth
  (( SCAN_ROOT_TOP )) || return 0
  find /root -mindepth 1 -maxdepth 1 -type f ! -name '.*' "${CRED_NAME_EXCL[@]}" ! -name 'id_*' ! -name '*.ppk' \
    ! -name '*.env' ! -name '*.pem' ! -name '*.key' ! -name '*.kdbx' ! -name '*.gpg' ! -name '*.asc' ! -name '*.p12' ! -name '*.pfx' 2>/dev/null
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
  done < "$TMP/refs_input.txt" | sort -u > "$TMP/basenames.txt"

  # Basenames come from every walked file; reference SOURCES exclude the organizer's own output
  grep -v "^$ORGANIZER_DIR/" "$TMP/refs_input.txt" > "$TMP/ref_sources.txt"
  xargs -d '\n' -r grep -HoFf "$TMP/basenames.txt" < "$TMP/ref_sources.txt" 2>/dev/null > "$INDEX_FILE"

  # Python modules are referenced by module name, never by "foo.py". The names after `import`
  # are optional so `from pkg.mod import (` still yields pkg + mod
  grep '\.py$' "$TMP/ref_sources.txt" | xargs -d '\n' -r grep -hoE \
    '^[[:space:]]*(from[[:space:]]+[A-Za-z0-9_.]+([[:space:]]+import[[:space:]]+[A-Za-z0-9_., ]+)?|import[[:space:]]+[A-Za-z0-9_., ]+)' 2>/dev/null \
    | tr -c 'A-Za-z0-9_\n' '\n' | grep -v '^$' | sort -u > "$TMP/py_imported.txt"

  # Paths named by cron, systemd units and symlinks. safety-rules.md makes these in-use signals,
  # so the walk reads them — path tokens only, never whole lines (unit Environment= may hold secrets)
  {
    if [[ -n "${ORGANIZER_SYS_REF_FILES:-}" ]]; then
      # Self-test override: fixture files stand in for the live crontab and unit dirs
      read -ra sys_ref_files <<<"$ORGANIZER_SYS_REF_FILES"
      cat "${sys_ref_files[@]}" 2>/dev/null
    else
      crontab -l 2>/dev/null
      cat /etc/crontab /etc/cron.d/* /var/spool/cron/crontabs/* /etc/cron.hourly/* /etc/cron.daily/* /etc/cron.weekly/* /etc/cron.monthly/* 2>/dev/null
      cat /etc/systemd/system/*.service /etc/systemd/system/*.timer /etc/systemd/system/*.path /etc/systemd/system/*.d/*.conf 2>/dev/null
    fi
  } | grep -oE '/[A-Za-z0-9_./@+-]+' > "$TMP/sys_refs.txt"
  # Symlinks inside the roots, plus the homes that link INTO them (~/.claude/skills -> My_AI_Skills)
  {
    for root in "${ROOTS[@]}"; do
      [[ -d "$root" ]] || continue
      find "$root" -path '*/.git' -prune -o -type l -print0 2>/dev/null
    done
    for d in "${SYMLINK_DIRS[@]}"; do
      [[ -d "$d" ]] && find "$d" -mindepth 1 -maxdepth 1 -type l -print0 2>/dev/null
    done
  } | xargs -0 -r readlink -f 2>/dev/null | sort -u > "$TMP/link_targets.txt"
  cat "$TMP/link_targets.txt" >> "$TMP/sys_refs.txt"
  # A linked DIRECTORY makes everything under it live
  while IFS= read -r t; do [[ -d "$t" ]] && echo "$t"; done < "$TMP/link_targets.txt" > "$TMP/link_dirs.txt"
}

all_files=$(walk_file_list)
echo "$all_files" > "$TMP/refs_input.txt"

build_ref_index

# Index lines are "<source>:<matched basename>". Exact suffix compare, not a regex: a basename
# holding [ or * made grep error out, which read as 0 refs -> SAFE. ENVIRON, not awk -v, keeps backslashes literal
count_refs() {
  REF_SUFFIX=":$1" awk 'BEGIN { b = ENVIRON["REF_SUFFIX"]; n = length(b) }
    substr($0, length($0) - n + 1) == b { c++ } END { print c + 0 }' "$INDEX_FILE"
}

check_inuse() {
  local path="$1" base
  base=$(basename "$path")
  # Systemd units anywhere — referenced via systemctl, not by other files
  case "$base" in
    *.service|*.socket|*.timer|*.target|*.path|*.mount) echo "systemd_unit"; return ;;
  esac
  # Passive infrastructure configs — referenced by daemons, not by other files
  case "$base" in
    Caddyfile|nginx.conf|httpd.conf|postgresql.conf|redis.conf|crontab) echo "passive_infrastructure_config"; return ;;
  esac
  case "$path" in
    */cron.d/*|*/cron.daily/*|*/cron.hourly/*|*/cron.weekly/*|*/cron.monthly/*) echo "cron_job"; return ;;
  esac
  if [[ "$base" == *.py ]] && grep -qxF "${base%.py}" "$TMP/py_imported.txt"; then
    echo "imported_as_module"; return
  fi
  grep -qF -- "$base" "$TMP/sys_refs.txt" && { echo "cron_systemd_or_symlink_ref"; return; }
  local d
  while IFS= read -r d; do
    [[ "$path" == "$d"/* ]] && { echo "inside_symlinked_dir"; return; }
  done < "$TMP/link_dirs.txt"
  for f in "${INUSE_FILES[@]}"; do
    [[ -f "$f" ]] || continue
    grep -qF -- "$base" "$f" 2>/dev/null && { echo "mentioned_in_$(basename "$f")"; return; }
  done
  for d in "${INUSE_DIRS[@]}"; do
    [[ -d "$d" ]] || continue
    grep -rqF --include='*.md' --include='*.sh' --exclude-dir=credentials --exclude-dir=secrets --exclude-dir=keys \
      -- "$base" "$d" 2>/dev/null && { echo "mentioned_in_$(basename "$d")"; return; }
  done
  echo ""
}

# Hard-skip floor for individual paths (applied per-file, not in find -prune)
floor_skip() {
  local p="$1"
  # Credentials class — never propose action, even duplicates
  case "$p" in
    */credentials/*|*/secrets/*|*/keys/*) return 0 ;;
  esac
  # /root/ dotfiles with system meaning
  case "$p" in
    /root/.forward|/root/.lesshst|/root/.selected_editor|/root/.bash_history|/root/.Xauthority|/root/.viminfo|/root/.python_history|/root/.profile|/root/.bashrc|/root/.bash_logout|/root/.zshrc|/root/.zsh_history|/root/.gitconfig|/root/.gitignore_global|/root/.npmrc|/root/.wget-hsts|/root/.sudo_as_admin_successful) return 0 ;;
    /root/.cache/*|/root/.local/*|/root/.config/*|/root/.gnupg/*) return 0 ;;
  esac
  return 1
}

# Build candidate list
# Initialised, not just declared: under set -u an empty `declare -a` array aborts the emit below
safe_q=(); watchlist=(); dated_hist=(); duplicates=()
declare -A hash_seen
# ISO dates anywhere, or the house "YYYYMMDD - Description" prefix
DATED_RE='([0-9]{4}-[0-9]{2}-[0-9]{2}|^[0-9]{8} - )'
# Paths go into JSON by interpolation — one quote or backslash in a filename made the whole file unparseable
json_esc() { local s=${1//\\/\\\\}; printf '%s' "${s//\"/\\\"}"; }
total_scanned=0
total_skipped_floor=0

while IFS= read -r f; do
  [[ -f "$f" ]] || continue
  total_scanned=$((total_scanned+1))
  # Floor: per-path hard-skip (credentials, /root dotfiles)
  if floor_skip "$f"; then
    total_skipped_floor=$((total_skipped_floor+1))
    continue
  fi
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
  # stdin, not a filename arg: sha256sum prefixes its output with "\" when the name holds a backslash
  hash=$(sha256sum < "$f" 2>/dev/null | cut -c1-12)
  size=$(stat -c %s "$f" 2>/dev/null || echo 0)
  is_dated=false
  if [[ "$base" =~ $DATED_RE ]]; then
    is_dated=true
  fi

  # Duplicate detection — refs + in-use travel with the entry so a cited copy is never proposed
  jf=$(json_esc "$f")
  if [[ -n "${hash_seen[$hash]:-}" ]]; then
    duplicates+=("{\"path\":\"$jf\",\"duplicate_of\":\"${hash_seen[$hash]}\",\"hash\":\"$hash\",\"mtime_days\":$mtime_days,\"size\":$size,\"refs\":$refs,\"in_use_signals\":\"$inuse\"}")
    continue
  fi
  hash_seen[$hash]="$jf"

  # Categorize
  entry="{\"path\":\"$jf\",\"mtime_days\":$mtime_days,\"size\":$size,\"hash\":\"$hash\",\"refs\":$refs,\"in_use_signals\":\"$inuse\""
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
