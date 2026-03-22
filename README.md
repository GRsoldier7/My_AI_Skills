# Aaron's AI Skill Library

A library of **55 AI specialist skills** and cross-platform configuration files for AI-assisted development, business strategy, faith, health, and life optimization. Each skill is a deep-domain expert that activates on demand — bringing genius-level specialist knowledge into any AI conversation. A **master-orchestrator** skill routes every request to the optimal skill chain automatically.

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

### Core (`skills/core/`) — 11 skills

Meta-layer skills that make everything else run better. `master-orchestrator` routes every request; `anti-hallucination` and `prompt-amplifier` run in the background on every response.

| Skill | When to Use |
|-------|-------------|
| `master-orchestrator` | **Auto-invoked on every non-trivial request.** Routes to optimal skill chain, ensures no relevant skill is missed. The brain of the library. |
| `skill-amplifier` | Optimizing any SKILL.md to peak performance via 8 amplification passes. On-demand, pre-commit, or batch mode. |
| `anti-hallucination` | **Always active.** Prevents context drift, enforces confidence tiers (VERIFIED→UNKNOWN), re-grounding protocol. Escalates automatically past 40% context. |
| `prompt-amplifier` | **Always active (silent mode).** Optimizes every prompt internally. Show mode available on explicit request. |
| `parallel-execution-strategist` | Decomposing work into parallel agents, fan-out patterns, worktree isolation, token optimization. Activates when 3+ independent tasks identified. |
| `session-optimizer` | Context window management, compaction strategy, hook patterns, permission optimization. Activates at 40%+ context. |
| `knowledge-management` | Organizing information across projects, PARA method, documentation standards, cross-system sync, Claude memory integration. |
| `personal-productivity` | Time architecture, Eisenhower matrix, deep work, energy-based scheduling, multi-domain life management, burnout prevention. |
| `polychronos-team` | Multi-agent orchestration with B.L.A.S.T. protocol. 13-specialist team with structured handoffs. |
| `skill-builder` | Creating, auditing, and improving skills. 5-module pipeline + 10-dimension quality rubric. |
| `portable-ai-instructions` | Cross-platform AI instruction files (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules). |

---

### Engineering (`skills/engineering/`) — 8 skills

Full-stack engineering: security, automation, data, containers, MCP servers, code quality, databases, and testing.

| Skill | When to Use |
|-------|-------------|
| `app-security-architect` | Security review, OWASP Top 10, LLM security, GCP hardening, auth flows, secrets management, security code review. |
| `n8n-workflow-architect` | n8n workflow design, node selection, webhook patterns, error handling, Docker/GCP/Power Platform integration. |
| `docker-infrastructure` | Dockerfiles, Compose patterns, networking, volumes, reverse proxy, security hardening, self-hosted services. |
| `data-analytics-engine` | SQL queries, Python/pandas analysis, visualization, dashboards, statistical testing, executive reporting. |
| `mcp-server-builder` | Building MCP servers (TypeScript/Python), tool/resource/prompt design, security, testing with Inspector. |
| `code-review` | Code review for correctness, security, failure handling, data integrity, performance. |
| `database-design` | PostgreSQL schema design, normalization, indexes, JSONB, provenance tracking, constraints. |
| `testing-strategy` | pytest fixtures, transaction-rollback isolation, hypothesis, async testing, coverage strategy. |

---

### Faith (`skills/faith/`) — 3 skills

Biblical study, life application, and teaching ministry.

| Skill | When to Use |
|-------|-------------|
| `bible-study-theologian` | Deep scripture study, historical-grammatical hermeneutics, word studies, doctrinal research, sermon prep. |
| `faith-life-integration` | Applying biblical wisdom to real business, financial, and relationship decisions. 6-lens framework. |
| `sunday-school-teacher` | Age-appropriate lesson plans (preschool–high school), curriculum design, object lessons, series planning. |

---

### Strategy & Business (`skills/strategy/`) — 9 skills

Business strategy, consulting operations, market intelligence, financial modeling, and go-to-market execution.

