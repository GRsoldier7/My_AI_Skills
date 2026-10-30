# Design import security review

The 23 canonical design/engineering imports may remain **trial source packages** after bounded contextual review. **The raw SkillSpector gate failed and remains failed. No native engine, browser, hooks, MCP server, global configuration or other runtime activation is granted by this review.**

The isolated static scan used SkillSpector 2.12.0 at `54921c8c7c23008c8af2328d5ab492a904b6ece4`, with network disabled, read-only candidate input, empty home/credential environment and no LLM. All 23 scans completed; there were no candidate-code executions or model-provider uploads. Raw reports are local at `/tmp/skillspector-design-imports-20261029`; report/receipt hashes and exact package hashes are retained in [the dispositions](20261029%20-%20My%20AI%20Skills%20-%20Design%20Import%20Scan%20Dispositions.json).

The scanner reported 253 findings: 78 HIGH, 171 MEDIUM and 4 LOW; no CRITICAL finding. Eight packages have incomplete coverage. Every high-severity finding and every coverage exception was inspected and dispositioned; lower-severity matches remain recorded and are not represented as a clean runtime certification.

## What the findings mean

- Contextual matches include visual “identity,” chart “states,” physical keyrings, the “curl” of a photographed wave, negative security examples, and quoted injection text that the skills explicitly reject. Four zero-width characters in Emil’s plan template escape nested Markdown CSS fences; their surrounding source was reviewed. These are exact-source dispositions, not global rule suppressions.
- Impeccable’s stored hook/update references describe real configuration surfaces. The adapted entry and local wrappers disable automatic setup/acquisition. Its native engine and live browser/loopback operations have not been activated or certified; minified/browser parser gaps remain explicit.
- UIUX catalog rows include security examples and a nonexecuted maintenance test that inherits process environment before removing a test key. Offline search/design-system calls use local data and passed synthetic smoke checks. The catalog/fixture parser gaps remain unresolved coverage limitations.
- Taste’s optional `library/scenes.json` and scene demos are absent upstream at the pin. Its scene reference explicitly describes that state and `draw.mjs` checks existence before loading the catalog, falling back to an empty scene list. The complete published source was imported. Its browser helper also sweeps abandoned owner-tagged profiles in its temporary base and enables unsafe SwiftShader: require a dedicated task-local `TASTE_SKILL_TMP` and employer browser-flag review before activation.
- Playwright’s “delete state” match concerns browser authentication files. No auth state was created or deleted; the local entry requires scoped authorization for session cleanup/account actions and forbids runtime acquisition.

## Coverage kept visible

| Package | Coverage | Principal retained limit |
| --- | ---: | --- |
| `impeccable` | 87.1% | obfuscated_instruction_text, reference_missing, static_parse_limit |
| `ui-ux-pro-max` | 84.2% | obfuscated_instruction_text, reference_missing, static_parse_limit |
| `design-taste-frontend` | 73.8% | obfuscated_instruction_text, reference_missing, static_parse_limit |
| `dogum-html-artifacts` | 93.8% | reference_missing, static_parse_limit |
| `html-artifacts-offline` | 90.9% | static_parse_limit |
| `break-ui` | 80.0% | obfuscated_instruction_text, reference_missing |
| `review-animations` | 80.0% | static_parse_limit |
| `playwright-cli` | 92.9% | reference_missing, static_parse_limit |

The other fifteen packages report complete static coverage, although some also contain expected project/output paths that the reference resolver marks missing. Relative Markdown links and JavaScript imports were checked separately, and all source-directory files were compared with the pinned Git trees. Typical resolver matches are generated screenshots, project manifests, native API member names, version numbers and host installation paths. No required source was deleted or replaced to satisfy the scanner.

## Verification and limits

All 387 imported/authored files received the baseline audit. Frontmatter, JSON, YAML, TOML, Python AST, JavaScript syntax and shell syntax passed; relative links/imports and canonical names have no unresolved collisions. Original file receipts cover 329 upstream files. Synthetic UIUX search, CSS inlining and approved-binary-only shell launcher tests passed. Upstream whitespace is retained; `git diff --check` reports inherited whitespace warnings.

The separate Codex provider package, four Copilot agents, two prompts and six ChatGPT adaptations received source/syntax/link/secret checks, but this 23-package scan does not claim a separate scanner pass for those exports. Native engine/browser/Windows compatibility, live dependency intelligence and final receiving-host capabilities remain unverified.

Security audit: reviewed staged source adaptations, exact upstream/source hashes, local-only synthetic operations, scanner isolation and targeted secret patterns; no live credentials, private account data or session artifacts were added or sent externally. Raw scanner failure and runtime/coverage limitations remain open and visible.
