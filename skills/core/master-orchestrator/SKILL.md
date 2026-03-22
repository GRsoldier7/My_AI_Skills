---
name: master-orchestrator
description: |
  The conductor of the entire skill library. Routes every request to the right specialist
  skills, chains multi-skill workflows, and ensures peak execution by activating the
  optimal combination of skills for any task. Think of this as the "brain" that knows
  what every skill does and when to call each one.

  AUTO-TRIGGER on EVERY request — this skill runs as a routing layer that ensures no
  relevant skill is missed. It activates silently, identifies which skills apply, and
  either invokes them directly or recommends the optimal skill chain.

  EXPLICIT TRIGGER on: "which skill should I use", "orchestrate", "route this",
  "what skills apply here", "skill chain", "multi-skill workflow", "use all relevant skills",
  "full power", "give me everything you've got", "optimize this request",
  "which specialists should handle this".

  This skill complements polychronos-team (which manages multi-agent team orchestration)
  by focusing on skill selection and chaining within a single agent's execution.

  CRITICAL: This skill makes the entire library more than the sum of its parts by ensuring
  the right skills fire for every request, every time.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: polychronos-team, skill-amplifier, parallel-execution-strategist, session-optimizer
  last-reviewed: "2026-03-21"
  review-trigger: "New skill added to library, user reports skill should have triggered but didn't"
  capability-assumptions:
    - "Access to all skills in the Master_Skills library"
    - "Skill tool available for invoking skills"
  fallback-patterns:
    - "If skill not found: recommend building it with skill-amplifier"
    - "If multiple skills compete: use the priority matrix below"
  degradation-mode: "strict"
---

## Composability Contract
- Input expects: any user request
- Output produces: skill routing decision, skill chain plan, or direct skill invocation
- Can chain from: this is the first link — it routes everything
- Can chain into: any skill in the library
- Orchestrator notes: this IS the orchestrator — it routes, it doesn't execute domain work itself

---

## The Skill Registry

### Core (Meta-Layer — Always Active)
| Skill | Triggers On | Priority |
|-------|------------|----------|
| `anti-hallucination` | Every response with factual claims | Background — always active |
| `prompt-amplifier` | Every user prompt (silent mode) | Background — always active |
| `master-orchestrator` | Every request (routing) | Background — always active |
| `session-optimizer` | Session start, context management | Background at 40%+ context |
| `skill-amplifier` | Skill creation or optimization | On-demand |
| `parallel-execution-strategist` | 3+ independent tasks identified | On-demand |
| `knowledge-management` | Information organization needs | On-demand |
| `personal-productivity` | Time/task/priority management | On-demand |
| `polychronos-team` | Multi-agent orchestration planning | On-demand |
| `portable-ai-instructions` | Cross-platform AI config | On-demand |
| `skill-builder` | Building new skills | On-demand |

### Engineering
| Skill | Triggers On |
|-------|------------|
| `app-security-architect` | Security review, auth, API protection, OWASP |
| `code-review` | Code review, PR review, quality check |
| `database-design` | Schema design, migrations, query optimization |
| `testing-strategy` | Test planning, TDD, test coverage |
| `n8n-workflow-architect` | Automation workflows, webhooks, n8n |
| `docker-infrastructure` | Containers, Docker Compose, self-hosted |
| `mcp-server-builder` | MCP server development, Claude tools |
| `data-analytics-engine` | Data analysis, SQL, visualization, BI |

### Faith
| Skill | Triggers On |
|-------|------------|
| `bible-study-theologian` | Deep scripture study, exegesis, theology |
| `faith-life-integration` | Applying faith to real decisions |
| `sunday-school-teacher` | Lesson planning, curriculum design |

### Strategy & Business
| Skill | Triggers On |
|-------|------------|
| `consulting-operations` | Client management, proposals, SOWs |
| `entrepreneurial-os` | Business stage navigation, startup ops |
| `business-plan-architect` | Business plans, pitch decks |
| `financial-model-architect` | Financial modeling, projections |
| `pricing-strategist` | Pricing models, rate setting |
| `go-to-market-engine` | Launch strategy, GTM plans |
| `market-intelligence` | Market research, competitive analysis |
| `business-genius` | Strategic thinking, business frameworks |
| `ai-agentic-specialist` | AI agent design, agentic systems |

### Legal-Financial
| Skill | Triggers On |
|-------|------------|
| `startup-tax-strategist` | Business taxes, S-Corp, deductions, quarterly estimates |

### Growth & Marketing
| Skill | Triggers On |
|-------|------------|
| `professional-communicator` | Emails, presentations, professional writing |
| `content-marketing-machine` | Content strategy, blog posts, SEO |
| `copywriting-conversion` | Sales copy, landing pages |
| `sales-closer` | Sales conversations, objection handling |
| `personal-brand-builder` | Personal branding, thought leadership |
| `social-media-architect` | Social media strategy |
| `community-builder` | Community building, engagement |
| `marketing-strategist` | Marketing strategy, campaigns |
| `growth-hacking-engine` | Growth experiments, viral loops |

