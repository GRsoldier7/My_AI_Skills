# 20261029 - My AI Skills - Initial Import Scan Review

34 exact packages were scanned: six Anthropic, seven Matt Pocock, fifteen Superpowers, four ECC, one Karpathy, and the owner-authored connected HTML skill. All source hashes remained unchanged during the scan and review. The adjacent JSON records every finding with its file/line, rule, reason, package hash and raw report hash.

The **raw gate failed**: 61 findings (34 HIGH, 26 MEDIUM, 1 LOW, no CRITICAL). Twenty-six packages had complete enabled static coverage; eight retained limitations. No rules, exclusions, baselines or scanner runtime files were changed. Contextual review supports source staging under the existing trial/reference statuses; it does not authorize native activation or turn the raw result into a pass.

| Finding family | Context and disposition |
|---|---|
| Anti-refusal AR1/AR2 | Discernment's answer-before-nudge ordering, UI error copy, questionnaire recipient knowledge and neutral conflict reporting. None overrides the host's safety or authorization rules. |
| Theme PDF AE1/SC9 | Isolated PDF inspection found ten theme pages, no JavaScript, forms, encryption or embedded files. The binary static gap remains recorded. |
| Web builder AE1/SC9 | Archive inventory: 45 regular UTF-8 files and four directories, 115,785 expanded bytes; no links/devices/path escapes. Supplemental scan of the expanded source passed with zero findings and 100% enabled static coverage. The initializer still contains global pnpm installation and unpinned acquisition; do not run it automatically. |
| Superpowers TM1 | The two `git clean` matches warn about destruction. Push/PR examples require the user's selected option. Companion cleanup is real deletion: `stop-server.sh:113–114` checks a raw `/tmp/*` prefix, so it must not receive arbitrary paths. Destructive cleanup remains separately authorized. |
| Debugging PE3/E4 | Signing-identity/keychain metadata and local diagnostic logging examples. Limit to an authorized diagnosis, redact private outputs, and do not copy them into retained artifacts. |
| Skill authoring RA1/AS1 | Deliberate authoring and narrow skill-directory discovery, rather than hidden self-modification or credential access. Host configuration and destructive deletion remain outside implicit skill authority. |
| Coverage AE1 | JavaScript templates, Markdown fences and authoring examples trigger parser/projection limits. Focused manual review found no unexplained malicious payload. Raw limits remain visible; see the calibration note. |

The eight incomplete packages are `theme-factory` (92.3%), `web-artifacts-builder` (75%), `brainstorming` (77.8%), `executing-plans` (75%), `systematic-debugging` (91.7%), `test-driven-development` (66.7%), `writing-skills` (81.8%), and `connected-html-artifacts` (88.9%). Runtime-sensitive guidance requires approved tools and current task authorization. The browser companion, installers, Git publication, config changes, real-data connections and destructive cleanup were not run. Existing source-reference status for ECC Team Builder is preserved.

The connected snapshot's full HTML was reviewed: it reads a selected local CSV, uses `textContent`, bounds file size/rows, neutralizes spreadsheet formulas and has no network calls or external scripts. The parser mistakes its status-message JavaScript template at `examples/snapshot.html:92` for shell syntax. Browser functionality is separate owner verification.

Evidence remains private in `/tmp/skillspector-initial-imports-20261029`, `/tmp/skillspector-initial-supplemental-pdf`, `/tmp/skillspector-initial-supplemental-archive`, and `/tmp/skillspector-initial-archive-components-scan`. Each scan proved a separate unreachable network namespace, read-only input, empty home and credential-free environment; no LLM ran. Live OSV vulnerability lookup was unavailable. Document-provider records for docx/pdf/pptx/xlsx contain no redistributed implementation and were outside this package scan.

Security audit: review-only repository changes; canonical packages untouched. Exact-hash records contain public-source paths and contextual reasons, not credentials or raw private reports. Secret scan results are recorded with the commit handoff. These checks establish review evidence, not a guarantee of runtime safety.
