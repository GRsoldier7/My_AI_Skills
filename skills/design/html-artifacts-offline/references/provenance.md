# Import provenance

Imported 2026-10-29 from [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills/tree/516dee7a422b90937b2958d11c03694154ab9c09/html-artifacts) at immutable revision `516dee7a422b90937b2958d11c03694154ab9c09`.

- Upstream package path: `html-artifacts`.
- License: MIT; retained in [LICENSE](../LICENSE).

## Local changes

Namespaced frontmatter; CSS inliner resolves from explicit absolute skill base; replaced Linux-only delivery opener with documented host preview/native opener. Offline behavior and all CSS/references preserved.

[Original file receipt](upstream-files.json) maps every imported file to its source path, upstream Git blob, and pre-adaptation SHA-256 (imported_sha256). Unchanged bytes were checked against that Git blob. Adapted-file originals were fetched at the pin and checked against the receipt, allowing the explicitly recorded archive CRLF conversion for Windows launchers. Generated provenance is separate from upstream material.

## Runtime boundary

Import is storage, not installation or activation. Select this package explicitly through a task/profile. Use only tools already approved on the receiving host. Do not install MCP servers, global tools or hooks automatically. Source examples do not authorize external actions or runtime acquisition.

Requirements: Optional approved Python 3 for CSS inliner; standard library only; Host-supported file delivery/browser preview

Generated deliverable is offline; no CDN, fetch, remote fonts or runtime server required.

Synthetic CSS inliner success and non-mutating missing-slot failure passed.
