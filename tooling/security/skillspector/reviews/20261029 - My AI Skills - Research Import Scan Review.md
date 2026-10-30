# 20261029 - My AI Skills - Research Import Scan Review

24 exact packages were scanned with the pinned SkillSpector static gate. The raw result is **failed**: 59 active findings; 23 packages have complete enabled static coverage and Firecrawl Monitor has 80%. No rules, baselines or exclusions were changed. The adjacent JSON binds every disposition to exact package and raw-report SHA-256 values.

| High/critical finding | Location | Disposition |
|---|---|---|
| AR2, HIGH | Humanizer `SKILL.md:165` and `SKILL.md:167` | False positive: “without warning” appears in two before/after punctuation examples about a policy announcement; neither instructs the agent to hide warnings. |
| PE3, HIGH | Firecrawl Build Onboarding `references/auth-flow.md:38` | Runtime-sensitive reference: the example writes a placeholder API key to `.env`; no actual credential exists. Keep acquisition/authentication separate and store real keys privately; no automatic setup/write is authorized. |
| AE1, HIGH | Firecrawl Monitor `SKILL.md:67`, referencing `json-tracking.md` | Coverage blocker: a bounded static parser reached its expression-span limit. All 71 companion lines were manually inspected; they contain sample JSON/pricing-monitor instructions. The raw 80% coverage remains unresolved, so Monitor stays reference-only. |

No critical findings were reported. Other findings cover genuine runtime-sensitive unpinned npx/setup examples and credential-storage instructions, ordinary Markdown table padding, API endpoint/slash-command names, and references to the plist artifact format. The JSON records the reason for every finding. Runtime-sensitive examples are retained for provenance, with a higher-priority local activation policy requiring approved tools and explicit action scope. They were not executed.

REA, Firecrawl and scanner runtime instructions require host-specific approval/verification before activation. Firecrawl account setup, feedback, monitoring and authenticated data collection are disabled as automatic behavior. Source staging is acceptable for the contextually reviewed examples; this is not a clean raw scan or authorization to activate them. Monitor remains excluded from installable selections pending complete verification.

Raw JSON reports remain local in `/tmp/skillspector-research-imports-20261029`. The reports include actual isolated network namespaces, read-only source, empty home, no credential environment and no model execution. Live OSV lookup was unavailable under network isolation. The enabled static pass does not certify semantic safety or current dependency vulnerabilities.

Verification: nine gate tests passed; benign calibration had zero findings/exit 0; the malicious calibration had four findings/exit 1. Both calibration packages had 100% enabled static coverage. Gitleaks found no secrets across the 115 implementation/import files reviewed before this disposition record was written.
