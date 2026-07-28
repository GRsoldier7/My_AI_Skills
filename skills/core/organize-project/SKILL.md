---
name: organize-project
description: |
  Organizes the current project: reads it deeply, classifies its type, applies best-practice
  structure, bootstraps short + long-term memory, sets up a lessons-learned + self-healing
  feedback loop, and activates the optimal skill stack. One invocation turns a messy or new
  project into a fully wired, session-persistent workspace.

  TRIGGER on: "organize this project", "set up this project", "get this organized",
  "best practices for this", "structure this project", "help me set up", "get things in order",
  "clean this up", "project setup", "start fresh", "what skills should I use", "set up my
  workflow", "initialize this project", "set up memory", "Claude keeps forgetting",
  "remember things across sessions", or any project missing a CLAUDE.md.

  Also trigger proactively when opening any new or disorganized project.
metadata:
  author: aaron-deyoung
  version: "2.0"
  domain-category: meta
  adjacent-skills: autoplan, superpowers:writing-plans, health, learn, investigate, knowledge-management
---

# Organize Project

**Your goal:** Read the project, understand it, organize it, wire up memory and a self-healing feedback loop, then activate the right skill stack — so every future session opens with full context and builds on prior work.

---

## Step 1: Discover (parallel reads)

Run these simultaneously:
1. `CLAUDE.md` (if exists — most important)
2. `README.md`
3. Top-level directory listing
4. Tech stack signals: `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `docker-compose.yml`, `Makefile`
5. `git log --oneline -20` (skip if no repo)
6. `skills/` or `.claude/` folder for custom skills
7. **Memory:** `~/.claude/projects/[folder-name]/memory/` for prior project memories
8. **Prior learnings:** `learnings/lessons.md`, `learnings/feedback.md` if they exist

After reading: know the project type, current focus, what's already good, what's broken.

---

## Step 2: Classify & Assess

**Project types** (see `references/project-types.md` for canonical structures):

| Type | Signals |
|------|----------|
| Python library | `pyproject.toml`, `src/` layout, `__init__.py` |
| Python scripts/automation | `.py` files, task-oriented, no package structure |
| Node/TS web app | `package.json`, framework (Next, React, etc.) |
| API/backend | Routes, controllers, models, DB migrations |
| Network/infra/automation | PowerShell/bash scripts, runbooks, configs |
| Data/ML | Notebooks, datasets, pipelines |
| Docs/knowledge | Markdown-heavy, runbooks, references |

**Assess:** structure, CLAUDE.md quality, memory/learnings present?, entry points clear?, right skills active?

---

## Step 3: Plan → Present → Execute

**Show the user:**
```
## Project Assessment: [Name]
Type: [type] | Focus: [current work] | Organization: [Good/Needs Work/Missing]
Memory/Learnings: [exists/thin/missing]

What I'll do:
1. [specific action]
2. [specific action — e.g., "Bootstrap memory at ~/.claude/projects/.../memory/"]
3. [specific action — e.g., "Create learnings/ with lessons.md + feedback.md + session-notes.md"]
4. [specific action — e.g., "Update CLAUDE.md with session checklist + quick commands"]

Skills to activate: [list]
Won't change: [what's already good]
```

Small scope (< 5 changes, no destructive ops): proceed. Larger scope: wait for thumbs-up.

---

## Step 4: Organize Structure

- Create missing dirs per `references/project-types.md` — never delete, use `archive/` for old content
- Root: only `CLAUDE.md`, `README.md`, `CHANGELOG.md`, main entry point(s)
- Consistent `lowercase-with-hyphens` naming

---

## Step 5: CLAUDE.md — The Memory Core

This is the most valuable artifact. Write it for a session with zero prior knowledge.

**Required sections:**
```markdown
# [Project Name]

## What this is
[2-3 sentences: purpose and scope]

