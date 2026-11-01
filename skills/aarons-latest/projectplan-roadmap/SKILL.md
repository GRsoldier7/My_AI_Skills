---
name: projectplan-roadmap
description: Use when a finished or approved plan (plan-mode file, chat plan, rescope or builder output) must be saved into the project as a durable, concise, highly prescriptive roadmap file using the YYYYMMDD - Project Name - Title.md naming convention. Triggers on "write this plan to the project", "save the plan", "save it as a roadmap", "put the plan in docs", "use the proper naming convention". Writes one planning file, verifies it, then stops. Not for creating a plan from scratch (projectplan-builder), revising one (projectplan-rescope), or executing one (workbetter).
metadata:
  author: Aaron
  version: "1.0.0"
  domain-category: aarons-latest
  last-reviewed: "2026-10-17"
---

# Project Plan Roadmap

Turn a plan that already exists into one file in the project that an executor can follow step by step without re-deriving anything. Write it, verify it, report the path, **stop**.

## Boundaries

- Authorizes writing **one planning file** (plus updating that same file later). Not code, not other docs, not commits, not deploys, not agent launches.
- The plan's content and decisions come from the source plan and the conversation. Do not add scope, tasks, or decisions the user didn't make. Mark planner choices as reversible.
- Never put secrets, tokens, DSNs, or personal identifiers beyond what the project already documents.
- If the project has its own instructions (AGENTS.md, CLAUDE.md) that say where plans go or how they're named, those win over this skill.

## Step 1 — Gather

1. Source plan: the plan-mode file, the latest plan in chat, or a file the user named. If several exist, use the newest approved one.
2. Project root and name. Read the README H1, AGENTS.md / CLAUDE.md title, or existing dated docs to learn the human-readable project name.
3. Existing plan folder and naming. Look for dated docs already in the project (for example under `docs/alm/`, `docs/plans/`, `docs/`). Match what is there.
4. Locked decisions, approvals, baseline plan, test baseline, and production constraints already stated in the session or the project docs.

## Step 2 — Name and place the file

**Naming convention (required):**

```text
YYYYMMDD - <Project Name> - <Title>.md
```

| Part | Rule | Example |
|---|---|---|
| `YYYYMMDD` | Today's local date, no separators | `20261017` |
| separators | Space, hyphen, space (` - `) exactly twice | |
| `<Project Name>` | Human-readable project name, Title Case, spaces not underscores. Reuse the exact spelling already used by the project's other dated docs | `Job Scraper` |
| `<Title>` | 3–7 words, Title Case, says what the plan delivers. Optional leading mode word: `Rescope`, `Roadmap`, `Plan`, `Spec`. No colons, slashes, quotes, or other characters illegal on Windows | `Owner Feedback Loop Roadmap` |
| H1 inside the file | Identical to the filename without `.md` | `# 20261017 - Job Scraper - Owner Feedback Loop Roadmap` |

**Placement, first match wins:**

1. A location the project's instructions name for plans.
2. The folder where dated plans with this convention already live (for example `docs/alm/`).
3. `docs/plans/`, if `docs/` exists.
4. `docs/`.

Never the repo root. If the same filename exists and it is the same plan, update it in place and add a changelog line. If it is a different plan, add ` v2` to the title.

## Step 3 — Write the roadmap

Use this section order. Drop a section only when it truly has no content. Keep it scannable: tables and numbered steps over prose.

```text
# YYYYMMDD - Project - Title
Header line: Date · Mode (PLAN | RESCOPE | UPDATE) · Status (proposed | approved YYYY-MM-DD | in progress)
Header line: Extends / Revises: <baseline docs, linked>. What is untouched.

1. Goal                one paragraph + success-metric table (metric | target | current)
2. Locked decisions    numbered, with who decided and when; then planner decisions marked reversible
3. Why                 evidence bullets with file:line or log references (the problem, not the solution)
4. Rules for executors numbered, project-specific: live/prod constraints, safe windows, test baseline,
                       reuse list (existing functions/utilities), approvals, handoff duty
5. Contracts           data schemas, file formats, formulas, interfaces the tasks share (code blocks)
6. Roadmap at a glance table: ID | Wave | Title | Main files | Depends | Approval | Status
                       + wave diagram showing serial lanes and safe parallelism
7. Task cards          one per ID (format below)
8. Side workstreams    optional (cleanup, org, docs) as a compact table: ID | Do | Approval
9. Release gate        checkbox list run after every wave
10. Risks              table: trigger | consequence | mitigation
11. End-to-end check   numbered steps proving the whole thing works
12. Next action        the first ready task as a paste-ready fenced instruction block
Changelog              dated lines
```

**Task card format (prescriptive, every card):**

```text
### <ID> · <Action-oriented title>
**Do**
1. Imperative step naming the exact file, function, and approximate line (~N).
2. ...
**Tests:** new or updated test files and what each asserts.
**Done when:** observable evidence (command output, log line, file state). Never "works".
**Don't / Stop if:** what is out of bounds; when to escalate.
**Approval:** only when needed (prod data, security config, first write of a new field, commits).
```

**Writing rules:**

- One idea per bullet. Imperative verbs. No hedging, no narrative of how the plan was made.
- Stable IDs in the project's existing scheme (for example `FB-01`). Never renumber surviving IDs.
- Status is separate from evidence: `not started | in progress | blocked | reported complete | verified complete`.
- Every task names its files. Every Done-when is checkable by someone who wasn't in the session.
- Approximate line numbers carry `~`. Function names must be exact.
- Link sibling docs with relative links; encode spaces as `%20`.
- Target length: as short as complete allows. Cut repetition between sections; reference instead.

## Step 4 — Verify before reporting

1. Grep every function, file, flag, and test file the roadmap names. Fix or mark `(new)` anything that doesn't exist yet.
2. Check the filename against the convention table, and that the H1 matches it.
3. Check every mandatory outcome from the source plan maps to at least one task ID.
4. Check the dependency order is acyclic and the "Next action" task has no unmet dependency.
5. Scan for secrets; there must be none.

## Step 5 — Report and stop

Reply with: the file path as a clickable link, one line naming the intended audience, the next ready task ID, and the approvals still pending. Then stop and wait. Do not start executing the roadmap. Do not commit unless the user asked.

## Common mistakes

| Mistake | Fix |
|---|---|
| Filename uses underscores, colons, or ISO dashes in the date | `YYYYMMDD - Project Name - Title.md` exactly |
| Plan saved to repo root or the tool's private plan folder only | Save inside the project per the placement rules |
| Task says "improve X" | Name file, function, change, and evidence |
| Re-explaining exploration findings | Keep evidence to the Why section with references |
| Inventing approvals or completion | Copy only what the user stated; everything else is `not started` |
| Starting implementation after saving | Stop after Step 5 |
