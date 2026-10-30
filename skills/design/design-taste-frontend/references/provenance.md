# Import provenance

Imported 2026-10-29 from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill/tree/12af471f627f866411b4bd785b19646d3672784c/skills/taste-skill) at immutable revision `12af471f627f866411b4bd785b19646d3672784c`.

- Upstream package path: `skills/taste-skill`.
- License: MIT; retained in [LICENSE](../LICENSE).
- Reviewed upstream package/version: 2.1.5.

## Local changes

No upstream source changes. Folder uses existing upstream frontmatter name design-taste-frontend. Root license and import provenance bundled.

[Original file receipt](upstream-files.json) maps every imported file to its source path, upstream Git blob, and pre-adaptation SHA-256 (imported_sha256). Unchanged bytes were checked against that Git blob. Adapted-file originals were fetched at the pin and checked against the receipt, allowing the explicitly recorded archive CRLF conversion for Windows launchers. Generated provenance is separate from upstream material.

## Runtime boundary

Import is storage, not installation or activation. Select this package explicitly through a task/profile. Use only tools already approved on the receiving host. Do not install MCP servers, global tools or hooks automatically. Source examples do not authorize external actions or runtime acquisition.

Requirements: Approved Node 22+; Installed approved Chrome, Edge or Chromium for rendering/inspection

assets.mjs searches/downloads public image collections; selected URLs are visible to those services. Never include private material in queries.

Node syntax and relative imports checked; no browser launched or asset service contacted.

Receiving-host review requirements: set `TASTE_SKILL_TMP` to a dedicated task-local directory before any browser script; the CDP helper sweeps abandoned `ad-chrome-*` directories in that base using its owner-file check. Never point it at a shared/system temporary base. Review the helper's `--enable-unsafe-swiftshader` flag under employer browser policy before activation. Browser screenshots, local profile cleanup and public image-service requests have not been exercised here.
