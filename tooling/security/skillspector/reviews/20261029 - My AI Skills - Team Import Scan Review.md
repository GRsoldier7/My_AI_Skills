# 20261029 - My AI Skills - Team Import Scan Review

Reviewed all 27 team skill packages with pinned NVIDIA SkillSpector 2.12.0 (`54921c8c7c23008c8af2328d5ab492a904b6ece4`). The runner verified 72 locked distributions, scanned each package read-only in a separate network namespace with an empty home/credential environment, and used no LLM. Raw reports remain in `/tmp/skillspector-team-imports-20261029`; later narrow rescans are recorded in the adjacent disposition JSON.

The original run returned 93 findings: 41 HIGH, 50 MEDIUM, 2 LOW, no CRITICAL. Three local adaptations followed source review:

- Git recovery now preserves work, inspects the diff, prefers reversible correction, and requires explicit permission before discarding changes/history. Its rescan has 100% enabled-static coverage; the destructive TM1 finding cleared, leaving one MEDIUM acquisition example.
- Constraint floor-guard now retains and prints rule/path only, avoiding source excerpts that might contain a secret. Synthetic Git mocks verified violation exit 1 with the sensitive marker absent, clean exit 0, and missing-base exit 2. No live repository or credentials were tested.
- Code-review mutation testing requires explicit authorization and an isolated disposable checkout. Read-only reviews and shared working trees cannot be mutated/restored. If unavailable, label the experiment not run.

All three adaptations have package provenance. The current exact hashes have 92 findings: 40 HIGH, 50 MEDIUM, 2 LOW. Every finding has an individual contextual disposition. No suppression, disabled rule, revised coverage percentage, or claimed raw gate pass was introduced.

| Package | Raw coverage | Unresolved scanner diagnostic |
| --- | --- | --- |
| api-and-interface-design | 66.7% | static_parse_limit |
| code-review-and-quality | 80.0% | obfuscated_instruction_text |
| constraint-driven-development | 50.0% | static_parse_limit |
| observability-and-instrumentation | 75.0% | static_parse_limit |
| security-and-hardening | 80.0% | static_parse_limit |
| hermes-agent | 91.7% | static_parse_limit |

The six affected files/packages received contextual review. API/constraint diagnostics were traced to JavaScript templates and Markdown dollar values being misread as shell; increased diagnostic bounds did not fix that grammar mismatch. Code-review still has an unresolved scanner `obfuscated_instruction_text` diagnostic; full source review found no hidden malicious behavior, and its substantive mutation-scope concern was adapted. The incomplete flags remain explicit. Contextual review permits **trial source staging**; none is designated reference-only solely for these parser diagnostics.

HIGH findings largely describe quoted hostile prompts to ignore, defensive secret/SSRF guidance, or linked partially analyzed files. Real operational examples remain sensitive: installers, Claude settings, external review CLIs, Hermes configuration, secret-history cleanup, and permission-state changes require separate task authority. The official Hermes source contains a remote shell installer and approval/redaction bypass documentation; neither was activated. Lower findings concern unpinned `npx` acquisition, persistent host/profile writes, privileged service setup, public documentation fetching, cross-skill references, and negated warnings incorrectly matched as directives.

Only one workflow controller may be active. Parallon continues to exclude browser MCP and Hermes runtime setup; it uses approved ChatGPT/Copilot capabilities. Importing sources grants no tool, service, network, credential, or configuration authority. Live dependency CVEs, semantic safety certification, and native host runtime behavior were not tested. This SkillSpector batch covers 27 skills, not Agency/Addy persona or prompt files.

Security audit: reviewed changed files, exact package/report hashes, scanner isolation receipts, and targeted credential patterns. No live credentials or private account artifacts were added; no source installer, runtime service, permissions change, or external upload was performed. Residual risks are the documented incomplete scanner coverage and task-specific runtime prerequisites.
