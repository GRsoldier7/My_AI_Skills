# Investigation checklist

Mark each relevant area assessed or not assessed, with the reason; a listed
item is not evidence that a check ran.

## A. Code, assets, and runtime usage

- Code: imports, callers, inheritance, reflection, dynamic loading,
  subprocess, native, and cross-language calls.
- Conventions: routing, auto-discovery, plugin registries, dependency
  injection, config-selected implementations, filename lookups.
- Interfaces: package exports, CLI entrypoints, scripts, APIs, feature flags,
  fallbacks, emergency paths, compatibility shims.
- Assets: templates, localization, static and generated files, tests,
  fixtures, examples.

Search identifiers, paths, config keys, and aliases. Rarely run is not
unreachable; missing telemetry is not non-use; similar text is not equal
behavior. Keep tests whose targets merely look obsolete.

## B. Packaging, builds, and generated material

- Manifests, export maps, include/exclude rules, compiler roots, bundler and
  container contexts, release scripts, deploy globs, public serving. Inspect
  real build output when safe.
- Generated files: generator, inputs, version, regeneration command,
  consumers. Prove reproducibility before deletion; committed output may serve
  bootstrapping, offline use, or distribution.
- Ignored is not disposable: local databases, credentials, user exports, and
  unique artifacts are never "cache".

## C. Dependencies and toolchains

- Direct and transitive, prod and dev, workspaces, optional and peer
  dependencies, lockfile consistency, runtime support, package sources,
  integrity enforcement, install scripts.
- Keep apart: unused candidates, available updates, support-window risks,
  verified advisory matches, reachability questions. Dev-only is not
  risk-free.
- Upgrades follow the support policy, not the latest release. Pins need an
  update process. SBOMs only via approved tools.

## D. Automation, workflows, and operations

- CI/CD, scheduled jobs, hooks, task runners, release and deploy scripts,
  bots, infrastructure; their triggers, filters, manual dispatch,
  reusable-workflow consumers, artifacts, environment approvals.
- No recent runs may mean seasonal, manual, external, or emergency-only.
  Before retiring, check required status checks, branch protection, external
  callers, rollback dependencies, ownership. Unseen platform settings are not
  assessed. Never disable automation for looking idle.

## E. Security and privacy

- **Application:** authn/authz, tenancy, injection, deserialization, path
  traversal, request forgery, file handling, error leakage, insecure defaults,
  denial of service.
- **Secrets and data:** committed credentials, sensitive logs, sample config,
  personal data in fixtures, broad access, retention, public artifacts.
- **Supply chain:** advisories, untrusted sources, mutable references,
  lifecycle scripts, provenance, evidenced abandonment.
- **Automation:** untrusted pull-request execution, unsafe interpolation, token
  scope, cache/artifact trust, mutable third-party actions, approval bypass.
- **Infrastructure:** excess privilege, exposed services, insecure images,
  unsafe mounts, missing limits, open admin paths.
- **Lifecycle:** end-of-support dates, API removals, certificate or credential
  expiry, compatibility deadlines, stale exceptions.

Per finding: environment, conditions, evidence, assumptions. Rate severity and
confidence separately; critical or high needs an exposure rationale. Future
risks need a dated trigger and source, else they are hypotheses. Record tool
versions and advisory freshness; unknown is never "current". Secrets: redacted
location only; tree removal purges neither copies nor history, so track
rotation separately, with no unapproved external action. Archiving is not a
security boundary.

## F. Documentation, governance, and maintenance

- Setup, architecture, runbooks, ownership, support policy, links, release
  steps: verify against behavior; old is not wrong.
- Contradictory sources of truth: propose one owner. A neglected process may
  still serve retention, contracts, audits, or recovery.
- Performance claims need a concrete problem and a benchmark; no speculative
  rewrites or new tools.

## G. Retirement evidence gate

Before archiving, retiring, or deleting, establish:

1. **Identity:** exact paths, role, owner if known, proposed action.
2. **Internal usage:** callers, config, discovery, scripts, tests, build rules.
3. **Distribution and operations:** packaging, deploy, workflows, rollback.
4. **External obligations:** public interfaces, external callers, retention,
   compatibility windows.
5. **Verification:** baseline and post-change checks available, or their
   limits reviewed.
6. **Recovery:** a recoverable revision or archive recorded and checked to
   exist; recovery never overwrites current work.
7. **Authority:** within explicit approval and change limits.

Grade: **strong** (surfaces covered, no contrary evidence, obligations met,
validation and recovery adequate), **partial** (dynamic behavior, consumers,
settings, or validation uncertain), **insufficient** (age, naming, inactivity,
one search, or one tool). Only strong qualifies for routine approved
retirement; the others need more investigation or a documented, authorized
decision accepting the named uncertainty. Confidence is never proof of non-use.

## H. Archive and recovery policy

- Prefer Git-backed retirement when the pre-removal revision is retained;
  never copy what history already recovers.
- Record original path, action, reason, CP ID, recovery reference,
  compatibility notes, validation result.
- An in-repository archive sits outside discovery, builds, publication,
  deployment, and serving.
- Keep attribution, licensing, and retention data. Never archive live secrets,
  needless personal data, or dumps.
- A backup counts only when its content is shown present and readable. Recover
  into an isolated location or worktree, never over active changes.
