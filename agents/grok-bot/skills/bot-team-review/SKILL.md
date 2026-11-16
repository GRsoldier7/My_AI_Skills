---
name: bot-team-review
description: >-
  Use when asked to review, audit, or check in on a team of Grok Bots: inspect
  each bot's purpose and recent work, catch duplicate ownership or gaps, and
  propose changes for approval.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Bot team review

Purpose: keep a multi-bot team clear, non-overlapping, and high value. Read-only until the owner approves a change.

## Steps
1. **List the team.** Read every teammate bot's name and description, plus any new bots since the last review.
2. **Check recent work.** Skim each bot's recent transcript: what it was asked to do, what it delivered, and anything stuck, repeated, or waiting on the owner.
3. **Check ownership.** Compare the work against the team's routing plan (the saved plan page or memory). Flag:
   - work done by a bot outside its lane
   - two bots covering the same thing
   - work that has no owner
   - a bot that has gone idle
4. **Check open loops.** Collect the top open items across the team (deadlines, blocked approvals, alerts), ranked by urgency and by the owner's stated priorities.
5. **Propose, don't apply.** Write a short list of recommended changes (keep, rename, re-scope, combine, add, pause), each with its reason and risk. Prefer additive, reversible changes. Never delete or rewrite a bot without explicit approval.
6. **Report.** Give the owner a brief summary: team health in one or two lines, the top open loops, and the proposed changes as a one-tap approval question. If nothing changed and nothing needs attention, say so in one line.
7. **After approval.** Apply only the approved changes, update the routing plan page, and record what changed and why in memory.
