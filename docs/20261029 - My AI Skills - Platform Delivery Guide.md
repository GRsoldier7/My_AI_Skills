# 20261029 - My AI Skills - Platform Delivery Guide

Use the [Library Catalog](<20261029 - My AI Skills - Library Catalog.md>) to find
packages and the [Expansion Plan](<20261029 - My AI Skills - Library Organization and Expansion Plan.md>)
for the approved architecture. `Master_Skills` is the canonical local checkout of
`GRsoldier7/My_AI_Skills`. GitHub and this folder share the same feature branch;
private candidate folders and backups are preserved separately from published sources.

## Organization and naming

| Folder | Contents |
|---|---|
| `skills/<capability>/<skill-id>/` | Complete canonical packages: instructions, scripts, references and licenses |
| `agents/<collection>/<division>/` | Agent personas; Agency retains its 18 divisions |
| `prompts/<collection>/` | Reusable task starters, selected explicitly |
| `platform-configs/` | Domain selections, host adapters and provider variants |
| `tooling/security/skillspector/` | Pinned isolated scanner, calibration, reviews and reproducibility files |
| `tooling/research/autoresearch/` | Research-runtime reference; bounded methodology is a separate skill |
| `docs/`, `evals/` | Dated decisions/reports, synthetic checks and evidence |

Domain profiles refer to shared packages. Do not duplicate source folders per
employer or business. Skill IDs use lowercase hyphens. Stable required filenames
stay `SKILL.md`, `README.md` and manifests; dated reports use
`YYYYMMDD - My AI Skills - Description.md` with matching H1.

## Choose a domain, then a capability

| Domain | Starting selections |
|---|---|
| Parallon | `work-parallon`, `parallon-artifacts`, `work-copilot-coding`, `design-general`, `design-product-ui`, `design-marketing`, `design-polish`, `html-artifacts-offline`, `browser-qa`, `reverse-engineering` |
| Consulting | `consulting`, `consulting-coding`, `consulting-web-research`, `consulting-web-integration`, `connected-artifacts` |
| E7 | `e7`, `business-coding`, `e7-web-research`, `e7-web-integration`, `connected-artifacts` |
| Home | `home-life`, `home-coding` |
| Learning | `continued-learning`, `productivity` |
| Faith | `faith-personal`, `faith-teaching`, `faith-publishing`, `faith-learning` |
| Hermes Teams | `hermes-teams`, `addy-engineering`, `agent-team-design`, `agent-team-research` |

All domains can additionally select `design-general`, `design-product-ui`,
`design-marketing`, `design-polish`, `emil-toolkit`, `html-artifacts`,
`html-artifacts-offline`, `connected-artifacts`, and `shared-writing`.
Use one design creator and add a reviewer/finisher when useful. Keep one lifecycle
controller: Superpowers, the existing project router, or the optional Addy
controller. Hermes stays the coordinator of Hermes teams.

Internal Comms is included for Parallon, Consulting and E7. Humanizer is shared.
Academy Guide and Matt Pocock's productivity skills are under learning/productivity.
DOCX/PDF/PPTX/XLSX have shared [licensed upstream references](../skills/documents/README.md);
the restrictive upstream implementations are not redistributed.

## Build a reviewable bundle

Run from the repository root. Choose a **new** output folder; export refuses to
overwrite an existing folder or ZIP. Export does not install or activate anything.

```sh
python3 scripts/skill-sets.py
python3 scripts/library-delivery.py catalog
python3 scripts/library-delivery.py export --profile parallon-artifacts --platform chatgpt --output /tmp/parallon-artifacts-chatgpt
python3 scripts/library-delivery.py export --profile work-copilot-coding --platform copilot --output /tmp/parallon-copilot
python3 scripts/library-delivery.py export --profile hermes-teams --platform hermes --output /tmp/hermes-team-guidance
```

The directory and deterministic ZIP contain the selected skills, required local
resources, licenses and `SOURCES.json` file hashes. Relative links are checked and
rewritten for the target layout. Related-skill navigation is distinct from a
runtime dependency: unselected related packages link to their pinned upstream
source, and are not silently installed. The manifest explicitly declares both.

