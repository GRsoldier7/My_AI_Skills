---
name: wrapitup
description: |
  Close out a working session cleanly and produce a handoff another chat can pick up cold.
  Commits or stages outstanding work, verifies claims against real command output, writes or
  updates the project's dated plan document, saves memory, and prints a structured handoff
  summary. Use when the user says "wrap it up", "wrapitup", "wrap up this session", "let's
  close out", "summarize and hand off", "I'm taking this to another chat", "before we run out
  of context", "context is getting full", or when context use approaches roughly 60 percent
  during long multi-step work.
metadata:
  author: aaron-deyoung
  version: "1.1"
  domain-category: core
  adjacent-skills: wrapup, continuing-alm-work
  last-reviewed: "2026-09-27"
  review-trigger: "Change to the session memory contract in ~/.claude/CLAUDE.md (HANDOFF.md + Agent memory DB)"
---

# Wrap It Up

A session ends well when someone who was not here can resume it without asking questions.
That person may be a fresh chat with no memory of this one. Write for them.

## When to trigger

Explicitly on request, and proactively when context use nears **60 percent** during long work.
Do not wait to be asked at 90 percent: the wrap-up itself costs context, and a rushed handoff
is the one most likely to lose something.

## Procedure

Work through these in order. Do not skip a step because it seems obvious.

### 1. Stop expanding scope

No new features, no new refactors, no "while I'm here" fixes. If you find a problem now,
write it into the Next Steps section instead of solving it.

### 2. Establish what is actually true

Never summarize from memory of what you intended. Run the commands and read the output:

```bash
git status --porcelain
git log --oneline -10
git diff --stat
```

Re-run the project's tests and build. If something fails, that failure goes in the summary.
If you never ran them, say so plainly rather than implying they passed. Separate failures you
caused from failures that were already there, and prove which is which before claiming it.

### 3. Land the work

Stage and commit in coherent units with real messages, not one "wip" blob. Never commit
secrets; scan the diff for credentials before staging. If the user has not authorized a push,
commit locally and say so. Leave the tree clean, or explain exactly what is intentionally
left uncommitted and why.

### 4. Write the durable record

Update the project's dated plan document, following the project's documentation convention.
Mark what is done, what is in flight, and what is blocked. A plan that still describes
finished work as pending will mislead the next session.

**Append to the project's `HANDOFF.md`** (create it at the repo root if absent). This is the
append-only narrative log the next session reads first. Add a new dated entry directly under the
*Current state* section — never rewrite an older entry — and refresh *Current state* itself if the
branch, the blockers or the open decisions moved. Never put a secret, DSN, password or token in it.

Save anything non-obvious to memory: decisions and their reasons, environment facts discovered
the hard way, and traps that cost time. Do not save what the code or git history already says.

**Memory means the ADR-0034 `memory_vectors` Agent memory DB** — one table every project and
node reads, scoped by `project`. Write it with `hermes-mem` on agent-pve-01 (from Windows:
`ssh root@agent-pve-01 '/root/bin/hermes-mem write ...'`):

- `--project <kebab-project>` (reuse the name `hermes-mem projects` already lists),
  `--kind decision|state|lesson|note`, `--topics`, `--importance`, `--agent claude-code`.
- Always a stable `--ref-id <kind>:<project>:<slug>` — writes upsert by `ref_id`, so rewriting
  `state:<project>:current` keeps one up-to-date "latest state" row. The store has **no DELETE
  verb**; pick ref-ids once.
- Confirm with `hermes-mem recent --project <p> -n 3`.

Hermes/ATB only: curated files in `/root/hermes-deploy/lessons_learned/*` or
`self_healing/playbooks` also ingest via `hermes-memory-ingest.timer` (stamped `project=hermes`,
stem ≤ 80 chars, require `failed=0` in the ingest log). If the host is unreachable, list the
pending facts in `HANDOFF.md` and say so; never claim a DB write you did not make.

### 5. Print the handoff

Output this structure, in the chat, as the final message. It must stand alone: assume the
reader sees only this message and the repository.

```
## Session summary

**Goal:** what this session set out to do, in one sentence.

**Done:** each completed item, with the file or command that proves it.

**Verified:** what was actually run and what it returned. Name anything unverified.

**Not done / blocked:** what remains, and what is blocking it.

**Next steps:** ordered, concrete, each one startable without further discovery.

**Watch out for:** traps, pre-existing breakage, and anything that looks done but is not.

**Pick up here:** the exact file, command, or document the next session should open first.
```

## Rules

- Report outcomes faithfully. A tracker claiming completion that was never verified is worse
  than no tracker; it costs the next session a full audit to discover the lie.
- Distinguish "code written" from "actually works end to end". Say which one you achieved.
- Name real paths, commands, and identifiers. A next step that says "finish the integration"
  is not a next step.
- Keep the handoff short enough to read in one pass. Detail belongs in the plan document.
- Do not close out with an open question to the user unless it genuinely blocks all remaining
  work. Put decisions the user must make into Next Steps instead.

## Anti-patterns

| Tempting | Why it fails |
|---|---|
| "Everything works" without running anything | The most common way a handoff becomes a lie. |
| One giant commit named "updates" | The next session cannot bisect or review it. |
| Summarizing the conversation instead of the state | The next chat cannot read this conversation. |
| Leaving a half-finished edit unmentioned | It surfaces later as a mystery bug. |
| Starting one more task because it is small | Small tasks are how wrap-ups run out of context. |
