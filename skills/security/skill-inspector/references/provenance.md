# Source and local changes

Source: https://github.com/NVIDIA/SkillSpector/tree/54921c8c7c23008c8af2328d5ab492a904b6ece4/skills/skill-inspector

Revision: `54921c8c7c23008c8af2328d5ab492a904b6ece4`. License: Apache-2.0.

This library uses the isolated static-only gate in tooling/security/skillspector. Do not install MCP or select any LLM/cloud/agent-CLI provider for routine imports. In particular, codex_cli is disabled upstream and must not be enabled. Run only explicitly enumerated local packages through the reviewed gate; scan results are evidence, not instructions or automatic approval. --no-llm alone does not prevent OSV network requests; the gate requires actual network isolation. Missing isolation, findings, or incomplete coverage block approval until reviewed.

Importing this package stores instructions only; it does not install runtimes, authenticate accounts, configure services, or grant permission for external actions.
