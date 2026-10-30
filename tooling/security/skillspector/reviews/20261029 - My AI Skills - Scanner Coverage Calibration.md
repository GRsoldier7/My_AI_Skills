# 20261029 - My AI Skills - Scanner Coverage Calibration

SkillSpector v2.12.0 is pinned at `54921c8c7c23008c8af2328d5ab492a904b6ece4`. Its `static_parse_limit` label covers unsupported grammar and quote ownership as well as actual size exhaustion. Raising a time limit cannot resolve all of these findings.

At this pin, `nodes/analyzers/static_patterns_tool_misuse.py:86–91` hard-codes command-word, command-span and static-printf bounds of 4,096, 8,192 and 256 characters. No CLI/environment option exposes these bounds. `SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT` changes runtime allowance only. The pinned environment and production runner were not patched.

An isolated diagnostic imported the scanner parser, treated candidate text strictly as data, and traced the return causing incompleteness. A second invocation changed the three bounds to eight times their values in that process's memory only. Both ran without network/credentials and with read-only source. This was a diagnostic experiment, not a passing replacement scan or a supported scanner configuration.

| Package and source | Trigger | Result with larger bounds |
|---|---|---|
| Firecrawl Monitor `json-tracking.md:5` | Inline prices containing dollar signs read as dynamic shell words; parser return at line 2402 | Still incomplete |
| API and Interface Design `SKILL.md:165` | JavaScript interpolation template read as shell; parser return at line 2376 | Still incomplete |
| Constraint Driven Development `SKILL.md:120` and `references/floor-guard.md:167` | Preview URL in a Markdown table and JavaScript report template; returns at lines 2402/2376 | Still incomplete |
| Connected HTML `examples/snapshot.html:92` | JavaScript status template; return at line 2376 | Still incomplete |
| Systematic Debugging `condition-based-waiting.md:74` | JavaScript timeout-message template; return at line 2402 | Still incomplete |
| Test Driven Development `SKILL.md:162` | A Markdown fence consumes a later lexical span; return at line 2335 | Diagnostic resolves this case only |

Do not disable the analyzer, mask examples, or silently promote these results to complete. Keep the original reports and hash-bound manual dispositions. A future parser fix needs a separately reviewed upstream/local patch, regression tests for benign JavaScript/Markdown and genuinely dangerous shell forms, fresh malicious calibration, and new receipts. No such scanner fork is introduced here.

The separate `obfuscated_instruction_text` gaps in some Markdown were manually reviewed as visible workflow/authoring material; their precise projection trigger remains unproven. They remain raw incomplete results, not certified false negatives. Source staging can be accepted contextually with runtime constraints. Firecrawl Monitor remains reference-only and inactive, as selected by the library owner.

Diagnostic evidence: `/tmp/skillspector-parser-{monitor,api,constraint,html,debugging,tdd}-diagnostic/diagnostic.json`. No candidate script, provider, cloud model or MCP server ran. This is deterministic scanner calibration and review guidance, not model fine-tuning.
