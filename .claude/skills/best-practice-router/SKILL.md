---
name: best-practice-router
description: Meta-skill that auto-selects the optimal skill chain for any task. Ensures every project gets best-of-the-best execution by routing through domain-specific discover skills, community elite skills, and custom domain skills. Invoke on every non-trivial request.
---

# Best Practice Router

The master routing layer that ensures every task activates the optimal combination of skills — custom domain skills (skills/), Context7 library skills (.claude/skills/), and community elite skills — for best-of-the-best execution on every project.

## How It Works

This skill sits ABOVE `master-orchestrator` (which routes custom skills in `skills/`) and adds the `.claude/skills/` layer — library-specific patterns, community elite skills, and auto-discovery routing.

**Execution order:**
1. **Discover skills** fire first (auto-detect domain)
2. **Custom domain skills** from `skills/` (deep expertise)
3. **Library skills** from `.claude/skills/` (current docs + patterns)
4. **Design/polish skills** fire last (quality layer)

## Complete Skill Registry

### Auto-Discovery Layer (fires first — detects domain)
| Skill | Detects |
|-------|---------|
| `discover-database` | SQL, PostgreSQL, schema, queries, ORMs, migrations |
| `discover-data` | ETL, pipelines, streaming, batch processing, data validation |
| `discover-frontend` | React, Next.js, UI, state, forms, accessibility, SEO |
| `discover-api` | REST, GraphQL, auth, rate limiting, API design |
| `discover-security` | Auth, input validation, secrets, vulnerability assessment |
| `discover-testing` | Unit, integration, e2e, TDD, mocking, coverage |
| `discover-engineering` | Code review, docs, debugging, profiling, deployment |
| `discover-cloud` | GCP, AWS, Cloud Run, Terraform, serverless |
| `discover-caching` | Redis, CDN, query cache, connection pooling |
| `discover-observability` | Logging, metrics, tracing, health checks, alerts |

### Database Lifecycle (full pipeline)
| Phase | Skill | What It Does |
|-------|-------|-------------|
| 1. Schema Design | `postgresql-table-design` | Data types, indexing, constraints, normalization |
| 2. Data Modeling | `senior-data-engineer` | Full data architecture, pipeline design |
| 3. ORM Layer (Python) | `fastapi-async-postgres-architecture` | Async SQLAlchemy, Pydantic v2, DI |
| 4. ORM Layer (TypeScript) | `prisma-cli` + `prisma-client-api` + `prisma-database-setup` | Prisma schema, queries, setup |
| 5. Migrations | `database-migration` | Zero-downtime, rollback, data transforms |
| 6. Query Optimization | `sql-optimization-patterns` | EXPLAIN analysis, indexing strategy |
| 6b. Advanced Performance | `postgresql-performance-patterns` | JSONB, pgbouncer, partitioning, BRIN, auto_explain |
| 7. Async Migrations | `alembic-async-migrations` | Alembic + async SQLAlchemy, autogenerate, batch ops |
| 8. Data Quality | `data-quality-frameworks` | Great Expectations, dbt tests, contracts |
| 9. Python Pipelines | `python-data-pipeline-patterns` | Polars, pandas, pandera, async ETL, streaming |
| 10. Transformations | `dbt-transformation-patterns` | dbt models, testing, incremental |
| 11. Orchestration | `airflow-dag-patterns` | Production DAGs, operators, sensors |
| 12. Reporting | `data-storytelling` | Visualization, narrative, executive decks |

### Frontend Premium ($100k Website Suite)
| Phase | Skill | What It Does |
|-------|-------|-------------|
| 1. Design System | `frontend-design` (Anthropic) | Production-grade UI, avoids AI aesthetics |
| 2. Theme | `theme-factory` (Anthropic) | 10 pre-set color/typography systems |
| 3. Guidelines | `web-design-guidelines` (Vercel) | Web Interface Guidelines compliance |
| 4. React Patterns | `vercel-react-best-practices` (Vercel) | Performance optimization |
| 5. Composition | `vercel-composition-patterns` (Vercel) | Scalable component patterns |
| 6. Tailwind | `tailwind-design-system` | Design tokens, responsive patterns |
| 7. Next.js | `nextjs-react-tailwind-shadcn` | App Router, Server Components, shadcn |
| 8. Animation | `animate` (Impeccable) | Micro-interactions, motion design |
| 9. Color | `design-colorize` (Impeccable) | Strategic color application |
| 10. Bold | `design-bolder` (Impeccable) | Amplify safe designs |
| 11. Delight | `design-delight` (Impeccable) | Joy, personality, memorable moments |
| 12. Simplify | `design-distill` (Impeccable) | Strip to essence |
| 13. Critique | `design-critique` (Impeccable) | UX evaluation and feedback |
| 14. Polish | `design-polish` (Impeccable) | Final pixel-perfect pass |

### Infrastructure & Deploy
| Skill | What It Does |
|-------|-------------|
| `docker-compose-production` | Multi-stage Dockerfiles, health checks, secrets |
| `terraform-gcp-cloud-run` | Cloud Run, Cloud SQL, IAM, Secret Manager |
| `cloudflare` | Workers, Pages, KV, D1, R2, WAF, DDoS |

### Testing
| Skill | What It Does |
|-------|-------------|
| `pytest-async-testing-patterns` | Async fixtures, hypothesis, transaction rollback |

## Routing Decision Tree

```
User Request
│
├─ "Build a website/page/UI" ──────────► Frontend Premium chain
│   → frontend-design → tailwind-design-system → nextjs-react-tailwind-shadcn
│   → animate → design-polish (finish)
│
├─ "Design a database/schema" ────────► Database chain
│   → postgresql-table-design → fastapi-async-postgres-architecture
│   → alembic-async-migrations → sql-optimization-patterns
│   → postgresql-performance-patterns (JSONB/partitioning/pgbouncer)
│
├─ "Build a data pipeline/ETL" ───────► Data Engineering chain
│   → senior-data-engineer → python-data-pipeline-patterns
│   → dbt-transformation-patterns → airflow-dag-patterns
│   → data-quality-frameworks
│
├─ "Deploy to production" ────────────► Infrastructure chain
│   → docker-compose-production → terraform-gcp-cloud-run
│   → cloudflare (CDN/WAF)
│
├─ "Build an API" ────────────────────► API chain
│   → fastapi-async-postgres-architecture → app-security-architect
│   → pytest-async-testing-patterns
│
├─ "Review/audit code" ───────────────► Quality chain
│   → discover-security → discover-testing → code-review
│   → design-critique (if frontend)
│
└─ "Full project from scratch" ───────► Complete chain
    → Database: postgresql-table-design → alembic-async-migrations → postgresql-performance-patterns
    → API: fastapi-async-postgres-architecture → app-security-architect
    → Frontend: frontend-design → nextjs-react-tailwind-shadcn → animate
    → Infra: docker-compose-production → terraform-gcp-cloud-run → cloudflare
    → Tests: pytest-async-testing-patterns
    → Polish: design-polish → design-delight
```

## Quality Gate

Before marking ANY task complete, verify:
- [ ] Was the discover-* skill for this domain invoked?
- [ ] Was the primary domain skill used (not just general knowledge)?
- [ ] For frontend: did the design-polish pass run?
- [ ] For database: was sql-optimization-patterns + postgresql-performance-patterns consulted?
- [ ] For migrations: was alembic-async-migrations used (not just database-migration)?
- [ ] For data pipelines: was python-data-pipeline-patterns used?
- [ ] For deploy: was security reviewed (app-security-architect)?
