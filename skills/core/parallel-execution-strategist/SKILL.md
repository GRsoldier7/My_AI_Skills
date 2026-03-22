---
name: parallel-execution-strategist
description: |
  Tactical parallel execution patterns for Claude Code. Optimizes how work is decomposed,
  distributed across agents, and reassembled. The difference between a 10-minute task and
  a 2-minute task is often parallelization — this skill makes that automatic.

  AUTO-TRIGGER when planning multi-step work, spawning subagents, or any task that could
  benefit from parallelization. Activates whenever 3+ independent tasks are identified.

  EXPLICIT TRIGGER on: "parallel", "subagent", "background", "concurrent", "speed up",
  "parallelize", "run simultaneously", "split this up", "divide and conquer",
  "run in background", "worktree", "multi-agent", "faster", "how to run these together",
  "batch this", "fan out", "fan in", "pipeline", "dependency graph", "independent tasks",
  "can these run at the same time".

  Also trigger when the user presents a list of tasks and the question of ordering/parallelism
  is relevant, even if they don't explicitly ask.

  Complements polychronos-team (high-level orchestration strategy) with ground-level
  Claude Code execution tactics.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: polychronos-team, session-optimizer, skill-amplifier
  last-reviewed: "2026-03-21"
  review-trigger: "New Claude Code agent features, worktree improvements, user reports parallelization failures"
  capability-assumptions:
    - "Claude Code Agent tool with run_in_background parameter"
    - "Git worktree support for isolated parallel execution"
    - "TaskCreate/TaskUpdate for progress tracking"
  fallback-patterns:
    - "If no git repo: skip worktree patterns, use background agents only"
    - "If simple task (<3 steps): recommend sequential, don't over-parallelize"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: multi-step task, list of work items, or implementation plan
- Output produces: parallelization strategy, agent decomposition, dependency graph
- Can chain from: polychronos-team (strategy → tactical execution)
- Can chain into: any implementation skill (parallel execution of skill-guided work)
- Orchestrator notes: always validate independence before parallelizing

---

## The Parallelization Decision

### When to Parallelize
- Tasks touch **different files** or directories
- Tasks are **read-only research** (exploring, searching, reading docs)
- Tasks produce **independent outputs** (separate skills, separate features, separate docs)
- Tasks are **different types of work** (one builds, one tests, one researches)

### When to Serialize
- Task B **needs Task A's output** as input
- Tasks **modify the same files** (merge conflicts guaranteed)
- **Design decisions** are needed between steps (human review gate)
- Tasks share **mutable state** (database, shared config)

### When to Hybrid (Serial-Parallel)
Build a dependency DAG — parallelize within each tier:
```
Tier 1 (parallel): Research API docs | Explore codebase | Read requirements
        ↓ sync point: synthesize findings
Tier 2 (parallel): Build component A | Build component B | Write tests for C
        ↓ sync point: integration review
Tier 3 (parallel): Run test suite | Update docs | Prepare PR
```

### Quick Decision Tree
```
Is output of A needed as input to B? → SERIALIZE
Do they touch the same files?        → SERIALIZE
Is one blocking a design decision?   → SERIALIZE
Are they different files/topics?     → PARALLELIZE
Are they all research/read-only?     → PARALLELIZE
Can they run in worktrees?           → PARALLELIZE with isolation
```

---

## Agent Spawning Patterns

### Pattern 1: Fan-Out Research
**Use when:** You need information from multiple independent sources.
```
Spawn in parallel:
  Agent A → "Read and summarize the auth module at src/auth/"
  Agent B → "Read and summarize the database schema at src/models/"
  Agent C → "Search for all API endpoints in src/routes/"
Wait for all → Synthesize findings → Proceed with informed plan
```
- Use `subagent_type: "Explore"` for lightweight research agents
- Each agent gets specific file paths and search queries
- You synthesize — agents don't see each other's results

### Pattern 2: Parallel Implementation
**Use when:** Building independent components that don't share files.
```
Spawn in parallel:
  Agent A → "Build the user authentication skill at skills/auth/"
  Agent B → "Build the database design skill at skills/database/"
  Agent C → "Build the API testing skill at skills/testing/"
Wait for all → Review each → Commit
```
- Give each agent **exclusive file ownership** — specify exact paths
- Use `isolation: "worktree"` when there's any risk of file overlap
- Verify outputs before merging

