# 20261121 - My AI Skills - Enterprise Work Skills

Select one pack for the job. Paste or attach its `INSTRUCTIONS.md` in the approved ChatGPT Enterprise chat. Give GitHub Copilot the instructions and the relevant sanitized code or schema. The read brief can use a previously approved work reader on a surface where it is exposed. Other packs produce specifications, code drafts and tests. Keep live administration and deployment with the authorized operator.

| Job | Pack | First deliverable |
| --- | --- | --- |
| Morning triage or meeting prep | `work-read-brief` | Decisions, open requests, scheduled times and original source references from Outlook and SharePoint |
| Validate a KPI or diagnose a slow report | `work-bi` | A reconciled DAX measure, Power Query checks and a model/refresh investigation |
| Review a BigQuery job or a stale cloud-to-BI pipeline | `work-gcp` | GoogleSQL, expected totals, partition and cost checks, and an evidence-based escalation |
| Improve Python, SQL Server SQL, PowerShell or general code | `work-code` | A focused patch with a regression case and an explicit failure case |
| Improve a prompt, skill or plugin | `work-ai` | Baseline, revised instructions, activation and near-miss checks |
| Build a reusable ChatGPT workflow or Space | `work-chatgpt` | Skill or plugin draft, a page map, ownership and a manual fallback |
| Export, import and release a canvas app or cloud flow | `work-apps-flows` | A managed release, target-specific settings and a clean-install, upgrade and first-user test |
| Prepare shared decisions and team notes | `work-collaboration` | SharePoint record, Loop working decision and OneNote meeting evidence |
| Choose the right Copilot | `work-copilot` | GitHub Copilot review, 365 drafting or a Copilot Studio test plan matched to available features |
| Build an HTML or internal web artifact | `work-web-artifacts` | An accessible offline brief or a hosting decision for Power BI, SPFx or Power Apps |

Run `python scripts/skill-picks.py inspect work-read-brief` for scope. To create a new pack, run `python scripts/skill-picks.py export work-read-brief --platform chatgpt --output ./my-read-brief` from the checkout. Replace the profile or use `--platform copilot` for the corresponding work host. Each export includes a source inventory, licenses and a SHA-256 receipt. The active instructions load the reviewed work sections. Public packages contain reusable instructions and synthetic examples. Store organization-specific data in the approved private workspace.

## Source choices

| Source | Material carried into the packs | Reason for the selection |
| --- | --- | --- |
| [Google Skills](https://github.com/google/skills/tree/4bb21ebfa085f6307d5d62bc21765e1d3433f11d/skills/cloud/bigquery-optimization) | BigQuery SQL optimization reference and Apache-2.0 license | Use the query patterns with a bounded reporting task. Consult Google's observability and troubleshooting guides for deeper diagnosis. |
| [Microsoft Skills for Fabric](https://github.com/microsoft/skills-for-fabric/tree/540c3c58abc804c2715c6632026784f04b342388/skills/semantic-model-authoring/references) | DAX guidelines, metadata discovery and MIT license | Helps when a model owner supplies DAX or metadata. The manual pack works without Fabric deployment, refresh or write access. |
| [Microsoft Work IQ](https://github.com/microsoft/work-iq/tree/206072a88695f14000fc72cddcd5f2f40871ba01/plugins/workiq/skills/workiq/references) | Mail read, calendar read, SharePoint search, MIT license and notices | Three focused references cover the reader's real evidence. The host-specific work instructions control access and citation behavior. |
| [GitHub Awesome Copilot](https://github.com/github/awesome-copilot/tree/f10fdb8b2660ce85c98f220b2f1ca24653768a5c/instructions) | PowerShell, safe T-SQL, prompt format and MIT license | Useful conventions for the specific code-review host. |
| [Wshobson Agents](https://github.com/wshobson/agents/tree/0f73766f80b0b5eb6aa9faaa2fdf90df85a6793f/plugins/python-development/skills/python-testing-patterns) | Python testing guide, its two references and MIT license | A practical testing shelf for transforms and replay cases. |
| [Anthropic Skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/frontend-design) | Frontend design direction and Apache-2.0 license | Complements a working offline template and accessibility checks. Its guide is a reference so its trigger does not collide with another frontend skill. |

The catalog already has Prompt Master, a skill creator, data validation and regression-evaluation skills. The work instructions adapt those jobs to short, repeatable trials. Impeccable and React-focused guidance remain candidates for larger frontend projects. Promptfoo is an option when an authorized environment needs automated evaluation at higher volume.

## Acceptance and maintenance

- Replay the read brief with one duplicated email, one private calendar block, an approved document and a newer draft. Require source-level citations, partial coverage when appropriate, and a clear distinction between a proposed and a scheduled meeting.
- Reconcile two disjoint groups of 1/2 and 2/8 to 3/10. Preserve an undefined result for a zero denominator. For an existing BI model check slicers, grand totals, data quality and effective visibility in the receiving tenant.
- Open the standalone HTML from the web pack. Check all areas, one area, zero eligibility, keyboard focus, small screens, print and the no-JavaScript table. Keep live tenant, connector and hosting tests separate.
- For Power Platform, use the standalone `scripts/check-solution.py` included in the flow package, then rehearse a clean QA import and an upgrade from the previous release. Check the linked app and flow as an ordinary target user. The preflight does not establish production readiness on its own.
- Run `python scripts/check-library.py` after an update. The portable suite verifies upstream file integrity and all supported profile/host exports. The Linux workflow also runs the standalone browser check with its installed Chrome and ChromeDriver.
- To update an upstream, review its license and changed behavior, refresh the pinned files and Git blob IDs in `registry/curation.json`, and repeat the tests. Export to a fresh folder and keep the previous receipt for rollback. No new configuration is required in the work tenant.

## Offline release evidence

Microsoft Power Platform CLI 2.6.3 generated deployment settings directly from two pinned public examples. The [Microsoft staging and import sample](https://github.com/microsoft/PowerApps-Samples/tree/81d1364ff6ac4d4f94ba2719d308efc31995059e/dataverse/orgsvc/CSharp/SolutionStagingAndImport) contained a managed solution, version 1.0.0.1. The CLI unpacked it and repacked its managed source. The preflight accepted the original ZIP with its recorded SHA-256 and synthetic target mappings. The [PnP SharePoint upload sample](https://github.com/pnp/powerplatform-samples/tree/fce58178ed5a99e80c47e5cc9c98062e2fc9e963/samples/upload-to-sharepoint) contained a canvas app and a cloud flow. PAC generated settings from it, and the release preflight rejected its unmanaged manifest. A repack can change the ZIP hash. Production promotion uses the original QA-tested bytes. These were local checks and did not contact a Dataverse environment.