## Current focus
[What's being actively worked on — specific, not vague]

## Project type + tech stack
[Type + languages/frameworks/key deps]

## Directory structure
[One-line per folder]

## How to run / develop
[Copy-pasteable commands]

## Key files
[3-5 most important, one-line each]

## Active issues / known blockers
[Current problems + explicit next action]

## Lessons learned
See learnings/lessons.md — check this before starting any session.

## Known failure modes
[Things that went wrong before + how to avoid — updated by the self-healing loop]

## Session start checklist
1. Read learnings/lessons.md
2. Read learnings/feedback.md (corrections log)
3. Check "Current focus" above
4. Run /learn

## Quick commands
[Skill invocation reference — see Step 8]
```

---

## Step 6: Memory Bootstrap

### Long-term memory (persists across all conversations)

Write to: `~/.claude/projects/[project-folder-name]/memory/project_[name].md`

```markdown
---
name: [Project Name] — Context
description: Type, focus, and key facts for [project name] — check at session start
type: project
---

**Project:** [Name] | **Path:** [full path] | **Type:** [type]
**Current focus:** [what's being worked on]
**Why:** [the main goal or constraint]
**How to apply:** Read at the start of every session on this project.

**Key facts:** [bullet list]
**Failure modes to avoid:** [things that went wrong]
```

Add pointer to `MEMORY.md` index at that same directory.

### Short-term memory (within-session)

The Session start checklist in CLAUDE.md (Step 5) handles this.

---

## Step 7: Learnings Architecture (Self-Healing Loop)

Create `learnings/` in the project:

**`learnings/lessons.md`** — accumulated knowledge
```markdown
# Lessons Learned — [Project Name]
## Architecture / Design
## Common Pitfalls
## Useful Discoveries
## Solved Problems (hard problems + solutions, so they're never rediscovered)
```

**`learnings/feedback.md`** — correction log (the self-healing mechanism)
```markdown
# Corrections Log
Read at session start — prevents repeating mistakes.

| Date | What happened | What was wrong | Correct approach |
|------|---------------|----------------|------------------|
```

**`learnings/session-notes.md`** — session log (`/wrapup` fills this automatically)
```markdown
# Session Notes
## [Date]
**Focus:** | **Progress:** | **Blockers:** | **Next:**
```

Tell the user: "Run `/wrapup` at session end — it fills `session-notes.md`. Run `/learn` at session start. When I get something wrong, correct me and I'll update `feedback.md` — that's what makes the loop self-healing."

---

## Step 8: Activate Skill Stack

See `references/skill-recommendations.md` for the curated list by project type.

**Universal:** `/learn` (session start), `/wrapup` (session end), `/checkpoint` (before risky ops)

Add a **Quick commands** table to CLAUDE.md:
```markdown
## Quick commands
| Command | When to use |
|---------|-------------|
| /learn | Session start — surface prior learnings |
| /wrapup | Session end — log progress + next steps |
| /investigate | Chasing a bug or unexplained behavior |
| /health | Code quality check |
| /careful | Before any destructive or irreversible operation |
| /superpowers:writing-plans | Planning a new feature or approach |
| /superpowers:brainstorming | Exploring options or architecture decisions |
| /checkpoint | Before risky changes — save working state |
```

Invoke `/learn` now to surface any existing learnings.

---

## Step 9: Brief the User

```
## Project organized ✓

What I did:
- [structural changes]
- CLAUDE.md: [sections created/updated]
- Memory: ~/.claude/projects/[folder]/memory/project_[name].md
- Learnings: learnings/lessons.md + feedback.md + session-notes.md

Memory systems:
- Long-term: [memory file path]
- Session checklist: CLAUDE.md section
- Self-healing loop: learnings/feedback.md (I update this when you correct me)

Active skill stack: [quick table from references/skill-recommendations.md]

Current focus: [restate what they're working on]
Next step: [one clear recommendation]

How to keep memory fresh:
- Session start: /learn + CLAUDE.md checklist
- Session end: /wrapup
- When I make a mistake: correct me → I log it to feedback.md
- After hard problems: I'll add to lessons.md
```

---

## Principles

- **Don't over-engineer.** A 3-file script doesn't need 8 directories.
- **Preserve intent.** Unusual structure for a reason? Ask first.
- **CLAUDE.md is everything.** A great one = every session starts at full speed.
- **Memory compounds.** Session 10 should be dramatically faster than session 1.
- **The self-healing loop is the key differentiator.** `feedback.md` + reading it at session start = Claude that actually learns.
