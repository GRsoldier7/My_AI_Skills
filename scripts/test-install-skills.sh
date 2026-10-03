#!/usr/bin/env bash
# Tests for scripts/install-skills.sh. Uses this repo's real skill directories and a throwaway
# HOME; nothing outside a temp directory is touched.
#
# Usage: ./scripts/test-install-skills.sh

set -uo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
INSTALL="$REPO_DIR/scripts/install-skills.sh"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
PASSES=0
FAILS=0
RC=0

check() {  # check <name> <command...>: passes when the command succeeds
    local name="$1"; shift
    if "$@"; then PASSES=$((PASSES + 1)); echo "ok   $name"; else FAILS=$((FAILS + 1)); echo "FAIL $name"; fi
}
run() {  # run <home> <installer args...>: sets RC, output in $T/out.txt
    local home="$1"; shift
    RC=0
    HOME="$home" "$INSTALL" "$@" > "$T/out.txt" 2>&1 || RC=$?
}
rc_is() { [[ "$RC" -eq "$1" ]]; }
links_to() { [[ -L "$1" && "$(readlink "$1")" == "$2" ]]; }
absent() { [[ ! -e "$1" && ! -L "$1" ]]; }
out_has() { grep -q -- "$1" "$T/out.txt"; }

A=skills/engineering/to-spec
B=skills/engineering/to-tickets
C=skills/engineering/domain-modeling
printf '%s\n# comment\n\n  %s  \n' "$A" "$B" > "$T/set.txt"
mkdir -p "$T/elsewhere"

# T1-T3: dry run, apply, idempotence
H="$T/h1"; mkdir -p "$H"
run "$H" --set "$T/set.txt"
check "T1 dry run exits 3 when changes are pending" rc_is 3
check "T1 dry run creates no Claude dir" absent "$H/.claude"
check "T1 dry run creates no Codex dir" absent "$H/.agents"
run "$H" --set "$T/set.txt" --apply
check "T2 apply exits 0" rc_is 0
check "T2 Claude link points at the repo" links_to "$H/.claude/skills/to-spec" "$REPO_DIR/$A"
check "T2 Codex link points at the repo" links_to "$H/.agents/skills/to-tickets" "$REPO_DIR/$B"
run "$H" --set "$T/set.txt"
check "T3 second dry run is in sync (exit 0)" rc_is 0

# T4-T6: never clobber a real dir or a foreign link; repair a wrong in-repo link
H="$T/h2"; mkdir -p "$H/.claude/skills/to-spec" "$H/.agents/skills"
echo keep > "$H/.claude/skills/to-spec/SKILL.md"
ln -s "$T/elsewhere" "$H/.agents/skills/to-spec"
ln -s "$REPO_DIR/$C" "$H/.claude/skills/to-tickets"
run "$H" --set "$T/set.txt" --apply
check "T4 existing real directory keeps its content" grep -qx keep "$H/.claude/skills/to-spec/SKILL.md"
check "T4 existing real directory is not replaced by a link" test ! -L "$H/.claude/skills/to-spec"
check "T4 reported as SKIP" out_has "SKIP    to-spec (existing directory"
check "T5 foreign symlink survives" links_to "$H/.agents/skills/to-spec" "$T/elsewhere"
check "T6 wrong in-repo link is relinked" links_to "$H/.claude/skills/to-tickets" "$REPO_DIR/$B"

# T7: --prune removes only links into the repo that left the set
H="$T/h1"
mkdir -p "$H/.claude/skills/real-dir"
ln -s "$T/elsewhere" "$H/.claude/skills/foreign"
printf '%s\n' "$A" > "$T/set-small.txt"
run "$H" --set "$T/set-small.txt" --apply --prune
check "T7 dropped Claude link removed" absent "$H/.claude/skills/to-tickets"
check "T7 dropped Codex link removed" absent "$H/.agents/skills/to-tickets"
check "T7 kept link stays" links_to "$H/.claude/skills/to-spec" "$REPO_DIR/$A"
check "T7 real directory untouched" test -d "$H/.claude/skills/real-dir"
check "T7 foreign link untouched" links_to "$H/.claude/skills/foreign" "$T/elsewhere"

# T8: bad entries are refused before anything is written; a trailing slash is normalised
for bad in skills/nope/zzz ../x /etc skills/engineering skills/../skills/engineering/to-spec .claude/skills/frontend-design; do
    H="$T/h-bad"; rm -rf "$H"; mkdir -p "$H"
    printf '%s\n' "$bad" > "$T/set-bad.txt"
    run "$H" --set "$T/set-bad.txt" --apply
    check "T8 bad entry '$bad' exits 1" rc_is 1
    check "T8 bad entry '$bad' creates nothing" absent "$H/.claude"
done
H="$T/h3"; mkdir -p "$H"
printf '%s/\n' "$C" > "$T/set-slash.txt"
run "$H" --set "$T/set-slash.txt" --apply
check "T8 trailing slash installs under the right name" links_to "$H/.claude/skills/domain-modeling" "$REPO_DIR/$C"
H="$T/h3b"; mkdir -p "$H"
printf './%s\n' "$C" > "$T/set-dot.txt"
run "$H" --set "$T/set-dot.txt" --apply
check "T8 ./ prefix is normalised to a managed link" links_to "$H/.claude/skills/domain-modeling" "$REPO_DIR/$C"

