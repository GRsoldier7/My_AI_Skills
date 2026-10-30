# 20261029 - My AI Skills - Library Organization and Expansion Plan

Implementation annex to [Architecture and Delivery Plan](<20261025 - My AI Skills - Architecture and Delivery Plan.md>). User authorized saving, implementation, and feature-branch synchronization on October 29, 2026. Live account activation, employer-device installation, production data connections, and main merge remain separate.

## 1. Structure and source of truth

Use Master_Skills as the local canonical library, synchronized with [My_AI_Skills](https://github.com/GRsoldier7/My_AI_Skills). Preserve GitHub's newer catalog, the existing backup, and all unpublished local work.

| Area | Contents |
|---|---|
| `skills/<capability>/<skill>/` | Reusable procedures and complete supporting references, scripts, and assets |
| `agents/<collection>/` | Specialist personas and team roles |
| `prompts/` | Reusable task prompts and command workflows |
| `platform-configs/` | Domain selections, platform adapters, plugin manifests, and export instructions |
| `tooling/` | Scanners, runtime integration records, and experimental tooling |
| `evals/` | Synthetic examples, behavior checks, and scanner calibration fixtures |
| `docs/` | Generated catalog, usage guide, provenance explanations, and sync receipts |

Keep one canonical copy of each package. Parallon, Consulting, E7, Home, Learning, and Hermes Teams select shared packages through profiles. Extend the existing manifests and generate an index showing purpose, source, immutable revision, license, hash, location, domains, supported platforms, runtime requirements, status, recommended use, and overlapping alternatives. Preserve the fixed seven-skill project-router distributor.

## 2. Package placement

### Design and HTML artifacts

Make the whole collection available across domains through task-specific selections.

| Package | Canonical placement | Role |
|---|---|---|
| [Impeccable](https://github.com/pbakaus/impeccable) | `skills/design/impeccable/` | General interface design/refinement and Agent Teams design role |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `skills/design/ui-ux-pro-max/` | Searchable local design reference |
| [Interface Design](https://github.com/Dammyjay93/interface-design) | `skills/design/interface-design/` | Dashboards, business applications, forms, data interfaces |
| [Taste](https://github.com/Leonxlnx/taste-skill) | `skills/design/design-taste-frontend/` | Expressive marketing/product pages and team specialist |
| [Dogum HTML Artifacts](https://github.com/dogum/html-artifacts) | `skills/design/dogum-html-artifacts/` | Interactive reports/tools with approved services |
| [Josh Thomas HTML Artifacts](https://github.com/joshuadavidthomas/agent-skills/tree/main/html-artifacts) | `skills/design/html-artifacts-offline/` | Offline explanations, comparisons, walkthroughs, presentations |
| [Emil Kowalski](https://github.com/emilkowalski/skills) | Design category; write-swift in engineering | All 16 packages, including complete companion files |
| Anthropic Frontend Design | Existing engineering package | Reuse lightweight alternative already imported |
| [Playwright CLI](https://github.com/microsoft/playwright-cli) | `skills/engineering/playwright-cli/` | Browser interaction and visual verification |

Preserve both distinct HTML implementations with unique names. Rename Emil's prototype directory/frontmatter to emil-prototype; preserve Aaron's existing prototypes. Record provider-path, platform-opening, and unavailable-runtime adaptations. Retain licenses and supporting assets.

Defaults: Impeccable for general design; Interface Design for business interfaces; Dogum for interactive artifacts; Josh Thomas for explicitly offline documents; Taste when expressive visual direction warrants it. UI UX Pro Max, Emil, and Playwright supply focused supporting capabilities. Do not activate competing creators automatically.

### Writing, engineering, research, and teams

| Source | Placement and treatment |
|---|---|
| [Humanizer](https://github.com/blader/humanizer) | Refresh existing skills/core/humanizer in place; shared writing selections |
| [REA](https://github.com/morluto/rea) | Complete reverse-engineer-anything engineering skill; separate CLI record |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Official operating skill in engineering; extend Hermes platform guidance |
| [Agency Agents](https://github.com/msitarzewski/agency-agents) | Full persona collection under agents/agency/<division>; generated roster |
| [Addy Osmani](https://github.com/addyosmani/agent-skills) | All 25 skills, four personas, nine command workflows in their proper sections |
| [Firecrawl](https://github.com/firecrawl/firecrawl) | Official firecrawl/skills catalog: research skills under research, build skills under engineering |
| [Autoresearch](https://github.com/karpathy/autoresearch) | tooling/research/autoresearch plus a bounded Agent Teams workflow |
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | tooling/security/skillspector plus skills/security/skill-inspector |

Addy packages must include their shared references within distributable packages; rename its TDD identity to addy-test-driven-development. Firecrawl gets optional Consulting/E7 research and integration profiles, complete core/build packages and market/competitive/lead-research recipes. Application servers remain external runtime references.

Preserve earlier imports: internal-comms for Parallon/Consulting/E7; shared artifacts across domains; Academy Guide and productivity for learning/productivity; Superpowers and Karpathy for coding; ECC for teams. Keep DOCX/PDF/PPTX/XLSX provider-authorized/reference-only licensing treatment.

### Reviewed source baselines

| Source | Immutable revision |
|---|---|
| Impeccable 4.8.0 | 02523aec3e4c4580102d996d1b6a71fbe062e03f |
| UI UX Pro Max | 28b3b8dee8c976df4fa3e94aed4e092ad43fcb03 |
| Interface Design | 2f9be3206855bcb2d1d0af262c8bae25cba6658d |
| Taste 2.1.5 | 12af471f627f866411b4bd785b19646d3672784c |
| Dogum HTML Artifacts 2.0.0 | d54982f5da13392481f122b533b4ab9a8b2dc3d9 |
| Josh Thomas HTML Artifacts | 516dee7a422b90937b2958d11c03694154ab9c09 |
| Emil Kowalski | a81dbca07f2217b7103e510c0f13f8d5b017afc9 |
| Playwright CLI 0.1.22 | b85c7a736bb473bf55b584e54a09ffa698d6d871 |
| Humanizer 3.1.0 | 225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8 |
| REA 6.8.0 | 160d821ac9a0310afcb8d1fc427862dd6508add5 |
| Hermes 0.22.5 | bf0203a794a07aac3ff764972ab9087baa4e4f4e |
| Agency Agents | b37b5bb33b78f2c1d6567d98e25ca818e3259219 |
| Addy Osmani 0.6.14 | eb07f19f52c2669f2364897aaa293e2aaddd7b1c |
| Firecrawl skills | 2bf714d9f45e85085036a533ceb943c8577aef2b |
| Firecrawl CLI 1.26.24 | a9a46fe23af001d726a05d8448d25a7188b42fdc |
| Autoresearch | 228791fb499afffb54b46200aca536f79142f117 |
| SkillSpector 2.12.0 | 54921c8c7c23008c8af2328d5ab492a904b6ece4 |

## 3. Platform and Agent Teams delivery

Parallon ChatGPT receives portable skills/plugin instructions and references. Runtime packages need labeled reduced-capability adaptations; never claim browser/native-engine/OAuth/live connectivity without actual-host evidence. Parallon Copilot receives selected workspace skills, agents and prompts using approved tools, without MCP, automatic hooks, global installation or first-run binary acquisition.

- Impeccable: approved engine or documented manual fallback. Preserve matching provider package variants; do not use unresolved source templates.
- UI UX Pro Max: approved Python for search, reference guidance otherwise.
- REA: approved CLI-only work adapter; no automatic MCP setup/repair or engine acquisition.
- Addy Chrome DevTools MCP skill: catalogued but excluded from Parallon exports. Playwright supplies browser QA.
- Playwright: pinned approved CLI/browser; NO_UPDATE_NOTIFIER=1 for the reviewed release's work launcher.
- Interface Design: project decision persistence is optional, never an import-time write.

Hermes remains the coordinator. ECC, Addy and Agency provide selectable specialists/procedures; Impeccable/Taste supply design roles. Choose one lifecycle controller. Prepare Agency's optional lazy search/inspect/load/delegate plugin; never preload the entire roster as skills. Test synthetic delegation before enabling a real profile. Keep memory, profiles, credentials and sessions private. The reviewed lifecycle is in-process and does not provide durable restart recovery.

Autoresearch retains experiment methodology with explicit trial/time/compute budgets, immutable evaluation, isolated workspaces and retained results. Its upstream target is GPU model training. Do not inherit infinite execution, disabled permissions, or destructive reset defaults.

Exports are staged reviewable bundles. Account/service/device activation is separate.

## 4. Connected HTML artifacts

Add skills/analytics/connected-html-artifacts for Parallon analytics, Consulting and E7, reusing Power BI, BigQuery, metric-contract and artifact skills.

| Mode | Behavior |
|---|---|
| Snapshot | Local Excel/CSV import; portable HTML; source and refresh timestamp |
| Secure Power BI embed | Authorized report access controls; fallback link when embedding/sign-in is blocked |
| Authenticated live API | Approved read-only endpoints for Power BI semantic models, BigQuery or Azure database views |

One HTML frontend can use live data, but authenticated services may need a hosted backend. No database credentials/client secrets in HTML. Power BI embedding and model querying are distinct; preserve identity/RLS semantics, query limits and partial-result errors. Do not use Publish to web for private reports. Use BigQuery as the documented initial GCP recipe, not an assertion about the user's actual service. Prefer read-only Excel file download over broader workbook permissions where feasible. Only synthetic examples belong in this repository. Production connections/deployment need target-specific implementation.

## 5. Import, verification, and synchronization

1. Preserve/stage: verify branch and backup; exclude unpublished candidates from publication.
2. Import immutable sources: licenses, complete dependencies, hashes and explicit adaptation records; do not bulk-vendor application repositories.
3. Scan/calibrate: enumerate every package; isolated static-first SkillSpector; benign/malicious calibration fixtures. No-LLM still may contact OSV, so strict offline mode requires network isolation and recorded coverage limits. No implicit cloud model or training pipeline.
4. Validate: unique identities, reference closure, hashes, domain selections, provider exports, work MCP/hook exclusions; existing profile/installer/router regression suites.
5. Exercise synthetic behavior: HTML controls, responsive/keyboard operation, export, invalid/empty data, denied authentication and network failures; team success/failure/cancellation and missing-runtime fallbacks. Separate repository checks from native-host evidence.
6. Sync reviewed feature branch and Master_Skills without overwriting local work; verify commit/package hashes; record receipt and activation remainder. Main merge is separate.

Acceptance: every requested source has a correct content type, canonical location, domain mapping, platform compatibility and verification status.

Planning baseline: local/remote feature HEAD 41c8e88dd87f95c82aac9c4638fe2eb86d9d7fad; 25 existing profiles validated; 46 pre-existing untracked entries preserved. New runtime and account integrations were not executed during planning. Implementation status and verification belong in the current HANDOFF and implementation report.

Implementation evidence: [Library Expansion Implementation and Sync](<20261029 - My AI Skills - Library Expansion Implementation and Sync.md>).
