---
name: wrapup
description: |
  End-of-session wrap-up: summarizes the session, saves key memories to the operator file
  memory at /root/.claude/projects/-root/memory/, and updates the MEMORY.md index so a future
  session can find them.

  EXPLICIT TRIGGER on: "/wrapup", "wrap up", "end of session", "save this session",
  "session summary", "commit this to memory", "save what we did", "wrap this up",
  "before we close", "summarize our session", "end of day summary".

  Also activates when user says "I'm done for today", "let's call it here", "save everything
  we worked on", "I need to step away", or similar session-ending phrases.
metadata:
  author: aaron-deyoung
  version: "2.0"
  domain-category: core
  adjacent-skills: knowledge-management, project-memory-bootstrap
  last-reviewed: "2026-07-28"
  review-trigger: "Memory system format change, MEMORY.md index structure update"
allowed-tools: Bash Write Read Glob
---

## Purpose and Scope

Closes a session with four actions: review what happened, save memories (new and updated),
write a session summary document, and file the durable slice of that summary into the operator
file memory at `/root/.claude/projects/-root/memory/`.

Does NOT: write code, answer questions, or continue active work. This skill runs AFTER the
session's substantive work is complete. If there is more work to do, finish it first.

---

## Section 1 — Core Knowledge

### Key Principles

1. **Memory over recollection** — The goal is durable, cross-session context. Write memories
   so a future Claude with no conversation history can read them and act intelligently.
2. **Update, don't duplicate** — Always check MEMORY.md before creating a new file.
   Update an existing memory if it covers the same topic; create new only if genuinely new.
3. **Feedback memories are the most valuable** — User corrections and confirmed approaches
   prevent repeated mistakes. Capture both directions: what to avoid AND what worked.
4. **File memory plus the Hermes stack is the archive** — Operator memory files under
   `/root/.claude/projects/-root/memory/` (indexed by `MEMORY.md`) are the fast-access layer;
   the internal Hermes stack — Postgres/pgvector `memory_vectors` on pg-prime CT252,
   FalkorDB/Graphiti graph on CT253, Redis L0 — is the durable, searchable backbone.
   NotebookLM is not a memory layer, not a backup target, and not a recall source.
5. **Dates must be absolute** — Relative dates ("next Thursday") are meaningless in a week.
   Always convert to `YYYY-MM-DD` before saving.

### Memory Type Decision Framework

| What you learned | Memory type |
|-----------------|-------------|
| User's role, preferences, expertise level | `user` |
| Correction or confirmed approach | `feedback` |
| Active project, goal, deadline, decision | `project` |
| External system, tool, URL, location | `reference` |
| Code pattern, architecture, file paths | ❌ Skip — derivable from code |
| What was built this session | ❌ Skip — in git history |

---

## Section 2 — Advanced Patterns

### Pattern 1: High-Signal Memory Extraction
Don't save everything. Ask: "Would this help a future Claude session in a non-obvious way?"
- User corrected an assumption → `feedback` memory (high value)
- Project decision with a "why" → `project` memory (high value)
- User mentioned a deadline → `project` memory with absolute date (high value)
- User said "good job" → not a memory
- We wrote Python code → not a memory (code is in the repo)

### Pattern 2: Session Summary Structure
Keep summaries concise but complete. Future sessions grep these files, so consistent headers
are what let a search land on the exact section that matters:
```
# Session Summary — YYYY-MM-DD
## What We Did (bullet list)
## Decisions Made (bullet list with rationale)
## Key Learnings (non-obvious, experience-encoded)
## Open Threads (specific next steps, not vague)
## Tools & Systems Touched (list)
```

### Pattern 3: Memory Deduplication
Before writing any memory file, search MEMORY.md for overlap. If an entry covers the same
topic, read the existing file and update it — don't create a new one. Version bump the memory
file's content when significant new information is added.

---

## Section 3 — Standard Workflow

1. **Review the session:**
   - Read back through the full conversation
   - Identify: decisions made, work completed, user corrections, new preferences, open threads

2. **Save/update memories:**
   - Read `MEMORY.md` to check for existing entries to update
   - For each insight: choose type (user/feedback/project/reference), write file, update MEMORY.md index
   - Skip anything derivable from code, git, or external docs

3. **Write session summary:**
   ```bash
   # Check for same-day collision
   ls /tmp/session-summary-$(date +%Y-%m-%d)*.md 2>/dev/null
   # Write (append counter if collision: -2, -3, etc.)
   ```
   Use the 5-section format from Section 2 Pattern 2.

