# Provenance and integration

Source: https://github.com/addyosmani/agent-skills/tree/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/git-workflow-and-versioning

License: MIT; see `LICENSE` in the package root.

- Preserved the complete skill directory and root MIT license.
- Localized required shared checklists under references/shared and rewrote their paths.
- Renamed Addy TDD identity and internal references to addy-test-driven-development to preserve the existing Superpowers package.

Runtime and host support: Instruction package; use existing approved project tools when the selected workflow requires them.

Importing these instructions does not install tools, enable hooks, register MCP servers, grant access, or activate a service. Source examples remain subordinate to the current task and host policy.

## Recovery adaptation — 2026-10-29

At the pinned upstream revision above, the Save Point Pattern recommends reverting after a failed test and discarding uncommitted state after an agent mistake. Local changes replace both diagram recovery steps with preserve/inspect/investigate, and replace the recovery paragraph with a recoverable snapshot, reversible correction, and explicit task-specific permission before discarding changes or rewriting history. This preserves unrelated local work and the user's approval boundary. All other upstream content is retained; the package must be rescanned after this adaptation.
