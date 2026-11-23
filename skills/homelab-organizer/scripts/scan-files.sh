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
for v in ORGANIZER_ROOTS ORGANIZER_SYMLINK_DIRS ORGANIZER_DIR ORGANIZER_INUSE_FILES ORGANIZER_INUSE_DIRS ORGANIZER_SYS_REF_FILES ORGANIZER_CT_REF_FILES ORGANIZER_CT_CONFIG_FILES; do
  [[ -n "${!v:-}" ]] && overrides+=("$v")
done
[[ "${SCAN_ROOT_TOP:-1}" != 1 ]] && overrides+=("SCAN_ROOT_TOP=$SCAN_ROOT_TOP")
# A tuned floor moves files in or out of SAFE as surely as a narrowed root
[[ "$STALE_DAYS" != 90 ]] && overrides+=("STALE_DAYS=$STALE_DAYS")
[[ "$SAFE_DAYS" != 7 ]] && overrides+=("SAFE_DAYS=$SAFE_DAYS")
if (( ${#overrides[@]} )); then echo "scan-files.sh: override active: ${overrides[*]}" >&2; fi
# The guest seams replace a safety signal outright: one naming a missing file would drop every guest ref
# and mount without a trace beyond the notice above, so an unreadable one stops the scan. -d '': the whole
# value, split on any whitespace, exactly as the readers below take it (a plain read stops at a newline).
# Fed NUL-terminated so read ends on its delimiter and returns 0, not 1 at EOF
for v in ORGANIZER_CT_REF_FILES ORGANIZER_CT_CONFIG_FILES; do
  [[ -n "${!v:-}" ]] || continue
  read -ra seam_files -d '' < <(printf '%s\0' "${!v}")
  for sf in "${seam_files[@]}"; do
    [[ -f "$sf" && -r "$sf" ]] || { echo "scan-files.sh: $v names an unreadable file ($sf): scan stopped" >&2; exit 2; }
  done
done

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

# Absolute paths named in cron/unit text: bare tokens, plus whole quoted or backslash-escaped paths, so a
# script whose name holds a space is named in full. Tokens only, never whole lines (Environment= may hold secrets)
read -r UNIT_PATH_RE <<'RE'
"/[^"]+"|'/[^']+'|/([A-Za-z0-9_./@+-]|\\ )+
RE
unit_paths() { grep -oE -- "$UNIT_PATH_RE" | sed -E "s/^[\"']//; s/[\"']\$//; s/\\\\ / /g"; }

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
  # Basenames cited by exactly one source: quarantining that source leaves them unreferenced (#27).
  # Split at the LAST ":" — a source path may hold one, a basename rarely does
  awk '{ if (!match($0, /:[^:]*$/)) next; src = substr($0, 1, RSTART - 1); b = substr($0, RSTART + 1)
         if (!((b, src) in seen)) { seen[b, src] = 1; n[b]++; one[b] = src } }
       END { for (b in n) if (n[b] == 1) print b "\t" one[b] }' "$INDEX_FILE" > "$TMP/sole_citer.tsv"

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
  } | unit_paths > "$TMP/sys_refs.txt"
  # Guest side (safety-rules.md: container service definitions). A repo script copied into a guest and
  # run there names only the copy's path, so each RUNNING guest's crontabs, cron dirs and every unit file
  # and drop-in (admin and package unit dirs) are read too: path tokens only, as above, and never into
  # link_dirs (a guest's /root is not the host's). A guest whose dump fails is listed in
  # ct_refs_unreadable; a failed listing stops the scan — neither may read as "names nothing"
  : > "$TMP/ct_unreadable.txt"
  ct_live=0
  if [[ -z "${ORGANIZER_CT_REF_FILES:-}" ]] && command -v pct >/dev/null 2>&1; then
    pct list > "$TMP/pct_list.txt" 2>/dev/null \
      || { echo "scan-files.sh: pct list failed, so no guest's cron/unit refs can be read: scan stopped" >&2; exit 3; }
    ct_live=1
  fi
  {
    if [[ -n "${ORGANIZER_CT_REF_FILES:-}" ]]; then
      read -ra ct_ref_files -d '' < <(printf '%s\0' "$ORGANIZER_CT_REF_FILES")
      cat "${ct_ref_files[@]}" 2>/dev/null
    elif (( ct_live )); then
      while read -r id status _; do
        [[ "$id" =~ ^[0-9]+$ && "$status" == running ]] || continue
        # stdin from /dev/null: this loop reads the listing on stdin, and exec must not drain it
        timeout 20 pct exec "$id" -- sh -c 'cat /etc/crontab /etc/cron.d/* /etc/cron.hourly/* /etc/cron.daily/* /etc/cron.weekly/* /etc/cron.monthly/* /var/spool/cron/* /var/spool/cron/crontabs/* /etc/systemd/system/* /etc/systemd/system/*/* /lib/systemd/system/* /lib/systemd/system/*/* /usr/lib/systemd/system/* /usr/lib/systemd/system/*/* 2>/dev/null; exit 0' </dev/null 2>/dev/null \
          || echo "$id" >> "$TMP/ct_unreadable.txt"
      done < "$TMP/pct_list.txt"
    fi
  } | unit_paths >> "$TMP/sys_refs.txt"
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
  # LXC mount points bind a host dir or a single host file into a guest (safety-rules.md: container
  # service definitions), so the bound path is live there. Host paths only: a volume-backed mp
  # (storage:vm-N-disk-M) names none. The seam stands in for /etc/pve/lxc/*.conf
  {
    if [[ -n "${ORGANIZER_CT_CONFIG_FILES:-}" ]]; then
      read -ra ct_config_files -d '' < <(printf '%s\0' "$ORGANIZER_CT_CONFIG_FILES")
      cat "${ct_config_files[@]}" 2>/dev/null
    else
      cat /etc/pve/lxc/*.conf 2>/dev/null
    fi
  } | sed -nE 's#^(mp[0-9]+|lxc\.mount\.entry):[[:space:]]*(/[^,[:space:]]*).*#\2#p' \
    | while IFS= read -r m; do realpath -m -- "$m"; done | sort -u > "$TMP/ct_mounts.txt"
  # Held is the safe direction, but a bind covering a whole scan root holds everything under it, and an
  # audit that proposes nothing has to say why. Canonical paths, so a bind of / or of <dir>/. still counts
  while IFS= read -r m; do
    for root in "${ROOTS[@]}"; do
      croot=$(realpath -m -- "$root")
      [[ "$m" == / || "$croot" == "$m" || "$croot" == "$m"/* ]] && echo "scan-files.sh: CT mount $m covers scan root $root: everything under it reads in use" >&2
    done
  done < "$TMP/ct_mounts.txt"
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
  # A package marker is referenced by the import system, never by name — and __init__.py is kept out
  # of the ref index as over-common, so by name it could only ever read as unreferenced
  [[ "$base" == __init__.py ]] && { echo "package_marker"; return; }
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
  # Mount sources are canonical, but find emits paths under a root as given (a root may sit below a symlink)
  if [[ -s "$TMP/ct_mounts.txt" ]]; then
    local cpath
    cpath=$(realpath -m -- "$path")
    while IFS= read -r d; do
      [[ "$d" == / || "$cpath" == "$d" || "$cpath" == "$d"/* ]] && { echo "ct_mount"; return; }
    done < "$TMP/ct_mounts.txt"
  fi
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
# Credential SHAPES, not names (names are pruned at walk time): a PEM private-key block, well-known token
# prefixes and a JWT (case-sensitive), and, case-insensitively, a password/secret/token/key assignment
# whose value is a literal: quoted and 8+ chars (spaces allowed, a passphrase has them), or bare, 12+ token
# chars, ending at a separator (so a call result, token = make_token(x), is not one). A reference ($VAR,
# <placeholder>, {{ tmpl }}, %var%) is not a literal. A heuristic, not a secret scanner: a short bare default
# (password: changeme) passes
read -r CRED_SHAPE_RE <<'RE'
-----BEGIN [A-Z ]*PRIVATE KEY-----|(^|[^A-Za-z0-9])(AKIA|ASIA)[0-9A-Z]{16}|(^|[^A-Za-z0-9])sk[-_][A-Za-z0-9_-]{20,}|(^|[^A-Za-z0-9])gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,}|(^|[^A-Za-z0-9])xox[abpr]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}
RE
read -r CRED_ASSIGN_RE <<'RE'
(password|passwd|pwd|secret|token|api[_-]?key|apikey|private[_-]?key|access[_-]?key|secret[_-]?key)s?["'`]?[[:space:]]*[=:][[:space:]]*(["'`][^"'`$<{%]{8,}["'`]|[A-Za-z0-9+/=_@#!^*-]{12,}([[:space:],;]|$))
RE
# basename -> its only citing file (#27); proposed rows collect the files they would orphan
declare -A sole_citer orphans_of
while IFS=$'\t' read -r b src; do sole_citer[$b]=$src; done < "$TMP/sole_citer.tsv"
safe_paths=(); dated_paths=(); dup_paths=()
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

  jf=$(json_esc "$f")
  entry="{\"path\":\"$jf\",\"mtime_days\":$mtime_days,\"size\":$size,\"hash\":\"$hash\",\"refs\":$refs,\"in_use_signals\":\"$inuse\""
  reason=""
  (( refs > 0 )) && reason="${reason}has_inbound_refs;"
  [[ -n "$inuse" ]] && reason="${reason}${inuse};"
  # Credential-shaped content is never proposed, and never printed: the match is an exit status. Gated
  # before dedup, so a same-content copy cannot surface as a DUPLICATE of a held file either
  if (( size > 0 )) && { grep -qE -- "$CRED_SHAPE_RE" "$f" || grep -qiE -- "$CRED_ASSIGN_RE" "$f"; } 2>/dev/null; then
    watchlist+=("$entry,\"reason\":\"${reason}credential_shaped;\"}")
    continue
  fi
  # Zero bytes carry no evidence: every empty file is hash-equal, so dedup is meaningless, and an empty
  # file may be a marker (__init__.py, a placeholder config) whose existence is the point
  if (( size == 0 )); then
    watchlist+=("$entry,\"reason\":\"${reason}zero_byte;\"}")
    continue
  fi
  # Held only by refs, all from one file: quarantining that file would orphan this one (#27)
  if (( refs > 0 )) && [[ -z "$inuse" ]]; then
    src=${sole_citer[$base]:-}
    [[ -n "$src" && "$src" != "$f" ]] && orphans_of[$src]+="\"$jf\","
  fi

  # Duplicate detection — refs + in-use travel with the entry so a cited copy is never proposed
  if [[ -n "${hash_seen[$hash]:-}" ]]; then
    # DUPLICATE is a proposed bucket: a cited or in-use copy is held like any other cited file (#30)
    if (( refs > 0 )) || [[ -n "$inuse" ]]; then
      watchlist+=("$entry,\"reason\":\"${reason}duplicate;\"}")
      continue
    fi
    duplicates+=("{\"path\":\"$jf\",\"duplicate_of\":\"${hash_seen[$hash]}\",\"hash\":\"$hash\",\"mtime_days\":$mtime_days,\"size\":$size,\"refs\":$refs,\"in_use_signals\":\"$inuse\"}")
    dup_paths+=("$f")
    continue
  fi
  hash_seen[$hash]="$jf"

  # Categorize
  if (( refs == 0 )) && [[ -z "$inuse" ]]; then
    if [[ "$is_dated" == "true" ]]; then
      dated_hist+=("$entry,\"reason\":\"dated_artifact_no_refs\"}")
      dated_paths+=("$f")
    else
      safe_q+=("$entry,\"reason\":\"mtime_gt_${STALE_DAYS}d_no_refs\"}")
      safe_paths+=("$f")
    fi
  else
    watchlist+=("$entry,\"reason\":\"$reason\"}")
  fi
done <<< "$all_files"

# Every proposed row names the files its quarantine would leave unreferenced (#27)
with_orphans() {
  local -n rows=$1 paths=$2
  local i o
  for i in "${!rows[@]}"; do
    o=${orphans_of[${paths[$i]}]:-}
    rows[$i]="${rows[$i]%\}},\"would_orphan\":[${o%,}]}"
  done
}
with_orphans safe_q safe_paths
with_orphans dated_hist dated_paths
with_orphans duplicates dup_paths

ct_unreadable=$(sort -un "$TMP/ct_unreadable.txt" | paste -sd, -)
if [[ -n "$ct_unreadable" ]]; then
  echo "scan-files.sh: guest cron/unit dump failed for CT ${ct_unreadable//,/, CT }: scripts those guests run are NOT protected, check them by hand" >&2
fi

# Emit JSON
join_arr() {
  local IFS=,
  echo "$*"
}

cat <<JSON
{
  "audit_date": "$(date +%Y-%m-%d)",
  "totals": {"scanned": $total_scanned, "skipped_floor": $total_skipped_floor, "candidates_safe_quarantine": ${#safe_q[@]}, "candidates_watchlist": ${#watchlist[@]}, "candidates_dated": ${#dated_hist[@]}, "candidates_duplicates": ${#duplicates[@]}},
  "ct_refs_unreadable": [$( [[ -n "$ct_unreadable" ]] && printf '"%s"' "${ct_unreadable//,/\",\"}" )],
  "categorized": {
    "SAFE_QUARANTINE": [$(join_arr "${safe_q[@]:-}")],
    "WATCHLIST": [$(join_arr "${watchlist[@]:-}")],
    "DATED_HISTORICAL": [$(join_arr "${dated_hist[@]:-}")],
    "DUPLICATE": [$(join_arr "${duplicates[@]:-}")]
  }
}
JSON