### Pattern 3: Build + Validate Split
**Use when:** You can write code and tests independently.
```
Spawn in parallel:
  Agent A → "Implement the feature at src/feature.py" (foreground or worktree)
  Agent B → "Write tests for feature at tests/test_feature.py" (worktree)
Wait for both → Run tests → Fix mismatches
```
- Test-writing agent needs the interface spec, not the implementation
- Both work from the same requirements/spec document

### Pattern 4: Foreground + Background
**Use when:** A heavy task can run while you continue interactive work.
```
Spawn in background:
  Agent A → "Research all dependencies and create audit report" (run_in_background: true)
Continue in foreground:
  Interactive work with user (code review, planning, small fixes)
Agent A completes → notification → integrate results
```
- Background agents are ideal for: large file generation, test suites, research, builds
- You'll be notified on completion — don't poll or sleep
- Continue meaningful work in the foreground

### Pattern 5: Pipeline (Phased Execution)
**Use when:** Work has natural phases with sync points.
```
Phase 1 — Research (parallel):
  3 Explore agents gather information
  → Sync: synthesize into plan

Phase 2 — Implement (parallel):
  2 agents build independent components
  → Sync: integration review

Phase 3 — Validate (parallel):
  1 agent runs tests, 1 agent updates docs
  → Sync: final review, commit
```
- Each phase gate requires review before proceeding
- Phases can mix serial and parallel work

---

## Writing Effective Agent Prompts

Every agent prompt must be **complete and self-contained**. Agents don't share your context.

**Include:**
1. **Exact task** — what to do, with specifics
2. **File paths** — where to read, where to write
3. **Scope boundaries** — "only modify files in X", "do not touch Y"
4. **Output format** — "save to path/file.md", "return findings as text"
5. **Context** — any background the agent needs to do the job
6. **Intent** — research only, or implement? Read only, or write?

**Bad prompt:**
> "Look into the auth system and fix any issues"

**Good prompt:**
> "Read src/auth/login.py and src/auth/middleware.py. The login endpoint returns 500 when
> the user's session token is expired instead of 401. Fix the error handling in the token
> validation function. Only modify files in src/auth/. Do not change the database schema.
> Save your changes to the files directly."

---

## Worktree Isolation

Use `isolation: "worktree"` when parallel agents need to modify code:

- Each agent gets its own copy of the repo (separate git branch)
- No merge conflicts during execution — conflicts resolved after
- Worktrees auto-cleanup if no changes are made
- If changes are made, worktree path and branch are returned

**When to use worktrees:**
- Two+ agents modifying code simultaneously
- Experimental changes that might be discarded
- Long-running implementations alongside interactive work

**Merge strategy:**
- Review each worktree's diff independently
- Merge one at a time, resolving conflicts between
- If conflicts are extensive, one agent's work may need manual integration

---

## Token and Cost Optimization

- **Specific > broad:** "Read lines 50-80 of src/config.py" beats "explore the config"
- **Explore agents are lighter** than general agents — use them for research
- **Don't duplicate context:** each agent carries its own window, don't send redundant info
- **Kill early:** if an agent's results are no longer needed, its context cost is already spent —
  but don't spawn a replacement unnecessarily
- **Batch small tasks:** 3 related one-line changes don't need 3 agents — do them sequentially

---

## Progress Tracking

Before spawning parallel work:
1. Create one task per work item (`TaskCreate`)
2. Mark `in_progress` when agent launches
3. Mark `completed` when agent returns AND results are verified
4. Use `addBlockedBy` to visualize dependencies between tasks

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Over-parallelization (10 agents for 3 tasks worth of work) | Overhead > savings |
| Fire-and-forget (spawn and never check results) | Unverified output ships |
| Redundant work (you research what an agent is also researching) | Wasted tokens |
| Vague agent prompts ("fix the code") | Agent wastes time exploring |
| Parallelizing dependent tasks | Race conditions, wrong outputs |
| Skipping the dependency check | "These look independent" → they weren't |

---

## Self-Evaluation (run before parallelizing)

Before spawning parallel agents, silently check:
[ ] Are these tasks truly independent (no shared files, no data dependencies)?
[ ] Does each agent have a complete, self-contained prompt with file paths?
[ ] Have I specified output locations to avoid file conflicts?
[ ] Is parallelization actually faster than sequential for this case?
[ ] Am I tracking progress with tasks?
[ ] Did I avoid duplicating work I'm also doing myself?
If any check fails, restructure before spawning.
