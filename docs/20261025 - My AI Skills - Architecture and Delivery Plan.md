# My AI Skills: architecture and delivery plan

**Original assessment: October 25, 2026. Focused analytics integration approved October 26, 2026.**

## Current scoped implementation: October 26, 2026

Approved scope: three trial skills (bi-metric-contract, bigquery-review,
knowledge-synthesis), upgrades to existing analytics/Power BI/SQL/sprint/intake
packages, curated profiles, and verification. Preserve the existing domains and
fixed seven-skill lifecycle bundle. Defer the reconciler, live authoring/publishing,
flow diagnostics, and additional domain coverage.

Use one manifest and the existing installer. No additional runtime controller,
memory service, MCP server or package manager is introduced. Counts and revisions
in the original assessment below remain historical observations.

| Existing task | Current scoped result | Remaining gate |
|---|---|---|
| SK-01 | In progress: clean remote baseline d6dd254; 195 original canonical plus 44 Claude-specific definitions; 3 new canonical trials; selected overlaps mapped | NAS untracked definitions, historical exclusions, other devices and full provenance reconciliation |
| SK-02 | In progress: local advisory/synthetic surface available; no employer data/tools used | Actual clients, employer policy and Muse capability |
| SK-03 | In progress: selected manifest, aliases, hashes, root/master routing and refreshed legacy registry | Full-library curation and remaining platform templates |
| SK-04 | In progress: analytics 5, work-parallon 8, consulting 7, maintainer 2; existing installer reused | Actual target discovery, unmanaged/plugin collisions and cross-platform verification |
| SK-05 | In progress: six existing packages upgraded; portable cohort cases pass; Power BI reference supplied and balance expression repaired | Native SQL normalization, live DAX/RLS/performance and approved context pilots |
| SK-06 | Not started in this slice | Existing analytics/release gates, then scoped website/business/client work |
| SK-07 | Not started in this slice | Existing analytics/release gates, then scoped domain work |
| SK-08 | In progress: set/hash/resource validation, regressions and scoped GitHub workflow | Hosted CI and actual-host release/recovery verification |
| SK-09 | Not started | Observed usage and release evidence before promotion or retirement |

All 11 selected packages remain trial. The manifest is a curated pilot, not a
complete source inventory. Google/Anthropic advisory adaptations retain source
revisions/licenses without importing execution/setup branches. The SQL/sprint
packages intentionally adapt matching phuryn source blobs; names/licenses and
their documented upstream baselines are preserved.

### Execution checks

- [x] Router baseline: nine tests; run with CODEX_HOME absent from the test
  subprocess to match temporary default-home assumptions.
- [x] Existing installer baseline: 98 checks.
- [x] Original cohort denominator reproduced as 1.0 where expected was 0.2.
- [x] Seven portable SQLite cases: 20% retention, duplicate activity/membership,
  unrelated users, complete empty/incomplete periods, separate cohorts and
  offsets beyond twelve months.
- [x] Curated profile tests: dependencies/cycles, collisions, resource hashes,
  missing references, traversal/symlinks, read-only drift checks, idempotent
  generation and isolated profile installation.
- [x] Three fresh-agent exercises using the new skills. The no-skill baseline
  also passed; no measured uplift or statistical reliability claim is made.
- [ ] Live BigQuery/PostgreSQL and Power BI DAX/RLS/performance checks.
- [ ] Actual-device discovery, source/plugin collisions and rollback.
- [ ] Repeated behavioral and unrelated-task activation suite before promotion.

The current HANDOFF entry records commands/results. Behavioral materials are in
evals/analytics-skills.json. Local checks do not satisfy the full SK-08 release
gate; no native-host or production-ready claim follows from these source changes.

### Review focus

Verify dependency/collision handling, drift detection, complete package hashing,
reference/symlink handling, cohort arithmetic and coverage; preserve vendor
identity/license and installer ownership; distinguish synthetic/static checks
from live-engine evidence and privacy guarantees.

### Resume marker

RESUME FROM:
- Phase: Analytics pilot integration; selected repository implementation.
- Task: SK-01/02/03/04/05/08 remain in progress at broader gates.
- Status: Trial sources/local checks implemented; actual-host release pending.
- Last verified result: See current HANDOFF entry and committed checks.
- Exact next action: Review the integration PR; reconcile NAS sources read-only, then verify a chosen profile in an approved clean target workspace.
- Required inputs: Target/product versions and access to the NAS checkout.
- Relevant artifacts: This plan, manifest, generated sets, evals and HANDOFF.
- Blockers: Actual devices, native DAX/BigQuery and employer policy unavailable.
- Pending approvals: Repository slice authorized; merge/target deployment separate.

