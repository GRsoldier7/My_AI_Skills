---
name: discover-observability
description: Auto-discover observability and monitoring skills when working with logging, metrics, tracing, alerting, health checks, or production monitoring. Routes to optimal observability patterns.
---

# Discover Observability Skills

Auto-routing skill for observability, monitoring, and production health across the stack.

## When This Activates

- Structured logging (structlog, Python logging)
- Health check endpoints
- Performance monitoring and metrics
- Error tracking and alerting
- Database monitoring and slow query detection
- Container health and resource monitoring

## Skill Chain

| Task | Primary Skill | Supporting |
|------|--------------|------------|
| API health checks | `fastapi-async-postgres-architecture` | `docker-compose-production` |
| DB performance monitoring | `sql-optimization-patterns` | `postgresql-table-design` |
| Container monitoring | `docker-compose-production` | `terraform-gcp-cloud-run` |
| Error tracking setup | `app-security-architect` | `senior-data-engineer` |
| Production readiness | `docker-compose-production` | `cloudflare` |

## Decision Rules

1. **Need health endpoints?** Use `fastapi-async-postgres-architecture` for /health patterns
2. **Slow DB queries in prod?** Use `sql-optimization-patterns` for pg_stat_statements
3. **Container resource issues?** Use `docker-compose-production` for resource limits and health checks
4. **Cloud monitoring?** Use `terraform-gcp-cloud-run` for GCP Cloud Monitoring integration
