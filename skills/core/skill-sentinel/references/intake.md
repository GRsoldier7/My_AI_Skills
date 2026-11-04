# Package and permission review

Review complete package contents: entry point, references, scripts, executable
assets, hooks, manifests, dependencies, network endpoints and update behavior.
Check exact source revision, license and any declared local modifications.
A legitimate documented adaptation is not automatically a compromise.

Record requested versus actually available operations, data classes,
credentials, outbound traffic, telemetry/local logs, persistence and destructive
actions. A read-only instruction cannot remove privileges from a powerful tool.
Profiles select skills; host permissions must enforce operational boundaries.

For curated packages, compare the complete package hash in the manifest. A
changed hash requires source review before refresh. Never fetch and execute an
installer from an unpinned branch as an intake shortcut.

Use findings as review evidence, not certification. State static versus executed
checks and unknown transitive/runtime behavior. Run positive and negative cases:
missing resources, denied tool access, malicious retrieved instructions,
cross-domain data, stale/conflicting sources and update/rollback behavior.

No automatic approval, production activation, privilege changes or data export
results from a clear static scan. Mark deployment-specific behavior unverified
until exercised with the actual permitted host and data scope.