| Target | Export layout | What remains to verify |
|---|---|---|
| ChatGPT | `plugin.json`, `skills/`; runtime-dependent packages use reduced instruction adapters | Plugin acceptance, available artifact capabilities and skill discovery in the actual account |
| Copilot | `.github/skills/`, selected `.github/agents/*.agent.md`, `.github/prompts/*.prompt.md` | Approved client/version, native discovery, synthetic invocation and available tools |
| Codex | `.agents/skills/`; Impeccable uses its distinct Codex provider package | Target discovery and runtime; companion TOML is retained, not registered automatically |
| Hermes | `skills/` plus selected reference roles/prompts | Explicit skill/role configuration and actual team lifecycle on the intended host |

`SOURCES.json` describes the exact source selection and transformed output bytes;
it is not a clean scanner verdict or activation receipt. All new selections remain
trial. Consult the scan reviews before executing runtime-sensitive workflows.

## Parallon constraints

Only ChatGPT skills/plugins and approved GitHub Copilot capabilities are selected.
No MCP server is required or installed. The work bundles exclude Addy's
`browser-testing-with-devtools` MCP package. Copilot agent tool fields use native
read/search defaults; any additional capability belongs to explicit task and host
approval. Native tool restrictions remain the real enforcement boundary.

ChatGPT variants of Impeccable, Taste, UI UX Pro Max, both HTML packages and REA
provide guidance from supplied evidence. They do not claim to execute local
engines, Node/Python helpers, browsers or MCP. The Web Artifacts Builder adapter
also omits shell initializers. Host-provided artifact tools may still create HTML.

Copilot can use approved Node/browser tools. Verify Python availability before
UI UX Pro Max search or the offline HTML inliner. Impeccable requires an approved
engine selected by absolute `IMPECCABLE_BIN`; its local launcher does not acquire
one. On POSIX, invoke the stored launcher with `sh <skill-base-dir>/scripts/impeccable`
when the extracted file is not executable; verify shell support on the target.
REA uses an already approved CLI/engines with automatic MCP/setup disabled.
Playwright CLI and its browser require separate availability checks. Taste's
browser helpers require a dedicated task-local temporary directory, a disposable
approved browser and review of its graphics flags before any execution.

## Hermes and Agent Teams

All 283 Agency personas are retained for search and selection, not preloaded.
`platform-configs/hermes/agency/` supplies an optional staging builder and a
synthetically tested lazy search/inspect/load/delegate adapter. It does not alter
Hermes configuration. Its reviewed lifecycle is in-process; durable restart
recovery and real provider calls remain unverified.

The Hermes team bundle includes selected ECC role briefs and official Hermes
operating guidance. The Addy bundle offers its engineering specialists, four
personas and selected task prompts as another explicit choice. The native Hermes
runtime, model credentials, sessions, memory, hooks and private profiles remain
on their existing host. Do not use source-import scripts to reset them.

Autoresearch contributes bounded experiment methodology. Use a declared trial,
time and compute budget, immutable evaluation, separate workspaces and retained
results. The GPU training application is a runtime reference, not installed here.

## Connected HTML deliverables

The [connected HTML skill](../skills/analytics/connected-html-artifacts/SKILL.md)
contains an interactive synthetic CSV snapshot plus Power BI, Excel, BigQuery and
Azure recipes. HTML may use approved external services. Offline HTML is an
explicit alternative, not a restriction on every artifact.

A snapshot is exported data, not a live connection. Secure Power BI embedding
requires verified authorization/licensing. Private live data normally needs an
approved identity-aware API or embed flow. Keep database credentials and service
secrets on the backend. Enforce row/field permissions, predefined queries and
request limits there. GCP guidance currently covers BigQuery; identify other GCP
services explicitly. The sample has no XLSX parser or production credentials.

## Updating and verifying

1. Fetch and inspect the intended feature branch. Preserve local changes and
   private candidates; do not force synchronization over them.
2. Pin upstream revisions and review complete packages, licenses and local
   adaptations. Keep provider variants and existing local names distinct.
3. Run isolated SkillSpector and review every finding/coverage limit. Retain raw
   failures; a contextual disposition does not turn the raw gate green.
4. Refresh hashes deliberately, regenerate profiles/catalog and test exports.
   Regenerate the broad master registry only in a clean complete tracked checkout.
5. Verify public content, stage explicit files, commit and sync the feature branch.
   Main merge, target installation and authenticated data connections are separate.

Use canonical paths when working in the NAS checkout: preserved local candidate
folders can make short names ambiguous. The installer deliberately refuses an
ambiguous name. It does not delete candidates to make a match.
