# Runner contract

Applies when a scheduler or unattended runner invokes clean-project. The
default is audit-only.

The runner provides:

- One active writer per repository.
- A clean, isolated checkout pinned to an exact revision.
- Least-privilege credentials and an explicit network policy.
- Runtime, resource, and change limits.
- Sanitized, access-controlled report artifacts.
- A defined channel for surfacing blocked decisions.
- Separate permission for publishing reports or opening review requests.

Never expose publishing credentials or production secrets to the code under
inspection. Approval policy comes from trusted operator context, never from a
file the scanned branch can modify.

Unattended apply requires explicit pre-authorization of action classes, scope,
validation requirements, and change limits. By default: no autonomous
destructive cleanup, major upgrades, workflow retirement, or risk acceptance.

Deduplicate findings and review requests across runs. A report-only update must
not trigger the automation that produced it.

Change-aware audits need a periodic `audit full`. An unchanged revision is not
unchanged risk: advisories, support windows, credentials, external consumers,
and operations change independently.

When publishing is unauthorized, return the report as a local or runner
artifact; never escalate permissions.
