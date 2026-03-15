# Aaron's AI Skill Library

A library of **36 AI specialist skills** and cross-platform configuration files for AI-assisted development and business strategy. Each skill is a deep-domain expert that activates on demand — bringing genius-level specialist knowledge into any AI conversation.

The library supports **five AI platforms**: Claude Code (slash commands), Google Antigravity / Gemini CLI, OpenAI Codex, Cursor, and ChatGPT. A dedicated **`skill-builder` meta-skill** manages the creation, auditing, and continuous improvement of all skills using a 5-module pipeline and a 10-dimension quality rubric.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [How Skills Work](#how-skills-work)
3. [Skill Catalog](#skill-catalog)
4. [Platform Guides](#platform-guides)
   - [Claude Code](#claude-code)
   - [Google Antigravity (Gemini CLI)](#google-antigravity-gemini-cli)
   - [OpenAI Codex](#openai-codex)
   - [Cursor](#cursor)
   - [ChatGPT](#chatgpt)
5. [Deploying Skills to Projects](#deploying-skills-to-projects)
6. [Repository Structure](#repository-structure)
7. [The skill-builder System](#the-skill-builder-system)
8. [Adding New Skills](#adding-new-skills)
9. [Shared Content Fragments](#shared-content-fragments)

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/GRsoldier7/My_AI_Slills.git
cd My_AI_Slills

# 2. Register all 36 skills as Claude Code global slash commands
./scripts/register-commands.sh

# 3. Verify registration
./scripts/register-commands.sh --list
```

After registration, type any slash command in Claude Code to activate that skill:

```
/polychronos-team    → Activate the full multi-agent team
/business-genius     → Business strategy + routing to specialist skills
/power-bi            → Power BI / DAX expert
/go-to-market-engine → GTM strategy for a new product launch
```

---

## How Skills Work

Each skill is a `SKILL.md` file with YAML frontmatter and a full domain-expert knowledge base:

```yaml
---
name: skill-name
description: |
  What the skill does and when to activate it. This description is read by
  the AI to decide whether to trigger the skill automatically.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: strategy
  adjacent-skills: other-skill, another-skill
  last-reviewed: "2026-03-15"
  review-trigger: "What should prompt the next review of this skill"
---

# Skill Name — Savant-Level Skill

## Philosophy
...

## 1. Framework or Domain Content
...

## Anti-Patterns
...

## Quality Gates
...

## Failure Modes and Fallbacks
...

## Composability
**Hands off to:** (skills this one routes work to)
**Receives from:** (skills that feed into this one)
```

Skills are designed to **compose** — `business-genius` routes to specialist sub-skills, `polychronos-team` orchestrates specialists for multi-step projects, and `skill-builder` creates and audits new skills.

---

## Skill Catalog

### Core Orchestration (`skills/core/`) — 4 skills

These skills manage orchestration, meta-operations, and cross-platform configuration. Use these for complex multi-step work, prompt engineering, and setting up new projects.

| Skill | When to Use |
|-------|-------------|
| `skill-builder` | Creating a new skill, auditing an existing skill for quality, improving a skill that isn't performing well. The meta-skill that governs the library itself. Uses a 5-module pipeline (Brief → Draft → Review → Audit → Deploy) and a 10-dimension rubric. |
| `polychronos-team` | Any non-trivial project work. Activates the full 13-specialist team (PM, Architect, Engineer, QA, DevOps, etc.) with the B.L.A.S.T. protocol for structured, high-quality output. |
| `prompt-amplifier` | Improving a prompt before sending it to any AI. Transforms vague or incomplete prompts into precision-engineered instructions with explicit success criteria, missing context filled in, and structural scaffolding. |
| `portable-ai-instructions` | Setting up a new project for AI-assisted development. Generates optimized CLAUDE.md, AGENTS.md, GEMINI.md, and .cursorrules tailored to each tool's specific strengths and conventions. |

---

### Strategy & Business (`skills/strategy/`) — 8 skills

Business strategy, market intelligence, financial modeling, and go-to-market execution. `business-genius` is the orchestrator that routes to specialist sub-skills.

| Skill | When to Use |
|-------|-------------|
| `business-genius` | High-level business strategy, niche identification, evaluating new opportunities, deciding what to build next. The orchestrator — it diagnoses the situation and routes to the right specialist. |
| `entrepreneurial-os` | Deciding what stage you're in as a founder, building a weekly operating rhythm, running a pivot/persist analysis, designing leverage systems for a solo founder. Stage-gate model, OODA loop, priority stack. |
| `ai-agentic-specialist` | Evaluating AI tools and frameworks, designing agentic systems, staying current on the LLM landscape, comparing model capabilities and costs. Bleeding-edge AI intelligence. |
| `market-intelligence` | Market sizing (TAM/SAM/SOM), competitive landscaping, validating whether a market exists, scoring business opportunities. Research and data-driven analysis. |
| `business-plan-architect` | Writing a business plan, building an investor pitch deck, creating an executive summary or investor memo. Covers the 7 Powers framework, unit economics, traction hierarchy. |
| `pricing-strategist` | Designing or redesigning your pricing model, running a willingness-to-pay analysis, choosing between pricing models, packaging tiers, building a price increase playbook. Van Westendorp, $100M Offers value equation. |
| `financial-model-architect` | Building a financial model, calculating runway, stress-testing unit economics, creating 3-scenario projections, building an investor metrics dashboard. SaaS metrics, cohort revenue model, default-alive test. |
| `go-to-market-engine` | Getting first customers, planning a product launch, choosing acquisition channels, building ICP profiles, sequencing a GTM motion from 0 to 1,000 customers. Sean Ellis PMF test. |

---

### Growth & Marketing (`skills/growth/`) — 8 skills

Full-funnel growth: marketing strategy, content, social media, copywriting, sales, community, and personal brand.

| Skill | When to Use |
|-------|-------------|
| `marketing-strategist` | Defining your positioning, building a messaging hierarchy, planning full-funnel strategy, comparing B2B vs B2C vs SMB marketing approaches. April Dunford 6-step positioning process. |
| `copywriting-conversion` | Writing landing pages, email sequences, ad copy. Improving conversion rates on existing copy. Uses PAS, AIDA, BAB, FAB, and STAR frameworks with full templates. |
| `content-marketing-machine` | Building a content strategy, SEO pillar/cluster model, starting a newsletter, creating a one-to-many content repurposing system. |
| `social-media-architect` | Platform-specific growth strategy for LinkedIn, X/Twitter, YouTube, TikTok/Reels/Shorts. Hook formulas, algorithm patterns, consistency systems. |
| `growth-hacking-engine` | Viral loop design, PLG strategy, activation funnel optimization, retention improvement, A/B test design, referral program mechanics. K-factor math, ICE scoring. |
| `personal-brand-builder` | Building a LinkedIn presence, becoming known as a thought leader, positioning yourself as an expert, creating an authority monetization ladder. |
| `sales-closer` | Improving close rates, qualifying deals with MEDDIC/MEDDPICC, running discovery calls with SPIN Selling, applying the Challenger Sale method, handling objections, writing proposals. |
| `community-builder` | Building a paid or free community, choosing between Discord/Circle/Skool/Slack, designing the engagement flywheel, monetizing an audience, preventing community decay. |

---

### Product & Infrastructure (`skills/product/`) — 5 skills

Product strategy, data pipelines, cloud infrastructure, brand, and SaaS building.

| Skill | When to Use |
|-------|-------------|
| `micro-saas-builder` | Validating a SaaS idea before writing code, scoping an MVP, choosing a tech stack for speed, planning the path from $0 to $10K MRR, diagnosing a revenue plateau. |
| `ai-business-optimizer` | Auditing your business processes for AI automation opportunities, designing agentic workflows, calculating ROI on AI tools, building an AI-native operations stack. |
| `biohacking-data-pipeline` | Designing data pipelines for health/supplement/biomarker data, building ingestion scripts, designing normalized schemas, integrating health data APIs. |
| `brand-website-strategy` | Building a brand identity system, website architecture, SEO strategy, conversion optimization, competitive positioning in health tech or AI consulting. |
| `cloud-migration-playbook` | Migrating from Proxmox homelab to GCP production. Docker, Cloud Run, Cloud SQL, Terraform, CI/CD, security hardening. |

---

### Engineering (`skills/engineering/`) — 3 skills

Software engineering quality, database architecture, and testing. Use these for any code-focused work.

| Skill | When to Use |
|-------|-------------|
| `code-review` | Reviewing code for correctness, security vulnerabilities, failure handling, data integrity, performance. Expert-level analysis with actionable fix recommendations. |
| `database-design` | Designing PostgreSQL schemas, normalization decisions, index strategy, JSONB patterns, provenance tracking, constraint design, query performance. |
| `testing-strategy` | Building a pytest test suite, fixture design, transaction-rollback isolation, property-based testing with hypothesis, async test patterns, coverage strategy. |

---

### Microsoft Power Platform (`skills/microsoft/`) — 8 skills

The complete Power Platform suite. See also [skills/microsoft/README.md](skills/microsoft/README.md) for the Microsoft ecosystem overview.

| Skill | When to Use |
|-------|-------------|
| `power-bi` | Data modeling (star schema, relationships), DAX measures, Power Query transformations, report design, RLS, deployment pipelines, performance optimization. |
| `power-apps` | Canvas app or model-driven app development, Power Fx formulas, gallery/form patterns, Dataverse integration, delegation management, component libraries, ALM. |
| `power-automate` | Cloud flow design, desktop RPA, expression writing, error handling/retry patterns, approval workflows, solution packaging, performance and throttling. |
| `sharepoint` | Site architecture, list and library design, PnP PowerShell, SharePoint search (KQL), permissions, content types, migration, SPFx, governance. |
| `copilot-studio` | Bot design, topic/entity configuration, generative AI orchestration, plugin actions, adaptive cards, multi-channel deployment, analytics. |
| `power-platform-admin` | Environment strategy, DLP policies, CoE Starter Kit, licensing, managed environments, ALM pipelines, governance at scale, tenant settings. |
| `microsoft-dataverse` | Table and relationship design, business rules, security roles, column types, Web API, FetchXML, OData queries, virtual tables, solution management. |
| `m365-integration` | Microsoft Graph API, Teams app development (tabs, bots, message extensions), MSAL authentication, delegated/application permissions, M365 cross-service integration. |

---

## Platform Guides

### Claude Code

**How skills activate:** Skills are registered as slash commands in `~/.claude/commands/`. Typing `/skill-name` in any Claude Code conversation loads the full `SKILL.md` content as context for that conversation. Claude reads the YAML `description` field to determine when to auto-suggest a skill.

**Setup:**
```bash
# Register all 36 skills globally (run once)
./scripts/register-commands.sh

# Register only one category
./scripts/register-commands.sh --category microsoft

# List all registered commands
./scripts/register-commands.sh --list

# Remove all registered commands
./scripts/register-commands.sh --clean
```

**Using skills in a conversation:**
```
/polychronos-team     → Activate multi-agent orchestration
/business-genius      → Business strategy + specialist routing
/power-bi             → Power BI / DAX expert
/skill-builder        → Create or audit a skill
/list-skills          → Show the full skill catalog (meta-command)
```

**Project-level skills (scoped to one project):**
```bash
# Register specific skills for a project (creates .claude/commands/ symlinks in that project)
./scripts/deploy.sh --target /path/to/project --skills polychronos-team,code-review,database-design

# Register all Microsoft skills for a consulting project
./scripts/deploy.sh --target /path/to/project --category microsoft
```

**Project instructions:** Deploy a `CLAUDE.md` to a project:
```bash
./scripts/deploy.sh --target /path/to/project --platforms claude
```

This copies `platform-configs/claude/CLAUDE.md.template` to the project root as `CLAUDE.md`. Customize it for the specific project context.

**How skills compose in Claude Code:** Skills are designed to route between each other. For example:
- Ask a business question → `business-genius` responds, then says "for the GTM strategy, activate `/go-to-market-engine`"
- Start a complex build → `/polychronos-team` orchestrates specialists and may invoke `/code-review` or `/testing-strategy` for quality gates
- When you're stuck on pricing → `entrepreneurial-os` says "route to `/pricing-strategist` for packaging design"

---

### Google Antigravity (Gemini CLI)

**How skills activate:** Antigravity (Google's Gemini CLI, also called `antigravity`) reads `GEMINI.md` at the project root as its instruction file. Unlike Claude Code, Antigravity has **no slash command system** — skills are used by including their content inline in `GEMINI.md` or by manually pasting the skill content into the conversation.

**Setup for a project:**
```bash
# Deploy GEMINI.md to a project
./scripts/deploy.sh --target /path/to/project --platforms gemini
```

This creates `GEMINI.md` in the project root from `platform-configs/gemini/GEMINI.md.template`.

**Using skills with Antigravity:**

Option 1 — **Include inline:** Open the relevant `SKILL.md` and paste its content directly into your GEMINI.md for skills you use constantly on that project (e.g., always include `cloud-migration-playbook` for a GCP project).

Option 2 — **Paste on demand:** When you need a skill, copy the `SKILL.md` content and paste it at the start of your message:
```
[Paste full content of skills/strategy/go-to-market-engine/SKILL.md here]

Now help me plan the GTM strategy for my biohacking app...
```

Option 3 — **Reference by path:** Tell Antigravity to read the file directly (Gemini CLI has file reading capabilities):
```
Read the file at skills/strategy/pricing-strategist/SKILL.md and then help me design pricing for my SaaS product.
```

**Best practices for Antigravity:**
- Always deploy `GEMINI.md` to the project root — it auto-loads on startup
- The Polychronos team roster is embedded in `GEMINI.md.template` since there are no slash commands; the full agent team is always available
- For recurring business questions, add the relevant business skill (e.g., `business-genius`) inline in your GEMINI.md

---

### OpenAI Codex

**How skills activate:** Codex CLI reads `AGENTS.md` at the project root as its instruction file. Like Antigravity, Codex has **no native skill/slash command system** — all context must be in `AGENTS.md` or pasted directly.

**Setup for a project:**
```bash
# Deploy AGENTS.md to a project
./scripts/deploy.sh --target /path/to/project --platforms codex
```

This creates `AGENTS.md` in the project root from `platform-configs/codex/AGENTS.md.template`.

**Using skills with Codex:**

Option 1 — **Add to AGENTS.md:** For skills relevant to the entire project, append the `SKILL.md` content to `AGENTS.md`. This is best for domain-specific skills like `biohacking-data-pipeline` or `cloud-migration-playbook`.

Option 2 — **Paste on demand:** Copy and paste skill content at the start of a task:
```
[Paste full content of skills/engineering/database-design/SKILL.md here]

Design the schema for the supplement tracking tables.
```

Option 3 — **Reference inline:** Because Codex operates in a sandboxed environment with your project files, you can tell it to read the skill files directly:
```
Read skills/engineering/testing-strategy/SKILL.md and then write tests for the pipeline module.
```

**Codex-specific notes:**
- Codex runs in a sandboxed environment — instructions in `AGENTS.md` must be self-contained
- The `AGENTS.md.template` includes coding standards and constraints inline (not by reference)
- Codex excels at engineering tasks — `code-review`, `database-design`, `testing-strategy`, and `cloud-migration-playbook` are highest-value skills here
- Keep `AGENTS.md` focused: don't embed business strategy skills in a code-focused project

---

### Cursor

**How skills activate:** Cursor reads `.cursorrules` at the project root as its system-level instruction file. Skills work by embedding relevant content into `.cursorrules` or referencing them in the Cursor chat.

**Setup for a project:**
```bash
# Deploy .cursorrules to a project
./scripts/deploy.sh --target /path/to/project --platforms cursor
```

This creates `.cursorrules` from `platform-configs/cursor/cursorrules.template`.

**Using skills with Cursor:**

Option 1 — **Embed in `.cursorrules`:** For skills central to the project (e.g., `database-design` for a data-heavy project), add the skill content to `.cursorrules`. It will apply to every file in the project.

Option 2 — **Reference in chat:** In Cursor's composer or chat, paste skill content before your request:
```
[Paste skills/engineering/code-review/SKILL.md content]

Review this module: @src/pipeline/ingestion.py
```

Option 3 — **Use `@file` references:** Cursor supports `@file` context references. You can point directly to a skill:
```
Using @skills/engineering/testing-strategy/SKILL.md, write tests for this function.
```

**Cursor-specific notes:**
- `.cursorrules` is always active — keep it focused on coding conventions and the most critical skill for that project
- Cursor's multi-file editing and inline suggestions work best with engineering skills (`code-review`, `database-design`, `testing-strategy`)
- For business strategy conversations, use Claude Code or ChatGPT instead — Cursor is optimized for code

---

### ChatGPT

**How skills activate:** ChatGPT uses Custom Instructions (account-wide) and Custom GPTs (task-specific). Neither supports dynamic skill loading — skills are embedded permanently at setup time.

**Setup:**

1. **Custom Instructions** (applies to all ChatGPT conversations):
   - Go to Settings → Custom Instructions in ChatGPT
   - Copy content from `platform-configs/chatgpt/custom-instructions.md`
   - Paste into the "What would you like ChatGPT to know about you?" and "How would you like ChatGPT to respond?" fields

2. **Custom GPTs** (skill-specific tools):
   Three pre-built Custom GPT configurations are available in `platform-configs/chatgpt/custom-gpts/`:
   - `polychronos-builder.md` — Multi-agent orchestration GPT
   - `business-strategist.md` — Business strategy and opportunity analysis GPT
   - `ai-advisor.md` — AI tools, landscape, and agentic systems advisor GPT

   To create a GPT: Open ChatGPT → Explore GPTs → Create a GPT → paste the configuration content into the system prompt.

**Using skills with ChatGPT:**

For skills not covered by Custom GPTs, paste the `SKILL.md` content at the start of a new conversation:
```
[Paste full content of skills/growth/sales-closer/SKILL.md]

I have a deal with a Fortune 500 ops team stuck at procurement. Here's the situation...
```

**ChatGPT-specific notes:**
- ChatGPT works best for business and strategy skills — `business-genius`, `market-intelligence`, `go-to-market-engine`, `pricing-strategist`
- Custom GPTs persist their system prompt across sessions — ideal for skills you use repeatedly
- ChatGPT doesn't have access to your local files; you must paste skill content manually
- For code-heavy tasks, Claude Code or Cursor are better choices

---

### Platform Comparison

| Platform | Instruction File | Skill Loading | Best Skill Categories |
|----------|-----------------|---------------|----------------------|
| **Claude Code** | `CLAUDE.md` | Slash commands (`/skill-name`) | All categories |
| **Antigravity (Gemini CLI)** | `GEMINI.md` | Inline or paste-on-demand | Engineering, Product, Microsoft |
| **Codex** | `AGENTS.md` | Inline or paste-on-demand | Engineering, Product |
| **Cursor** | `.cursorrules` | `.cursorrules` embed or `@file` | Engineering |
| **ChatGPT** | Custom Instructions | Custom GPTs or paste | Strategy, Growth, Business |

---

## Deploying Skills to Projects

### New project setup (all platforms at once)
```bash
./scripts/deploy.sh --target /path/to/new-project --platforms claude,codex,gemini,cursor
```

### Register specific skills as Claude Code project commands
```bash
# For a GCP migration project
./scripts/deploy.sh --target /path/to/project --skills polychronos-team,cloud-migration-playbook,database-design

# For a consulting engagement
./scripts/deploy.sh --target /path/to/project --category microsoft

# For a SaaS build
./scripts/deploy.sh --target /path/to/project --skills micro-saas-builder,go-to-market-engine,pricing-strategist,copywriting-conversion
```

### Force overwrite existing files
```bash
./scripts/deploy.sh --target /path/to/project --platforms claude --force
```

### Validate all skills pass quality checks
```bash
./scripts/validate-skills.sh
```

---

## Repository Structure

```
aaron-skill-library/
├── README.md                          # This file
├── CLAUDE.md                          # Master Claude Code project instructions
├── .gitignore
│
├── skills/                            # All 36 skills, organized by category
│   ├── core/                          # Orchestration & meta-skills (4)
│   │   ├── skill-builder/             # Meta-skill: creates + audits all other skills
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   │       ├── skill-template.md
│   │   │       ├── quality-rubric.md
│   │   │       ├── domain-brief-template.md
│   │   │       └── library-audit-2026-03-15.md
│   │   ├── polychronos-team/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   │       ├── strategic-agents.md
│   │   │       ├── architecture-agents.md
│   │   │       └── implementation-agents.md
│   │   ├── prompt-amplifier/
│   │   └── portable-ai-instructions/
│   │
│   ├── strategy/                      # Business & market advisory (8)
│   │   ├── business-genius/           # Orchestrator → routes to all 15 specialist sub-skills
│   │   ├── entrepreneurial-os/
│   │   ├── ai-agentic-specialist/
│   │   ├── market-intelligence/
│   │   ├── business-plan-architect/
│   │   ├── pricing-strategist/
│   │   ├── financial-model-architect/
│   │   └── go-to-market-engine/
│   │
│   ├── growth/                        # Marketing, sales & growth (8)
│   │   ├── marketing-strategist/
│   │   ├── copywriting-conversion/
│   │   ├── content-marketing-machine/
│   │   ├── social-media-architect/
│   │   ├── growth-hacking-engine/
│   │   ├── personal-brand-builder/
│   │   ├── sales-closer/
│   │   └── community-builder/
│   │
│   ├── product/                       # Product & infrastructure (5)
│   │   ├── micro-saas-builder/
│   │   ├── ai-business-optimizer/
│   │   ├── biohacking-data-pipeline/
│   │   ├── brand-website-strategy/
│   │   └── cloud-migration-playbook/
│   │
│   ├── engineering/                   # Software engineering (3)
│   │   ├── code-review/
│   │   ├── database-design/
│   │   └── testing-strategy/
│   │
│   └── microsoft/                     # Microsoft Power Platform (8)
│       ├── README.md
│       ├── power-bi/
│       ├── power-apps/
│       ├── power-automate/
│       ├── sharepoint/
│       ├── copilot-studio/
│       ├── power-platform-admin/
│       ├── microsoft-dataverse/
│       └── m365-integration/
│
├── platform-configs/                  # Per-tool instruction file templates
│   ├── shared/                        # DRY source of truth (edit once, applies everywhere)
│   │   ├── identity.md                # Who Aaron is, current projects
│   │   ├── tech-stack.md              # Python/FastAPI/PostgreSQL/GCP stack
│   │   ├── conventions.md             # Coding conventions, operating principles
│   │   └── blast-protocol.md          # B.L.A.S.T. workflow and task tier classification
│   ├── claude/
│   │   └── CLAUDE.md.template         # Template for Claude Code project instructions
│   ├── codex/
│   │   └── AGENTS.md.template         # Template for Codex CLI (self-contained)
│   ├── gemini/
│   │   └── GEMINI.md.template         # Template for Antigravity (Polychronos team inline)
│   ├── cursor/
│   │   └── cursorrules.template       # Template for Cursor IDE
│   └── chatgpt/
│       ├── custom-instructions.md     # ChatGPT Custom Instructions content
│       └── custom-gpts/
│           ├── polychronos-builder.md
│           ├── business-strategist.md
│           └── ai-advisor.md
│
├── scripts/
│   ├── register-commands.sh           # Register all skills as Claude Code global slash commands
│   ├── deploy.sh                      # Deploy platform configs + skills to a project
│   └── validate-skills.sh             # Validate all SKILL.md files (YAML + quality checks)
│
├── evals/
│   └── evals.json                     # Skill evaluation test cases
│
└── .claude/
    └── commands/
        └── list-skills.md             # /list-skills — show full catalog in any conversation
```

---

## The skill-builder System

The `skill-builder` is the meta-skill that creates, audits, and improves all other skills. It uses a 5-module pipeline:

| Module | Name | What It Does |
|--------|------|-------------|
| 1 | Domain Brief | Captures the skill's purpose, trigger conditions, and key frameworks before drafting |
| 2 | Skill Draft | Writes the full SKILL.md using the canonical 9-section structure |
| 3 | Peer Review | Checks completeness, clarity, and composability against the library |
| 4 | Quality Audit | Scores the skill on 10 dimensions (D1-D10); any score < 4 triggers mandatory revision |
| 5 | Deploy | Registers the skill as a slash command and updates CLAUDE.md |

**The 10-Dimension Quality Rubric:**

| # | Dimension | What It Measures |
|---|-----------|-----------------|
| D1 | Description Precision | YAML description triggers the right use cases and excludes the wrong ones |
| D2 | Domain Depth | Frameworks, heuristics, and mental models are expert-level and specific |
| D3 | Signal Density | Every line earns its place; no filler or generic advice |
| D4 | Anti-Pattern Coverage | Real failure modes named with specific root causes and fixes |
| D5 | Edge Case Handling | Handles the hard cases, not just the easy ones |
| D6 | Composability | Both "hands off to" and "receives from" sections are populated with skill slugs |
| D7 | Failure Mode Documentation | Specific failure detection signals + concrete fallback strategies |
| D8 | Progressive Disclosure | Skill is ≤ 500 lines; deep content lives in `references/` subdirectories |
| D9 | Future-Proofing | No brittle tool names, prices, or platform specifics without "validate current" qualifiers |
| D10 | Auditability | Review-trigger field is specific and actionable; version tracking is present |

To audit an existing skill: `/skill-builder` → Module 4 (Quality Evaluation) → name the skill to audit.

To create a new skill: `/skill-builder` → Module 1 (Domain Brief).

---

## Adding New Skills

```bash
# 1. Create the skill directory under the appropriate category
mkdir -p skills/strategy/new-skill-name

# 2. Create SKILL.md — use the template
cp skills/core/skill-builder/references/skill-template.md skills/strategy/new-skill-name/SKILL.md

# 3. Edit the skill (or run skill-builder to draft it)
# /skill-builder → Module 1: Domain Brief → Module 2: Draft

# 4. Audit the skill before deploying
# /skill-builder → Module 4: Quality Audit on new-skill-name

# 5. Register the new skill as a Claude Code command
./scripts/register-commands.sh

# 6. Validate the full library
./scripts/validate-skills.sh
```

**Category selection guide:**
- `core` — Orchestration, meta-operations, cross-platform configuration
- `strategy` — Business strategy, market analysis, financial modeling, GTM
- `growth` — Marketing, sales, content, social, community, personal brand
- `product` — Product building, infrastructure, data pipelines, brand
- `engineering` — Code quality, database design, testing
- `microsoft` — Power Platform, M365, Microsoft ecosystem

---

## Shared Content Fragments

The `platform-configs/shared/` directory is the **single source of truth** for content that repeats across all platform instruction files. Edit here once; deploy everywhere.

| Fragment | Content | Used In |
|----------|---------|---------|
| `identity.md` | Who Aaron is, current projects (biohacking platform, consulting, brand) | All platform templates |
| `tech-stack.md` | Python/FastAPI/PostgreSQL/GCP stack details, tools list | All platform templates |
| `conventions.md` | Coding conventions (snake_case, Google docstrings, structlog), operating principles, constraints | All platform templates |
| `blast-protocol.md` | B.L.A.S.T. workflow (Blueprint→Link→Architect→Stylize→Trigger), task tier classification | All platform templates |

**How to update across all platforms:**
```bash
# 1. Edit the relevant fragment in platform-configs/shared/
# 2. Re-deploy to all projects that need the update
./scripts/deploy.sh --target /path/to/project --platforms claude,codex,gemini,cursor --force
```

---

## Cross-Project Usage Rules

1. **This repo is the single source of truth.** Never edit skill content or platform configs inside a project repo — edit here and re-deploy.
2. **Claude Code commands are symlinked.** Changes to a `SKILL.md` in this repo are immediately reflected in all Claude Code conversations — no re-registration needed.
3. **Gemini/Codex/Cursor configs are copied.** After editing a platform template or shared fragment, re-run `deploy.sh --force` to update project copies.
4. **New project setup:** Run `deploy.sh --target . --platforms claude,codex,gemini,cursor` to get all platform instruction files in one command.
5. **Skill count:** 36 skills across 6 categories. Run `/list-skills` in Claude Code or `./scripts/register-commands.sh --list` in the terminal for the full inventory.
