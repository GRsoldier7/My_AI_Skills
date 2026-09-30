# Approval Boundaries

Load this reference before a risky, destructive, irreversible, production, external, paid, credential-sensitive, or materially scope-changing action.

## Proceed without another approval

Proceed when the action is all of the following:

- Within the already approved objective and architecture.
- Routine and reversible.
- Limited to the established workspace and permissions.
- Unlikely to affect production, external users, money, secrets, regulated data, or another contributor's work.
- Supported by a clear rollback or ordinary version-control recovery.

## Require explicit approval

Pause only the affected action before:

- Destructive or difficult-to-reverse file, repository, infrastructure, or data changes.
- Production deployment, rollback, restart, deletion, or access change not already authorized.
- Data migration, schema change, bulk update, or customer-data operation with material risk.
- External publication, message, ticket, purchase, subscription, or other action performed as the user.
- Reading, copying, rotating, exposing, or materially changing secrets, credentials, or sensitive data.
- Material changes to approved scope, architecture, security posture, cost, or operational ownership.
- Resetting, cleaning, overwriting, deleting, or claiming ownership of unknown uncommitted work.
- Creating, publishing, or materially modifying a reusable skill unless the user already requested that exact skill work.

## Unknown or dirty working tree

1. Inspect status and diff without altering them.
2. Identify ownership from available evidence.
3. Preserve all unknown work.
4. Use a separate branch or worktree when isolation is safe and useful.
5. Never run destructive cleanup merely to restore a tidy state.

## Approval request format

State only what the decision-maker needs:

- **Action:** exact command, change, or external effect.
- **Why now:** dependency or value unlocked.
- **Risk:** material failure modes and affected scope.
- **Reversibility:** rollback and evidence preserved.
- **Alternatives:** safer or deferred options.
- **Decision required:** one precise yes/no or option choice.

While approval is pending, mark the affected task `Blocked` and continue independent safe work.
