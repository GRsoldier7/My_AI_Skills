# Handoff — My_AI_Skills

Running session log for this repo. Newest entry first. Append; never rewrite history. No secrets.

## Current state (2026-09-28)

- Library: 180 skills. Repo and Windows global copies were identical on 2026-09-27.
- `continuing-alm-work` has 4 of its 17 files. It is blocked on `continuing-alm-work-v2.0.0.zip`, which is not on any reachable disk.
- SkillSpector gate (host `/root/bin/skill-scan`): the engine runs **stock `main`**. Tuning round 4 (`a0917a4`) is validated but not deployed; three review bypasses must be fixed first (see the 2026-09-28 entry).

## Log

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