| Skill | When to Use |
|-------|-------------|
| `consulting-operations` | Client engagements, proposals, SOWs, pricing, scope creep prevention, change orders, consulting business ops. |
| `business-genius` | High-level business strategy orchestrator. Routes to specialist sub-skills. |
| `entrepreneurial-os` | Founder operating system, stage gates, weekly rhythm, pivot/persist analysis. |
| `ai-agentic-specialist` | AI landscape intelligence, agentic team design, LLM evaluation, cost strategies. |
| `business-plan-architect` | Business plans, investor pitch decks, executive summaries, unit economics. |
| `pricing-strategist` | Value-based pricing, SaaS models, WTP research, rate-setting frameworks. |
| `financial-model-architect` | Unit economics, runway, 3-scenario modeling, investor-ready financials. |
| `go-to-market-engine` | ICP definition, channel selection, launch sequencing, PMF measurement. |
| `market-intelligence` | TAM/SAM/SOM, competitive landscapes, opportunity scoring. |

---

### Legal-Financial (`skills/legal-financial/`) — 1 skill

| Skill | When to Use |
|-------|-------------|
| `startup-tax-strategist` | Business taxes, S-Corp election, deductions, quarterly estimates, entity structure, tax planning calendar. |

---

### Growth & Marketing (`skills/growth/`) — 9 skills

Full-funnel growth: professional communication, marketing, content, social media, copywriting, sales, community, and personal brand.

| Skill | When to Use |
|-------|-------------|
| `professional-communicator` | Emails, presentations, executive summaries, client communication, tone calibration, meeting agendas. |
| `marketing-strategist` | Brand positioning (April Dunford), messaging hierarchy, full-funnel strategy, channel ROI. |
| `copywriting-conversion` | PAS/AIDA/BAB frameworks, landing pages, email sequences, ad copy, conversion optimization. |
| `content-marketing-machine` | SEO topical authority, pillar/cluster architecture, newsletter systems, repurposing workflows. |
| `social-media-architect` | Platform-specific strategy for LinkedIn, X/Twitter, YouTube, TikTok. Hooks, algorithms, consistency. |
| `growth-hacking-engine` | PLG design, viral loops, activation optimization, retention, A/B testing, K-factor math. |
| `sales-closer` | SPIN Selling, Challenger Sale, MEDDIC/MEDDPICC, discovery calls, objection handling, closing. |
| `personal-brand-builder` | LinkedIn domination, thought leadership positioning, authority monetization ladder. |
| `community-builder` | Platform selection, flywheel design, engagement mechanics, community monetization. |

---

### Product (`skills/product/`) — 6 skills

Product strategy, health optimization, data pipelines, cloud infrastructure, brand, and SaaS building.

| Skill | When to Use |
|-------|-------------|
| `health-biohacking-protocol` | Evidence-based health protocols, supplement stacks, biomarker interpretation, N=1 experiments, sleep/nutrition/exercise optimization. |
| `micro-saas-builder` | SaaS validation, MVP scoping, $0→$10K MRR playbook, churn prevention. |
| `ai-business-optimizer` | AI business audit, agentic workflow design, tool stack ROI, process automation. |
| `biohacking-data-pipeline` | Data pipelines for health/supplement data, schema design, ETL, API integrations. |
| `brand-website-strategy` | Brand identity, website architecture, SEO, conversion optimization. |
| `cloud-migration-playbook` | Homelab → GCP production. Docker, Terraform, Cloud Run, Cloud SQL, security hardening. |

---

### Microsoft Power Platform (`skills/microsoft/`) — 8 skills

The complete Power Platform suite. See also [skills/microsoft/README.md](skills/microsoft/README.md) for the Microsoft ecosystem overview.

| Skill | When to Use |
|-------|-------------|
| `power-bi` | Data modeling (star schema), DAX measures, Power Query, report design, RLS, deployment pipelines. |
| `power-apps` | Canvas/model-driven apps, Power Fx, gallery/form patterns, Dataverse integration, delegation, ALM. |
| `power-automate` | Cloud flows, desktop RPA, expressions, error handling/retry, approvals, solution packaging. |
| `sharepoint` | Site architecture, lists/libraries, PnP PowerShell, search (KQL), permissions, SPFx, governance. |
| `copilot-studio` | Bot design, generative AI orchestration, plugin actions, adaptive cards, multi-channel deployment. |
| `power-platform-admin` | Environment strategy, DLP policies, CoE Starter Kit, licensing, managed environments, governance. |
| `microsoft-dataverse` | Table design, relationships, security roles, Web API, FetchXML, OData, virtual tables. |
| `m365-integration` | Microsoft Graph API, Teams apps, MSAL auth, delegated/application permissions. |

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