---

## Original October 25 assessment

**Recommendation:** Keep a broad, versioned source library, expose a small set of capabilities for each job, and keep employer/client/personal context in separate approved locations. Fix routing, inventory and distribution before moving folders. Reuse external skills selectively; measure their usefulness instead of optimizing the number collected.

## A. Delivery decision

### What this should accomplish

You should be able to start a Parallon analytics task, a client engagement, Echelon Seven business work, a Temple Protocol product task, or a personal activity without deciding among hundreds of skill files. The same generic capability can serve several domains, while each domain retains its own context, accounts, permissions and project state.

The first useful release is one corrected catalog and routing policy, plus a tested analytics set used for a synthetic Parallon-style task and a consulting task. It includes a ChatGPT instruction-pack fallback. No live employer data or new integration is needed to prove the pattern.

**Requirements:** Windows/macOS/Linux; Claude, ChatGPT/Codex, Muse and work Copilot/ChatGPT; reuse external skills; preserve recent owner-authored workflows; support overlapping domains; preserve Git history and local work; minimize context and maintenance.

**Assumptions:** No fixed delivery date or weekly capacity was supplied. The current assignment authorizes analysis and a proposed plan, not restructuring, installation or publication. Parallon policy, actual installed client versions and the exact Muse product remain unverified. No new paid service is needed for the proposed baseline.

### Evidence and actual repository state

