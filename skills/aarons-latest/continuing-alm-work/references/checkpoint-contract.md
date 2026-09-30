# Checkpoint Contract

## Canonical record selection

Use this order:

1. The state file or tracker explicitly named by the user.
2. The record named in project instructions or the accepted plan.
3. The existing active roadmap, issue tracker, project-state file, or handoff convention.
4. Conversation-only checkpoint when no authoritative writable record exists.

Do not create a second plan, duplicate tracker, or alternate handoff filename merely for convenience. Treat an old handoff as a resume hint, not authority; verify it against current repository, artifact, test, CI, deployment, and tracker state.

## Minimum state

Keep current:

- Project objective and accepted constraints.
- Active phase and current task.
- Last verified completed task.
- Status of relevant tasks.
- Decisions, assumptions, dependencies, and blockers.
- Artifacts created or modified.
- Verification performed and failures.
- Exact next action.
- Pending approvals and approved skill candidates.

## Exact resume marker

Use this block verbatim and replace every value with concise, verified content. Use `None` where appropriate.

```text
RESUME FROM:
- Phase:
- Task:
- Status:
- Last verified result:
- Exact next action:
- Required inputs:
- Relevant artifacts:
- Blockers:
- Pending approvals:
```

The next action must be executable and unambiguous. Separate verified facts from assumptions or unknowns. Name the canonical record updated, or state `Checkpoint: conversation-only`.

## Context-pressure interaction

If a host context warning or the `context-checkpoint` skill activates, it takes precedence over starting new work. Finish only the current atomic operation when required for workspace coherence, update the checkpoint, and stop according to that protocol.
