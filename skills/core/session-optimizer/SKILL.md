---
name: session-optimizer
description: |
  Maximize Claude Code session efficiency, output quality, and context window longevity.
  The difference between a frustrating session and a productive one is session architecture —
  this skill makes that deliberate.

  AUTO-TRIGGER at session start for complex projects and when context window approaches 40%.

  EXPLICIT TRIGGER on: "optimize session", "context management", "compaction", "compact",
  "session strategy", "how to structure this session", "this is a big project",
  "long session", "multi-day project", "running out of context", "token usage",
  "efficiency", "hooks", "permissions", "settings optimization", "session architecture",
  "how to work faster", "Claude Code tips", "power user", "worktree",
  "multi-session", "handoff between sessions", "context window", "save context".

  Also trigger when planning work that will clearly exceed a single context window,
  or when the user seems frustrated with session performance.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: parallel-execution-strategist, anti-hallucination, skill-amplifier, polychronos-team
  last-reviewed: "2026-03-21"
  review-trigger: "New Claude Code features, context window changes, user reports session inefficiency"
  capability-assumptions:
    - "Claude Code CLI with standard tool suite"
    - "Settings at ~/.claude/settings.json and .claude/settings.json"
    - "CLAUDE.md support for project-level context"
    - "Hook system for automation"
  fallback-patterns:
    - "If not Claude Code: provide general LLM session management principles"
    - "If no hook access: focus on prompt and workflow patterns only"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: session planning question, efficiency concern, or context management need
- Output produces: session architecture, settings configuration, or workflow optimization
- Can chain from: any skill (optimize how that skill executes)
- Can chain into: parallel-execution-strategist (session → parallel work within session)
- Orchestrator notes: meta-layer that improves all other skill execution

---

## Session Architecture Patterns

### Pattern A: Single-Focus Session
One clear objective, one project, start to finish.
- **Start:** State the goal, read relevant files, execute
- **Compact when:** Context hits ~50%, preserving key decisions and file states
- **Best for:** Bug fixes, single feature, skill creation, code review
- **Duration:** Typically completes within one context window

### Pattern B: Multi-Phase Session
Large project broken into phases within one session.
- **Structure:** Research → Design → Implement → Test → Commit
- **Phase gates:** Review output before moving to next phase
- **Compact between phases** — summarize completed work, carry forward decisions
- **Track progress** with tasks — mark phases complete as you go
- **Best for:** New feature with design + implementation, multi-file refactor

### Pattern C: Multi-Session Project
Work too large for one context window — plan for handoff.
- **Session 1:** Research + design → save plan to `docs/plan.md` or CLAUDE.md
- **Session 2:** Implement phase 1 (read plan from file at start)
- **Session 3:** Implement phase 2 + test + deploy
- **Key rule:** Persist ALL decisions to files — memory across sessions lives in the filesystem
- **Write a handoff document** at session end: what's done, what's next, key decisions, gotchas
- **Best for:** Large features, multi-day projects, complex migrations

### Pattern D: Exploration/Discovery Session
No clear plan — exploring possibilities.
- Start broad, use subagents for parallel research
- When direction emerges, compact and switch to Pattern A or B
- Don't commit to implementation until you've converged
- **Best for:** Investigating bugs, exploring new libraries, architecture decisions

---

## Context Window Management

### The Context Budget
Think of your context window as a budget. Every file read, tool output, and conversation
turn spends from it. Spend wisely.

| Context Fill | Status | Action |
|-------------|--------|--------|
| 0-30% | Green | Full speed, no constraints |
| 30-50% | Yellow | Be selective about file reads, use line ranges |
| 50-70% | Orange | Compact proactively, save state to files |
| 70-85% | Red | Compact or start new session with handoff |
| 85%+ | Critical | Finish current task, write handoff, new session |

### Context-Efficient Reading
- **Grep before Read** — find line numbers first, then read only what you need
- **Use `limit` and `offset`** on Read — never read a 2000-line file to check one function
- **Don't re-read** files already in context — reference what you already know
- **Use Explore agents** for broad searches — their context is separate from yours
- **Glob for structure** — find files by pattern instead of reading directories

### Context-Efficient Writing
- **Edit over Write** — Edit sends only the diff, Write sends the entire file
- **Batch related changes** — multiple edits to the same file in one Edit call
- **Don't echo back** large file contents in conversation — reference by path and line

---

## Compaction Strategy

### What to Preserve
- Current task state and progress
- Key decisions made and their reasoning
- File paths modified and what was changed
- Errors encountered and their solutions
- User preferences expressed in this session
- Uncommitted work and its status

