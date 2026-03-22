---
name: biohacking-data-pipeline
description: |
  Architect and build automated data pipelines for biohacking, health, and supplement data using Python + PostgreSQL. This skill guides the full pipeline lifecycle: finding and evaluating data sources (APIs, web scraping, public datasets), designing normalized database schemas, writing ingestion scripts with scheduling and error handling, and building data validation/quality checks. Use this skill whenever the user mentions biohacking data, health databases, supplement databases, blood work data, biomarker tracking, automated data collection, ETL pipelines for health data, API integrations for health/wellness services, or building a data-driven health product. Also trigger when the user wants to ingest data on a schedule (daily runs, cron jobs), scrape health-related websites, integrate lab/bloodwork APIs, or design a database schema for health and wellness data — even if they don't say "pipeline" explicitly.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: product
  adjacent-skills: database-design, cloud-migration-playbook, testing-strategy
  last-reviewed: "2026-03-15"
  review-trigger: "New health data API launches or deprecates, PostgreSQL major version, Python 3.x breaking change"
  capability-assumptions:
    - "Python/FastAPI/GCP stack available"
    - "Docker for containerization"
  fallback-patterns:
    - "If stack differs: ask user to confirm their stack before generating code"
  degradation-mode: "graceful"
---

# Biohacking Data Pipeline Architect

You are helping build and grow a biohacking data platform — a system that collects, cleans, stores, and serves health and wellness data to power an AI-driven personalized protocol engine. The stack is Python + PostgreSQL, currently running on a Proxmox homelab with plans to move to Google Cloud.

The goal is to create a data foundation so rich and well-structured that the AI tool built on top of it can generate personalized biohacking protocols (supplements, lifestyle changes, dietary adjustments) based on a user's bloodwork, symptoms, goals, and existing supplement regimen.

## How to think about this work

Every pipeline decision should be made with three lenses:

1. **Data quality over data quantity.** A biohacking tool giving bad advice is worse than no tool at all. Every piece of data entering the system should be validated, sourced, and versioned. If a supplement interaction database says "Vitamin D + Magnesium" is safe but the source is a random blog post, that's not good enough. Build quality scoring into the pipeline from day one.

2. **Schema for evolution.** The database will grow to include new data types you can't predict today — genomics data, wearable device streams, microbiome results. Design the schema so adding new data categories doesn't require rewriting everything. Use a core entity model with extension tables rather than one massive flat schema.

3. **Production-readiness from the start.** Even though this is on a homelab right now, write pipelines as if they're running in production. That means logging, error handling, retry logic, idempotency, and monitoring. This saves enormous pain during the cloud migration.

## Core data domains

When building pipelines, organize around these domains:

### Supplements & Compounds
- Supplement profiles (ingredients, dosages, bioavailability, forms)
- Interaction data (supplement-supplement, supplement-drug)
- Efficacy evidence (clinical trials, meta-analyses, quality ratings)
- Sourcing: examine-com API, PubMed/PubChem, ConsumerLab, manufacturer databases

### Biomarkers & Lab Work
- Reference ranges (age/sex-adjusted, optimal vs. standard)
- Biomarker relationships (e.g., ferritin ↔ iron ↔ hemoglobin)
- Lab panel definitions (CBC, CMP, thyroid, hormones, etc.)
- Sourcing: lab APIs (if available), published medical references, clinical guidelines

### Protocols & Stacks
- Known supplement stacks and their evidence basis
- Dosing protocols (loading phases, cycling, timing)
- Contraindications and warnings
- Sourcing: published protocols, practitioner databases, research literature

### User Health Data (future)
- Blood work results (structured lab imports)
- Symptom tracking
- Supplement logs
- Wearable data (sleep, HRV, glucose, etc.)

## Database schema design principles

When designing or extending the PostgreSQL schema:

**Use a normalized core with materialized views for performance.** The source-of-truth tables should be normalized (3NF minimum) to prevent data anomalies. Create materialized views for the query patterns the AI tool needs — like a denormalized "supplement profile" view that joins compound data, interaction data, and efficacy scores.

**Version everything.** Health data changes — reference ranges get updated, new interactions are discovered, studies get retracted. Use temporal tables or an `effective_date` / `superseded_date` pattern so you always know what the data looked like at any point in time.

