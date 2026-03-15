---
name: cloud-migration-playbook
description: |
  Guide the migration of applications, databases, and services from a self-hosted homelab (Proxmox) to Google Cloud Platform for production deployment. This skill covers containerization with Docker, GCP service selection (Cloud Run, Cloud SQL, GKE, Cloud Functions), database migration from local PostgreSQL to Cloud SQL, CI/CD pipeline setup, infrastructure-as-code with Terraform, cost optimization, security hardening, and production monitoring. Use this skill whenever the user mentions cloud migration, moving to production, deploying to GCP, containerizing applications, Docker, Kubernetes, Cloud Run, Cloud SQL, Terraform, production infrastructure, scaling, DevOps, CI/CD, or taking something from "homelab to cloud" — even if they just say "I need to get this running for real users" or "how do I scale this."
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: product
  adjacent-skills: biohacking-data-pipeline, database-design, testing-strategy
  last-reviewed: "2026-03-15"
  review-trigger: "GCP service pricing or feature change, Docker major version, Terraform breaking change"
---

# Cloud Migration Playbook: Proxmox Homelab → Google Cloud

You are helping migrate a biohacking data platform from a Proxmox homelab to Google Cloud Platform. The platform currently consists of Python data pipelines, a PostgreSQL database, and will eventually include an AI-powered API serving personalized health protocols. The goal is production-grade infrastructure that can scale with user growth while keeping costs manageable during the early stages.

## Migration philosophy

Three principles guide every decision:

1. **Start small, architect for scale.** Use managed services that auto-scale (Cloud Run, Cloud SQL) rather than provisioning fixed infrastructure. Pay for what you use during the early stage, but design the architecture so you can handle 100x growth without re-architecting.

2. **Automate everything from day one.** If you deploy manually, you'll deploy manually forever. Set up CI/CD, infrastructure-as-code, and automated testing before migrating the first service. The upfront cost saves enormous pain later.

3. **Security is not optional.** Health data has regulatory implications (HIPAA if you ever touch PHI). Even if you're not handling protected health information today, build the security posture now — it's 10x harder to retrofit.

## Migration phases

### Phase 1: Containerize locally (do this before touching GCP)

Before migrating anything, get everything running in Docker on the homelab first. This proves the containerization works in a familiar environment.

**For each service, create:**

```dockerfile
# Example: Python data pipeline service
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

CMD ["python", "-m", "pipelines.scheduler"]
```

