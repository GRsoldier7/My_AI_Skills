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
out_lacks() { ! grep -q -- "$1" "$T/out.txt"; }

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
for bad in skills/nope/zzz ../x /etc skills/engineering skills/../skills/engineering/to-spec .claude/skills/frontend-design \
           skills//aarons-latest/workbetter skills/./engineering/to-spec skills/aarons-latest/workbetter/.; do
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

# T15: Codex never gets the skills scripts/project-router.py installs (its SKILLS names)
H="$T/h8"; mkdir -p "$H"
run "$H" --apply workbetter
check "T15 owner skill links for Claude Code" links_to "$H/.claude/skills/workbetter" "$REPO_DIR/skills/aarons-latest/workbetter"
check "T15 owner skill is not linked for Codex" absent "$H/.agents/skills/workbetter"
check "T15 says why" out_has "managed by scripts/project-router.py"

# T22: an aarons-latest skill that project-router.py does not manage IS linked for Codex
H="$T/h14"; mkdir -p "$H"
run "$H" --apply grill-me
check "T22 non-router aarons-latest skill links for Claude Code" links_to "$H/.claude/skills/grill-me" "$REPO_DIR/skills/aarons-latest/grill-me"
check "T22 non-router aarons-latest skill links for Codex too" links_to "$H/.agents/skills/grill-me" "$REPO_DIR/skills/aarons-latest/grill-me"
check "T22 no project-router SKIP for it" out_lacks "project-router"

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

# T23-T25: the skip list is project-router.py's SKILLS, read before any write; unreadable fails closed
F="$T/fake"; mkdir -p "$F/scripts" "$F/skills/aarons-latest/workbetter" "$F/skills/aarons-latest/extra"
F="$(cd "$F" && pwd -P)"
cp "$INSTALL" "$F/scripts/"
for s in workbetter extra; do printf -- '---\nname: %s\ndescription: x\n---\n' "$s" > "$F/skills/aarons-latest/$s/SKILL.md"; done
printf "SKILLS = (\n    'extra',\n)\n" > "$F/scripts/project-router.py"
H="$T/h15"; mkdir -p "$H"
RC=0; HOME="$H" "$F/scripts/install-skills.sh" --tool codex --apply workbetter extra > "$T/out.txt" 2>&1 || RC=$?
check "T23 a name in SKILLS is skipped on Codex" absent "$H/.agents/skills/extra"
check "T23 a name not in SKILLS links on Codex" links_to "$H/.agents/skills/workbetter" "$F/skills/aarons-latest/workbetter"
printf "SKILLS: tuple[str, ...] = ('extra',)\n" > "$F/scripts/project-router.py"
H="$T/h15b"; mkdir -p "$H"
RC=0; HOME="$H" "$F/scripts/install-skills.sh" --tool codex extra > "$T/out.txt" 2>&1 || RC=$?
check "T23 an annotated SKILLS assignment is read too" out_has "SKIP    extra (the Codex copy is managed by scripts/project-router.py)"
printf 'SKILLS = tuple(sorted(()))\n' > "$F/scripts/project-router.py"
H="$T/h16"; mkdir -p "$H"
RC=0; HOME="$H" "$F/scripts/install-skills.sh" --apply workbetter > "$T/out.txt" 2>&1 || RC=$?
check "T24 unreadable SKILLS exits 1" rc_is 1
check "T24 unreadable SKILLS writes nothing" absent "$H/.claude"
check "T24 says why" out_has "cannot read SKILLS"
H="$T/h17"; mkdir -p "$H" "$T/nopy-bin"
printf '#!/bin/sh\nexit 127\n' > "$T/nopy-bin/python3"; chmod +x "$T/nopy-bin/python3"
printf 'SKILLS = tuple(sorted(()))\n' > "$F/scripts/project-router.py"
RC=0; PATH="$T/nopy-bin:$PATH" HOME="$H" "$F/scripts/install-skills.sh" --tool claude --apply workbetter > "$T/out.txt" 2>&1 || RC=$?
check "T25 Claude-only run needs neither python3 nor a readable SKILLS list" links_to "$H/.claude/skills/workbetter" "$F/skills/aarons-latest/workbetter"

# T26: a CRLF-emitting python3 (Windows Store build) still matches the SKILLS names
mkdir -p "$T/crlf-bin"
cat > "$T/crlf-bin/python3" <<EOF
#!/bin/sh
"$(command -v python3)" "\$@" | awk '{printf "%s\\r\\n", \$0}'
EOF
chmod +x "$T/crlf-bin/python3"
H="$T/h18"; mkdir -p "$H"
RC=0; PATH="$T/crlf-bin:$PATH" HOME="$H" "$INSTALL" --tool codex workbetter > "$T/out.txt" 2>&1 || RC=$?
check "T26 CRLF SKILLS output still skips workbetter on Codex" out_has "managed by scripts/project-router.py"

