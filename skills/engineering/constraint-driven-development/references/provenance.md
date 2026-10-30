# Provenance and integration

Source: https://github.com/addyosmani/agent-skills/tree/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/constraint-driven-development

License: MIT; see `LICENSE` in the package root.

- Preserved the complete skill directory and root MIT license.
- Localized required shared checklists under references/shared and rewrote their paths.
- Renamed Addy TDD identity and internal references to addy-test-driven-development to preserve the existing Superpowers package.

Runtime and host support: Instruction package; use existing approved project tools when the selected workflow requires them.

Importing these instructions does not install tools, enable hooks, register MCP servers, grant access, or activate a service. Source examples remain subordinate to the current task and host policy.

## Floor-guard output adaptation — 2026-10-29

At the pinned upstream revision above, `references/floor-guard.md` promises never to report matched secret values but stores and prints changed source excerpts. The local adaptation removes those excerpts from findings and outputs only the fixed rule name and file path. This prevents a suppression or stub line containing a secret from being copied into scan logs. A synthetic mock verifies violation, clean, and unavailable-base outcomes without any live repository or credential input.
