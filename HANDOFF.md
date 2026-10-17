# Handoff — My_AI_Skills

Running session log for this repo. Newest entry first. Append; never rewrite history. No secrets.

## Current state (2026-10-17)

- Library: 191 skills in the master-orchestrator registry, regenerated 2026-10-17 from a complete Windows checkout. README and CLAUDE.md counts match it.
- Vendored mattpocock skills are all at `49dd158d1076134a641b33efb035946536778336` (to-spec is identical at that commit): `setup-matt-pocock-skills`, `to-spec`, `to-tickets`, `domain-modeling` in `skills/engineering/`; `grill-me`, `grilling`, `grill-with-docs`, `teach` in `skills/aarons-latest/`. Provenance and scan results: `platform-configs/skill-sets/README.md`.
- `scripts/install-skills.sh` skips only the project-router skills on the Codex side (read from `SKILLS` in `scripts/project-router.py`); other `skills/aarons-latest/*` install for both tools. Test suite: 56/57 on Windows under `MSYS=winsymlinks:nativestrict`; T14 (relative link survives `--prune`) fails on Windows with the unmodified installer too, a pre-existing MSYS `readlink` difference, untested on Linux since 2026-10-03.
- Windows device (this machine): global set plus `domain-modeling`, `grill-me`, `grilling`, `grill-with-docs`, `teach` linked for Claude Code and Codex. Other devices: `git pull`, then `./scripts/install-skills.sh --apply` and `./scripts/install-skills.sh --apply domain-modeling grill-me grilling grill-with-docs teach`.
- `scripts/lint-skills.py`, `scripts/validate-skills.sh` and `scripts/generate-skill-registry.py` run from any clone location and on Windows (hardcoded `/root/My_AI_Skills` paths and a CRLF trap removed 2026-10-17).
- SkillSpector gate (host `/root/bin/skill-scan`): rounds 1-5 last verified 2026-09-28; current host state not rechecked.
- `continuing-alm-work` is the owner's nine-file v2.0.0 package (2026-09-30).

## Log

### 2026-10-17 — Vendor mattpocock grill-me + grilling into aarons-latest

**Done**
- Vendored `grill-me` and `grilling` byte-identical from mattpocock/skills @ `49dd158d1076134a641b33efb035946536778336` (`skills/productivity/*`) into `skills/aarons-latest/`, each with the upstream MIT `LICENSE`. `grill-me` is a one-line wrapper that calls `grilling`, so both are required.
- Placed in `aarons-latest` at the owner's request (not `engineering/` like the 2026-10-03 vendored set). `scripts/project-router.py` uses a fixed seven-skill list, so the Codex/ChatGPT plugin build is unaffected. Added both to `vendored_paths`; updated the catalog README, the aarons-latest README and the skill-sets provenance table.
- Installed on the Windows device: `./scripts/install-skills.sh --tool claude --apply grill-me grilling` made real symlinks in `~/.claude/skills` (run under `MSYS=winsymlinks:nativestrict`; PowerShell reports `SymbolicLink`). Claude Code listed `grilling` live in the same session.
- Fixed two Windows-only gate bugs found while validating: `scripts/validate-skills.sh` now strips CR from the `python3` pattern list (the Store python3 writes CRLF to pipes, so every `vendored_paths` entry but the last carried a `` and never matched); `scripts/lint-skills.py` derives `REPO_DIR` from its own location instead of the hardcoded `/root/My_AI_Skills`, and resolves `--files` paths before `relative_to`. Neither changes results on the homelab.