# T27-T28: a python3 that exits 0 with junk (a Store alias banner), or fails after printing, is refused
mkdir -p "$T/stub-bin"
printf '#!/bin/sh\necho "Python was not found; run without arguments to install from the Microsoft Store"\n' > "$T/stub-bin/python3"
chmod +x "$T/stub-bin/python3"
H="$T/h19"; mkdir -p "$H"
RC=0; PATH="$T/stub-bin:$PATH" HOME="$H" "$INSTALL" --apply workbetter > "$T/out.txt" 2>&1 || RC=$?
check "T27 junk SKILLS output exits 1" rc_is 1
check "T27 junk SKILLS output writes nothing" absent "$H/.claude"
printf '#!/bin/sh\necho workbetter\nexit 1\n' > "$T/stub-bin/python3"
H="$T/h20"; mkdir -p "$H"
RC=0; PATH="$T/stub-bin:$PATH" HOME="$H" "$INSTALL" --apply workbetter > "$T/out.txt" 2>&1 || RC=$?
check "T28 a failing python3 exits 1 even with output" rc_is 1

# T29: a string SKILLS would split into letters and skip nothing; it is refused
printf "SKILLS = 'extra'\n" > "$F/scripts/project-router.py"
H="$T/h21"; mkdir -p "$H"
RC=0; HOME="$H" "$F/scripts/install-skills.sh" --tool codex --apply extra > "$T/out.txt" 2>&1 || RC=$?
check "T29 a string SKILLS exits 1" rc_is 1
check "T29 a string SKILLS writes nothing" absent "$H/.agents"
check "T29 says why" out_has "cannot read SKILLS"

# T30: a BOM and mixed quotes still read every name (upstream's sed parse dropped the double-quoted one)
mkdir -p "$F/skills/aarons-latest/third"
printf -- '---\nname: third\ndescription: x\n---\n' > "$F/skills/aarons-latest/third/SKILL.md"
printf '\357\273\277SKILLS = (\n    %s, %s,\n)\n' "'workbetter'" '"extra"' > "$F/scripts/project-router.py"
H="$T/h22"; mkdir -p "$H"
RC=0; HOME="$H" "$F/scripts/install-skills.sh" --tool codex --apply workbetter extra third > "$T/out.txt" 2>&1 || RC=$?
check "T30 a BOM and mixed quotes read cleanly" rc_is 0
check "T30 the single-quoted name is skipped on Codex" out_has "SKIP    workbetter"
check "T30 the double-quoted name is skipped on Codex" out_has "SKIP    extra"
check "T30 a name outside SKILLS links on Codex" links_to "$H/.agents/skills/third" "$F/skills/aarons-latest/third"

# T31: a stray ast.py in the current directory is never imported (python3 -I)
mkdir -p "$T/planted"
printf 'open("%s", "w").write("x")\n' "$T/planted-marker" > "$T/planted/ast.py"
H="$T/h23"; mkdir -p "$H"
RC=0; (cd "$T/planted" && HOME="$H" "$INSTALL" --tool codex workbetter) > "$T/out.txt" 2>&1 || RC=$?
check "T31 a stray ast.py is not imported" absent "$T/planted-marker"
check "T31 the skip still works from that directory" out_has "managed by scripts/project-router.py"

# T32: SKILLS bound anywhere but a top-level tuple assignment fails closed (Python would read another list)
for shape in "plus-equals|SKILLS = ('workbetter',)\nSKILLS += ('extra',)\n" \
             "nested|SKILLS = ('workbetter',)\nif True:\n    SKILLS = ('extra',)\n" \
             "list|SKILLS = ['workbetter', 'extra']\n" \
             "del|SKILLS = ('workbetter',)\ndel SKILLS\n" \
             "import|SKILLS = ('workbetter',)\nfrom os import sep as SKILLS\n" \
             "def|SKILLS = ('workbetter',)\ndef SKILLS():\n    pass\n" \
             "dotted-import|SKILLS = ('workbetter',)\nimport SKILLS.sub\n"; do
    printf "${shape#*|}" > "$F/scripts/project-router.py"
    H="$T/h24"; rm -rf "$H"; mkdir -p "$H"
    RC=0; HOME="$H" "$F/scripts/install-skills.sh" --tool codex --apply extra > "$T/out.txt" 2>&1 || RC=$?
    check "T32 SKILLS ${shape%%|*} exits 1" rc_is 1
    check "T32 SKILLS ${shape%%|*} writes nothing" absent "$H/.agents"
done

echo "passed=$PASSES failed=$FAILS"
[[ "$FAILS" -eq 0 ]]
