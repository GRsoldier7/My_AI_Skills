# Delegation Contract

Use one capable worker by default. Delegate only when specialization, isolation, independent review, or genuine concurrency is likely to improve the verified result more than coordination will cost.

## Parallelism gate

Tasks may run in parallel only when they:

- Have independent inputs and outputs, or are isolated by repository, branch, worktree, directory, or immutable snapshot.
- Do not edit the same source of truth or depend on unsettled shared assumptions.
- Have a defined integration owner and integration test.
- Can fail independently without corrupting another workstream.

Run sequentially when one result determines the next task, shared state is mutable, edits can conflict, or integration cost erases the speed gain.

## Bounded assignment

A delegated assignment must include:

- Objective and why it matters now.
- Relevant context and authoritative inputs.
- Scope, non-goals, and files or systems allowed.
- Constraints, approval boundaries, and prohibited actions.
- Expected deliverable and output format.
- Definition of done and required evidence.
- Verification commands or acceptance criteria.
- Handoff content and exact integration point.

Subagents do not inherit the full conversation. Supply the continuation-critical context explicitly. Never use vague assignments such as "analyze this" or "improve everything."

## Integration

The orchestrator must independently inspect the returned artifact, diff, or evidence; reconcile contradictions and duplication; run cross-component checks; and update the canonical state. An agent report is evidence to inspect, not proof of completion.

Never claim parallel execution, agent use, or tool use that did not occur or was unavailable.
