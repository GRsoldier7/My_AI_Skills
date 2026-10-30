# Import provenance

Imported 2026-10-29 from [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli/tree/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli) at immutable revision `b85c7a736bb473bf55b584e54a09ffa698d6d871`.

- Upstream package path: `skills/playwright-cli`.
- License: Apache-2.0; retained in [LICENSE](../LICENSE).
- Reviewed upstream package/version: 0.1.22.

## Local changes

Removed unrestricted allowed-tools declaration and runtime bootstrap. Require approved preinstalled CLI/browser with NO_UPDATE_NOTIFIER=1; all fallback npx commands use --no-install. Existing project testing only; explicit session/privacy boundaries. Full references retained.

[Original file receipt](upstream-files.json) maps every imported file to its source path, upstream Git blob, and pre-adaptation SHA-256 (imported_sha256). Unchanged bytes were checked against that Git blob. Adapted-file originals were fetched at the pin and checked against the receipt, allowing the explicitly recorded archive CRLF conversion for Windows launchers. Generated provenance is separate from upstream material.

## Runtime boundary

Import is storage, not installation or activation. Select this package explicitly through a task/profile. Use only tools already approved on the receiving host. Do not install MCP servers, global tools or hooks automatically. Source examples do not authorize external actions or runtime acquisition.

Requirements: Approved installed @playwright/cli 0.1.22 or compatible existing project Playwright CLI; Approved installed browser; no MCP required

Browser requests only to task-selected destinations; CLI update notifier disabled with NO_UPDATE_NOTIFIER=1.

Syntax/resource/static instruction checks only; no actual CLI/browser/session run.