4. **File the durable slice into operator memory:**
   - Write one markdown file per fact into `/root/.claude/projects/-root/memory/`, named
     `<type>_<topic>.md` where `<type>` is one of `user`, `feedback`, `project`, `reference`
   - Frontmatter is YAML: `name`, `description`, and `metadata.type` (same four values),
     plus `created` / `updated` ISO stamps and `host` / `node` provenance
   - One fact per file — never bundle unrelated insights into a single memory
   - Append a one-line pointer to `MEMORY.md`:
     `- [Short Title](project_topic.md) — one-line gist of the fact`

5. **Confirm to user:**
   - N memories saved/updated (list which types)
   - Session summary written to `/tmp/session-summary-YYYY-MM-DD.md`
   - Open threads to pick up next time (1-3 bullets max)

---

## Section 4 — Edge Cases

**Edge Case 1: Multiple sessions same day**
Detection: `/tmp/session-summary-YYYY-MM-DD.md` already exists.
Mitigation: Append `-2`, `-3` to the summary filename. Durable facts still go to
`/root/.claude/projects/-root/memory/` one fact per file, as in every other run —
the suffix applies only to the `/tmp` summary.
Don't overwrite — earlier sessions are valid history.

**Edge Case 2: Session had nothing worth saving**
Detection: No decisions made, no corrections, no new preferences, trivial Q&A only.
Mitigation: Say so clearly. Don't manufacture memories. A short "nothing to save" message is
better than low-signal noise in the memory index.

**Edge Case 3: MEMORY.md index is near 200-line limit**
Detection: MEMORY.md has >180 lines.
Mitigation: Before adding new entries, prune stale project memories (completed projects,
outdated status). Consolidate related small memories into one file where possible.

---

## Section 5 — Anti-Patterns

**Anti-Pattern 1: Saving everything as a memory**
Temptation: The session was productive — save all of it for future reference.
Failure: Memory files become noise. Future Claude sessions have to read 20+ files to extract
1 relevant signal. High volume = low signal-to-noise = memory system fails at its purpose.
Instead: Apply the strict type filter from Section 1. If it's in the code or git log, skip it.

**Anti-Pattern 2: Creating duplicate memory files**
Temptation: The new info feels different enough to deserve its own file.
Failure: Two files covering the same topic produce conflicting signals. Future sessions see
both and don't know which is current.
Instead: Read MEMORY.md first. If an entry covers the same topic, update the existing file.

**Anti-Pattern 3: Sending session state to NotebookLM**
Temptation: NotebookLM is searchable and generates nice summaries — push the session log there
so it's "archived."
Failure: NotebookLM is not memory. Nothing in the stack reads from it, it carries no provenance
stamps, it does not dedup against MEMORY.md, and no future session recalls from it. State
written only to NotebookLM is state that quietly stops existing.
Instead: Write memory files under `/root/.claude/projects/-root/memory/` and update the
MEMORY.md index. NotebookLM produces human artifacts (podcast, briefing, deck) on explicit
request only — never as a persistence step.

**Anti-Pattern 4: Relative dates in memories**
Temptation: "Next Thursday" is clear right now.
Failure: Meaningless 3 days later. Memory files are read weeks or months after writing.
Instead: Always convert: "next Thursday" → "2026-04-09". Include context if helpful.

---

## Section 6 — Quality Gates

- [ ] MEMORY.md checked for duplicates before any new file is created
- [ ] Every memory file has correct frontmatter: `name`, `description`, `metadata.type` fields
- [ ] All relative dates in memories converted to `YYYY-MM-DD` absolute dates
- [ ] Session summary has all 5 sections and is saved to `/tmp/session-summary-YYYY-MM-DD.md`
- [ ] Every new memory file has a one-line pointer appended to `MEMORY.md`
- [ ] User confirmation message includes memory count and open threads

---

## Section 7 — Failure Modes and Fallbacks

**Failure 1: Memory write permission denied**
Detection: Write tool returns permission error on MEMORY.md or memory file.
Fallback: Write session summary to `/tmp/session-summary-YYYY-MM-DD.md` and print the
memory content as plain text in the response so the user can save it manually.

**Failure 2: Session was too large to review accurately**
Detection: Context window was compressed during session; early conversation is unavailable.
Fallback: Review from the most recent messages. Explicitly note in the session summary that
"earlier session context was unavailable due to compression." Focus on what is visible.

---

## Section 8 — Composability

**Hands off to:**
- `knowledge-management` — when the session produced content worth archiving in the vault

**Receives from:**
- Any skill — this is always the last skill in a session, not chained from specific skills
- `project-memory-bootstrap` — when setting up memory for a new project for the first time

---

## Section 9 — Improvement Candidates

- Memory health score: count memories by type and age, flag stale project memories
  (>30 days old) for review at wrap-up time