- Same session, second commit: vendored `grill-with-docs` (same upstream commit, `skills/engineering/grill-with-docs`) into `aarons-latest`. It calls `grilling` and `domain-modeling`; `domain-modeling` (vendored 2026-10-03 at `c55ee46`) was not installed on the Windows device, so it was linked at the same time.
- Re-synced `skills/engineering/domain-modeling` from `c55ee46` to `49dd158d` (byte-identical; upstream renamed `CONTEXT.md`/`CONTEXT-FORMAT.md` to `GLOSSARY.md`/`GLOSSARY-FORMAT.md`). Needed because `grill-with-docs` at `49dd158d` pairs with that version. `setup-matt-pocock-skills` stays at `c55ee46`; see Open.
- Vendored `teach` (`skills/productivity/teach`, 6 files, SAFE 0/100) into `aarons-latest` at the owner's request. Standalone; manual `/teach <topic>`.
- Third commit (loose ends, owner-requested): re-synced `setup-matt-pocock-skills` (7 files, SAFE 0/100) and `to-tickets` (2 files, CAUTION 25/100, same TM2 false positive as 2026-10-03) to `49dd158d`, so no vendored mattpocock skill mentions `CONTEXT.md` any more; `to-spec` is unchanged upstream. `scripts/install-skills.sh` now skips only the project-router skills on the Codex side (read from `SKILLS` in `scripts/project-router.py`) instead of all of `skills/aarons-latest/*`, so the vendored grill/teach skills install for Codex too (new test T22). `scripts/generate-skill-registry.py` lost its hardcoded `/root/My_AI_Skills` paths and the registry was regenerated from this complete checkout. README and CLAUDE.md skill counts now match the registry total. This Windows device also got the global set and the new skills linked for Codex.

**Verified**
- All vendored files match upstream sha256 (grill-me 3, grilling 3, grill-with-docs 3, teach 7, domain-modeling 5). grill-with-docs and teach SAFE 0/100. SkillSpector static: grill-me SAFE 0/100; grilling SAFE 10/100, one EA2 finding reviewed as a false positive (fact-finding prose; the skill requires user confirmation before acting).

**Open**
- Not added to `platform-configs/skill-sets/global.txt`; `grilling` is model-invocable and would cost context in every session. Install per device: `./scripts/install-skills.sh --apply grill-me grilling`.

### 2026-10-14 — homelab-organizer class-C fixes merged; 14 skill descriptions trimmed

**Done**
- Fast-forwarded local `main` to `origin/main` (`418f6f7`), then merged `fix/organizer-class-c` (`e675d1c`; brings in `dbd1bba` plus six class-C commits). The scanners no longer hide stale files, and quarantine moves the right file. `restore.sh` restores the exact entry, never overwrites, validates entry structure, rejects malformed paths and closes the `--by-original` traversal. `quarantine.sh` never overwrites an archived copy. The audit-procedure schemas are pinned to what the scripts emit.
- Trimmed 14 SKILL.md descriptions to a one-line purpose plus trigger phrases (`af86682`; 13,466 bytes smaller across the 14 files). `notebooklm` keeps upstream's artifacts-only rewrite, and only its description differs. Registry regenerated; exactly the 14 rows changed.

**Verified**
- `test_scanners.py` 61/61 on merged `main`. The merge tree is identical to a `git merge-tree` dry run taken before merging.
- Lint: the 14 files FAIL 0 / WARN 13. Full repo FAIL 5 / WARN 73, the same FAIL set as the `418f6f7` baseline.
- Review: codex returned HTTP 400 (model not available on this account), so no codex review ran. Sonnet and Fable review of the organizer changes is recorded in the owner's 2026-10-14 audit notes.

**Open**
- Push to origin is pending. It needs the owner's go-ahead after a scan of the unpushed commits for homelab IPs and hostnames.
- The installed `.git/hooks/pre-commit` only regenerates the registry. The lint hook in `scripts/git-pre-commit-hook.sh` is not installed, so staged SKILL.md files are not linted at commit time.
- `fix/homelab-organizer-scanners` and `fix/organizer-class-c` are merged but not deleted, and the class-C worktree still exists.

### 2026-10-03 — Cross-tool skill sets and four vendored third-party skills

**Done**
- Accounted for every candidate in the two 2026-09-26 skill-rating reports (about 60 skills and agents from mattpocock/skills, davidondrej/skills, affaan-m/ECC and msitarzewski/agency-agents): 4 vendored, the rest listed as reference or excluded with reasons in `platform-configs/skill-sets/README.md`.
- Vendored `to-spec`, `to-tickets`, `setup-matt-pocock-skills` and `domain-modeling` byte-identical from mattpocock/skills @ `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`, each with the upstream MIT `LICENSE`; added them to `vendored_paths`.
- Added `scripts/install-skills.sh` (dry run by default; symlinks a set into `~/.claude/skills` and `~/.agents/skills`; never replaces real directories or foreign links; skips `skills/aarons-latest/*` on the Codex side) with `scripts/test-install-skills.sh`, and the global set `platform-configs/skill-sets/global.txt`. It does not list `skills/aarons-latest/*`, which `scripts/project-router.py` installs for Codex.
- `scripts/validate-skills.sh` now skips house-convention checks for `vendored_paths`; `scripts/lint-skills.py` allowlists the tracker's triage labels. README's Quick Start and Claude Code section now use `install-skills.sh` (the old "register all skills" path is labelled legacy, and the misspelled clone URL is fixed); its Codex section no longer says Codex has no native skills.

