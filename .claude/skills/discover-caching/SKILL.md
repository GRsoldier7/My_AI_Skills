---
name: discover-caching
description: Auto-discover caching and performance skills when working with Redis, CDN caching, query caching, application caching, or performance optimization. Routes to optimal caching strategy.
---

# Discover Caching Skills

Auto-routing skill for caching strategy and performance optimization across the stack.

## When This Activates

- Redis configuration and patterns
- CDN/edge caching (Cloudflare)
- Database query caching and connection pooling
- Application-level caching (in-memory, distributed)
- Next.js ISR/SSG caching strategies
- API response caching

## Skill Chain

| Task | Primary Skill | Supporting |
|------|--------------|------------|
| Redis setup in Docker | `docker-compose-production` | `sql-optimization-patterns` |
| CDN/edge caching | `cloudflare` | `vercel-react-best-practices` |
| DB query optimization | `sql-optimization-patterns` | `postgresql-table-design` |
| Next.js caching | `vercel-react-best-practices` | `nextjs-react-tailwind-shadcn` |
| Full-stack perf audit | `sql-optimization-patterns` | `docker-compose-production` |

## Decision Rules

1. **Slow queries?** Start with `sql-optimization-patterns` for EXPLAIN analysis
2. **API latency?** Check `cloudflare` for edge caching or `docker-compose-production` for Redis
3. **Page load slow?** Use `vercel-react-best-practices` for Next.js optimization
4. **DB connection issues?** Use `postgresql-table-design` for connection pooling patterns
