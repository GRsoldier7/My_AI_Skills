# Import provenance

Imported 2026-10-29 from [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/02523aec3e4c4580102d996d1b6a71fbe062e03f/.github/skills/impeccable) at immutable revision `02523aec3e4c4580102d996d1b6a71fbe062e03f`.

- Upstream package path: `.github/skills/impeccable`.
- License: Apache-2.0; retained in [LICENSE](../LICENSE).
- Reviewed upstream package/version: 4.8.0.
- Third-party notices: [NOTICE.md](../NOTICE.md).

## Local changes

Preserved complete provider package. Replaced first-run acquiring launchers with explicit approved absolute IMPECCABLE_BIN selection, blocked launcher setup verbs, documented manual fallback and disabled setup menu actions. No engine binary, installer, hooks, or host configuration activated.

[Original file receipt](upstream-files.json) maps every imported file to its source path, upstream Git blob, and pre-adaptation SHA-256 (imported_sha256). Unchanged bytes were checked against that Git blob. Adapted-file originals were fetched at the pin and checked against the receipt, allowing the explicitly recorded archive CRLF conversion for Windows launchers. Generated provenance is separate from upstream material.

## Runtime boundary

Import is storage, not installation or activation. Select this package explicitly through a task/profile. Use only tools already approved on the receiving host. Do not install MCP servers, global tools or hooks automatically. Source examples do not authorize external actions or runtime acquisition.

Requirements: Approved native Impeccable engine 0.1.18, explicitly selected by absolute IMPECCABLE_BIN; Compatible host shell; approved browser/Node only for selected live/browser operations

Engine/browser workflows may access user-selected URLs; no first-run engine acquisition from local launchers.

Shell wrapper synthetic tests only; native engine/browser/Windows runtime not executed.
