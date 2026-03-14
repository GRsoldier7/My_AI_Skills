# GCP Cost Optimization for Early-Stage Startups

Strategies to keep your Google Cloud bill minimal while building a production-grade platform.

## Table of Contents
1. [Free Tier Maximization](#free-tier-maximization)
2. [Compute Optimization](#compute-optimization)
3. [Database Cost Management](#database-cost-management)
4. [Storage Strategies](#storage-strategies)
5. [Monitoring Your Bill](#monitoring-your-bill)

---

## Free Tier Maximization

GCP offers a generous free tier — use every bit of it:

- **Cloud Run:** 2M requests/month, 360,000 GB-seconds compute, 180,000 vCPU-seconds
- **Cloud Functions:** 2M invocations/month, 400,000 GB-seconds
- **Cloud Storage:** 5GB standard storage, 5,000 Class A operations, 50,000 Class B
- **BigQuery:** 1TB query processing/month, 10GB storage
- **Artifact Registry:** 500MB storage
- **Cloud Build:** 120 build-minutes/day
- **Secret Manager:** 6 active secret versions, 10,000 access operations/month

Design your architecture to stay within these limits during early development.

## Compute Optimization

### Cloud Run
- **Scale to zero:** Default behavior — you pay nothing when no traffic arrives
- **Min instances = 0:** Unless cold start latency matters for your API, keep min at 0
- **Right-size containers:** Start with 256MB memory / 1 vCPU and increase only if you see OOM errors or slow responses
- **Concurrency:** Set to 80-100 (default) to handle multiple requests per instance
- **Request timeout:** Set appropriately — don't let hung requests burn compute time

### Cloud Run Jobs (pipelines)
- **Execution time is money:** Optimize pipeline scripts to run faster — batch database inserts, use connection pooling, minimize API round-trips
- **Schedule smartly:** Daily runs at off-peak hours (2-4 AM) can sometimes avoid congestion

## Database Cost Management

### Cloud SQL
- **Start with the smallest instance:** `db-f1-micro` (shared vCPU, 0.6GB RAM) is ~$7/month and handles light workloads fine
- **Auto-storage increase:** Enable it but start with 10GB — you'll get alerts before hitting limits
- **Stop the instance when not in use:** During early development, stop the instance at night/weekends. Use Cloud Scheduler to auto-start/stop
- **No HA until you need it:** High availability doubles the cost. Enable it when you have real users who need uptime guarantees
- **Connection pooling:** Use PgBouncer or Cloud SQL Auth Proxy connection pooling to reduce connection overhead

### When to upgrade
- Move to `db-g1-small` (~$25/month) when you see slow query performance
- Move to `db-custom-1-3840` (~$50/month) when you need dedicated resources
- Enable HA when downtime costs more than the ~$50/month HA premium

## Storage Strategies

- **Lifecycle rules:** Automatically move old data to cheaper storage classes (Nearline at 30 days, Coldline at 90 days, Archive at 365 days)
- **Delete what you don't need:** Temporary files, old build artifacts, test data
- **Compress before storing:** gzip pipeline outputs before writing to Cloud Storage

## Monitoring Your Bill

### Set up budget alerts immediately
```bash
# Create a budget alert (do this on day 1)
gcloud billing budgets create \
  --billing-account=YOUR_BILLING_ACCOUNT \
  --display-name="Monthly Budget Alert" \
  --budget-amount=50 \
  --threshold-rules=percent=0.5 \
  --threshold-rules=percent=0.9 \
  --threshold-rules=percent=1.0
```

### Use the Cost Table in Cloud Console
- Check weekly during development
- Group by service to see where money goes
- Look for unexpected charges (often: forgotten instances, storage growth, egress)

### Common surprise costs
- **Egress (data leaving GCP):** Charged per GB. Keep data within GCP where possible
- **Cloud SQL backups:** Automated backups consume storage — keep retention reasonable (7 days is fine to start)
- **Logging:** Cloud Logging ingestion is free up to 50GB/month but can add up. Set log exclusion filters for verbose services
- **Idle resources:** Instances, disks, and IPs that exist but aren't being used still cost money. Audit monthly.
