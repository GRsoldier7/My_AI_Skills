# 20261029 - My AI Skills - Library Imports and Sync

## Scope and structure

Import the requested upstream skills, separate skill procedures from agent
personas and prompt templates, and synchronize the reviewed library with
Master_Skills. The owner confirmed that Master_Skills is the intended MY_Skills
folder and chose GitHub's newer catalog as canonical, preserving local work.

Canonical layout: `skills/<capability>/<skill>/`, `agents/ecc/`,
`prompts/copilot/`, `platform-configs/`, `docs/`, and `evals/`. Skill-specific
assets and embedded prompts stay with their skill. Profiles select shared sources;
no duplicate copies per business domain and no changes to global instructions.

## Imports

| Source | Pinned revision | Result |
|---|---|---|
| anthropics/skills | ca45fc496a3436251f191354091d557da31c15b5 | Six Apache-2.0 packages: frontend design, internal comms, web artifacts, themes, discernment, Academy Guide |
| mattpocock/skills | a496f5513d4a4cf889bc48e189e579f4b0bdf6aa | All seven productivity skills; existing grill-me, grilling and teach updated in place |
| obra/superpowers | 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b | All 15 skills; existing core/using-superpowers reused; MIT licenses included |
| affaan-m/ECC | 91b5f6a371f7b06d2c3e0c208147c559e11f022c | Four skills, four agent personas and five Copilot prompts; MIT licenses included |
| multica-ai/andrej-karpathy-skills | 2c606141936f1eeef17fa3043a72095b4765b9c2 | karpathy-guidelines; MIT declared in upstream frontmatter, no standalone license file supplied |

33 imported/refreshed skill packages: 29 new and four refreshed. The reviewed
tracked library contains 231 skills; the selection manifest records 74 packages,
25 installable profiles and four preserved reference profiles. ECC's full 313-skill
collection was not bulk-imported. Its focused Hermes set is portable guidance;
Claude-specific team-builder is reference-only pending a Hermes adaptation.

DOCX/PDF/PPTX/XLSX have individual reference folders under `skills/documents/`.
Their pinned Anthropic license restricts copying, retention outside Services and
redistribution, so none of their implementation files were retained in the library
or published. Use an authorized provider installation. They are available by
reference for every domain, not represented as installed packages.

## Domain mapping

- Parallon, Consulting, E7/government-contracting and business operations include
  internal-comms and shared-artifacts.
- Shared-artifacts provides theme-factory, web-artifacts-builder and
  discernment-nudge across business, home, faith, learning and web profiles.
- continued-learning combines academy-guide (Claude product learning) and teach
  (general learning). productivity contains all seven Matt Pocock skills.
- work-copilot-coding, home-coding, consulting-coding and business-coding combine
  the complete Superpowers set, Karpathy guidelines and Anthropic frontend design.
- hermes-teams selects portable ECC team orchestration, harness construction and
  import guidance. See the separate Hermes and Copilot adapter guides.

## Preservation and adaptations

Started from GitHub faith branch c0f0f143c7831bff58e72092bdf9641fac5f7b95,
which includes analytics 62edc59 and main d6dd254. The NAS checkout started at
386701f with CRLF-only differences, eight substantive tracked-file differences,
and additional local sources. A full working-file archive and Git bundle were
created on a separate local filesystem; every archived regular file was
SHA-256 verified before consolidation. The local backup receipt records paths
and restoration details without publishing its contents.

Existing local profile selections were carried into the newer manifest, with
existing blockers retained. Empty core policy and the lifecycle bundle are
reference entries because the latter has a separate seven-skill distributor.
Unique local candidate files remain local, outside the publication set; superseded
local compiler files remain recoverable in the backup. No force push, destructive
reset, branch deletion or automatic plugin activation is part of this work.

Four minimal upstream adaptations are explicit in the manifest:

1. Anthropic frontend-design is named anthropic-frontend-design to avoid colliding
   with the existing ce-frontend-design package's frontend-design identity.
2. Academy Guide's example `[Title](URL)` is rendered as code rather than a live
   missing-file link.
3. Two writing-skills links point to the existing core/using-superpowers folder.

4. One trailing space in the internal-comms 3P example is removed; wording unchanged.

Complete references, templates, scripts, binary assets and provided licenses are
retained. Cross-package dependencies are recorded for review prompts and runtime
mapping references. Original user guardrails continue to control permissions and
clarification; imported broad triggers do not override them.

## Verification

- Catalog validation and generation: 25 profile sets verified, full package hashes
  and local references checked.
- Profile/compiler tests: 32 passed, including isolated installation and repeat
  checks for every installable profile.
- Existing installer regression checks: 98 passed.
- Project-router packaging/installer tests: 9 passed; fixed seven-skill bundle unchanged.
- Imported-skill lint: 33 scanned, zero failures, 11 upstream/editorial warnings
  (short descriptions and a product-brand token). Warnings retained, not concealed.
- Generated broad registry refreshed from the complete reviewed checkout.
- Secret scan includes imported archive contents. One generic-key finding in the
  existing linter's model-name token was reviewed as a false positive; no live
  credential found. No scanner rule or hook was disabled.
- Static source review: optional Superpowers visual server binds to loopback by
  default and includes an external logo request; its opt-out is documented. Bundled
  build/cleanup scripts were stored and parsed, not executed. No listener started.

Native Copilot/Hermes discovery and live task behavior are not verified by these
repository checks. No employer workspace, runtime hooks, secrets, MCP servers or
account installations were changed. GitHub main merge and runtime activation are
separate actions from feature-branch publication.