# T9-T11: usage errors, NAME mode, --project
run "$T/h1" --apply --prune to-spec
check "T9 --prune with names exits 2" rc_is 2
H="$T/h4"; mkdir -p "$H"
run "$H" --apply domain-modeling
check "T10 NAME mode links the named skill" links_to "$H/.agents/skills/domain-modeling" "$REPO_DIR/$C"
run "$H" --apply no-such-skill-zz
check "T10 unknown name exits 1" rc_is 1
PROJ="$T/proj"; mkdir -p "$PROJ"
run "$T/h5" --project "$PROJ" --set "$T/set.txt" --apply
check "T11 --project targets DIR/.claude/skills" links_to "$PROJ/.claude/skills/to-spec" "$REPO_DIR/$A"
check "T11 --project targets DIR/.agents/skills" links_to "$PROJ/.agents/skills/to-tickets" "$REPO_DIR/$B"
check "T11 --project leaves HOME alone" absent "$T/h5/.claude"

# T12-T14: duplicate names, empty set, relative links are left alone
printf '%s\n%s\n' "$A" "$A" > "$T/set-dup.txt"
run "$T/h6" --set "$T/set-dup.txt" --apply
check "T12 duplicate names exit 1" rc_is 1
printf '# only a comment\n\n' > "$T/set-empty.txt"
run "$T/h6" --set "$T/set-empty.txt" --apply
check "T13 empty set exits 1" rc_is 1
check "T13 empty set says why" out_has "no skills to install"
H="$T/h7"; mkdir -p "$H/.claude/skills"
rel="$(python3 -c 'import os, sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "$REPO_DIR/$A" "$H/.claude/skills")"
ln -s "$rel" "$H/.claude/skills/to-spec"
run "$H" --set "$T/set-slash.txt" --apply --prune
check "T14 relative link into the repo survives --prune" links_to "$H/.claude/skills/to-spec" "$rel"

# T15: Codex never gets skills/aarons-latest/* (scripts/project-router.py manages those copies)
H="$T/h8"; mkdir -p "$H"
run "$H" --apply workbetter
check "T15 owner skill links for Claude Code" links_to "$H/.claude/skills/workbetter" "$REPO_DIR/skills/aarons-latest/workbetter"
check "T15 owner skill is not linked for Codex" absent "$H/.agents/skills/workbetter"
check "T15 says why" out_has "managed by scripts/project-router.py"

# T16: a fully skipped set says so instead of a bare "In sync."
H="$T/h9"; mkdir -p "$H/.claude/skills/to-spec" "$H/.agents/skills/to-spec"
printf '%s\n' "$A" > "$T/set-a.txt"
run "$H" --set "$T/set-a.txt"
check "T16 fully skipped set exits 0" rc_is 0
check "T16 summary counts the skips" out_has "In sync (2 skipped: see SKIP lines)"

# T17: usage errors exit 2
run "$T/h1" --tool
check "T17 --tool without a value exits 2" rc_is 2
run "$T/h1" --project "$T/no-such-dir"
check "T17 --project with a missing dir exits 2" rc_is 2

# T18: --tool codex, CRLF set files, --help
H="$T/h10"; mkdir -p "$H"
run "$H" --tool codex --set "$T/set.txt" --apply
check "T18 --tool codex links Codex" links_to "$H/.agents/skills/to-spec" "$REPO_DIR/$A"
check "T18 --tool codex leaves Claude Code alone" absent "$H/.claude"
H="$T/h11"; mkdir -p "$H"
printf '%s\r\n' "$A" > "$T/set-crlf.txt"
run "$H" --set "$T/set-crlf.txt" --apply
check "T18 CRLF set file installs the right link" links_to "$H/.claude/skills/to-spec" "$REPO_DIR/$A"
run "$T/h1" -h
check "T18 --help exits 0 and prints usage" out_has "Usage:"

# T19: an unset HOME is refused instead of writing under /
RC=0; env -u HOME "$INSTALL" --set "$T/set.txt" > "$T/out.txt" 2>&1 || RC=$?
check "T19 unset HOME exits 2" rc_is 2

# T20: a dangling foreign link is flagged
H="$T/h12"; mkdir -p "$H/.claude/skills"
ln -s "$T/no-such-target" "$H/.claude/skills/to-spec"
run "$H" --set "$T/set-a.txt" --tool claude
check "T20 dangling foreign link is reported as dangling" out_has "dangling, not managed by this repo"

# T21: a stale repo link at a Codex owner-skill name is called out
H="$T/h13"; mkdir -p "$H/.agents/skills"
ln -s "$REPO_DIR/skills/aarons-latest/workbetter" "$H/.agents/skills/workbetter"
run "$H" --tool codex workbetter
check "T21 stale Codex owner link is called out" out_has "remove the stale link"

echo "passed=$PASSES failed=$FAILS"
[[ "$FAILS" -eq 0 ]]