### Microsoft
| Skill | Triggers On |
|-------|------------|
| `power-apps` | Power Apps development |
| `power-automate` | Power Automate flows |
| `power-bi` | Power BI reports, DAX |
| `copilot-studio` | Copilot Studio agents |
| `microsoft-dataverse` | Dataverse design |
| `sharepoint` | SharePoint sites, lists |
| `m365-integration` | Microsoft 365 integration |
| `power-platform-admin` | Power Platform administration |

### Product
| Skill | Triggers On |
|-------|------------|
| `micro-saas-builder` | SaaS product development |
| `biohacking-data-pipeline` | Biohacking data systems |
| `health-biohacking-protocol` | Health protocols, supplements, biomarkers |
| `brand-website-strategy` | Website strategy and design |
| `cloud-migration-playbook` | Cloud migration, GCP deployment |
| `ai-business-optimizer` | AI-powered business optimization |

---

## Routing Algorithm

For every request, run through this decision tree:

### Step 1: Identify the Domain
What is the user asking about? Map to one or more domains:
- Building/coding something → Engineering
- Business decision → Strategy
- Client/consulting work → Strategy + Growth
- Faith/ministry question → Faith
- Health/wellness → Product (health-biohacking-protocol)
- Data/analysis → Engineering (data-analytics-engine)
- Microsoft/Power Platform → Microsoft
- Tax/financial → Legal-Financial
- Writing/communication → Growth (professional-communicator)
- Productivity/organization → Core

### Step 2: Identify Primary + Supporting Skills
Every request has:
- **Primary skill** — the main domain expert (1 skill)
- **Supporting skills** — skills that add quality layers (0-3 skills)

**Examples:**
| Request | Primary | Supporting |
|---------|---------|------------|
| "Build a FastAPI endpoint" | code-review | app-security-architect, testing-strategy |
| "Write a client proposal" | consulting-operations | professional-communicator, pricing-strategist |
| "Create a Sunday school lesson on grace" | sunday-school-teacher | bible-study-theologian |
| "Analyze my blood work results" | health-biohacking-protocol | data-analytics-engine |
| "Build an n8n workflow for data sync" | n8n-workflow-architect | docker-infrastructure, app-security-architect |
| "How should I structure my LLC for taxes?" | startup-tax-strategist | consulting-operations |
| "Build an MCP server for my database" | mcp-server-builder | app-security-architect, database-design |
| "I'm overwhelmed with too many projects" | personal-productivity | faith-life-integration, knowledge-management |

### Step 3: Check Meta-Layer Skills
These always apply on top of the primary + supporting:
- `anti-hallucination` — on every response with factual claims
- `prompt-amplifier` — silently optimizes the request
- `session-optimizer` — if context is getting long

### Step 4: Determine Execution Order
1. Meta-layer skills (background, automatic)
2. Primary skill (invoke first — this sets the framework)
3. Supporting skills (invoke as needed during execution)
4. `parallel-execution-strategist` (if work can be parallelized)

---

## Multi-Skill Chain Patterns

### Pattern: Design → Build → Secure → Test
```
Request: "Build a user authentication system"
Chain: app-security-architect (threat model) →
       code-review (design patterns) →
       database-design (schema) →
       testing-strategy (test plan) →
       parallel-execution-strategist (parallelize implementation)
```

### Pattern: Research → Strategy → Execute → Communicate
```
Request: "Enter a new market with my AI consulting services"
Chain: market-intelligence (research) →
       go-to-market-engine (strategy) →
       pricing-strategist (pricing) →
       consulting-operations (proposal templates) →
       professional-communicator (outreach emails)
```

### Pattern: Study → Apply → Teach
```
Request: "Prepare to teach on the parable of the talents"
Chain: bible-study-theologian (exegesis) →
       faith-life-integration (personal application) →
       sunday-school-teacher (lesson plan)
```

### Pattern: Measure → Analyze → Optimize → Track
```
Request: "Optimize my health protocol based on recent blood work"
Chain: health-biohacking-protocol (interpret results) →
       data-analytics-engine (trend analysis) →
       personal-productivity (schedule the protocol) →
       n8n-workflow-architect (automate tracking reminders)
```

---

## When Skills Are Missing

If a request doesn't map to any existing skill:
1. Execute with general knowledge (Claude is capable without skills)
2. Note the gap for the user: "This would benefit from a dedicated [X] skill"
3. Offer to build one using `skill-amplifier` + `skill-builder`

---

## Self-Evaluation (run before routing)

Before routing a request, silently check:
[ ] Have I identified ALL skills that apply, not just the obvious one?
[ ] Is the primary skill correct, or am I defaulting to a familiar one?
[ ] Are meta-layer skills (anti-hallucination, prompt-amplifier) active?
[ ] If multiple skills apply, is the execution order logical?
[ ] Am I invoking skills, not just thinking about them?
If any check fails, re-route before proceeding.
