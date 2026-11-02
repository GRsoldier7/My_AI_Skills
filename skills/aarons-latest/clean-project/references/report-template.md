# Project Optimization Register

Report schema version: 2

Canonical cleanup register. Preserve CP IDs and decisions. Record observed
results only: "unknown", "not assessed", or "not run" beat inferred success.
No secrets; redacted locations only. Timestamps: ISO-8601 with local offset
(`date -Iseconds`).

## 1. Current assessment

| Field | Value |
|---|---|
| Last assessment (ISO-8601, local offset) | <timestamp> |
| Outcome | <clean, findings, or could-not-assess> |
| Repository | <identifier> |
| Revision and branch | <values or unavailable> |
| Working-tree condition | <clean, modified, or unavailable> |
| Mode | <audit, audit full, apply, or verify> |
| Assessed scope | <scope; change-aware base revision if used> |
| Exclusions and limits | <list or none> |
| Baseline | <passed, failed, partial, or not run; evidence> |
| Assessment completeness | <complete within scope, or partial: gaps> |
| Main conclusion | <evidence-backed; never a blanket security claim> |

### Coverage and evidence freshness

| Area | Method/tool and version | Coverage | Result | Evidence freshness (timestamp or unknown) | Limitation |
|---|---|---|---|---|---|

## 2. Prioritized findings

| ID | Category | Finding | Severity | Confidence | Status | Owner | Next action |
|---|---|---|---|---|---|---|---|
| <ID> | <category> | <summary> | <severity> | <confidence> | <status> | <owner or unknown> | <action> |

Categories: Security and privacy; Code and assets; Dependencies and
toolchains; Automation and infrastructure; Documentation and processes; Data
and compatibility; Performance and maintainability.

## 3. Finding details

One block per §2 row; resolved findings keep their evidence.

### <ID> — <Title>

| Field | Detail |
|---|---|
| Category | <category> |
| Status | <status> |
| First observed / last checked | <timestamps> |
| Affected paths and environments | <scope> |
| Observation | <what was found> |
| Evidence | <paths, commands, sanitized output, sources> |
| Contrary evidence and uncertainty | <what weakens it> |
| Risk | <impact and conditions> |
| Severity / confidence | <ratings and rationale> |
| Lifecycle trigger | <date or condition and source, or not applicable> |
| Proposed action | <retain, investigate, update, consolidate, archive, retire, delete> |
| Dependencies and blast radius | <consumers, prerequisites> |
| Approval | <authority and decision, or not approved> |
| Owner | <owner or unknown> |
| Validation plan | <checks> |
| Recovery plan | <recoverable state, procedure> |
| Completion evidence | <result or not completed> |
| Review date | <date or not assigned> |

## 4. Ordered action plan

| Order | Finding IDs | Action | Prerequisites | Approval | Validation gate | State |
|---|---|---|---|---|---|---|

## 5. Archive and retirement ledger

Completed actions only; proposals stay in §4.

| Record / finding ID | Original path or component | Action | Reason and usage evidence | Recovery reference | Date | Approval | Verification |
|---|---|---|---|---|---|---|---|
| <ID> | <path> | <archived, Git-retired, deleted> | <evidence> | <verified revision or destination> | <date> | <decision> | <result> |

### Recovery notes

Isolated-location procedure, tooling, limits, and whether recovery was tested.

## 6. Verification record

Results: passed, failed, blocked, not run; pre-existing failures apart.

| Check | Revision / environment | Baseline | Post-change result | Evidence | Limitation |
|---|---|---|---|---|---|

## 7. Accepted risks and deferred decisions

Acceptance needs an authorized owner, rationale, and review date.

| Finding ID | Decision or blocker | Authorized owner | Rationale | Mitigation | Review / expiry | Reopen trigger |
|---|---|---|---|---|---|---|

## 8. Run and decision history

One row per meaningful run, oldest first; no scanner output.

| Run / date | Revision | Mode and scope | Findings changed | Actions completed | Verification | Remaining blockers |
|---|---|---|---|---|---|---|
