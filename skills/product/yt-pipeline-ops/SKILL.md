---
name: yt-pipeline-ops
description: |
  Operate, debug, and re-run Aaron's Echelon YouTube pipeline — transcripts,
  entity extraction, embeddings, comments, evidence, dbt marts, schema governance,
  Temple Protocol export. The cron map, log paths, re-run recipes, and hard rules
  that keep the 36-day-silent-failure incident from recurring.

  EXPLICIT TRIGGER on: "extraction failed", "pipeline status", "transcript coverage",
  "re-run extraction", "dbt build", "schema drift", "golden set", "tier routing",
  "publish protocol export", "pipeline_events", "embeddings watchdog", "yt-dlp errors",
  "collector failed", "freshness alert", "parity check", "extraction backlog".

  Also trigger before ANY schema change on DB1/DB2 (governance gate) and when
  wiring new pipeline stages.
metadata:
  author: aaron-deyoung
  version: "0.9"
  domain-category: product
  adjacent-skills: yt-knowledge, biohacking-data-pipeline, database-design
  last-reviewed: "2026-07-04"
  review-trigger: "P1 collector unification, P2 tier router lands, yt2pg cron retirement"
  capability-assumptions:
    - "Runs on pve1 (192.0.2.10) as root; repo at /opt/echelon/Biohacking_Optimization"
    - "DB1 = 192.0.2.13:5432/youtube_videos (CT203); DB2 = 192.0.2.12:5433/postgres (CT105)"
    - "Cron = root crontab on pve1, NOT systemd timers"
  fallback-patterns:
    - "If a check script is missing: consult docs/ROADMAP_2026-06-05_data_platform.md before improvising"
    - "If DB creds fail: source /opt/echelon/Biohacking_Optimization/.env (override=False discipline)"
  degradation-mode: "strict — never bypass governance gates"
---

## Composability Contract
- Input expects: a pipeline symptom, re-run request, coverage question, or schema-change intent
- Output produces: diagnosis with log/SQL evidence, safe re-run commands, governance-compliant change steps
- Can chain from: yt-knowledge (missing/stale data), master-orchestrator
- Can chain into: superpowers:systematic-debugging (root-cause), database-design (schema work)
- Orchestrator notes: governance rules here are BLOCKING — schema change without expectations update = drift alarm

---

## Hard Rules (post-incident, non-negotiable)

1. **Any DDL on DB1/DB2** → update `scripts/cron/schema_expectations.sh` in the SAME change-set, deployed within the same hour (drift check fires hourly at :15 via `schema_drift_check.sh`).
2. **Freezing/retiring any feed** → update `scripts/cron/data_freshness_check.sh` (e.g. `:73` watches DB1 `video_transcripts.created_at`) + parity scope in the same change-set.
3. **New pipeline stage** → emit `pipeline_events` via `scripts/cron/emit_pipeline_event.py`; pipeline name must exist in `pipeline_logger.py` KNOWN_PIPELINES (`:36-37`) AND dbt `sources.yml` accepted_values.
4. **No `load_dotenv(override=True)`** with default APP_ENV on Echelon scripts (.env overlay trap).
5. **Unqualified DDL lands in `core`** (role search_path). Always schema-qualify.

## Cron Map (root crontab on pve1, verified 2026-07-04)

Times are SERVER-LOCAL **America/Chicago** (verified via timedatectl) — NOT UTC. No CRON_TZ set.

| Local (CT) | Job | Log |
|---|---|---|
| 01:00 | YT metadata sync `/opt/YouTube2Sheets/scripts/run_youtube_sync.sh` | /var/log/youtube_sync.log |
| 01:30 | DB2 backup `backup_db.sh` · 02:15 DB1 backup `backup_db1.sh` | /var/log/echelon_backup.log |
| 02:00, 22:00 | Echelon transcripts + embeddings `run_transcripts_scheduled.sh` | /var/log/echelon_transcripts.log |
| 02:30, 03:00, 12:00, 21:00 | yt2pg transcript collectors (DB1) — RETIRE after P1 soak | /var/log/yt2pg_transcripts.log |
| 04:00 | Extraction `run_extraction_scheduled.sh --topics $HEALTH_TOPICS --batch-per-topic 100` | /var/log/echelon_extraction.log |
| 04:30 | Parity check `05b_parity_check_wrapper.sh` | (wrapper-managed) |
| 05:00 / 06:00 | Comments collect / analyze | /var/log/echelon_comments.log, echelon_analyze_comments.log |
| 06:00 | Evidence scores `refresh_evidence_scores.sh` | /var/log/echelon_evidence_scores.log |
| 07:00 | Daily status report | /var/log/echelon_daily_status.log |
| 07:30 | dbt build `run_dbt_build.sh` (4h timeout, keepalive guards) | (script-managed) |
| every 30m | `embeddings_watchdog.sh` + `sync_db1_to_db2.sh` (FDW metadata only — NO transcripts) | /var/log/echelon_embeddings.log, echelon_db1_to_db2_sync.log |
| hourly :15 | `schema_drift_check.sh` | /var/log/echelon_schema_drift.log |
| every 4h :45 | `data_freshness_check.sh` | /var/log/echelon_freshness.log |
| Sun 02:00 / 08:00 / 19:00 | Evidence ingest / coverage report / junction population | /var/log/echelon_evidence_ingest.log etc |

