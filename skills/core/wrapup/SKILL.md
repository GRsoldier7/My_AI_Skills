---
name: wrapup
description: |
  End-of-session wrap-up: summarizes the session, saves key memories to persistent memory
  files, and pushes a session log to the user's AI Brain NotebookLM notebook for long-term
  searchable history.

  EXPLICIT TRIGGER on: "/wrapup", "wrap up", "end of session", "save this session",
  "session summary", "commit this to memory", "save what we did", "wrap this up",
  "before we close", "summarize our session", "end of day summary".

  Also activates when user says "I'm done for today", "let's call it here", "save everything
  we worked on", "I need to step away", or similar session-ending phrases.
metadata:
  author: aaron-deyoung
  version: "2.0"
  domain-category: core
  adjacent-skills: notebooklm, knowledge-management, project-memory-bootstrap
  last-reviewed: "2026-04-03"
  review-trigger: "Memory system format change, NotebookLM CLI auth flow changes, MEMORY.md index structure update"
allowed-tools: Bash Write Read Glob
---

## Purpose and Scope

Closes a session with four actions: review what happened, save memories (new and updated),
write a session summary document, and push that summary to the AI Brain NotebookLM notebook.

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
4. **AI Brain notebook is the long-term archive** — Local memory files are the fast-access
   layer; NotebookLM is the searchable, queryable, generatable archive. Both matter.
5. **Dates must be absolute** — Relative dates ("next Thursday") are meaningless in a week.
   Always convert to `YYYY-MM-DD` before saving.
6. **NotebookLM failure is non-fatal** — If auth is expired or CLI is unavailable, save
   memories locally and skip the push. Never block the wrap-up on NotebookLM.

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

### Pattern 1: AI Brain Notebook Discovery Without Saved ID
If no `reference_brain_notebook.md` memory exists:
```bash
notebooklm list --json
```
Parse output for a notebook titled "AI Brain" or "[Name]'s AI Brain". If found, save the ID
as a reference memory. If not found, ask user permission, then create it. Always save the ID
to memory — this check should only run once.

### Pattern 2: High-Signal Memory Extraction
Don't save everything. Ask: "Would this help a future Claude session in a non-obvious way?"
- User corrected an assumption → `feedback` memory (high value)
- Project decision with a "why" → `project` memory (high value)
- User mentioned a deadline → `project` memory with absolute date (high value)
- User said "good job" → not a memory
- We wrote Python code → not a memory (code is in the repo)

### Pattern 3: Session Summary Structure
Keep summaries concise but complete. The AI Brain notebook query interface works best with
well-structured content. Use consistent headers so future queries can target specific sections:
```
# Session Summary — YYYY-MM-DD
## What We Did (bullet list)
## Decisions Made (bullet list with rationale)
## Key Learnings (non-obvious, experience-encoded)
## Open Threads (specific next steps, not vague)
## Tools & Systems Touched (list)
```

### Pattern 4: Memory Deduplication
Before writing any memory file, search MEMORY.md for overlap. If an entry covers the same
topic, read the existing file and update it — don't create a new one. Version bump the memory
file's content when significant new information is added.

---

## Section 3 — Standard Workflow

1. **Ensure AI Brain notebook exists:**
   - Check memory index for `reference_brain_notebook.md`
   - If missing: `notebooklm list --json` → find or create AI Brain notebook → save ID to memory
   - If notebook ID saved: verify with `notebooklm list --json` (notebook may have been deleted)

2. **Review the session:**
   - Read back through the full conversation
   - Identify: decisions made, work completed, user corrections, new preferences, open threads

3. **Save/update memories:**
   - Read `MEMORY.md` to check for existing entries to update
   - For each insight: choose type (user/feedback/project/reference), write file, update MEMORY.md index
   - Skip anything derivable from code, git, or external docs

4. **Write session summary:**
   ```bash
   # Check for same-day collision
   ls /tmp/session-summary-$(date +%Y-%m-%d)*.md 2>/dev/null
   # Write (append counter if collision: -2, -3, etc.)
   ```
   Use the 5-section format from Section 2 Pattern 3.

5. **Push to AI Brain:**
   ```bash
   export PATH="$HOME/bin:$PATH"
   notebooklm use <BRAIN_NOTEBOOK_ID>
   notebooklm source add /tmp/session-summary-YYYY-MM-DD.md
   ```
   If CLI unavailable: `~/.notebooklm-venv/bin/notebooklm source add ...`