**Verified**
- 15/15 vendored files match upstream sha256. Security scan: ALLOW ×3 (2/100); `to-tickets` NOTIFY 27/100, findings reviewed as false positives (details in the guide).
- Installer tests 55/55 (after Gate 1 and Gate 2 fixes); sabotaging any guard (no-clobber, Codex owner-skill skip, skip count, argument checks, `..`, `skills/` prefix, `./` normalisation, unset HOME, dangling and stale-link notes) fails its test. Both installers coexist in a temp home (each skips the other's skills; re-runs are idempotent).
- Validator FAIL 177 → 1 after exempting the 110 `vendored_paths` skills from house-style checks (a narrower gate, not a quality gain; all 110 trace to third-party import commits). The remaining FAIL is `clean-project`'s missing metadata, owner-authored, correctly not exempted. Lint findings identical to the `b9446a0` baseline (FAIL 5, WARN 73). `test-phantom-refs.py` 25/17/0.

**Open**
- Committed and merged to `main` on Aaron's homelab clone; **push to origin pending** (that host has no GitHub push credentials). Applied there on 2026-10-03: Claude Code lists all four skills in a fresh session; Codex lists `domain-modeling` (the three manual-only skills are not in its implicit list by design; explicit `$name` use not yet tested). Other devices: run the setup in `platform-configs/skill-sets/README.md` after the push.
- The master-orchestrator registry was regenerated on 2026-10-03 (187 skills, library-wide refresh per `AGENTS.md`). Windows junction steps are untested. Claude Code distribution of `skills/aarons-latest/*` is still per-device.

### 2026-09-30 — Replace the incomplete continuing-alm-work package

**Done**
- Replaced the four-file copy with the owner-supplied nine-file `continuing-alm-work-v2.0.0.zip` (SHA-256 `de9d4b74c909b2d0dca6166071f06852c9a046b9c511e61875a28927ba2f36a1`). Removed obsolete `TRACEABILITY.md`; added the new changelog, four references, validator, and evaluation cases.
- Added the repository's required category and review metadata without changing the supplied workflow body. Updated the README catalog entry and regenerated the master-orchestrator registry.

**Verified**
- ZIP integrity passed. The package validator reports `VALID` for nine files and 15 evaluation cases. Focused repository lint reports zero findings; category validation reports zero failures and 17 non-blocking warnings, including warnings in other skills.
- GitHub publication and live behavioral evaluation are separate from these local checks.

**Open**
- Windows global skill copies were not synchronized or checked in this update. The 15 evaluation cases have not been run as behavioral comparisons.

### 2026-09-28 (evening) — SkillSpector tuning round 5 built, reviewed, deployed to the gate

**Done**
- Round 5, Windows commit `f19e121` on `aaron/fp-tuning` in `~/.claude/tools/skillspector`. It closes the three bypasses from Fable's round-4 review and adds that review's follow-ups. Each bypass line is now a regression test that fails on round 4.
- A second Fable review of round 5 said deploy. Its three small consistency items were taken before the commit.
- Deployed rounds 4+5 to the host gate engine with `/root/.cache/skillspector-deploy-tuning.sh`, after a dry run in a detached worktree. Do not re-run the script: its patches are already on the branch.
- Updated the gate doc status (`/root/.claude/skills/skill-scan/SKILL.md`, uncommitted in `/root` like the earlier edits), `/skillspector` v1.5.0, DB row `decision:hermes:skillspector-fp-tuning`, and a new lesson `lesson:hermes:census-exemption-before-tightening`.

**Verified**
- `pytest -q`: 777 passed on Windows and on the host. Ruff clean.
- 313 third-party skills: identical to round 4 on every skill (stock BLOCK 83, round 5 BLOCK 1); no escalation fires.
- `redteam_ext` (45 independent): none below stock; stock BLOCK 12, round 5 BLOCK 21. The same numbers through the real `skill-scan` wrapper before and after the switch.
- Deploy script gates: own red team and `benign_noisy` ok; `test_skill_scan.sh` 31/31 on the live engine.

**Open**
- 13 of the 45 still score ALLOW on stock and tuned; static rules do not see them. Adding an LLM triage pass is an owner decision. Measure it together with the other session's re-score before stacking them.
- `continuing-alm-work-v2.0.0.zip` is still missing (see Current state).

### 2026-09-28 — Round 3 overfit and rolled back; round 4 built and reviewed, not deployed; Fable follow-ups applied

**Done**
- Applied Fable's follow-ups on the host (owner: "apply them"). Backups are in `/root/.cache/*.bak-20260927` and `*.bak-20260928`.
  - `agents/security-auditor.md` lines 27 and 37 now say "(scope: `skill-scan` §Scope)".
  - `CLAUDE.md` §DELEGATE now says "(third-party; scope in `skill-scan` §Scope)".
  - Superseded the stale host memory notes: `skillspector-fp-tuning-2026-09-27.md`, `feedback-owner-authored-skills-skip-security-scan.md`, and index lines 7 and 28. Ingest reported `failed=0`.
  - `standing-directive.md` is unchanged. It only routes installs to security-auditor, which now carries the scope.
- Found a security regression in the tuning and rolled the gate back.
  - An independent red team showed that round 3 let 7 attacks that stock BLOCKs fall to NOTIFY or ALLOW. The red team is 45 inert fixtures that the rev-1–3 session left on tmpfs.
  - Cause: counting each rule once caps a single blatant HIGH at 25 points. Examples: `rm -rf --no-preserve-root /` in an executed script, hidden zero-width text, `curl http://… | sh`.
  - The host engine went back to stock `main` at about 21:00 CDT on 2026-09-27. `test_skill_scan.sh` passed 31/31 on stock.
- Built round 4: commit `a0917a4`, local branch `aaron/fp-tuning` in `~/.claude/tools/skillspector`.
  - Blatant attack syntax in live files (code, SKILL.md, files it names) is escalated to CRITICAL.
  - Detection fixes: hidden files, PE3 inside code fences, deletes of credential stores, bidi and tag characters, a secrets-to-remote phrase, exec role for `package.json`/`hooks.json`/`.mcp.json`, and example hosts anchored to the end of the host.
  - The 45 fixtures are now `tests/fixtures/redteam_ext`, with a test that none scores below stock.
- Corrected the docs to the true state: the host gate doc's engine section (status: stock) and the Windows `/skillspector` doc (v1.4.0). Corrected DB row `decision:hermes:skillspector-fp-tuning`, which had claimed the tuned branch was live.

**Verified**
- `pytest -q`: 762 passed (Windows). Ruff clean. Secret scan of the diff: clean.
- `redteam_ext`: none below stock; stock BLOCKs 12, round 4 BLOCKs 21. `redteam`: 17/17 BLOCK. `benign_noisy`: 0 BLOCK.
- 313 third-party skills: stock BLOCKs 83, round 4 BLOCKs 1 (268 ALLOW, 44 NOTIFY). No escalation fires on any of them.
- The round-4 patch applies cleanly to the host's `aaron/fp-tuning` (checked in a throwaway worktree). The live engine is untouched: `main @ a5092dd`, clean.

**Open**
- Fable's round-4 review (`/root/.cache/skillspector-r4-review-20260928.md`) found three bypasses of the new exemptions. None scores below stock, but each defeats the escalation:
  1. a closed quote or `#` earlier on the line;
  2. a U+1F3F4 prefix that hides a tag-character run;
  3. GET or httpx sends that the send check misses.
- Next: fix all three as round 5 (item 1 has exact code in the review). Rerun the suite and the corpus. Then deploy both patches with `bash /root/.cache/skillspector-deploy-tuning.sh <r4.patch> <r5.patch>`.
- 13 of the 45 fixtures score ALLOW on both stock and tuned, which static rules cannot see. Whether to add an LLM triage pass is back with the owner.
- `continuing-alm-work-v2.0.0.zip` is still missing. This time also searched all of `C:\Users\Admin` and `agents/TEMP`, which holds only `context-checkpoint-skill-v1.0.0.zip`.

### 2026-09-27 (later) — Gate doc per Fable, stricter tuning invariant, scan time limit; caw zip still missing

**Done**
- The owner ordered "follow Fable's recommendations" for the host gate doc, and Fable (read-only review) wrote the text. Applied verbatim to `/root/workspace/claude-skills/skill-scan/SKILL.md`:
  - a provenance-scoped **Scope** section: owner-authored means his repo remote **and** not in `vendored_paths`, or his own in-session hand-over; vendored third-party packs stay scanned; the wrapper keeps no exemption path;
  - a fail-closed time-limit bullet and paragraph;
  - an engine-branch section.
  - Only measured figures were filled in. Backup: `/root/.cache/skill-scan-SKILL.md.bak-20260927`.
- SkillSpector round 3 (`27afe8d` Windows, `e20c601` host) adopts Fable's invariant. In SKILL.md and the files it names, only agency-language rules can be discounted as negated, never attack syntax, which closes the "Do not skip: `rm -rf ~`" evasion. Tool-misuse rules on one line now count once.
- `/root/bin/skill-scan` gained a scan time limit: `SKILL_SCAN_TIMEOUT_SECS`, default 600, 1-7200, invalid values fall back to the default, and rc 124 means BLOCK. 5 new gate tests. Backups: `/root/.cache/skill-scan.bak-20260927` and `test_skill_scan.sh.bak-20260927`.
- The Windows `/skillspector` skill (v1.3.0) carries Fable's scope note and the current figures; the literal payload strings were removed from its own text.

**Verified**
- On 313 third-party skills, stock BLOCKed 83 and tuned BLOCKs 1: plugin-dev `hook-development`, where a linked reference feeds a destructive-command string to a validator test; that is left for operator review. Tuned: 269 ALLOW, 43 NOTIFY, none higher than stock.
- `pytest -q`: 689 passed on Windows and on the host. `test_skill_scan.sh`: 31/31.
- The production gate on the host, run on the fixtures:
  - 17/17 red-team → BLOCK (rc 2); the unlinked-README payload → NOTIFY by design.
  - 15 benign → 10 ALLOW, 5 NOTIFY, 0 BLOCK.

**Open**
- `continuing-alm-work-v2.0.0.zip` (SHA-256 `97bced21…`, 36,588 bytes) is not on disk. Searched `%TEMP%`, `C:\temp`, `C:\tmp`, OneDriveTemp, Downloads, Desktop, `Z:`/NAS, `G:`, `S:` and the host's `/root/.cache/TEMP` (which holds only `context-checkpoint`). The build report shows it was made in a remote sandbox (`/mnt/data/...`). The owner needs to download it again or give the path.
- Fable's follow-ups for the owner (not applied):
  - add "(scope: `skill-scan` §Scope)" to `/root/.claude/agents/security-auditor.md` lines 27/37 and to `/root/.claude/CLAUDE.md` §5;
  - supersede the stale host memory row `skillspector-fp-tuning-2026-09-27.md`, which still says no live change was made.

### 2026-09-27 — Library synced to the Windows global skill dir; NotebookLM artifacts-only; SkillSpector gate tuned

**Done**
- Synced every repo skill into `~/.claude/skills/` on the Windows workstation, starting from `main` at `6c5778c` (which added `directory-cleanup` and `projectplan-builder/rescope`).
  - 103 were installed new, including the directory skills `directory-cleanup` and `homelab-organizer`; 34 stale copies were updated.
  - Backups are in `~/.claude/backups/skills-pre-sync-20260927/` and `skills-pre-resync-20260927/`.
- This commit brings the repo in line with the global copies:
  - `notebooklm` 4.1 is artifacts-only. Another session restored it globally at 17:00 as explicit-request artifact generation, never memory.
  - `scripts/sync-notebooklm.sh` is removed.
  - `wrapup` 3.0 delegates to `wrapitup`, and `wrapitup` is added: owner-authored, but previously installed only globally.
  - NotebookLM-as-memory lines are dropped from `homelab-organizer`, `ai-business-optimizer` and `entrepreneurial-os`.
  - Registry regenerated (176 → 180). README "Aaron's Latest Skills" now lists all 4 skills in that category.
- Tuned SkillSpector: branch `aaron/fp-tuning` (`69b2256` + `316ebdd`) in `~/.claude/tools/skillspector` **and** in the host gate engine `/root/.cache/agent-repos/SkillSpector`, which is used by `/root/bin/skill-scan`.
  - On 314 installed third-party skills, stock BLOCKs 84 and tuned BLOCKs 0 (269 ALLOW, 45 NOTIFY). No skill scores higher than stock.
  - The `/skillspector` skill (v1.2.0) documents the rules.
- Correction to the 2026-09-26 entry: the host has no `/root/My_AI_Skills` clone any more, so there is nothing to pull there.

**Verified**
- Repo vs global: 180/180 identical. Lint: 0 FAIL (the 4 WARNs are old `last-reviewed` dates on files that only lost a NotebookLM line).
- SkillSpector `pytest -q`: 687 passed on Windows and on the host. Host gate suite `test_skill_scan.sh`: 26/26 before and after the change.
- The production gate on the host was run on the new regression fixtures:
  - All 17 red-team skills → BLOCK (exit 2). One payload that exists only in an unlinked README → NOTIFY, by design.
  - All 15 benign-but-noisy skills → 11 ALLOW, 4 NOTIFY, 0 BLOCK.

**Open**
- `continuing-alm-work` still has only 4 of its 17 files; it needs `continuing-alm-work-v2.0.0.zip` (see the 2026-09-26 entry).
- The host gate doc `/root/workspace/claude-skills/skill-scan/SKILL.md` was **not** edited. The auto-mode classifier denied adding the owner rule ("never scan the owner's own skills") and the engine-tuning notes to a security gate's instructions. The owner decides whether to add them. The unmodified backup is at `/root/.cache/skill-scan-SKILL.md.bak-20260927`.
- `skill-scan` has no scan timeout. A 1.4 GB monorepo (the `gstack` root) scans for many minutes. Optional hardening: wrap the scanner call in `timeout` (rc 124 already fails closed).
- The tuning exists only as local branches on the two machines; NVIDIA upstream is not pushable. After an upstream pull, rebase and rerun both suites (steps in `/skillspector`).

### 2026-09-26 — `continuing-alm-work` v2.0.0 added under new "Aaron's Latest Skills" category

**Done**
- New category `skills/aarons-latest/`, listed first in the README Skill Catalog as "Aaron's Latest Skills", plus a repo-tree entry and a category-guide line.
- `skills/aarons-latest/continuing-alm-work/`: `SKILL.md`, `README.md`, `TRACEABILITY.md`, `evals/evals.json` from the v2.0.0 package.
- `SKILL.md` metadata gained `domain-category: aarons-latest` and `last-reviewed: "2026-09-26"`, the two fields `lint-skills.py` requires. Body unchanged.
- `generate-skill-registry.py` maps `aarons-latest` to "Aaron's Latest Skills"; the master-orchestrator registry was regenerated (175 → 176 skills).
- The same copy is installed globally on the Windows workstation at `~/.claude/skills/continuing-alm-work/`.

**Verified**
- `lint-skills.py` on the new `SKILL.md`: 0 findings. `validate-skills.sh --category aarons-latest`: passed, 5 WARN (review-trigger, adjacent-skills, anti-patterns, failure modes, composability).
- Full-library lint: 3 FAIL, all pre-existing phantom-refs in vendored `ce-compound` and `git-commit-push-pr`. None on files touched here.
- SkillSpector static scan: 10/100, LOW, SAFE. Its one finding (RA2) is the README's `unzip` install line, a false positive.

**Open**
- The package is incomplete. Only 4 of the 17 files in `continuing-alm-work-v2.0.0.zip` were provided. Missing: `CHANGELOG.md`, `MAINTENANCE.md`, `assets/execution-state-template.md`, `references/` (`state-and-evidence.md`, `execution-routing.md`, `verification-and-safety.md`, `checkpoints-and-skill-candidates.md`), `scripts/` (`capture_project_state.py`, `validate_package.py`), `evals/README.md`, and `tests/` (3 files). `SKILL.md` links to the references, the template and the capture script, so until they land the skill runs on its built-in fallbacks.
- To complete it: get the zip and check its SHA-256 against the build report (`97bced219108d78674d34feed82ede0329cac76c8546b2a341d70058d2efeaa2`). Scan `scripts/` with SkillSpector, because `allowed-tools` pre-approves `capture_project_state.py`. Extract over both copies, then re-add the two metadata lines, since the zip's `SKILL.md` lacks them. Run `python -m unittest discover -s tests` inside the skill folder, then commit.
- The host clone (`/root/My_AI_Skills`) needs a `git pull` to pick this up.
