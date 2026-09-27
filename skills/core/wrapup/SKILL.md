---
name: wrapup
description: |
  End-of-session wrap-up. Delegates to the wrapitup skill, which writes the project's HANDOFF.md
  and the Agent memory DB.

  EXPLICIT TRIGGER on: "/wrapup", "wrap up", "end of session", "save this session",
  "session summary", "commit this to memory", "save what we did", "wrap this up",
  "before we close", "summarize our session", "end of day summary".

  Also activates when user says "I'm done for today", "let's call it here", "save everything
  we worked on", "I need to step away", or similar session-ending phrases.
metadata:
  author: aaron-deyoung
  version: "3.0"
  domain-category: core
  adjacent-skills: wrapitup, continuing-alm-work
  last-reviewed: "2026-09-27"
  review-trigger: "Change to the session memory contract in ~/.claude/CLAUDE.md (HANDOFF.md + Agent memory DB)"
---

# Session Wrap-Up (delegates to `wrapitup`)

**This skill has no procedure of its own.** Invoke the **`wrapitup`** skill and follow it.

It appends a dated entry to the project's `HANDOFF.md` and writes durable facts to the ADR-0034
`memory_vectors` Agent memory DB so every other project can see this project's latest state.

See the "Session memory and handoff" section of `~/.claude/CLAUDE.md` for the full contract.