6. **Confirm to user:**
   - N memories saved/updated (list which types)
   - Session summary pushed to AI Brain (or skipped with reason)
   - Open threads to pick up next time (1-3 bullets max)

---

## Section 4 — Edge Cases

**Edge Case 1: NotebookLM auth expired mid-session**
Detection: `notebooklm auth check` shows SID missing.
Mitigation: Skip the push entirely. Save memories locally. Tell user auth has expired and
to run `notebooklm login` before the next session. Don't block wrap-up on this.

**Edge Case 2: AI Brain notebook was deleted**
Detection: `notebooklm list --json` shows the saved ID no longer exists.
Mitigation: Create a new notebook (`notebooklm create "[Name]'s AI Brain" --json`), save
the new ID to `reference_brain_notebook.md`, update MEMORY.md index.

**Edge Case 3: Multiple sessions same day**
Detection: `/tmp/session-summary-YYYY-MM-DD.md` already exists.
Mitigation: Append `-2`, `-3` suffix. Each gets its own NotebookLM source addition.
Don't overwrite — earlier sessions are valid history.

**Edge Case 4: Session had nothing worth saving**
Detection: No decisions made, no corrections, no new preferences, trivial Q&A only.
Mitigation: Say so clearly. Don't manufacture memories. Skip the NotebookLM push.
A short "nothing to save" message is better than low-signal noise in the AI Brain.

**Edge Case 5: MEMORY.md index is near 200-line limit**
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

**Anti-Pattern 3: Skipping the NotebookLM push "for now"**
Temptation: Auth is finicky, skip it and do it later.
Failure: "Later" never happens. The session summary accumulates in /tmp and gets lost.
The AI Brain notebook diverges from reality. Long-term queryability is the entire point.
Instead: Push or explicitly inform the user that auth needs renewal before next session.

**Anti-Pattern 4: Relative dates in memories**
Temptation: "Next Thursday" is clear right now.
Failure: Meaningless 3 days later. Memory files are read weeks or months after writing.
Instead: Always convert: "next Thursday" → "2026-04-09". Include context if helpful.

---

## Section 6 — Quality Gates

- [ ] MEMORY.md checked for duplicates before any new file is created
- [ ] Every memory file has correct frontmatter: `name`, `description`, `type` fields
- [ ] All relative dates in memories converted to `YYYY-MM-DD` absolute dates
- [ ] Session summary has all 5 sections and is saved to `/tmp/session-summary-YYYY-MM-DD.md`
- [ ] NotebookLM: `notebooklm auth check` run before attempting push
- [ ] User confirmation message includes memory count, push status, and open threads

---

## Section 7 — Failure Modes and Fallbacks

**Failure 1: `notebooklm` CLI not on PATH**
Detection: `command not found: notebooklm`
Fallback: Try `~/.notebooklm-venv/bin/notebooklm source add ...`. If that also fails,
inform user the push was skipped and to run `pip install notebooklm-py` + re-authenticate.
Memories are still saved locally — that part succeeded.

**Failure 2: Memory write permission denied**
Detection: Write tool returns permission error on MEMORY.md or memory file.
Fallback: Write session summary to `/tmp/session-summary-YYYY-MM-DD.md` and print the
memory content as plain text in the response so the user can save it manually.

**Failure 3: Session was too large to review accurately**
Detection: Context window was compressed during session; early conversation is unavailable.
Fallback: Review from the most recent messages. Explicitly note in the session summary that
"earlier session context was unavailable due to compression." Focus on what is visible.

---

## Section 8 — Composability

**Hands off to:**
- `notebooklm` — for all NotebookLM CLI operations (source add, list, auth check)
- `knowledge-management` — when the session produced content worth archiving in the vault

**Receives from:**
- Any skill — this is always the last skill in a session, not chained from specific skills
- `project-memory-bootstrap` — when setting up memory for a new project for the first time

---

## Section 9 — Improvement Candidates

- Auto-detect session end from conversation patterns (user says "thanks", signs off) to
  prompt wrap-up without explicit invocation
- Deduplicate AI Brain sources: before pushing, check if a same-day summary already exists
  in the notebook to prevent duplicate source accumulation
- Memory health score: count memories by type and age, flag stale project memories
  (>30 days old) for review at wrap-up time