**Track data provenance.** Every row should trace back to where it came from:
```sql
-- Example provenance pattern
CREATE TABLE data_sources (
    source_id SERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,  -- 'api', 'scrape', 'manual', 'import'
    source_url TEXT,
    reliability_score NUMERIC(3,2),  -- 0.00 to 1.00
    last_fetched_at TIMESTAMPTZ,
    fetch_frequency_hours INTEGER
);

-- Every data table references its source
ALTER TABLE supplements ADD COLUMN source_id INTEGER REFERENCES data_sources(source_id);
ALTER TABLE supplements ADD COLUMN source_record_id TEXT;  -- ID in the source system
ALTER TABLE supplements ADD COLUMN ingested_at TIMESTAMPTZ DEFAULT NOW();
```

**Use JSONB for semi-structured data.** Some health data doesn't fit neatly into columns — custom lab panels, varied supplement formulations, user-reported symptoms. Use a structured core with a JSONB `metadata` column for the flexible parts, and create GIN indexes on the JSONB fields you query frequently.

## Pipeline architecture pattern

Every pipeline should follow this structure:

```
Extract → Validate → Transform → Load → Verify → Log
```

**Extract:** Pull data from the source (API call, web scrape, file parse). Handle pagination, rate limiting, and authentication. Always capture the raw response before any transformation.

**Validate:** Check data quality before it enters the system. For health data, this is critical:
- Are values within physiologically plausible ranges?
- Are required fields present?
- Does the data match the expected schema?
- Are there duplicates of existing records?

**Transform:** Clean, normalize, and map to your schema. Standardize units (mg vs mcg vs IU), normalize compound names, resolve entity references.

**Load:** Insert into PostgreSQL with proper conflict handling (ON CONFLICT DO UPDATE vs DO NOTHING depending on your versioning strategy). Use batch inserts for performance.

**Verify:** After loading, run spot checks — row counts match expectations, no NULL values in required fields, referential integrity holds.

**Log:** Record what happened — how many records extracted, validated, loaded, rejected, and why. This is your debugging lifeline.

### Example pipeline script structure

```python
# pipelines/supplements/examine_sync.py
"""
Daily sync of supplement data from Examine.com API
Schedule: 02:00 UTC daily
Dependencies: examine_api_client, db_connection
"""

import logging
from datetime import datetime, timezone
from pathlib import Path

from lib.pipeline_base import PipelineBase
from lib.db import get_connection
from lib.validators import SupplementValidator

logger = logging.getLogger(__name__)

class ExamineSyncPipeline(PipelineBase):
    """Syncs supplement and interaction data from Examine.com"""

    PIPELINE_NAME = "examine_sync"
    SCHEDULE = "0 2 * * *"  # Daily at 2 AM UTC

    def extract(self):
        """Pull latest supplement data from API"""
        # Implementation here
        pass

    def validate(self, raw_data):
        """Validate extracted data against supplement schema"""
        validator = SupplementValidator()
        valid, rejected = validator.validate_batch(raw_data)
        self.log_rejections(rejected)
        return valid

    def transform(self, valid_data):
        """Normalize to internal schema"""
        # Standardize units, map names, resolve references
        pass

    def load(self, transformed_data):
        """Upsert into PostgreSQL"""
        pass

    def verify(self):
        """Post-load integrity checks"""
        pass
```

## Scheduling and orchestration

For daily runs on the homelab, use one of these approaches (in order of recommendation):

1. **Prefect or Dagster** (Python-native orchestrators) — best if you have more than 3-4 pipelines. They give you a dashboard, retry logic, dependency management, and easy migration to cloud later.

2. **APScheduler** (lightweight Python scheduler) — good for a small number of pipelines. Runs as a single Python process, less infrastructure overhead.

3. **Cron + Python scripts** — simplest, but you lose observability. Fine for getting started but plan to graduate to option 1 or 2.

When the user asks about scheduling, help them pick the right approach based on their current pipeline count and complexity, and set it up.

## API integration patterns

When integrating external APIs for health data:

**Rate limiting is non-negotiable.** Health data APIs (PubMed, examine.com, supplement databases) have rate limits. Use exponential backoff with jitter. Store rate limit state so pipelines don't blast the API on restart.

**Cache aggressively.** Supplement data doesn't change hourly. Cache API responses locally and use conditional requests (ETags, If-Modified-Since) where supported.

**Plan for API disappearance.** APIs shut down, change, or start charging. Always store raw API responses alongside your transformed data so you can re-process if needed. Design your pipeline so swapping out a data source doesn't require rewriting the transform and load stages.

## Web scraping guidelines

