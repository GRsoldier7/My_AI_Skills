# Aaron DeYoung — Master Project Instructions

## Who I Am
I'm Aaron DeYoung — AI consultant, entrepreneur, and builder. I help companies implement AI and automation (especially Microsoft Power Platform), and I'm building a biohacking data platform powered by AI that delivers personalized health protocols based on bloodwork, supplements, and biomarkers. I'm a solo founder bootstrapping everything, leveraging AI and agentic systems as my force multiplier.

## My Tech Stack
- **Languages:** Python 3.12+, TypeScript, SQL
- **Backend:** FastAPI, SQLAlchemy, Pydantic v2
- **Database:** PostgreSQL (local on Proxmox, migrating to GCP Cloud SQL)
- **Frontend:** Next.js, React, Tailwind CSS, shadcn/ui
- **Infrastructure:** Docker, Google Cloud Platform (Cloud Run, Cloud SQL, Cloud Storage)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Testing:** pytest, property-based testing with hypothesis
- **Linting/Formatting:** ruff (replaces black + isort + flake8)
- **Type checking:** pyright
- **AI Tools:** Claude Code, Cursor, Gemini CLI (Antigravity IDE), Codex

## Coding Conventions
- Python: snake_case, Google-style docstrings, type hints on all function signatures
- Files/directories: lowercase-with-hyphens
- Error handling: Explicit exception types, never bare `except`
- Logging: structlog with structured output
- Config: Environment variables via pydantic-settings
- Secrets: Never in code — Secret Manager or .env (local only)
- Tests: Written alongside implementation, not after. pytest with fixtures and parametrize.
- Commits: Descriptive messages explaining the WHY, not just the WHAT

## Operating Principles
1. **Reliability over speed.** Never guess at business logic. Ask if uncertain.
2. **Build for production from day one.** Even on the homelab, write code as if it's serving real users.
3. **AI-first but human-verified.** Use AI to move 10x faster but always validate critical decisions.
4. **Evidence-based everything.** Cite sources for claims. Label hypotheses clearly. Test assumptions.
5. **Security by default.** Least privilege, encrypted at rest and in transit, no secrets in code or logs.
6. **Document as you go.** Update docs in the same session as code changes. Keep everything current.

## The Skill Library

This CLAUDE.md works in concert with a library of **36 specialist skills** organized in `skills/`. Each skill is a deep-domain expert that activates on demand via slash commands (e.g., `/polychronos-team`). Use `/list-skills` to see the full inventory. Skills are designed to compose — `business-genius` orchestrates the full business-building suite; `polychronos-team` orchestrates everything.

### Core Orchestration (`skills/core/`) — 4 skills
- **skill-builder** — Meta-skill for creating, auditing, and improving other skills. 5-module pipeline + 10-dimension quality rubric. Use whenever adding a new skill or auditing an existing one.
- **polychronos-team** — Multi-agent orchestration with the B.L.A.S.T. protocol. Deploys 13 genius-level specialists with structured handoffs and quality gates. Use for any non-trivial project work.
- **prompt-amplifier** — Transforms any prompt into a precision-engineered instruction that extracts maximum capability from any AI model.
- **portable-ai-instructions** — Generates project instruction files (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules) tailored to each AI tool's strengths.

### Strategy & Business (`skills/strategy/`) — 8 skills
- **business-genius** — Master orchestrator for the full business-building suite. Routes to specialist sub-skills. Use as the entry point for any business strategy question.
- **ai-agentic-specialist** — Bleeding-edge AI landscape intelligence. LLM evaluation, agentic team design, cost-saving strategies.
- **market-intelligence** — Deep market research: TAM/SAM/SOM analysis, competitive landscapes, opportunity scoring.
- **entrepreneurial-os** — Founder operating system. Stage-gate model, decision frameworks, weekly rhythm, pivot/persist criteria.
- **business-plan-architect** — Full business plan construction: executive summary, market sizing, competitive moat, unit economics, traction narrative.
- **pricing-strategist** — Value-based pricing, packaging psychology, WTP research, SaaS pricing models, price increase playbooks.
- **financial-model-architect** — Unit economics, runway, 3-scenario modeling, SaaS metrics, investor-ready financials.
- **go-to-market-engine** — ICP definition, channel selection matrix, launch sequencing, PMF measurement, founder-led sales.

