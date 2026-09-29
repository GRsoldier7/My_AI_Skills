---
name: workbetter
description: Execute or resume multi-step project plans with grounded sequencing, task-specific tool selection, verification, and reusable workflow improvements. Use when asked to WorkBetter, work through a plan efficiently, recover from drift, or improve recurring execution workflows.
metadata:
  author: Aaron
  version: "1.0.0"
  domain-category: aarons-latest
  last-reviewed: "2026-09-28"
---

# WorkBetter

Optimize for verified outcomes, minimal rework, and maintainable solutions.
Novelty, agent count, and tool count are costs unless they improve the
outcome. Apply this workflow to the current assignment until completion
or a genuine blocker; respect planning-only requests and existing permissions.

## 1. Ground

Read applicable project instructions, the designated plan, and relevant
handoff. Inspect actual files, working changes, and verification evidence
before trusting completion labels. Preserve unrelated work. Do not infer
plan authority from modification time alone.

Establish the objective, phase, acceptance criteria, constraints, and next
unfinished dependency. Distinguish facts, assumptions, and unknowns.
Reuse the existing plan and tracker; create a short plan only when absent
and needed. For trivial tasks, act directly.

Resolve routine implementation choices autonomously. Ask only when an
unresolved choice materially changes scope, architecture, access, cost,
or irreversible behavior. If there is no actionable objective, ask for it
instead of inventing work.

## 2. Sequence

Order work by dependencies, risk reduction, and user value. Resolve
consequential uncertainties before expensive implementation. Deliver
the smallest useful, verifiable slice first.

Give each active task a concrete output and completion check. Keep one
primary task active; parallel branches need independent outputs and
explicit integration points. Reuse sound architecture and project
patterns. Choose the simplest design meeting requirements; explain
consequential tradeoffs briefly.

Separate necessary prerequisite fixes from optional improvements.
Park optional ideas in the existing backlog. Change the plan when evidence
requires it, recording the reason and impact without expanding the
authorized scope.

## 3. Select capabilities

Before each meaningful task, select the smallest sufficient combination:

- Established specialist procedure: read and apply the relevant skill.
- Repeated deterministic operation: existing script, CLI, or automation.
- Connected system data or action: authorized connector or MCP tool.
- Independent bounded work: subagent when coordination cost is justified.
- Unfamiliar or version-sensitive behavior: current official documentation
  and local configuration evidence.
- Small, clear task: direct execution.

Inspect relevant capability descriptions first; load full instructions
only when needed. Avoid repeated full-catalog scans and overlapping
workflow frameworks. Verify availability and compatibility; never invent
tools, model access, successful calls, or research. Use a sound alternative
when a capability is unavailable and disclose material limitations.

Adopt newer techniques for demonstrated benefit. Stop research when
sufficient evidence supports the decision. Add dependencies or MCP servers
only when necessary and authorized; explain benefits and access implications
when authorization is missing. This skill grants no additional permissions.

## 4. Execute and verify

Perform the next ready task, inspect its result against acceptance criteria,
and continue authorized work without routine approval pauses.

Delegate bounded work with an objective, relevant inputs, ownership
boundaries, constraints, expected output, and completion check. Keep
dependent edits sequential and prevent competing writes. Require concise
evidence-backed results. The lead reviews, integrates, and verifies them;
use independent review when complexity or consequence justifies it.

Choose verification proportional to the change: behavioral tests, targeted
regression checks, build/type checks, UI inspection, data validation, or
document review. Follow required project gates. A passing build alone does
not prove functional correctness. Distinguish new failures from existing
ones using evidence; report unavailable checks and uncertainty.

After repeated failure without new evidence, stop repeating the same
approach. Investigate the cause, change the hypothesis, or identify the
smallest missing input. Continue independent useful work while blocked.
Never mark untested behavior as verified.

## 5. Prevent drift

At task boundaries, after surprising results, and after context recovery,
compare the next action with the objective, phase, and acceptance criteria.
Park unrelated improvements.

Update the existing plan or handoff after meaningful completed slices,
decisions, and blockers. Keep one authoritative record, not duplicate
status files. Record only resumption essentials: objective, phase,
completed work with evidence, remaining tasks, changed files, decisions,
blockers, and exact next action. Exclude secrets and raw logs.

Use actual context telemetry if available; never invent usage percentages.
Checkpoint before long investigations or handoffs. After compaction,
reread the checkpoint and this skill when needed, then verify current
files before continuing.

## 6. Improve reusable workflows

Consider extraction after repeated successful use, or when an explicitly
requested reusable workflow has clear future value. Search existing skills
and helpers first; improve an appropriate existing asset instead of
duplicating it, respecting ownership and permissions.

Choose a skill for reusable judgment, a script for deterministic work,
a template for repeated structure, or a project instruction for a stable
local convention. Capture inputs, outputs, essential steps, failure
handling, and a completion check. Keep secrets and project-specific details
out of general skills; load optional references progressively.

Validate on a representative task before relying on the asset; check
missing inputs and a likely failure case when relevant. Report actual
verification, not universal reliability. Finish the active slice before
optional extraction. Queue improvements that would derail delivery.
Never recursively optimize the optimizer or rewrite this skill merely
because it was invoked.

## 7. Close

Report concisely: delivered outcome; verification and limitations;
remaining blocker or next action; reusable improvement only if created.
Stop when agreed acceptance criteria are met. Do not manufacture more
work to appear thorough.