### What to Drop
- Full file contents already written to disk
- Exploratory dead ends and abandoned approaches
- Verbose tool outputs (search results, long diffs)
- Repeated conversation patterns

### Pre-Compaction Checklist
Before compacting (or asking the user to compact):
1. Save any in-progress work to files
2. Update task list with current status
3. Note any key context that's only in conversation (not in files)
4. If mid-implementation: write a brief state note to CLAUDE.md or a temp file

---

## CLAUDE.md as Session Memory

Your project's `CLAUDE.md` is the most important file for session efficiency.
It loads into every session automatically.

**What belongs in CLAUDE.md:**
- Architecture decisions that affect every session
- Coding conventions and patterns specific to this project
- Build/test/deploy commands
- Known gotchas and workarounds
- Key file paths and their purposes

**What doesn't belong:**
- Temporary state (use tasks or temp files)
- Full documentation (use docs/ directory)
- Personal preferences (use ~/.claude memory)
- Anything over ~200 lines (it loads into every session's context)

**Update it actively** — when you learn something a future session needs, add it.

---

## Hook Patterns for Efficiency

### Auto-Format After Writes
```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "jq -r '.tool_response.filePath // .tool_input.file_path' | { read -r f; prettier --write \"$f\"; } 2>/dev/null || true"
    }]
  }]
}
```

### Pre-Compaction Context Saver
```json
{
  "PreCompact": [{
    "hooks": [{
      "type": "command",
      "command": "echo '{\"systemMessage\": \"Remember to save any in-progress state to files before compaction.\"}'"
    }]
  }]
}
```

### Session Start Project Loader
```json
{
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "command": "echo '{\"systemMessage\": \"Project loaded. Check tasks and CLAUDE.md for current state.\"}'"
    }]
  }]
}
```

---

## Permission Optimization

### Safe to Auto-Allow
```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(pip:*)",
      "Bash(pytest:*)",
      "Bash(python -m pytest:*)",
      "Bash(wc:*)",
      "Bash(mkdir:*)"
    ]
  }
}
```

### Keep Gated (Never Auto-Allow)
- `rm -rf`, `git push --force`, `git reset --hard`
- Deployment commands, production database access
- Any command that modifies shared infrastructure
- File deletions outside the project directory

### Project-Specific Permissions
Use `.claude/settings.json` (committed) for team-wide permissions.
Use `.claude/settings.local.json` (gitignored) for personal overrides.

---

## Prompt Patterns for Efficiency

### Front-Load Context
```
Bad:  "Can you fix the bug?"
Good: "In src/auth/login.py around line 45, the token validation
       returns 500 instead of 401 when the session is expired. Fix
       the error handling to return the correct status code."
```

### Scope Your Requests
```
Bad:  "Update the auth system"
Good: "In src/auth/middleware.py, add rate limiting to the /login
       endpoint. Use slowapi. Don't modify other endpoints."
```

### Batch Related Work
```
Bad:  Three separate prompts for three related changes
Good: "In the user module: (1) add email validation to UserCreate
       schema, (2) add a unique constraint on email in the migration,
       (3) update the test to verify duplicate emails are rejected."
```

### Reference by Path
```
Bad:  "Look at the config file and update the database URL"
Good: "Read src/config.py and change DATABASE_URL to use the
       Cloud SQL connection string format"
```

---

## Multi-Project Session Management

When working across projects in one session:
- Use `additionalDirectories` in settings for cross-project access
- Be explicit about which project when switching: "Now working in Master_Skills at Z:/..."
- Consider separate sessions for truly unrelated projects — shared context isn't free
- Use tasks to track which project each work item belongs to

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Reading entire large files "just to check" | Grep first, read specific lines |
| Re-reading files already in context | Reference what you know |
| "Explore the codebase" without direction | Give specific search targets |
| Not compacting until context limit | Proactively compact at 50-60% |
| Over-specifying trivial tasks | Match prompt length to task complexity |
| Starting sessions cold on multi-day projects | Read CLAUDE.md and handoff doc first |

---

## Self-Evaluation (run before starting complex sessions)

Before starting a complex session, silently check:
[ ] Do I have a clear session goal, or is this exploration?
[ ] Have I set up the right permissions for this project?
[ ] Is CLAUDE.md current for this project?
[ ] Should I plan for multi-session work?
[ ] Are there tasks I can parallelize with background agents?
[ ] Am I using the right session pattern (A/B/C/D)?
If any check fails, address before diving into work.