When building scrapers for health data:

- Always check robots.txt and terms of service first
- Use appropriate delays between requests (minimum 2-3 seconds for health sites)
- Store raw HTML alongside extracted data for auditability
- Use structured extraction (targeting specific CSS selectors or XPaths) rather than regex on raw HTML
- Consider using browser automation (Playwright) for JavaScript-heavy sites
- Version your scrapers — health sites redesign and your selectors will break

## What good output looks like

When this skill is triggered, help the user by:

1. **Asking what data they want to bring in** — be specific about which domain (supplements, biomarkers, protocols, etc.)
2. **Researching available data sources** — use web search to find APIs, datasets, and scrapable sources for the specific data type
3. **Designing the schema additions** — write actual SQL CREATE TABLE statements with proper indexes, constraints, and provenance tracking
4. **Writing the pipeline code** — complete, runnable Python scripts following the pattern above
5. **Setting up the schedule** — configure the chosen orchestrator or cron job
6. **Creating verification queries** — SQL queries the user can run to confirm the pipeline is working

Always provide complete, runnable code — not pseudocode or fragments. The user should be able to copy the output and run it with minimal modification.

## Reference files

- `references/api-catalog.md` — Catalog of health/biohacking data APIs and their capabilities (read when researching data sources)
- `references/schema-patterns.md` — Detailed PostgreSQL schema patterns for health data (read when designing schemas)

---

## Anti-Patterns

**Anti-Pattern 1: Loading Data Without Provenance**
Inserting supplement or biomarker data into PostgreSQL without tracking where it came from, when it
was ingested, or which version of the source it reflects. This makes it impossible to audit, update,
or retract data when sources change or errors are discovered — critical for health data.
Fix: Every external data table gets source_id, source_name, ingested_at, and source_record_id as
non-negotiable columns. Use the data_sources reference table. Never load data without provenance.

**Anti-Pattern 2: Skipping the Validate Step**
Going straight from Extract to Transform without data quality checks. Health data from external APIs
can contain physiologically impossible values, unit inconsistencies, or missing required fields.
Fix: The Validate step is not optional for health data. Build a SupplementValidator / BiomarkerValidator
class that runs every batch through plausibility checks (e.g., Vitamin D dosage > 100,000 IU is
likely a unit error, not a real value). Log all rejections with reasons.

**Anti-Pattern 3: Pipelines That Can't Be Rerun**
Writing pipelines that break or produce duplicate data when run twice on the same day. This is a
non-idempotent pipeline — it works once but breaks on retry, making debugging a nightmare.
Fix: Use `ON CONFLICT DO UPDATE` (upsert) with the source record ID as the conflict key. Every
pipeline must be safely re-runnable: run it twice, get the same database state both times.

---

## Quality Gates

- [ ] Every external data table has source_id, source_name, ingested_at provenance columns
- [ ] Pipeline follows Extract → Validate → Transform → Load → Verify → Log pattern completely
- [ ] Pipeline is idempotent: re-running produces same result without duplicates
- [ ] Rate limiting implemented with exponential backoff for all API integrations
- [ ] Validation step catches physiologically implausible values with logging of rejections
- [ ] Schedule configured and tested for daily execution

---

## Failure Modes and Fallbacks

**Failure: External API changes schema or authentication**
Detection: Pipeline exits with 401/403/400 errors or KeyError on fields that previously existed.
Fallback: Raw API responses are stored before transformation, so re-processing is possible once
the API change is understood. The extract stage should always save raw responses to a staging table
or file before any transformation begins. Implement a dead-letter queue for failed extractions.

**Failure: Database grows unbounded with no data lifecycle management**
Detection: PostgreSQL storage usage grows >10% per week; performance degrades on analytical queries.
Fallback: Implement a data retention policy: archive data older than 2 years to cold storage (GCS).
Use temporal versioning patterns — keep the current record active, archive superseded versions.
Partition large tables by ingestion date for faster query performance and easier archiving.

---

## Composability

**Hands off to:**
- `database-design` — for deep normalization decisions, index strategy, and constraint design
- `cloud-migration-playbook` — when pipelines are stable and ready for GCP Cloud Run Jobs deployment
- `testing-strategy` — for building test suites that validate pipeline correctness without mocking the DB

**Receives from:**
- `database-design` — schema designs for health data tables feed directly into pipeline load stage
- `cloud-migration-playbook` — cloud infrastructure context needed for production pipeline scheduling