### Growth & Marketing (`skills/growth/`) — 8 skills
- **marketing-strategist** — Brand positioning (April Dunford), messaging hierarchy, full-funnel strategy, channel ROI.
- **copywriting-conversion** — PAS/AIDA/BAB/FAB/STAR frameworks, landing pages, email sequences, ad copy.
- **content-marketing-machine** — SEO topical authority, pillar/cluster architecture, newsletter systems, repurposing workflows.
- **social-media-architect** — LinkedIn, X/Twitter, YouTube, TikTok platform-specific strategy, hooks, consistency systems.
- **growth-hacking-engine** — PLG design, viral loops, activation optimization, retention engineering, A/B testing.
- **sales-closer** — SPIN Selling, Challenger Sale, MEDDIC/MEDDPICC, discovery calls, objection handling, closing.
- **personal-brand-builder** — LinkedIn domination, thought leadership positioning, authority monetization ladder.
- **community-builder** — Platform selection, flywheel design, engagement mechanics, community monetization.

### Engineering (`skills/engineering/`) — 3 skills
- **code-review** — Expert code reviewer: correctness, security, failure handling, data integrity, performance.
- **database-design** — PostgreSQL schema architect: normalization, indexes, constraints, JSONB, provenance patterns.
- **testing-strategy** — pytest expert: fixture design, transaction-rollback isolation, hypothesis, async testing.

### Product & Infrastructure (`skills/product/`) — 5 skills
- **micro-saas-builder** — Niche validation, concierge MVP, $0→$10K MRR playbook, churn prevention.
- **ai-business-optimizer** — AI business audit, agentic workflow design, tool stack ROI, process automation.
- **brand-website-strategy** — Brand identity, visual systems, website architecture, SEO, conversion optimization.
- **biohacking-data-pipeline** — Data pipeline architect for health/supplement data. Schema design, ETL pipelines, API integrations.
- **cloud-migration-playbook** — Proxmox homelab → GCP production. Docker, Terraform, Cloud Run, Cloud SQL, security hardening.

### Microsoft Power Platform (`skills/microsoft/`) — 8 skills
- **power-bi**, **power-apps**, **power-automate**, **sharepoint**, **copilot-studio**, **power-platform-admin**, **microsoft-dataverse**, **m365-integration**

## BLAST Protocol (For All Non-Trivial Work)

**B — Blueprint:** Ask discovery questions. Define schemas and contracts. Halt until confirmed.
**L — Link:** Verify integrations and credentials with minimal tests before full implementation.
**A — Architect:** Design before building. SOPs before code. Update the doc before updating the code.
**S — Stylize:** Polish for production quality. Code review. Documentation review. Usability validation.
**T — Trigger:** Deploy, automate, monitor. A project is only complete when it's in its final destination.

## Approval Requirements (Non-Negotiable)

Always ask before:
- Git commits, PRs, merges, or pushes
- Deployments or production changes
- Secrets or credential changes
- Destructive actions (delete data, drop tables, rotate keys)
- Scope changes affecting cost, timeline, security, or compliance

## Current Projects

### Biohacking Data Platform (Primary)
- **Status:** Building data pipelines and database on Proxmox homelab
- **Next:** Migrate to GCP, build API, launch MVP
- **Stack:** Python + FastAPI + PostgreSQL + Docker → Cloud Run + Cloud SQL
- **Goal:** AI-powered personalized biohacking protocols based on bloodwork, supplements, and biomarkers

### AI Consulting Business
- **Services:** Power Platform (PowerBI, Power Apps, Power Automate), AI adoption training
- **Goal:** Revenue generation while building the product business

### Brand & Website
- **Status:** Building brand identity and website
- **Goal:** Professional online presence for both consulting and the biohacking product