**Use docker-compose for local orchestration:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: biohacking
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"

  pipeline-scheduler:
    build: ./pipelines
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/biohacking
    depends_on:
      - db

  api:
    build: ./api
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/biohacking
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  pgdata:
```

**Verify everything works locally in containers before proceeding.** If it doesn't work in Docker on the homelab, it won't work in the cloud.

### Phase 2: Set up GCP foundation

**Project structure:**

```
biohacking-platform/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── networking/
│   │   ├── database/
│   │   ├── cloud-run/
│   │   └── monitoring/
│   └── environments/
│       ├── staging/
│       └── production/
├── .github/workflows/   (or cloudbuild.yaml)
│   ├── deploy-api.yml
│   ├── deploy-pipelines.yml
│   └── migrate-db.yml
└── ...application code...
```

**GCP service selection guide:**

| Component | Homelab | GCP Service | Why |
|-----------|---------|-------------|-----|
| PostgreSQL | Local PostgreSQL | **Cloud SQL for PostgreSQL** | Managed backups, HA, auto-scaling storage, no DBA needed |
| Pipeline scheduler | Cron/systemd | **Cloud Run Jobs + Cloud Scheduler** | Pay-per-execution, auto-scales, no server to maintain |
| API server | Python process | **Cloud Run** | Auto-scales to zero when idle (saves money early on), scales up under load |
| Secrets | .env files | **Secret Manager** | Encrypted, versioned, auditable, IAM-controlled |
| Container registry | Local | **Artifact Registry** | Integrated with Cloud Build, vulnerability scanning |
| Monitoring | Manual | **Cloud Monitoring + Cloud Logging** | Built-in alerting, dashboards, log analysis |
| CDN/DNS | None | **Cloud CDN + Cloud DNS** (when needed) | Global distribution for the website/API |

**Cost estimation for early stage (minimal traffic):**

- Cloud SQL (db-f1-micro, 10GB): ~$10-15/month
- Cloud Run (light API traffic): ~$0-5/month (generous free tier)
- Cloud Run Jobs (daily pipelines): ~$1-3/month
- Artifact Registry: ~$0.10/GB/month
- Secret Manager: ~$0.06 per secret version per month
- **Estimated total: $15-30/month** to start

This is the beauty of managed, serverless-ish services — you pay almost nothing at low scale and costs grow proportionally with usage.

### Phase 3: Database migration

This is the most critical and highest-risk step. Do it carefully.

**Migration approach:**

1. **Set up Cloud SQL instance** via Terraform
2. **Export from local PostgreSQL:**
   ```bash
   pg_dump -Fc -h localhost -U postgres biohacking > biohacking_backup.custom
   ```
3. **Upload to Cloud Storage:**
   ```bash
   gsutil cp biohacking_backup.custom gs://your-bucket/migrations/
   ```
4. **Import to Cloud SQL** (use the GCP Console or gcloud CLI)
5. **Verify data integrity:**
   - Row counts match for every table
   - Spot-check critical records
   - Run your existing data validation queries
   - Test all application queries against the new database
6. **Set up ongoing backups** (Cloud SQL does automated daily backups, but configure point-in-time recovery too)

**Critical: Run both databases in parallel for at least a week.** Point your pipelines at Cloud SQL but keep the local database running and compare results. Only decommission the local database after you're confident the cloud version is working correctly.

### Phase 4: Deploy services

Deploy in this order (each step should be stable before moving to the next):

1. **Database** (Cloud SQL) — already done in Phase 3
2. **Pipeline scheduler** (Cloud Run Jobs + Cloud Scheduler) — test that daily data ingestion works
3. **API** (Cloud Run) — point it at Cloud SQL, verify all endpoints
4. **CI/CD** — automate the above so future deploys are push-button

### Phase 5: Production hardening

Once services are running in GCP:

**Security:**
- Enable VPC with private IP for Cloud SQL (no public IP)
- Use IAM service accounts with least-privilege permissions
- Enable Cloud Armor WAF on the API (when public-facing)
- Encrypt data at rest (Cloud SQL does this by default) and in transit (enforce SSL)
- Set up security alerts for suspicious activity

**Monitoring:**
- Uptime checks on API endpoints
- Alerts for pipeline failures (Cloud Run Job failures → PagerDuty/Slack)
- Database performance monitoring (slow queries, connection pool usage)
- Budget alerts to avoid surprise bills

**Reliability:**
- Enable Cloud SQL high availability (regional) when traffic justifies the cost
- Set up Cloud Run min-instances to 1 for the API (eliminates cold starts, adds ~$15/month)
- Configure retry policies for pipeline jobs

## When to use which GCP compute service

This decision comes up constantly, so here's the decision tree:

**Cloud Run (services):** Your default choice for any long-running process that responds to HTTP requests. The API server goes here. Auto-scales including to zero.

**Cloud Run (jobs):** For batch processing that runs on a schedule or trigger. Data pipelines go here. Runs, completes, exits. You only pay for execution time.

**Cloud Functions:** For small, single-purpose event handlers. Like "when a new file lands in Cloud Storage, kick off processing." Not for complex pipelines.

**GKE (Kubernetes):** Only if you outgrow Cloud Run — typically when you need persistent connections (WebSockets), custom networking, or very fine-grained scaling control. Don't start here.

**Compute Engine (VMs):** Avoid for application workloads. Use only for things that truly need a persistent VM (like a bastion host or legacy software that can't be containerized).

## Terraform patterns

When writing Terraform for this project, follow these patterns:

- Use modules for reusable components (database, Cloud Run service, etc.)
- Separate environments (staging/production) using workspaces or directory structure
- Store state in a GCS backend bucket (never locally)
- Use variables for anything that differs between environments
- Tag all resources consistently for cost tracking

## Reference files

- `references/terraform-templates.md` — Ready-to-use Terraform templates for common GCP patterns (read when setting up infrastructure)
- `references/cost-optimization.md` — Detailed cost optimization strategies for GCP (read when the user asks about costs or bills)

---

## Anti-Patterns

**Anti-Pattern 1: Migrating Before Containerizing**
Attempting to migrate a non-containerized application directly to GCP by running it on a Compute
Engine VM, bypassing Docker and Cloud Run. This creates the same maintenance burden in the cloud
that existed in the homelab, without any of the managed service benefits.
Fix: Phase 1 is always "containerize locally first." If it doesn't run in Docker on the homelab,
don't touch GCP. Prove containerization works before cloud credentials are touched.

**Anti-Pattern 2: Decommissioning the Homelab Prematurely**
Shutting down local PostgreSQL and pipelines before the cloud version has been running correctly
for at least a week with verified data integrity.
Fix: Run parallel infrastructure for a minimum of 7 days after cloud migration. Compare row counts,
spot-check critical records, run validation queries against both databases. Only decommission the
homelab after explicit confirmation that the cloud version is producing identical results.

**Anti-Pattern 3: Manual Deployment Forever**
Setting up GCP services manually once and never building CI/CD. Every subsequent deployment requires
remembering the exact gcloud commands, configurations, and secrets. One wrong step corrupts production.
Fix: Terraform from day one for infrastructure. GitHub Actions (or Cloud Build) for application
deployments. The rule: if you can't deploy with a single `git push`, the infrastructure is not done.

---

## Quality Gates

- [ ] Application runs successfully in Docker locally before any GCP work begins
- [ ] All infrastructure defined in Terraform (no manually-provisioned resources)
- [ ] Terraform state stored in GCS backend (never local)
- [ ] All secrets in Secret Manager (no .env files or environment variables in container definitions)
- [ ] Cloud SQL connection uses private IP only (no public IP enabled)
- [ ] Budget alert configured at $30/month to catch runaway costs early
- [ ] Parallel run period of ≥7 days before homelab decommission

---

## Failure Modes and Fallbacks

**Failure: Cloud SQL migration produces data integrity issues**
Detection: Row counts mismatch between local and Cloud SQL after pg_dump/restore, or application
queries return incorrect results.
Fallback: Never delete the homelab database until this is resolved. Re-run the pg_dump with
`--data-only` and check for encoding issues or collation mismatches. Run the full data validation
query suite against both databases and compare output row-by-row for discrepancies.

**Failure: GCP costs spike unexpectedly**
Detection: Budget alert fires above $30/month threshold during early stage.
Fallback: Check Cloud Monitoring cost breakdown immediately. The most common culprits:
Cloud SQL instance left running at wrong tier (db-f1-micro → db-n1-standard-1 accidentally),
Cloud Run min-instances set too high, or Artifact Registry storing too many large images.
Set Cloud SQL auto-delete for old backups and implement image cleanup in CI/CD pipeline.

---

## Composability

**Hands off to:**
- `database-design` — when the Cloud SQL schema needs optimization for production query patterns
- `testing-strategy` — for integration testing against Cloud SQL before decommissioning homelab

**Receives from:**
- `biohacking-data-pipeline` — the application being migrated; pipeline architecture informs Cloud Run Jobs setup
- `database-design` — finalized schema design is the input to the Cloud SQL setup phase
