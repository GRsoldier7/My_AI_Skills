---
name: discover-cloud
description: Auto-discover cloud infrastructure skills when working with GCP, AWS, Azure, Cloud Run, Cloud SQL, Terraform, serverless, or cloud deployment. Routes to the optimal cloud skill for the task.
---

# Discover Cloud Skills

Auto-routing skill that activates when cloud infrastructure work is detected and chains the optimal skills.

## When This Activates

- GCP services (Cloud Run, Cloud SQL, Cloud Storage, IAM, Secret Manager)
- Terraform infrastructure-as-code
- Docker containerization for cloud deployment
- Serverless architecture
- Cloud migration from homelab/on-prem

## Skill Chain

| Task | Primary Skill | Supporting |
|------|--------------|------------|
| Provision GCP infra | `terraform-gcp-cloud-run` | `cloudflare` (CDN/WAF) |
| Containerize for deploy | `docker-compose-production` | `app-security-architect` |
| Migrate homelab to GCP | `cloud-migration-playbook` | `terraform-gcp-cloud-run` |
| Cloud SQL setup | `postgresql-table-design` | `database-migration` |
| Secure cloud services | `app-security-architect` | `cloudflare` |

## Decision Rules

1. **New GCP project?** Start with `terraform-gcp-cloud-run` for IaC foundation
2. **Dockerizing existing app?** Start with `docker-compose-production` for Dockerfile
3. **Cloud SQL schema?** Chain `postgresql-table-design` then `database-migration`
4. **Edge/CDN/WAF?** Use `cloudflare` for Cloudflare Workers/Pages/WAF
5. **Security audit?** Use `app-security-architect` with cloud context
