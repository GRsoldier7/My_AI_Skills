# Project Optimization Register

Report schema version: 1

This is the canonical working register for project cleanup, security,
maintenance, verification, and retirement decisions.

Preserve finding IDs and historical decisions. Record only observed results.
Use "unknown," "not assessed," or "not run" rather than inferred success.
Do not include secrets or unnecessarily sensitive data.

## 1. Current assessment

| Field | Value |
|---|---|
| Last assessment, UTC | <actual timestamp> |
| Repository | <project identifier> |
| Revision and branch | <actual values or unavailable> |
| Working-tree condition | <clean, modified, or unavailable> |
| Mode | <audit, apply, or verify> |
| Assessed scope | <actual scope> |
| Exclusions and limits | <explicit list or none> |
| Baseline | <passed, failed, partial, or not run; evidence link> |
| Assessment completeness | <complete within stated scope or partial> |
| Main conclusion | <evidence-backed summary, not a blanket security claim> |

### Coverage and evidence freshness

| Area | Method/tool and version | Coverage | Result | Evidence freshness | Limitation |
|---|---|---|---|---|---|
| <area> | <actual method> | <scope> | <result> | <timestamp or unknown> | <gap> |

## 2. Prioritized findings

Use stable IDs such as CP-0001. Order by justified urgency and dependencies.

| ID | Category | Finding | Severity | Confidence | Status | Owner | Next action |
|---|---|---|---|---|---|---|---|
| <ID> | <category> | <summary> | <severity> | <confidence> | <status> | <known owner or unknown> | <action> |

Canonical categories:
Security and privacy; Code and assets; Dependencies and toolchains;
Automation and infrastructure; Documentation and processes;
Data and compatibility; Performance and maintainability.

## 3. Finding details

Group findings under the canonical categories. Retain resolved findings with
their decisions and verification evidence.

### <ID> — <Title>

| Field | Detail |
|---|---|
| Category | <category> |
| Status | <status> |
| First observed / last checked | <actual timestamps> |
| Affected paths and environments | <scope> |
| Observation | <what was actually found> |
| Evidence | <paths, symbols, commands, sanitized output references, sources> |
| Contrary evidence and uncertainty | <what weakens or limits the conclusion> |
| Risk | <impact and required conditions> |
| Severity / confidence | <separate assessments and rationale> |
| Lifecycle trigger | <date or condition and source; or not applicable> |
| Proposed action | <retain, investigate, update, consolidate, archive, retire, delete> |
| Dependencies and blast radius | <affected consumers and prerequisites> |
| Approval | <required authority and actual decision, or not approved> |
| Owner | <known owner or unknown> |
| Validation plan | <specific checks> |
| Recovery plan | <recoverable state and safe procedure> |
| Completion evidence | <actual result or not completed> |
| Review date | <date or not assigned> |

## 4. Ordered action plan

| Order | Finding IDs | Action | Prerequisites | Approval | Validation gate | State |
|---|---|---|---|---|---|---|
| <order> | <IDs> | <bounded change> | <dependencies> | <state> | <checks> | <state> |

Keep proposed actions separate from completed changes.

## 5. Archive and retirement ledger

Record completed actions here. Proposed retirements remain in the action plan.
Distinguish archived, Git-retired, and deleted material accurately.

| Record / finding ID | Original path or component | Action | Reason and usage evidence | Recovery reference | Date | Approval | Verification |
|---|---|---|---|---|---|---|---|
| <ID> | <path> | <action> | <evidence link> | <retained revision or verified destination> | <date> | <decision> | <result> |

### Recovery notes

Document recovery into an isolated location. Include compatibility limitations,
required tooling, and whether recovery was actually checked.

Do not imply that retired code is safe or supported merely because it is
recoverable.

## 6. Verification record

Use outcomes: passed, failed, blocked, not run.
Identify pre-existing failures separately from regressions.

| Check | Revision / environment | Baseline | Post-change result | Evidence | Limitation |
|---|---|---|---|---|---|
| <check> | <context> | <result> | <result> | <sanitized reference> | <gap> |

## 7. Accepted risks and deferred decisions

| Finding ID | Decision or blocker | Authorized owner | Rationale | Mitigation | Review / expiry | Reopen trigger |
|---|---|---|---|---|---|---|
| <ID> | <decision> | <owner or unknown> | <reason> | <mitigation> | <date or not assigned> | <condition> |

Do not mark a risk accepted without an authorized decision.
Expired acceptances require renewed review.

## 8. Run and decision history

Append meaningful entries in chronological order. Do not copy complete scanner
output into this section.

| Run / date | Revision | Mode and scope | Findings changed | Actions completed | Verification | Remaining blockers |
|---|---|---|---|---|---|---|
| <run> | <revision> | <scope> | <IDs and changes> | <actual actions> | <summary> | <blockers> |
