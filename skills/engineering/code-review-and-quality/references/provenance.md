# Provenance and integration

Source: https://github.com/addyosmani/agent-skills/tree/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/code-review-and-quality

License: MIT; see `LICENSE` in the package root.

- Preserved the complete skill directory and root MIT license.
- Localized required shared checklists under references/shared and rewrote their paths.
- Renamed Addy TDD identity and internal references to addy-test-driven-development to preserve the existing Superpowers package.

Runtime and host support: Instruction package; use existing approved project tools when the selected workflow requires them.

Importing these instructions does not install tools, enable hooks, register MCP servers, grant access, or activate a service. Source examples remain subordinate to the current task and host policy.

## Review mutation boundary — 2026-10-29

At the pinned upstream revision above, Step 2 prescribes mutating source during review and restoring it from a copy. The local adaptation permits the experiment only when explicitly authorized in an isolated disposable checkout; read-only reviews and shared working trees remain untouched. Otherwise the reviewer reports the coverage concern and labels mutation testing not run. This is a local safety boundary, not a claim that upstream code is malicious.
