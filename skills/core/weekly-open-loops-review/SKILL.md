---
name: weekly-open-loops-review
description: >-
  Use when running a weekly review of commitments: open loops, waiting-for
  items, stale threads, upcoming deadlines, and decisions not yet logged.
  Complements bot-team-review, which covers bot ownership.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Weekly Open Loops Review

Get clear, get current, get creative, in one short digest. Timebox it.

## Inputs
Where open loops live (memory, notes, task lists, decision log, waiting-for list), the past 7 and next 14 days of calendar (ask the calendar owner or the user if you don't run the calendar), and the stale threshold (default 14 days).

## Workflow
1. **Collect:** unchecked items, TODO/WAITING markers, threads with no follow-up, decisions not logged, items handed to others. Group as next actions, waiting-for, stale, and decisions to log.
2. **Mind sweep:** ask once whether anything is uncaptured.
3. **Triage each loop:** DO (owner, date), DELEGATE (who, chase date), DEFER (date), DROP. Propose; don't execute.
4. **Next actions:** mark done only on confirmation; every active project gets exactly one next action; flag projects with none.
5. **Past 7 days:** promised deliverables, unlogged decisions, missed commitments.
6. **Next 14 days:** add a prep action the day before each deadline; add waiting-for items where someone else delivers first.
7. **Waiting-for:** chase or drop anything stale; chase messages are drafts only.
8. **Decisions:** list unlogged decisions as drafts with owner and a one-line rationale.
9. **Health score:** 100 - 10 x stalled projects - 5 x overdue - 2 x stale waiting-for. 80+ healthy, 50-79 drifting, <50 overcommitted (recommend deferring about 30%). Report it honestly.

## Output
```
Weekly Open Loops - [date] | health ## - [verdict]
Top 3 this week | Overdue | Waiting-for (chase by) | Next 14 days | Decisions to log | Proposed drops
```
Keep it to one screen.

## Guardrails
- Never send, post, delete, archive, or purchase without explicit approval; chases are drafts.
- Never invent commitments, dates, or figures; mark [VERIFY].
- Don't mark items complete without confirmation. No external scripts or webhooks.

_Adapted from: alirezarezvani/claude-skills (weekly-review, decision-logger), MIT._
