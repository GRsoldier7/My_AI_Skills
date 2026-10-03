# Investigation checklist

Use the sections relevant to the repository. Mark areas not assessed and
explain why. A checklist item is not evidence that a check was performed.

## A. Code, assets, and runtime usage

Investigate direct and indirect usage:

- Imports, exports, callers, inheritance, reflection, and dynamic loading.
- Framework conventions, routing, automatic discovery, plugin registries,
  dependency injection, and configuration-selected implementations.
- Public package exports, command-line entrypoints, scripts, and supported APIs.
- Templates, localization, static assets, generated code, and filename-based
  lookups.
- Native bindings, subprocess calls, shell scripts, and cross-language use.
- Tests, snapshots, fixtures, examples, benchmarks, and documentation examples.
- Feature flags, fallback paths, emergency procedures, and compatibility shims.

Search using identifiers, paths, filenames, configuration keys, and aliases.
Inspect relevant build and runtime conventions instead of relying on one grep.

Distinguish unreachable code from rarely executed code. Absence of runtime
telemetry is not proof of non-use, especially with incomplete observation.

For duplicate implementations, compare behavior and consumers before proposing
consolidation. Similar text does not establish equivalent behavior.

Do not remove tests simply because their targets look obsolete; they may define
supported behavior or expose a mistaken retirement assumption.

## B. Packaging, builds, and generated material

Check package manifests, export maps, include/exclude rules, compiler roots,
bundler configuration, container contexts, image copies, release scripts,
deployment globs, and public asset serving.

Inspect actual build or package outputs when safely possible.

For generated material, identify the generator, inputs, required version,
regeneration command, and consumers. Verify reproducibility before deletion.

Determine whether generated files are intentionally committed for bootstrapping,
offline use, distribution, review, or environments lacking the generator.

Review ignored outputs without assuming ignored files are disposable. Never
delete local databases, credentials, user exports, or unique artifacts under
the label "cache."

## C. Dependencies and toolchains

Inspect direct and transitive dependencies, production and development usage,
workspace boundaries, optional and peer dependencies, and lockfile consistency.

Check declared runtime support, reproducibility, package-source configuration,
registry access, integrity enforcement, and installation scripts.

Separate:
- Unused dependency candidates.
- Available updates.
- Compatibility or support-window risks.
- Verified advisory matches.
- Reachability and exposure questions.

Do not equate development-only with risk-free or an advisory match with proven
application exploitability.

Evaluate upgrades against the project's support policy. Prefer supported,
compatible versions over automatic adoption of the newest release.

Immutable version or digest pins should have an update process; pinning alone
does not address vulnerabilities discovered later.

Generate or update inventories and SBOMs only through approved existing tools
when they add concrete value. Avoid redundant compliance artifacts.

## D. Automation, workflows, and operational processes

Inspect CI/CD, scheduled jobs, local hooks, task runners, release automation,
deployment scripts, maintenance jobs, bots, and infrastructure definitions.

Check triggers, branch and path filters, matrix jobs, manual dispatch,
reusable-workflow consumers, artifact dependencies, and environment approvals.

A workflow without recent runs may be seasonal, manual, externally invoked,
or required for emergency recovery.

Before retirement, assess required status checks, branch protection, external
callers, deployment dependencies, rollback procedures, and ownership.

Distinguish what is visible in repository files from settings or consumers that
require external evidence. Mark inaccessible platform settings not assessed.

Do not disable automation solely because it appears idle.

## E. Security and privacy

Assess relevant risks in:

**Application behavior**
Authentication and authorization, tenant boundaries, injection, unsafe
deserialization, path traversal, request forgery, file handling, error leakage,
insecure defaults, and denial-of-service exposure.

**Secrets and data**
Committed or exposed credentials, sensitive logs, unsafe sample configuration,
personal data in fixtures, overly broad access, retention gaps, and publicly
served artifacts.

**Supply chain**
Dependency advisories, untrusted sources, mutable references, lifecycle scripts,
artifact provenance, excessive update permissions, and abandoned critical
dependencies when supported by evidence.

**Automation**
Untrusted pull-request execution, unsafe interpolation, token permissions,
secret exposure, cache or artifact trust boundaries, mutable third-party
actions, and deployment approval bypasses.

