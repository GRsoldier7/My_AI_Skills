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

This CLAUDE.md works in concert with a library of **55 specialist skills** organized in `skills/`. Each skill is a deep-domain expert. Skills compose — `master-orchestrator` routes every request to the optimal skill chain.

### Auto-Routing (Non-Negotiable)

For EVERY non-trivial request, invoke `master-orchestrator` first. It identifies which skills apply and chains them in the right order. This is the single highest-leverage behavior — it ensures the full library is used, not just the obvious skill.

**Always-on meta-layer** (these run in the background on every response):
- `anti-hallucination` — confidence tiers, context drift prevention, re-grounding
- `prompt-amplifier` — silently optimizes every prompt before execution
- `token-optimizer` — maximizes token efficiency on every call (lean, zero waste)
- `session-optimizer` — activates at 40%+ context fill for proactive management

### Core (`skills/core/`) — 11 skills
- **master-orchestrator** — Routes every request to optimal skill chain. Invoke first.
- **skill-amplifier** — 8-pass optimization of any SKILL.md to peak performance.
- **anti-hallucination** — Context drift prevention, confidence tiers (VERIFIED→UNKNOWN), re-grounding.
- **prompt-amplifier** — Always-on prompt optimization (silent + show modes).
- **parallel-execution-strategist** — Agent decomposition, fan-out patterns, worktree isolation, token optimization.
- **session-optimizer** — Context window management, compaction strategy, hook patterns, session architecture.
- **knowledge-management** — PKM architecture (PARA), documentation standards, cross-system sync.
- **personal-productivity** — Time architecture, Eisenhower matrix, deep work, multi-domain management.
- **polychronos-team** — Multi-agent orchestration with B.L.A.S.T. protocol.
- **skill-builder** — Meta-skill for creating and auditing skills.
- **portable-ai-instructions** — Cross-platform AI instruction files.

### Engineering (`skills/engineering/`) — 8 skills
- **app-security-architect** — OWASP Top 10, LLM security, GCP hardening, security code review.
- **n8n-workflow-architect** — Workflow design, node patterns, Docker/GCP integration, error handling.
- **docker-infrastructure** — Dockerfile best practices, Compose patterns, networking, security hardening.
- **data-analytics-engine** — SQL patterns, Python analysis, visualization guide, reporting templates.
- **mcp-server-builder** — TypeScript/Python MCP server patterns, security, testing.
- **code-review** — Expert code reviewer: correctness, security, failure handling, performance.
- **database-design** — PostgreSQL schema architect: normalization, indexes, JSONB, provenance.
- **testing-strategy** — pytest expert: fixtures, transaction-rollback isolation, hypothesis, async.

### Faith (`skills/faith/`) — 3 skills
- **bible-study-theologian** — Historical-grammatical hermeneutics, 4 study modes, scholarly engagement.
- **faith-life-integration** — 6-lens framework for applying biblical wisdom to real decisions.
- **sunday-school-teacher** — Age-appropriate curriculum design, lesson plans, object lessons.

### Strategy & Business (`skills/strategy/`) — 9 skills
- **consulting-operations** — Engagement lifecycle, proposals, SOWs, pricing, scope creep prevention.
- **business-genius** — Master orchestrator for the business-building suite.
- **ai-agentic-specialist** — AI landscape intelligence, agentic team design.
- **entrepreneurial-os** — Founder operating system, stage gates, decision frameworks.
- **business-plan-architect** — Full business plan construction.
- **pricing-strategist** — Value-based pricing, SaaS models, rate-setting frameworks.
- **financial-model-architect** — Unit economics, 3-scenario modeling, investor-ready financials.
- **go-to-market-engine** — ICP definition, channel selection, launch sequencing, PMF measurement.
- **market-intelligence** — TAM/SAM/SOM, competitive landscapes, opportunity scoring.

### Legal-Financial (`skills/legal-financial/`) — 1 skill
- **startup-tax-strategist** — S-Corp election, deductions, quarterly estimates, entity structure.

### Growth & Marketing (`skills/growth/`) — 9 skills
- **professional-communicator** — Emails, presentations, executive summaries, tone calibration.
- **marketing-strategist** — Brand positioning, messaging hierarchy, full-funnel strategy.
- **copywriting-conversion** — PAS/AIDA/BAB frameworks, landing pages, email sequences.
- **content-marketing-machine** — SEO topical authority, pillar/cluster, newsletter systems.
- **social-media-architect** — Platform-specific strategy, hooks, consistency systems.
- **growth-hacking-engine** — PLG design, viral loops, activation, retention, A/B testing.
- **sales-closer** — SPIN Selling, Challenger Sale, discovery calls, objection handling.
- **personal-brand-builder** — Thought leadership, LinkedIn domination, authority ladder.
- **community-builder** — Flywheel design, engagement mechanics, community monetization.

### Product (`skills/product/`) — 6 skills
- **health-biohacking-protocol** — Evidence-based protocols, biomarker interpretation, N=1 experiments.
- **micro-saas-builder** — Niche validation, concierge MVP, $0→$10K MRR playbook.
- **ai-business-optimizer** — AI audit, agentic workflow design, tool stack ROI.
- **biohacking-data-pipeline** — Data pipeline architect for health/supplement data.
- **brand-website-strategy** — Brand identity, website architecture, SEO, conversion.
- **cloud-migration-playbook** — Homelab → GCP. Docker, Terraform, Cloud Run, Cloud SQL.

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
