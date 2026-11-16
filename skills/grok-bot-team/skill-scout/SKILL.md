---
name: skill-scout
description: Use when a bot or skill gap needs the best public agent skill. Before drafting from scratch. When asked to pull best-of-the-best skills from public repos.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---

## Process

### 1. Define the Gap
Name the bot, the scorecard/history evidence, and the exact job the missing skill would do.

### 2. Diff the Existing Library First
Search to avoid duplicates. A close match means upgrade or reject, not a second skill.
- `/home/box/agent-data/workflows/`
- `/home/box/agent-os/skills/`
- `/workspace/My_AI_Skills` (including `skills/grok-bot-team/` and `skills/core/find-skills`)
- In-flight drafts: `/home/box/agent-os/proposals/skill-drafts-*/`

### 3. Search Sources (In Order)
1. Aaron's `My_AI_Skills`
2. `gh search repos --sort stars` with "claude skills", "agent skills", "SKILL.md", plus topic terms
3. `gh search code --filename SKILL.md` with topic terms
4. Canonical collections:
   - `anthropics/skills`
   - `obra/superpowers`
   - `vercel-labs/skills`
   - `VoltAgent/awesome-agent-skills` (MIT list; list is not a license for linked repos)
5. `skills.sh` leaderboard (install counts) as popularity signal only, never a license pass

### 4. Ranking Signals
GitHub stars, last push/recency, license, maintenance (recent commits, not a one-shot dump), source reputation (official orgs vs unknown), exact fit to the gap. Treat <100 stars with skepticism. Prefer a maintained mid-star licensed skill that fits over a famous skill that does not.

### 5. License Gate (Hard)
Adapt only: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, CC-BY (including CC-BY-4.0).
Skip: GPL, AGPL, copyleft.
No license or NOASSERTION: ideas only, no shared wording, record as skipped.
Cite URL, SPDX license, and star count in the draft and in `CREDITS.md`. Confirm license against the repo `LICENSE` file, not only the GitHub API.

### 6. Adapt-and-Scrub
Condense rewrite (do not vendor byte-identical unless the existing `My_AI_Skills` third-party vendor procedure applies and Aaron asks). Credit the source.
Run 8-gram overlap check (0 shared 8-grams, or quote with attribution).
Scrub secrets, contact details, internal ids/hosts, client/prospect names (`scripts/skill_scrub.py` + `scrub-denylist.txt`).
Apply `output-quality-no-slop` (and `scripts/slop_check.py`).
Never copy "install with -y" or auto-apply steps.

### 7. L1 Tests
Run on real past tasks from `runs/<bot>/history.jsonl` (and any saved deliverable).
Heavy work through `/home/box/agent-os/scripts/llm.sh`: OpenRouter :free models first, then Claude or OpenAI on their own keys.
Write assertions first. Prefer paired with-skill vs baseline, 2 runs/arm when budget allows.
Run `python3 scripts/quote_check.py` on any file with file quotes; `python3 scripts/slop_check.py` on prose drafts.
Record in `TEST-RESULTS.md`.

### 8. Ranked Proposal
Yes/no line per item (add vs upgrade, bot, gap, source+license+stars, test result).
Include `CREDITS.md`, `TEST-RESULTS.md`, and a search record in `proposals/skill-prior-art-<date>.md`.
Cap the set; do not pile thin skills. Rejected candidates get a one-line reason.

### 9. Hand-off
Stop. Nothing is applied.
On Aaron's explicit yes, hand to Foundry to apply exactly as tested, run `python3 scripts/no_regress.py check` and CI, commit, then `scripts/backup_skills.sh` (scrubbed) to `My_AI_Skills`.
Follow current repo-safety rules (PR flow, additive-only, run repo validators, update catalog).
Do not edit another bot's prompt, contract, or routine; that is Bot Optimizer / Foundry and needs a separate yes.

## Already in the Library
`find-skills` (vendored from `vercel-labs/skills`, MIT) installs from `skills.sh` for a human user. `skill-scout` is different: it vets, adapts, tests, and proposes for the bot-team library under L1. Do not replace `find-skills`.

## Anti-Slop
Every scout proposal and every adapted `SKILL.md` must follow `output-quality-no-slop`. Lead with the answer. No filler, no em dashes, no emoji.

## Guardrails
Drafts only. Never push to GitHub, never install a public skill onto Aaron's devices, never send or publish, never invent licenses or star counts. Mark unverified items `[VERIFY]`.

## Anti-Patterns
- Duplicate of an existing skill
- Adapting an unlicensed repo
- Installing with `-y`
- Applying before Aaron's explicit yes
- Skipping the library diff
- Treating `skills.sh` installs as a license pass

## Prior Art Credit
Adapted from: `vercel-labs/skills` (find-skills), MIT; `NVIDIA/skills` (nvidia-skill-finder) recommend-only / no install without explicit approval, CC-BY-4.0 AND Apache-2.0; `anthropics/skills` (skill-creator) eval method, Apache-2.0; `obra/superpowers` (writing-skills) lean TDD skill shape, MIT. Search, license gate, library diff, scrub, L1 tests, yes/no proposal, and Foundry hand-off are original to this team (AGENTS.md section 9 and the 2026-11-16 scout method).