**Infrastructure and containers**
Excessive privileges, exposed services, insecure images or configuration,
unnecessary capabilities, unsafe mounts, missing resource boundaries, and
unprotected administrative paths.

**Foreseeable lifecycle risks**
Documented end-of-support dates, announced API removals, certificate or
credential expiry, compatibility deadlines, stale exceptions, and dependencies
on services scheduled for retirement.

For each finding, identify the affected environment, required conditions,
observed evidence, and unresolved assumptions.

Use separate severity and confidence assessments:

Severity: critical, high, medium, low, informational.
Confidence: verified, probable, uncertain.

Critical or high severity requires a defensible impact and exposure rationale.
Uncertainty should remain visible, not be hidden in a precise-looking score.

For future risks, record the trigger or date and its source. Label unsupported
possibilities as hypotheses, not discovered vulnerabilities.

For suspected secret exposure, record redacted location metadata only. Removing
a secret from the current tree does not invalidate copies or remove Git history.
Track rotation, revocation, exposure assessment, and any approved history
remediation separately. Do not perform those external actions without approval.

Archived code still matters for secrets, licensing, distribution, and accidental
execution. Archiving is not a security boundary.

## F. Documentation, governance, and maintenance

Inspect onboarding, setup commands, architecture notes, runbooks, ownership,
support policies, examples, internal links, and release instructions.

Verify stale instructions against actual project behavior when safe. Do not
rewrite documentation solely because its last edit is old.

Identify contradictory sources of truth and propose consolidation with clear
ownership.

Check whether neglected processes are obsolete, undocumented but necessary,
or still required for retention, contracts, audits, migrations, or recovery.

For performance and maintainability recommendations, identify a concrete
problem. Benchmark performance claims. Avoid speculative rewrites, premature
abstractions, and adding tools without a demonstrated need.

## G. Retirement evidence gate

Before archiving, retiring, or deleting a candidate, establish:

1. Identity and scope
   Exact paths, role, owner when known, and proposed action.

2. Internal usage
   Relevant imports, callers, configuration, discovery conventions, scripts,
   tests, build rules, and indirect consumers have been investigated.

3. Distribution and operations
   Packaging, deployment, workflow, rollback, and operational consumers have
   been assessed.

4. External and compatibility obligations
   Public interfaces, external callers, old clients, retention rules, supported
   upgrade paths, and compatibility windows have been considered.

5. Verification
   Suitable baseline and post-change checks are defined and available, or
   limitations have been explicitly reviewed.

6. Recovery
   A recoverable revision or authorized archive is recorded and its existence
   is checked. Recovery must not overwrite current work.

7. Authority
   The action is within explicit approval and change limits.

Classify evidence as:

**Strong**
Relevant usage surfaces are covered, no contradictory evidence remains,
external obligations are addressed where applicable, and validation and
recovery are adequate.

**Partial**
Some evidence supports retirement, but dynamic behavior, external consumers,
operational settings, or validation remain uncertain.

**Insufficient**
The conclusion rests mainly on age, naming, inactivity, one search, or one tool.

Only strong evidence is eligible for routine approved retirement. Partial or
insufficient evidence requires further investigation or a separately documented
authorized decision accepting the specific uncertainty.

Never translate confidence into a claim of mathematical proof of non-use.

## H. Archive and recovery policy

Prefer Git-backed retirement for normal tracked project material when the
pre-removal revision is retained and retrievable.

Record the original path, action, reason, finding ID, recovery revision or
archive destination, compatibility considerations, and validation result.

For in-repository archives, verify that the new location does not remain inside
automatic discovery, compilation, package publication, deployment, or public
serving paths.

Avoid duplicating entire directories when existing version history already
provides recovery.

Preserve required attribution, licensing, and retention information.

Do not archive live secrets, unnecessary personal data, or sensitive dumps.
A secret-related finding requires its own containment and remediation process.

Never treat a backup as verified merely because a path or URL exists. Establish
that the intended recovery material is actually present and accessible within
authorized means.

Describe recovery into an isolated location or worktree. Do not use a restore
procedure that silently overwrites active user changes.
