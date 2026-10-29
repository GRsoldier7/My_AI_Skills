# Agent definitions

`ecc/` holds four MIT-licensed upstream personas: planner, architect, code-reviewer,
and security-reviewer. Provenance and hashes are in
[artifact-sources.json](../platform-configs/artifact-sources.json).

These are source definitions, not running agents. Keep procedures in `skills/`
and call them from a persona as needed. Hermes and Copilot need their own supported
tool mappings; do not copy Claude-specific tool fields into another host unchanged.
Use the [Hermes guide](../platform-configs/hermes/README.md) or
[Copilot guide](../platform-configs/copilot/README.md).
