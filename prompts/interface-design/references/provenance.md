# Import provenance

Imported 2026-10-29 from [Dammyjay93/interface-design](https://github.com/Dammyjay93/interface-design/tree/2f9be3206855bcb2d1d0af262c8bae25cba6658d/.claude/commands) at immutable revision `2f9be3206855bcb2d1d0af262c8bae25cba6658d`.

- Upstream package path: `.claude/commands`.
- License: MIT; retained in [LICENSE](../LICENSE).

## Local changes

Renamed the two command files to Copilot .prompt.md files and namespaced prompt names/references; full prompt bodies preserved. Host tool names and visual verification require receiving-host adaptation.

[Original file receipt](upstream-files.json) maps every imported file to its source path, upstream Git blob, and pre-adaptation SHA-256 (imported_sha256). Unchanged bytes were checked against that Git blob. Adapted-file originals were fetched at the pin and checked against the receipt, allowing the explicitly recorded archive CRLF conversion for Windows launchers. Generated provenance is separate from upstream material.

## Runtime boundary

Import is storage, not installation or activation. Select this package explicitly through a task/profile. Use only tools already approved on the receiving host. Do not install MCP servers, global tools or hooks automatically. Source examples do not authorize external actions or runtime acquisition.

Requirements: Portable instructions; implementation/testing depends on the project and approved host tools.

Only when separately required by the selected task/host tools; no runtime included.
