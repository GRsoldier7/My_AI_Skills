## Coding Conventions

- Python: snake_case, Google-style docstrings, type hints on all function signatures
- Files/directories: lowercase-with-hyphens
- Error handling: Explicit exception types, never bare `except`
- Logging: structlog with structured output (never `print()`)
- Config: Environment variables via pydantic-settings
- Secrets: Never in code -- Secret Manager or .env (local only)
- Tests: Written alongside implementation, not after. pytest with fixtures and parametrize.
- Commits: Descriptive messages explaining the WHY, not just the WHAT
- Async-first for I/O-bound operations (httpx, asyncpg)

## Operating Principles

1. **Reliability over speed.** Never guess at business logic. Ask if uncertain.
2. **Build for production from day one.** Even on the homelab, write code as if it's serving real users.
3. **AI-first but human-verified.** Use AI to move 10x faster but always validate critical decisions.
4. **Evidence-based everything.** Cite sources for claims. Label hypotheses clearly. Test assumptions.
5. **Security by default.** Least privilege, encrypted at rest and in transit, no secrets in code or logs.
6. **Document as you go.** Update docs in the same session as code changes. Keep everything current.

## What NOT To Do

- Don't use Django or Flask (we use FastAPI)
- Don't use MongoDB (we use PostgreSQL)
- Don't use AWS services (we use GCP)
- Don't skip type hints -- every function gets them
- Don't use print() for logging -- use structlog
- Don't hardcode configuration values -- use environment variables
- Don't put secrets in code
- Don't write bare except blocks
- Don't use string concatenation in SQL queries

## Approval Requirements (Non-Negotiable)

Always ask before:
- Git commits, PRs, merges, or pushes
- Deployments or production changes
- Secrets or credential changes
- Destructive actions (delete data, drop tables, rotate keys)
- Scope changes affecting cost, timeline, security, or compliance