## Status Queries (DB2 unless noted)

```sql
-- pipeline heartbeat: LATEST state per pipeline/stage (old failures don't linger next to later successes)
SELECT DISTINCT ON (pipeline, stage) pipeline, stage, status, ts
FROM public.pipeline_events WHERE ts > now() - interval '24 hours'
ORDER BY pipeline, stage, ts DESC;
-- volume view (counts by status, same window)
SELECT pipeline, stage, status, count(*), max(ts)
FROM public.pipeline_events WHERE ts > now() - interval '24 hours'
GROUP BY 1,2,3 ORDER BY max(ts) DESC;

-- extraction state
SELECT extraction_status, count(*) FROM ops.extraction_status GROUP BY 1;

-- per-model provenance (tier prefixes local/ orfree/ cli/ after P2)
SELECT extraction_model, count(*), round(sum(cost_usd)::numeric,4) AS usd
FROM ops.extraction_status GROUP BY 1 ORDER BY 2 DESC;

-- transcript ROW coverage per topic (DB1, via: pct exec 203 -- su - postgres -c "psql -d youtube_videos ...")
-- counts rows, not quality — add "AND t.word_count >= 50" for usable-transcript coverage
SELECT dt.topic_name, count(DISTINCT vt2.video_id) AS videos,
       count(DISTINCT t.video_id) AS transcript_rows
FROM dim_topic dt JOIN video_topics vt2 ON vt2.topic_id = dt.id
LEFT JOIN video_transcripts t ON t.video_id = vt2.video_id
GROUP BY 1 ORDER BY 2 DESC;
```
Ops dashboard table: `public.mart_video_intelligence` (pipeline_state, extraction_status, extraction_model, per-entity counts).

## Re-Run Recipes

**Preflight (EVERY manual run):** (1) confirm target — `.env` points at DB2 `.130:5433`, no APP_ENV overlay; (2) check no cron instance is running (`pgrep -f <script>` + lock files in /tmp); (3) state batch scope explicitly (`--topics`/`--limit`) — never unbounded; (4) capture output to a log file; (5) after: verify via `pipeline_events` + the status queries above. Aaron confirms before any run that mutates >100 rows.

- **Extraction batch (manual)**: `cd /opt/echelon/Biohacking_Optimization && .venv/bin/python scripts/ExtractIntelligence.py --topics Biohacking --batch-per-topic 50` (respects skip-if-processed at `ExtractIntelligence.py:413`; post-P3 use `--force` + `extraction_run_id` for supersede re-runs).
- **Transcripts (Echelon canonical)**: `scripts/cron/run_transcripts_scheduled.sh` or `TranscriptCollector.py` directly; post-P1 `--refresh-timings` mode backfills chunks for `chunked_at IS NULL`.
- **Embeddings backlog**: `scripts/cron/embeddings_watchdog.sh` (idempotent; clears pending across video_transcripts/extracted_claims/comment_insights — chunks post-P1).
- **Consensus**: `scripts/cron/refresh_consensus.sh` — run after ANY bulk extraction change (double-count guard).
- **dbt**: `scripts/cron/run_dbt_build.sh` (full) — models + tests. Never raw `dbt build` without its PGOPTIONS/keepalive guards (dbt-hang incident 2026-05-19).
- **Temple export**: `.venv/bin/python scripts/publish_protocol_export.py` — reads `public.mart_protocol_export` WHERE published; diff output before shipping.
- **Failure triage order**: log tail → `pipeline_events` for the run → `transcript_failures` / `extraction_status='failed'` → only then code.

## 2.0 Additions (update this section with concrete commands as each phase SHIPS; spec: docs/superpowers/specs/2026-07-04-yt-knowledge-db-2.0-design.md)

- Tier-router debug (post-P2): probe `curl -m2 http://100.112.192.78:11434/api/tags`; `pipeline_events` `stage='tier_fallback'`.

## Escalation

Webhook alerts → Discord via `notify_webhook.sh`. Auth-expired CLI tier → `pipeline_events stage='cli_auth_expired'` → tell Aaron (he re-auths). Drift alarm → check `schema_expectations.sh` vs live DDL diff in log; if intentional change forgot the expectations update, fix expectations FIRST, then investigate.
