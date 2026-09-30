---
name: continuing-alm-work
description: Use when resuming or continuing an existing multi-step project, implementation plan, roadmap, backlog, or interrupted Claude Code session where the verified checkpoint, active task, blockers, and next executable action must be reconstructed.
compatibility: Designed for Claude Code projects with access to project files and verification tools; degrades safely when repositories, trackers, CI, deployments, or connected services are unavailable.
metadata:
  version: "2.0.0"
  updated: "2026-09-30"
  owner: "Aaron DeYoung"
  domain-category: aarons-latest
  last-reviewed: "2026-09-30"
  adjacent-skills: workbetter, projectplan-rescope
  review-trigger: "Project checkpoint conventions or Claude Code skill loading change."
---

# Continuing ALM Work

## Outcome

Resume an established project from verified evidence, continue the highest-value safe work, and leave an exact continuation marker. Interpret "ALM" from the project context. State the interpretation only when ambiguity could change the next action.

## Do not use

- New-project ideation before an approved plan or current implementation exists.
- Isolated one-off questions with no project continuity requirement.
- Context-limit shutdown alone. If `context-checkpoint` or a host context warning activates, finish only the smallest safe atomic step and follow that protocol first.

## Non-negotiables

- Latest explicit user direction controls intent, scope, priority, and approvals. Direct artifacts and fresh tool output control technical status.
- Never promote a narrative claim, old handoff, or agent report to completion without corroborating evidence.
- Never fabricate files, commands, tests, deployments, tool access, agents, or results.
- Preserve approved decisions and unknown work. Do not reset, clean, overwrite, or delete unowned changes.
- Continue executable work after reconstructing state. Do not return plan-only advice unless the runtime is plan-only, a permission boundary is reached, or all work is blocked.
- Ask one precise question at a time, and only when its answer materially changes the safe next action. Continue every independent, non-blocked workstream.
- Use the smallest capable orchestration, authoritative live sources, and least-privileged access. Batch related retrieval and checks when practical.
- Match every completion claim to the scope of fresh evidence. Not run means not passed.
- If an action repeats without new evidence or progress, stop the loop, identify the blocker or failed assumption, and change approach.

## Workflow

### 1. Discover authority and state

Inspect the smallest sufficient set of available sources:

1. Latest user instructions and approval boundaries.
2. Project instructions, accepted specifications, decisions, and plan.
3. Repository, branch, status, diff, commits, artifacts, and deployed state.
4. Fresh command, test, build, CI/CD, monitoring, and validation output.
5. Current tracker, backlog, roadmap, or issue state.
6. Recent checkpoints and handoffs, corroborated before use.

Identify the project objective, active phase, last verified completed task, interrupted task, blockers, discrepancies, and exact next action. Do not confuse the most recently discussed task with the most recently completed task.

### 2. Reconcile evidence

Use only these statuses: `Verified complete`, `In progress`, `Blocked`, `Not started`, `Superseded`, or `Unknown`.

For each material state decision, retain the conclusion, evidence, confidence (`High`, `Medium`, or `Low`), and unresolved conflict. Resolve intent from explicit user direction; resolve implementation status from direct current evidence. When evidence conflicts, expose the conflict instead of silently choosing the convenient version.

### 3. Rebase only what execution needs

Normalize remaining work just enough to act. For each relevant task, identify outcome, prerequisites, dependencies, deliverable, definition of done, verification, risk, approval need, and best-fit capability. Remove, defer, combine, or reorder low-value work while preserving the approved objective and constraints.

Create a dependency map only when two or more workstreams interact. Mark the critical path. Parallelize only independent or safely isolated work and reserve an explicit integration and cross-check step. Scan the full lifecycle only for material gaps in requirements, architecture, implementation, testing, security, release, deployment, observability, documentation, feedback, or retirement. Eliminate, simplify, automate, standardize, instrument, or document recurring weakness before adding complexity.

### 4. Execute the highest-leverage ready task

Choose work that advances the objective, unlocks dependencies, reduces material risk, eliminates recurring effort, or shortens the critical path. Work in coherent atomic units:

1. Confirm prerequisites.
2. Produce the artifact or change.
3. Verify it.
4. Integrate related work.
5. Update status, evidence, risks, and exact next action.

Continue until the objective is complete, all remaining work is genuinely blocked, or an approval boundary is reached. Verify the current phase exit criteria before entering a new phase, or explicitly rebaseline the plan.

Use subagents only when specialization, isolation, independent review, or real concurrency provides a material advantage. Read [references/delegation-contract.md](references/delegation-contract.md) before delegating.

### 5. Verify before advancing

Apply the checks appropriate to the claim: requirements traceability, focused tests, full relevant suite, build, type check, lint, security, data quality, architecture consistency, deployment health, monitoring, or artifact inspection.

A task is `Verified complete` only when its deliverable exists, acceptance criteria are satisfied, relevant verification passed or an exception is recorded, state documentation is current, and the next dependent task can safely begin. A failed gate returns the task to `In progress` or `Blocked`.

### 6. Preserve continuity

Reuse the project’s existing canonical state record. Do not create competing plan, state, or handoff files. Update that record after each meaningful execution unit when writes are allowed. If no canonical record exists, do not invent one merely for ceremony; report `Checkpoint: conversation-only` unless project convention or the user authorizes a file.

Read [references/checkpoint-contract.md](references/checkpoint-contract.md) when a persistent checkpoint or session handoff is required.

## Approval boundaries

Routine, reversible, in-scope work may proceed. Before destructive, difficult-to-reverse, production, externally consequential, paid, credential-sensitive, privacy-sensitive, or materially scope-changing action, read [references/approval-boundaries.md](references/approval-boundaries.md) and obtain the required explicit decision. Continue unrelated safe work while approval is pending.

## Skill-candidate rule

When a stable, recurring, reusable workflow is detected, do not build or materially scaffold it automatically. Read [references/skill-proposal.md](references/skill-proposal.md), present the proposal, request explicit approval, and continue current non-blocked work.

## Response contract

Keep execution updates brief. At the end of each meaningful cycle, report:

1. **State** - objective, phase, last verified task, current task, exact next action, blockers, discrepancies, confidence.
2. **Performed** - only actions actually completed and artifacts actually changed.
3. **Verification** - checks run, results, failures, unverified areas, residual risk.
4. **Resume marker** - use the exact block in [references/checkpoint-contract.md](references/checkpoint-contract.md).

Include an execution-map table only when multiple workstreams require coordination. Include a skill-candidate section only when a credible candidate exists. If execution is impossible, name the exact blocking evidence and the first executable action once the blocker clears.
