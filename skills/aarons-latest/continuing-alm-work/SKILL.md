---
name: continuing-alm-work
description: Reconstructs the last verified project state, resumes the next safe high-leverage task, verifies progress, and leaves a precise checkpoint. Use when continuing an existing plan, roadmap, implementation, ALM workflow, delivery phase, or interrupted multi-step project.
compatibility: Optimized for Claude Code; automatic state capture uses Python 3 and CLAUDE_PROJECT_DIR support; git is optional; manual fallback works when scripts or capabilities are unavailable.
allowed-tools: "Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/capture_project_state.py *)"
argument-hint: "[resume|reconcile|checkpoint] [scope]"
arguments:
  - mode
  - scope
metadata:
  author: Aaron
  version: "2.0.0"
  category: workflow-orchestration
  domain-category: aarons-latest
  last-reviewed: "2026-09-26"
---

# Continuing ALM Work

Resume from evidence, create verified progress, and leave the project easier to resume than you found it.

Invocation inputs: mode=`$mode`, scope=`$scope`. Default mode is **resume**; blank scope means the current project. Interpret **ALM** from project evidence and state the interpretation only when ambiguity remains material.

## Modes

- **resume**: reconstruct state, then execute the next safe high-leverage unit.
- **reconcile**: determine state and improve the execution map without changing implementation.
- **checkpoint**: persist an exact handoff without starting new work.

## Non-negotiables

1. Latest explicit user direction controls intent and scope; direct repository, test, CI, deployment, and source-of-truth evidence controls implementation status.
2. Discussion, plans, generated files, and prior completion claims are not proof. A task is **Verified complete** only after its definition of done is evidenced.
3. Preserve unknown work. Inspect dirty files and ownership before editing; never reset, clean, overwrite, or discard uncertain changes silently.
4. Execute by default in resume mode. Do not stop at a better plan when a safe executable action exists.
5. Use the smallest sufficient orchestration. Add agents, skills, tools, or connectors only for material specialization, isolation, authoritative access, independent review, or genuine concurrency.
6. Parallelize only independent or safely isolated work; preserve an explicit integration step.
7. Ask one focused question only when the answer materially changes correctness, safety, scope, or the next action. Continue every non-blocked workstream.
8. Report only work, tools, agents, checks, and results actually performed or observed.
9. Do not build or materially modify another reusable skill without explicit approval.

## Workflow

### 1. Capture the live baseline

When available, run this read-only snapshot first:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/capture_project_state.py \
  --root "${CLAUDE_PROJECT_DIR}" --format markdown --max-items 30
```

Use the snapshot to target inspection; it is discovery evidence, not proof of completion. If the script or substitutions are unavailable, inspect the equivalent sources manually. Read [state and evidence](references/state-and-evidence.md) when state is unclear, stale, or conflicting.

### 2. Reconstruct the exact checkpoint

Determine the objective, approved phase structure, last **Verified complete** task, interrupted task, active phase, exact stop point, blockers, dependencies, unresolved decisions, and plan-versus-reality discrepancies.

Classify relevant tasks as **Verified complete**, **In progress**, **Blocked**, **Not started**, **Superseded**, or **Unknown / insufficient evidence**. For material conclusions, retain evidence, confidence, conflicts, and the next verification action. Most recently discussed does not mean most recently completed.

### 3. Normalize only what affects execution

Identify the critical path, safe parallel work, integration points, missing quality gates, duplicated work, unnecessary handoffs, and tasks to remove, defer, combine, or reorder. Preserve the approved objective and constraints; improve the route rather than silently expanding scope.

For the next candidate task, establish: outcome, prerequisites, dependencies, deliverable, definition of done, verification, risk, reversibility, best-fit capability, and approval requirement. Use [execution routing](references/execution-routing.md) for delegation or complex dependencies.

### 4. Select and execute the next unit

Choose the smallest unit that creates meaningful, verifiable progress. Prefer, in order: critical-path unlock, dangerous-uncertainty reduction, completion of started work, then highest reversible user value.

Use installed specialist skills for planning, TDD, debugging, code review, deployment, or domain work instead of duplicating them here. Perform the work; do not merely narrate it. Reassess only when evidence changes priorities.

### 5. Integrate and verify

Integrate concurrent outputs, resolve conflicts, remove duplication, and run the checks appropriate to the claim. Never infer a broad completion claim from narrow evidence. Use [verification and safety](references/verification-and-safety.md) before claiming success.

If verification fails, return the task to **In progress** or **Blocked**, preserve the failure evidence, diagnose before repeating, and continue independent safe work.

### 6. Persist continuity and continue

Update the existing canonical plan, issue, checkpoint, or state record after each meaningful execution unit. If none exists and persistence is useful, create `docs/alm/execution-state.md` from [the template](assets/execution-state-template.md).

Record credible recurring-workflow candidates without interrupting execution; surface them only when ready for a proposal or at a checkpoint.

Continue until the requested scope is complete, genuinely blocked, reaches an approval boundary, or requires a checkpoint because context pressure makes further work unreliable.

## Output Contract

### Normal iteration

Keep routine updates compact:

- **State delta:** what changed or was learned.
- **Work completed:** artifact or action actually produced.
- **Verification:** passed, failed, and not run.
- **Exact next action:** the next executable step or required decision.

Do not repeat the full project history or execution map every turn.

### Full checkpoint

Use a full checkpoint only when requested, stopping, finishing a phase, blocked, seeking approval, or protecting continuity before compaction. Follow [checkpoints and skill candidates](references/checkpoints-and-skill-candidates.md), including an exact `RESUME FROM` marker.

## Approval Boundary

Proceed with routine, reversible, in-scope work under existing permissions. Obtain explicit approval before destructive or difficult-to-reverse changes, unauthorized production deployment, material-risk migration, external publication or communication, financial commitment, credential or sensitive-data change, material scope or architecture change, or reusable-skill creation/modification. Continue unrelated safe work while approval is pending.