The live baseline is [commit 847e236](https://github.com/GRsoldier7/My_AI_Skills/tree/847e2364979dc69b7e0e1e4c5c3de3d87b51869f), October 25. A complete, non-truncated GitHub tree contained 725 entries. Counts below are file counts, not proven usable capabilities.

| Surface | Verified observation | Consequence |
|---|---|---|
| Public GitHub source | 194 SKILL.md files under skills/ across 11 top-level buckets | README and registry count of 191 is stale |
| Claude-specific source | Another 44 SKILL.md files under .claude/skills/ | The canonical generator and installer ignore a material skill population |
| Cross-surface content | None of those 44 SKILL.md blobs matches a canonical SKILL.md blob exactly | Do not delete them as assumed generated duplicates; functional overlap remains to be assessed |
| Aaron's latest | 14 skills, including the seven-skill router bundle, roadmap, interview/tutoring, research and discounts | Newness is an adoption signal, not a permanent category or quality certificate |
| Master orchestrator | 66,970-byte SKILL.md; generated registry last refreshed October 17 | Keep catalog data available without routinely loading this entire controller |
| Recent additions absent from registry | projectplan-roadmap, discount-codes, research_adaptive | Generate inventory from files rather than trust prose counts |
| Local NAS checkout | HEAD 386701f, October 17; 192 tracked canonical definitions plus 65 untracked definitions = 257 local definitions | Reconcile local additions before any pull, regeneration, move or staging |
| Install configuration | One set file, global.txt, selecting four mattpocock skills | Distribution infrastructure exists, but life/work profiles do not |
| Hosted CI | No .github/workflows files in the pinned tree | Existing local tests are not automatically enforced by GitHub Actions |
| Root license | No root LICENSE file in the pinned tree | Decide terms for owner-authored material; preserve each external package's own license |

The local status command also reported a filesystem error opening .git/sequencer/todo. It still returned status information, but this is another reason to use a separate clean, complete checkout for eventual migration instead of assuming this worktree is safe to manipulate.

**Master reconciliation:** Its latest file-changing commit is October 17, not March. March 21 is the frontmatter review date. Neither date proves when you last invoked it; invocation history was not available. More importantly, root CLAUDE.md still mandates master-orchestrator for every non-trivial request and several automatic meta-layers. AGENTS.md explicitly supersedes that lifecycle behavior with project-router. A different host may encounter different guidance, so this is a cross-platform behavior conflict, not merely old documentation.

The current [skill-set guide](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/platform-configs/skill-sets/README.md) already records external candidates as vendored, reference, duplicate or excluded. Several local untracked imports overlap those previously excluded candidates. Importing all 65 would undo deliberate curation.

### Content findings that change the plan

This was a structural inventory plus targeted inspection of routing, installer, generator, provenance, handoff, evaluation configuration and 11 representative domain skills. It was not an exhaustive behavioral/security audit of all 238 remote definitions.

- **Analytics correctness:** data-analytics-engine divides distinct active-user count by the same joined user IDs in its cohort example. Every nonempty group therefore returns 1.0. This is a code-inspection finding; the SQL was not executed.
- **Missing resources:** power-bi references fabric-integration.md, biohacking-data-pipeline references schema-patterns.md, and n8n-workflow-architect points to a references directory. Those resources are absent from their packages in the pinned tree.
- **Incorrect platform assumption:** n8n-workflow-architect says Execute Command was removed in n8n 2.x. Official documentation says disabled by default. Its private runner arrangement should be optional deployment context, not a universal requirement. [Official n8n change](https://docs.n8n.io/changelog/v20-breaking-changes.md)
- **Portability:** generic analytics examples are heavily PostgreSQL-oriented; Parallon needs explicit BigQuery dialect and cost controls. wrapitup assumes a shared remote memory target and automatic local commits, which are not appropriate universal defaults.
- **Intentional aliases:** wrapup delegates to wrapitup. Preserve useful aliases and model their dependency rather than treating them as duplicate implementations.
- **Health/product separation:** health-biohacking-protocol includes specific health claims and quantities without claim-level evidence. Treat it as unverified reference until reviewed; do not use it as Temple Protocol's evidence-grading system.
- **Naming:** research_adaptive preserves your expressly requested name but does not fit the open standard's hyphenated-name rule. Keep it unchanged for now; test target hosts and record a compatibility exception. A later alias or rename is a deliberate decision, never a silent cleanup. [Specification](https://agentskills.io/specification)

### Muse recommendation: retain, amend, defer

| Recommendation | Verdict and adjustment |
|---|---|
| Canonical sources with several install sets | Adopt. This is the strongest architectural recommendation. |
| Avoid moving the entire library at once | Adopt. Fix discoverability first; folder moves are optional later. |
| Treat 191 as the current inventory | Correct to 194 canonical plus 44 Claude-specific definitions; separately track 65 local untracked definitions. |
| Move lifecycle skills out of aarons-latest first | Defer. There is no immediate user benefit sufficient to justify path/installer churn. |
| Add analytics and automation | Make capability sets first. Add folders only when new canonical content needs a home. |
| Graduate after three tasks | Use three representative successes as an initial pilot, plus negative cases and required-resource checks. Three uses do not establish universal reliability. |
| Archive after 90 days of non-use | Use age as a review signal only. No reliable cross-device usage ledger was established. Check dependencies, external consumers and replacement evidence before retirement. |
| No Codex at work means instruction packs only | Correct. Eligible ChatGPT workspaces can support native skills; tenant settings decide. Maintain an instruction-pack fallback. |
| ALM is manual-only | Preserve documented invocation controls. Do not assume a router can bypass a host-enforced manual-only restriction. |
| Public versus private split | Adopt, but Parallon context belongs in employer-approved storage, not automatically in a personal private GitHub repository. |

### Architectural options

1. **Rename folders now:** visually tidy, high migration cost, leaves routing conflicts and stale distribution unresolved.
2. **Replace everything with a third-party framework:** gains its conventions, risks losing your recent workflows and reproduces controller overlap.
3. **Curate above the existing canonical library:** selected default. Preserve packages, introduce explicit profiles and status, generate platform outputs and prove real jobs. This has the best fit to the evidence and lowest irreversible cost.

This choice is a recommendation, not a claim that you already approved it.

## B. Scope and architecture boundaries

### Four responsibilities, one canonical procedure

| Layer | Owns | Location and rule |
|---|---|---|
| Reusable capabilities | Portable procedures, examples, references and scripts | Existing skills/ paths remain canonical initially |
| Selection and provenance | Which capabilities are active, their dependencies, source revision, status and permitted targets | Extend platform-configs/skill-sets/; add one machine-readable manifest |
| Private context | Business definitions, site decisions, client constraints, employer policies, project state | Approved work/client/personal repositories or workspaces; never embedded in generic public skills |
| Platform delivery | Host discovery paths, invocation settings, plugin packaging and instruction packs | Existing platform-configs/ and scripts/; generated outputs are not edited sources |

**Composition:** approved generic capabilities + one domain/project context + the actual host's tools and permissions. A profile chooses what is available; it does not grant access or change instruction precedence.

A domain or client switch starts a fresh scoped conversation/workspace. Do not reuse a conversation that already loaded another client's material. Memory, retrieval sources and connectors must be limited to the approved domain; shared personal memory is disabled or excluded for employer/client work where the host permits it. If those boundaries cannot be established, use the approved fallback or block sensitive work. Validate configuration and exports with synthetic sentinel data; do not promise that profile files alone guarantee model isolation.

Existing project plans and handoffs remain the authoritative delivery state. Skills contain methods, not every project's tasks. No new global memory database, graph service, MCP server or autonomous orchestrator is required.

### Proposed minimal repository additions

Preserve skills/<existing-category>/<skill>/ initially. Extend existing conventions rather than create a parallel system:

| Proposed path | Purpose |
|---|---|
| platform-configs/skill-sets/manifest.json | Stable IDs, canonical paths, lifecycle status, upstream URL/revision/license/hash, dependencies, host restrictions and explicit aliases |
| platform-configs/skill-sets/*.txt | Generated, flattened, deduplicated install sets compatible with the existing installer |
| platform-configs/skill-sets/README.md | Generated catalog and compact job-based entry points, with maintained install guidance |
| platform-configs/chatgpt/ | Reuse for generic instruction-pack exports and approved plugin adapters |
| platform-configs/copilot/ and platform-configs/muse/ | Small adapter definitions only after host capability checks |
| evals/ and existing tests | Routing, resource, correctness, profile-isolation and installation checks |

The manifest stores curation/provenance that upstream files do not own. SKILL.md remains authoritative for procedure and trigger description. Generated catalog rows join these sources by stable ID; they do not create another editable truth. Keep vendored content byte-identical unless a deliberate, documented fork is necessary.

Each external entry records repository URL, full commit, upstream subpath, license location, complete package hash, dependencies, local patch status and review evidence. Owner-authored entries need no invented upstream. Status vocabulary: **trial, active, reference, deprecated**. Usage is **unknown** until observed, not inferred from file modification time.

Required dependencies differ from adjacent recommendations. grill-with-docs needs grilling and domain-modeling; “useful together” is not a dependency. Host-native plugin identities also need collision checks so raw skills and plugins do not install the same effective capability twice.

### Profiles tailored to your actual work

These are proposed compositions, not claims that the named set files already exist.

| Profile / job | Reuse first | Context and capability gaps |
|---|---|---|
| Parallon analytics | data-analytics-engine after repair, power-bi, relevant Microsoft skills, validated data-quality patterns | Approved metric definitions, BigQuery schemas/dialect, data-quality checks, semantic-model/report QA, executive interpretation; no personal memory integration |
| Consulting delivery | consulting-operations, professional-communicator, selected planning and automation skills | One client workspace per engagement; discovery, SOW, acceptance, change control and handoff tied to actual contract |
| Echelon Seven business | consulting-operations, pricing-strategist, selected marketing/strategy | Service catalog, qualification, pipeline and delivery economics in business-private context |
| EchelonSeven.com | brand-website-strategy, selected web/UI specialists and SEO candidate | Consulting/government buyer audience, credibility, qualified-lead conversion, deployed stack and verified analytics |
| TempleProtocol.ai | micro-saas-builder, biohacking-data-pipeline after repair, shared site-improvement capabilities | Product roadmap and evidence/provenance model; separate scientific evidence appraisal from personal health guidance |
| Government contracting | research_adaptive, consulting/proposal patterns | Add a narrow capture workflow only for uncovered steps: opportunity qualification, bid/no-bid, requirement/evidence matrix and submission readiness |
| Personal, faith and family | Existing faith skills, personal-productivity, research, teach, discount-codes | Separate learning, household, faith and sensitive health context; load only the applicable subset |
| Homelab / automation | Repaired n8n-workflow-architect, home-assistant, docker-infrastructure | Actual hosts, paths, versions and approved integrations live in private deployment context |

One website workflow can serve both sites without sharing audiences, claims or conversion targets. One analytics skill can serve Parallon and clients without moving employer data. One consulting skill can serve many clients without pooling their access or memory.

### Routing and discovery

- Keep project-router as the lifecycle dispatcher. It selects a workflow, then transfers ownership explicitly; it is not an additional execution layer.
- Keep projectplan-builder for first baselines, rescope for changed baselines, continuing-alm-work for uncertain resumption, workbetter for ready execution, and roadmap as optional plan serialization. Preserve the current seven-skill plugin membership.
- Retain the master registry as a generated legacy view during transition. Narrow master-orchestrator to explicit catalog/domain discovery; remove contradictory “every request” policies only in the approved implementation.
- Treat Superpowers and Compound Engineering as alternative workflow families or bounded specialists. Do not automatically combine their planning/execution controllers with WorkBetter for the same task.
- Default to a tiny global set. Put engineering authoring workflows such as to-spec/to-tickets in development profiles rather than every personal session.
- Start pilots with roughly 8–12 relevant visible capabilities, counting dependencies and aliases honestly. This is a tuning target, not a platform limit. Compare activation and correction burden before increasing it.
- New discoveries enter trial/reference outside normal active sets. Preserve existing source paths initially; aarons-latest need not be moved to enforce this rule.
- Manifest status alone does not stop native discovery. Build curated outputs into isolated consumer workspaces/release directories containing only the selected packages; do not use the source repository with its 44 .claude skills as the consumer runtime. When maintaining the source repo itself, use verified host visibility overrides to disable unselected skills. If the host cannot do that, perform maintenance in an isolated environment with explicit manual loading. Test the actual discovered catalog, including global/unmanaged/plugin skills; record unresolved collisions and do not claim isolation until resolved.

### Cross-platform delivery contract

| Host | Proposed delivery | Required verification |
|---|---|---|
| Claude Code | Existing .claude/skills paths or one managed plugin, with invocation overrides | Discovery, manual-only behavior, resources and scripts on the actual client |
| Codex | Existing .agents/skills path or the supported account plugin | Avoid duplicate raw/plugin installs; preserve project-router.py ownership |
| Personal ChatGPT | Existing private skills plugin or supported native upload | Upload is a separately versioned release; GitHub changes do not automatically update it |
| Parallon ChatGPT | Tenant-approved native skills when available; otherwise compact instruction/reference pack | Workspace feature access and permitted data/tool boundaries |
| Work GitHub Copilot | Approved project .github/skills or .agents/skills; concise custom instructions for stable rules | Actual Copilot surface, account policy, resource and invocation behavior |
| Muse | Versioned instruction pack initially unless its exact product supports native packages | Distinguish Muse personal assistant from Muse Code; do not claim universal support |

These routes follow current [Claude documentation](https://code.claude.com/docs/en/skills), [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills), [ChatGPT workspace controls](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), [Copilot guidance](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) and [Muse Code documentation](https://meta-models.github.io/muse-code-sdk/next/guides/extend/skills/). Documentation support is not evidence of installation on your devices.

Use an independent local checkout per device and a reviewed release revision. The NAS can retain backups and source history; avoid making a live multi-device writable worktree the distribution mechanism.

Reuse the existing Bash installer where proven. Its current symlinks follow working-tree changes immediately; therefore point them at a stable release checkout, not the development checkout. The Python router installer preserves differing files rather than overwriting them, so a reviewed upgrade/rollback procedure is still necessary. Test a copy-based fallback where Windows symlinks are unavailable; do not weaken system permissions to make installation succeed.

The installer accepts one set, not automatic profile composition. Resolve profile unions before installation. **Never prune each component set independently:** current --prune removes other managed links, including named installs. Prune only the complete selected union after reviewing its preview. Reserve the seven Codex router targets for their current owner.

### External skills: narrow shortlist, broad reuse

These are candidates for controlled evaluation, not benchmarked winners or approved installs.

| Source | Best fit here | Selection rule |
|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | Discovery, domain vocabulary, specifications and teaching | You already vendor eight related packages. Verify pins and dependencies before importing more. |
| [obra/superpowers](https://github.com/obra/superpowers) | Debugging, verification and disciplined engineering | Reuse selected specialists or explicitly choose its whole workflow for a project; avoid controller stacking. |
| [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) | Engineering review and reusable lessons | Existing ce-* content is already present. Compare its active route with yours instead of importing a duplicate framework. |
| [google/skills](https://github.com/google/skills) | BigQuery knowledge and optimization | Evaluate relevant packages against synthetic BigQuery tasks; validate tools/auth/cost behavior before employer use. Repository-level review only in this assessment. |
| [microsoft/skills-for-fabric](https://github.com/microsoft/skills-for-fabric) | Power BI report/semantic-model authoring | Relevant source, but Fabric is not assumed to be your stack. Its install routes can register MCP servers; do not treat a bundle install as instructions-only. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | React/Next performance and web interface checks | Related skills already exist in your .claude tree. Establish their source/pin and evaluate before adding more copies. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Technical SEO and AI-search workflows | seo-audit and ai-seo were inspected. Trial against your compact baseline → fix → verify loop; validate claims rather than promising rankings. |
| [anthropics/skills](https://github.com/anthropics/skills) | Skill patterns and selected reusable assets | Check package-level terms. Document skills are described as source-available, not uniformly open source. Prefer existing native document capabilities where adequate. |

[vercel-labs/skills](https://github.com/vercel-labs/skills) is a useful ecosystem/discovery option, but replacing the current installer is deferred until a concrete compatibility problem justifies it. No new package manager is required for the first release.

Accept an external skill only when it improves a named job over the current baseline. Preserve the whole required package and license. Review scripts, hooks, tool requests and update behavior. Keep updates proposed and pinned; never automatically activate upstream main. A security scanner is supporting evidence, not proof of safe behavior.

**Deferred:** mass import, mass folder migration, a new web catalog, universal cross-client memory, autonomous self-updating skills, broad medical/tax advice validation, production access and automatic government-bid submission. Government opportunity rules must be verified from current official sources when that workflow is used; this plan makes no eligibility/compliance determination.

## C. Phased execution plan

All tasks below are **proposed / not started**. Shared completion means scoped changes reviewed, required references included, claimed behavior demonstrated, existing controls preserved, and checks labeled passed/failed/not run. Use one implementation owner by default.

### Phase 0 — establish a safe baseline

**Entry:** current plan reviewed; read-only inventory permitted. **Exit:** a complete reconciliation report; no local work lost and no source mistaken for generated output.

**SK-01 — Reconcile all source populations**
- Outcome/scope: reconcile remote 194 + 44 definitions, 65 local untracked definitions, historical exclusions and installed targets where accessible. Classify each as canonical, imported candidate, alias, platform output or unknown. Do not execute imported instructions.
- Inputs/dependencies: pinned remote tree, local git state, HANDOFF, skill-set provenance, import manifest; none.
- Done/evidence: every population accounted for with path/hash/origin; duplicate declared names and unresolved provenance flagged; inaccessible devices marked unknown. Propose a clean checkout location and preserve untracked content. Do not regenerate from this dirty checkout.

**SK-02 — Confirm deployment and privacy boundaries**
- Outcome/scope: record each target's product/version, OS, native skill support, allowed install mechanism and approved context location. Establish exact Muse product and Parallon policy.
- Inputs/dependencies: SK-01 inventory; owner/admin answers only for unavailable facts.
- Done/evidence: one target matrix with native/fallback/blocked status and a permitted synthetic test. Unknown work access blocks work installation, not generic capability development.

### Phase 1 — make selection coherent

**Entry:** SK-01 complete; implementation of this phase authorized. **Exit:** one routing policy and a reproducible candidate catalog.

**SK-03 — Reconcile routing and catalog**
- Outcome/scope: align AGENTS.md, CLAUDE.md and platform templates; preserve lifecycle router ownership; define explicit legacy-master behavior. Add curation/provenance manifest and generate set/catalog views. Account for .claude-only material without silently activating it.
- Inputs/dependencies: SK-01; existing generator/installer and fixed seven-skill bundle.
- Done/evidence: canonical count matches generated view; recent additions represented; every active dependency resolves; duplicate effective identities fail validation; no competing automatic controllers on representative prompts. A standalone factual question does not invoke a lifecycle pipeline.

**SK-04 — Prove profile composition and deployment**
- Outcome/scope: build shared analytics + consulting selection and platform exports; deduplicate dependencies; preserve host-specific manual controls. Use the existing install paths and one owner per target.
- Inputs/dependencies: SK-02, SK-03. Personal/synthetic targets can proceed while employer installation remains blocked.
- Done/evidence: preview matches chosen union; second install is idempotent; modified/unmanaged files are preserved; missing references fail; router targets stay with their installer; subset-prune regression is covered. Test Windows first on the actual personal device; record Mac/Linux as not run until exercised.

### Phase 2 — prove a useful analytics pilot

**Entry:** coherent profile machinery and permitted test surface. **Exit:** one reusable pilot candidate succeeds with two distinct contexts; SK-08 must pass before release.

**SK-05 — Repair and validate the analytics pilot**
- Outcome/scope: repair cohort SQL and relevant Power BI recipes; supply or remove broken references deliberately; isolate dialect-specific examples; test metric definition → query → reconciliation → executive explanation.
- Inputs/dependencies: SK-04; representative fixtures and expected outputs. No employer data.
- Done/evidence: ten original users/two retained yields 20%; missing activity is handled explicitly; query optimizations preserve results; DAX balance output is numeric and correct across blank periods. A BigQuery task does not receive PostgreSQL-only syntax. Two synthetic contexts remain isolated, with factual claims traceable to supplied data.
- Pilot candidate: analytics on approved personal test hosts plus a ChatGPT fallback. SK-08 is mandatory before calling this released; employer rollout also requires SK-02 permission.

### Phase 3 — extend only where recurring work earns it

**Entry:** SK-05 pilot and SK-08 release gate prove the architecture. **Exit:** each remaining domain has a tested selected set or explicit fallback/reference status.

**SK-06 — Curate website, business and client delivery**
- Outcome/scope: Echelon Seven operations, both websites and consulting share generic skills while keeping distinct project decisions. Evaluate SEO/UI candidates; reuse consulting-operations.
- Inputs/dependencies: SK-05, SK-08; actual project context and authorized repository access.
- Done/evidence: a website task produces a measured baseline, prioritized fix, verification and next step without fabricated ranking gains; a consulting task produces scoped acceptance and change-control criteria; fresh client sessions use only that client's approved context/connectors, and synthetic sentinel tests detect unintended export/retrieval crossover. This verifies configured boundaries, not universal model privacy.

**SK-07 — Add narrow contracting, evidence and personal coverage**
- Outcome/scope: identify uncovered contracting steps; separate Temple Protocol evidence appraisal from health advice; validate selected faith/learning/personal and automation/homelab capabilities. Correct n8n assumptions before active adoption.
- Inputs/dependencies: SK-05, SK-08; domain-specific sample tasks and appropriate current sources.
- Done/evidence: contracting matrix distinguishes sourced requirements from unknowns and makes no unauthorized submission; evidence output separates study quality from popularity; personal context is absent from work exports; handoff works without remote memory or automatic commits; n8n guidance reflects the selected version and permitted deployment.

### Phase 4 — sustain and simplify

**Entry:** a useful pilot candidate from SK-05; SK-08 gates its first release, then expands checks as domain sets mature. **Exit:** reviewed updates, recovery and bounded maintenance operate.

**SK-08 — Enforce release checks and recovery**
- Outcome/scope: add scoped GitHub checks, reproducible release artifacts and a minimal per-target install receipt (release, profile, hash, target, verification date/result). Existing local scripts remain primary.
- Inputs/dependencies: SK-05 for first release; rerun affected gates after SK-06/07.
- Done/evidence: packaging/installer/lint/resource/profile checks run on the release revision; native invocation tested on claimed hosts; prior release can be restored without overwriting unrelated files. Run scripts/test-project-router.py before publishing distribution changes and build with scripts/project-router.py build. Packaging success is not behavior proof.

**SK-09 — Review usage and retire proven dead weight**
- Outcome/scope: begin a 30-minute monthly review of changed upstreams, failed tasks and due trials. Graduate useful skills; deprecate only after dependency/consumer checks. No automatic deletion.
- Inputs/dependencies: SK-08 and observed pilot usage. Actual archival/moves require a separate scoped decision.
- Done/evidence: each promotion has a named job and representative positive/negative results; each retirement has replacement/recovery evidence. Catalog, active sets and archives agree. Skip a review with no meaningful change instead of generating paperwork.
- Optional later: lifecycle folder moves, only when their navigation benefit exceeds migration cost. Do not add projectplan-roadmap to the fixed seven-skill bundle incidentally.
## D. Dependencies and execution capacity

Provisional gating sequence:

SK-01 → SK-02 and SK-03 → SK-04 → SK-05 → SK-08 → SK-06 / SK-07 → SK-09.

SK-08 gates the first release. Apply its affected checks again after SK-06/07 before releasing those profiles.

SK-04 requires both target status from SK-02 and catalog contracts from SK-03. SK-08 starts with the first pilot and repeats only affected checks for later releases. Public generic work can continue while private work approval is unresolved.

One writer owns shared routing, manifest, installer and catalog files. After these contracts settle, independent domain review is possible, but integration remains serial and each combined release receives dependency/collision checks. Agent parallelism does not grant permission to write employer/client data.

**Capacity:** Begin with a time-boxed 2–4 hour SK-01 reconciliation and re-estimate from the findings. This is a planning allowance, not a measured estimate. Cross-device access and employer review determine elapsed rollout time; a calendar commitment is premature.

**Success measures:** compare against baseline on the same representative tasks: time to find the right capability, corrective prompts, task correctness, irrelevant activations, setup repeatability and maintenance time. Suggested pilot gate: all critical data-isolation and permission cases pass, all required resources resolve, and at least 9/10 applicable routing cases plus 5/5 unrelated-task rejection cases pass. These are acceptance targets, not current scores or statistical guarantees.

## E. Material risks and release gate

| Trigger / uncertainty | Consequence | Mitigation or fallback |
|---|---|---|
| Dirty/stale NAS worktree and pending imports | Lost work, accidental activation or broken catalog | Separate clean complete checkout; explicit inventory and selective reconciliation |
| Imported workflow changes its own tools/permissions | Unwanted writes, servers or external access | Inspect complete package; preserve host controls; no auto-install or auto-update |
| Private context sits in public skill examples | Work/client/personal information crosses boundaries | Keep generic public core; employer/client-approved contexts and negative export tests |
| Unknown Parallon feature policy or Muse product | Unsupported deployment promises | Native-capability spike; versioned instruction pack where permitted |
| Path move or profile-prune changes ownership | Missing skills or removal of other sets | Defer moves; resolve union; test previews and preserve seven-skill ownership |
| Popular/old/new used as quality proxy | Incorrect procedures become broadly distributed | Representative correctness tests and evidence review before active status |
| Health/contracting claims treated as static facts | Misleading decisions | Current source checks, evidence/uncertainty labels and human domain review where needed |
| Public or archived sensitive content | Archiving does not undo exposure | Investigate scoped exposure if found; handle actual credentials/history separately rather than assuming a folder move fixes it |

**Release acceptance:**
1. Inventory covers all known source populations without inventing device state.
2. Active skills have complete references, required dependencies and provenance/license decisions.
3. Each target has one declared installation owner and verified discovery path.
4. Profiles are deduplicated and exclude unrelated context; hidden plugins/global skills are considered in collision checks.
5. Critical examples and positive/negative activation cases pass for released profiles.
6. Installs are idempotent, preserve unmanaged content and support a tested previous-release restoration.
7. Only platform/OS combinations actually exercised are called verified.
8. Public exports contain only approved generic content; proprietary work contexts stay in their authorized systems.

**Rollback:** preserve the previous manifest, package hashes and release artifact. Restore only managed targets after comparing current bytes; refuse conflicts with user modifications. Reverse approved path moves through reviewed commits, not broad reset/clean commands. An uploaded account plugin requires its own rollback/update; restoring Git alone is insufficient.

**Assessment verification status:** complete pinned tree/count comparison — passed; targeted source/resource inspection — passed; comparison against official platform documentation — completed; local source inventory — completed with the git filesystem warning noted; behavioral, installer, packaging, medical, employer-policy and device tests — not run. Historical “98/98” Linux installer results are recorded in HANDOFF, not rerun or independently certified here.

## F. First execution handoff

First ready task is **SK-01, read-only reconciliation**. The supplied analysis already establishes its starting populations; the executor should verify the revision has not changed, then produce the exact mapping needed for implementation. No need to redesign the architecture before this step.

Paste-ready instruction:

> Use project-router with this architecture plan as a draft baseline. Perform SK-01 only: reconcile live My_AI_Skills, the stale NAS checkout and its 65 untracked skill definitions, the 44 .claude skill definitions, prior import/exclusion decisions and accessible installed copies. Read AGENTS.md, HANDOFF.md, the skill-set guide and installer ownership rules first. Preserve all local work. Compare source paths, hashes, declared names, upstream revisions, dependencies and aliases. Do not install, execute imported skills, move/delete files, regenerate the registry, commit or push. Return one proposed canonical mapping, unresolved conflicts, the exact files a first implementation would touch, and checks marked passed/failed/not run. Stop before any mutation. Ask only for facts that block the next safe step.

After reconciliation, implement the smallest approved slice through SK-03/04/05 and pass SK-08 before calling it released. Keep this plan as the single baseline; later discovery changes its tasks rather than spawning another competing roadmap.

### Evidence references

Repository claims are pinned to 847e236. Primary inspected files include [AGENTS.md](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/AGENTS.md), [CLAUDE.md](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/CLAUDE.md), [master-orchestrator](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/skills/core/master-orchestrator/SKILL.md), [installer](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/scripts/install-skills.sh), [router packager](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/scripts/project-router.py), [installation boundaries](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/platform-configs/openai/project-router/README.md), [analytics source](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/skills/engineering/data-analytics-engine/SKILL.md), [Power BI source](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/skills/microsoft/power-bi/SKILL.md) and [n8n source](https://github.com/GRsoldier7/My_AI_Skills/blob/847e2364979dc69b7e0e1e4c5c3de3d87b51869f/skills/engineering/n8n-workflow-architect/SKILL.md).

Muse's attached recommendation was read in full and treated as a proposal to verify. Local inventory was read directly from the supplied NAS workspace. Research used official platform documentation and upstream repositories; proposed fit and prioritization are architectural judgments, not benchmark rankings.
