---
name: postgresql-performance-patterns
description: Advanced PostgreSQL performance tuning — EXPLAIN ANALYZE deep dives, BRIN/covering/expression indexes, JSONB path queries, pgbouncer pooling, declarative partitioning with pg_partman, pg_stat_statements analysis, and vacuum/autovacuum tuning. Complements sql-optimization-patterns and postgresql-table-design with production-grade operational patterns.
---

# PostgreSQL Performance Patterns

Production-grade performance tuning patterns for PostgreSQL 14+. This skill covers the operational and diagnostic patterns that go beyond schema design and basic query optimization — the patterns that separate a working database from one that performs under load.

## When to Apply

- Query takes >100ms and basic indexing has not resolved it
- EXPLAIN ANALYZE output shows unexpected scan types, poor row estimates, or high buffer reads
- Application experiences connection exhaustion or pool saturation
- Tables exceed 50M+ rows and need partitioning or maintenance tuning
- JSONB columns need performant path-based queries beyond simple containment
- Autovacuum is falling behind, causing bloat or transaction ID wraparound warnings
- pg_stat_statements shows high total_exec_time for specific query patterns
- Connection count approaches max_connections or pgbouncer limits

## Critical Rules

### EXPLAIN ANALYZE: Always Use BUFFERS and FORMAT

```sql
-- WRONG: Basic EXPLAIN tells you almost nothing actionable
EXPLAIN SELECT * FROM events WHERE user_id = 42;

-- RIGHT: Full diagnostic output with buffers, timing, and settings
EXPLAIN (ANALYZE, BUFFERS, TIMING, SETTINGS, FORMAT TEXT)
SELECT * FROM events WHERE user_id = 42;

-- RIGHT: JSON format for programmatic analysis and visualization tools
EXPLAIN (ANALYZE, BUFFERS, TIMING, FORMAT JSON)
SELECT * FROM events WHERE user_id = 42;

-- RIGHT: Include WAL stats for write-heavy queries (PG13+)
EXPLAIN (ANALYZE, BUFFERS, WAL, TIMING)
UPDATE events SET status = 'processed' WHERE created_at < now() - interval '90 days';
```

### Never Guess at Index Type — Measure

```sql
-- WRONG: Assuming B-tree is always correct
CREATE INDEX idx_events_created ON events (created_at);
-- On a 500M-row append-only table, this wastes gigabytes

-- RIGHT: Use BRIN for large, naturally ordered tables (1000x smaller)
CREATE INDEX idx_events_created_brin ON events USING BRIN (created_at)
  WITH (pages_per_range = 32);

-- WRONG: Full GIN index when you only query one JSONB path
CREATE INDEX idx_config ON services USING GIN (config);

-- RIGHT: Expression index on the specific path you actually query
CREATE INDEX idx_config_region ON services ((config->>'region'));
```

### Never Tune Vacuum Without Measuring First

```sql
-- WRONG: Blindly increasing autovacuum thresholds
ALTER TABLE events SET (autovacuum_vacuum_scale_factor = 0.5);

-- RIGHT: Check current dead tuple ratio, then decide
SELECT relname,
       n_live_tup,
       n_dead_tup,
       round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
       last_autovacuum,
       last_autoanalyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Key Patterns

### Advanced EXPLAIN ANALYZE Interpretation

Reading EXPLAIN output is a diagnostic skill. Focus on these signals.

**Buffer analysis — where is time actually spent?**

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders
WHERE customer_id = 1234 AND created_at > '2025-01-01';
```

Key buffer metrics to interpret:

| Metric | Meaning | Action |
|--------|---------|--------|
| `shared hit` | Page found in shared_buffers (RAM) | Good — fast read |
| `shared read` | Page read from OS cache or disk | High count = cold cache or working set > RAM |
| `shared dirtied` | Page modified in memory | Write-heavy — check checkpoint frequency |
| `shared written` | Page written to disk during query | Backend writes — increase shared_buffers or checkpoint frequency |
| `temp read/written` | Spill to disk for sorts/hashes | Increase work_mem for this query |

**Detecting bad row estimates (the #1 cause of bad plans):**

```sql
-- Look for large divergence between estimated and actual rows
-- estimated rows=1000, actual rows=500000 → stale statistics or correlation issues
EXPLAIN ANALYZE SELECT * FROM events
WHERE category = 'purchase' AND created_at > '2025-01-01';

-- Fix: update statistics with increased sampling
ALTER TABLE events ALTER COLUMN category SET STATISTICS 1000;
ANALYZE events;
```

**auto_explain for production query plan logging:**

```sql
-- In postgresql.conf or ALTER SYSTEM
ALTER SYSTEM SET shared_preload_libraries = 'auto_explain';
-- Requires restart for shared_preload_libraries

-- Configure at session or system level (no restart needed after loaded)
ALTER SYSTEM SET auto_explain.log_min_duration = '500ms';
ALTER SYSTEM SET auto_explain.log_analyze = on;
ALTER SYSTEM SET auto_explain.log_buffers = on;
ALTER SYSTEM SET auto_explain.log_timing = on;
ALTER SYSTEM SET auto_explain.log_nested_statements = on;
ALTER SYSTEM SET auto_explain.log_format = 'json';
SELECT pg_reload_conf();  -- Apply without restart

-- Per-session for debugging (no restart, no shared_preload needed)
LOAD 'auto_explain';
SET auto_explain.log_min_duration = '200ms';
SET auto_explain.log_analyze = on;
SET auto_explain.log_buffers = on;
```

### pg_stat_statements Deep Analysis

The most important extension for production performance work.

**Setup:**

```sql
-- postgresql.conf (requires restart for shared_preload_libraries)
-- shared_preload_libraries = 'pg_stat_statements'
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Recommended settings
ALTER SYSTEM SET pg_stat_statements.max = 10000;
ALTER SYSTEM SET pg_stat_statements.track = 'all';       -- includes nested statements
ALTER SYSTEM SET pg_stat_statements.track_utility = on;   -- DDL and utility commands
ALTER SYSTEM SET pg_stat_statements.track_planning = on;  -- planning time (PG13+)
SELECT pg_reload_conf();
```

**Top queries by total execution time (the workload profile):**

```sql
SELECT
    queryid,
    substr(query, 1, 80) AS query_preview,
    calls,
    round(total_exec_time::numeric, 2) AS total_ms,
    round(mean_exec_time::numeric, 2) AS mean_ms,
    round(stddev_exec_time::numeric, 2) AS stddev_ms,
    rows,
    round(100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 2) AS cache_hit_pct,
    shared_blks_dirtied,
    temp_blks_read + temp_blks_written AS temp_blks_total
FROM pg_stat_statements
WHERE calls > 10
ORDER BY total_exec_time DESC
LIMIT 20;
```

**Queries with poor cache hit rate (need more RAM or better indexes):**

```sql
SELECT
    queryid,
    substr(query, 1, 100) AS query_preview,
    calls,
    shared_blks_hit + shared_blks_read AS total_blks,
    round(100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 2) AS hit_pct
FROM pg_stat_statements
WHERE (shared_blks_hit + shared_blks_read) > 1000
  AND 100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) < 95
ORDER BY (shared_blks_hit + shared_blks_read) DESC
LIMIT 10;
```

**Queries with high planning time relative to execution (PG13+):**

```sql
SELECT
    queryid,
    substr(query, 1, 80) AS query_preview,
    calls,
    round(mean_plan_time::numeric, 2) AS mean_plan_ms,
    round(mean_exec_time::numeric, 2) AS mean_exec_ms,
    round(100.0 * mean_plan_time / nullif(mean_plan_time + mean_exec_time, 0), 2) AS plan_pct
FROM pg_stat_statements
WHERE calls > 100
  AND mean_plan_time > mean_exec_time
ORDER BY mean_plan_time DESC
LIMIT 10;
-- High plan_pct → consider prepared statements or plan_cache_mode = force_generic_plan
```

**Queries spilling to disk (need work_mem increase):**

```sql
SELECT
    queryid,
    substr(query, 1, 80) AS query_preview,
    calls,
    temp_blks_read,
    temp_blks_written,
    round(mean_exec_time::numeric, 2) AS mean_ms
FROM pg_stat_statements
WHERE temp_blks_written > 0
ORDER BY temp_blks_written DESC
LIMIT 10;
-- Fix: SET work_mem = '256MB' for specific sessions/queries, not globally
```

**Reset after analysis window:**

```sql
-- Reset all stats (do this after capturing baseline)
SELECT pg_stat_statements_reset();

-- Reset a single query (PG14+)
SELECT pg_stat_statements_reset(0, 0, <queryid>);
```

## JSONB Operators & Indexing

Beyond basic containment — the full JSONB performance toolkit.

### Operator Reference

```sql
-- Containment: does the JSONB contain this sub-document?
SELECT * FROM products WHERE attrs @> '{"color": "red"}';
-- Uses GIN index

-- Key existence: does the key exist at top level?
SELECT * FROM products WHERE attrs ? 'color';
-- Uses default GIN index (NOT jsonb_path_ops)

-- Any key existence: does ANY of these keys exist?
SELECT * FROM products WHERE attrs ?| array['color', 'size'];

-- All key existence: do ALL of these keys exist?
SELECT * FROM products WHERE attrs ?& array['color', 'size'];

-- Path extraction with type cast
SELECT * FROM products WHERE (attrs->>'price')::numeric > 100;
-- Needs expression index (GIN won't help here)

-- Nested path extraction
SELECT * FROM products WHERE attrs #>> '{dimensions,weight}' IS NOT NULL;
```

### JSONB Indexing Strategies

```sql
-- Strategy 1: Default GIN — supports @>, ?, ?|, ?& operators
CREATE INDEX idx_products_attrs ON products USING GIN (attrs);
-- Good for: flexible queries on any key, existence checks
-- Size: moderate

-- Strategy 2: jsonb_path_ops GIN — containment only, 2-3x smaller
CREATE INDEX idx_products_attrs_path ON products USING GIN (attrs jsonb_path_ops);
-- Good for: @> containment queries only
-- Cannot use: ?, ?|, ?& operators
-- Size: significantly smaller than default GIN

-- Strategy 3: Expression B-tree — for equality/range on specific paths
CREATE INDEX idx_products_price ON products ((attrs->>'price')::numeric);
-- Good for: WHERE (attrs->>'price')::numeric BETWEEN 10 AND 50
-- Only works for queries on this exact extracted path

-- Strategy 4: Expression B-tree for text fields
CREATE INDEX idx_products_brand ON products ((attrs->>'brand'));
-- Good for: WHERE attrs->>'brand' = 'Acme'

-- Strategy 5: Partial GIN — index only documents matching a condition
CREATE INDEX idx_active_product_attrs ON products USING GIN (attrs)
  WHERE status = 'active';
-- Smaller index, only useful when query includes WHERE status = 'active'
```

### SQL/JSON Path Queries (PG12+)

```sql
-- jsonb_path_query: extract values using SQL/JSON path language
SELECT jsonb_path_query(attrs, '$.dimensions.weight') FROM products;

-- jsonb_path_exists: check if path matches (returns boolean)
SELECT * FROM products
WHERE jsonb_path_exists(attrs, '$.tags[*] ? (@ == "organic")');

-- jsonb_path_match: evaluate predicate at path
SELECT * FROM products
WHERE jsonb_path_match(attrs, '$.price > 100');

-- Path queries with variables
SELECT * FROM products
WHERE jsonb_path_exists(attrs, '$.tags[*] ? (@ == $tag)', '{"tag": "organic"}');

-- Note: jsonb_path_* functions do NOT use GIN indexes.
-- For performance, prefer @> containment when possible:
-- SLOW (no index): WHERE jsonb_path_match(attrs, '$.price > 100')
-- FAST (GIN index): WHERE attrs @> '{"category": "electronics"}'
-- FAST (B-tree):    WHERE (attrs->>'price')::numeric > 100  -- with expression index
```

## Connection Pooling

PostgreSQL forks a process per connection (~5-10MB each). At scale, connection pooling is non-negotiable.

### pgbouncer Configuration

```ini
;; pgbouncer.ini

[databases]
myapp = host=127.0.0.1 port=5432 dbname=myapp

[pgbouncer]
;; Pool mode: transaction (recommended), session, or statement
pool_mode = transaction

;; Pool sizing
;; Formula: default_pool_size = (max_connections - superuser_reserved) / num_databases
;; For max_connections=100, 1 database: default_pool_size = 95
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3

;; Connection limits
max_client_conn = 1000         ;; max application connections to pgbouncer
max_db_connections = 50        ;; max connections per database to PostgreSQL

;; Timeouts
server_idle_timeout = 300      ;; close idle server connections after 5 min
client_idle_timeout = 0        ;; 0 = disabled (app manages idle clients)
query_timeout = 30             ;; kill queries running longer than 30s
client_login_timeout = 15

;; Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1
stats_period = 60

;; Auth
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
```

### Pool Mode Trade-offs

| Mode | Connection Reuse | SET/Prepared Stmts | Use Case |
|------|-----------------|-------------------|----------|
| **transaction** | Between transactions | NOT preserved | Web apps, APIs (recommended) |
| **session** | When client disconnects | Preserved | Legacy apps needing session state |
| **statement** | Between statements | NOT preserved | Simple read-only loads, pgbouncer <1.21 |

### Transaction Mode Gotchas

```sql
-- WRONG: Prepared statements break in transaction mode
PREPARE get_user (bigint) AS SELECT * FROM users WHERE id = $1;
EXECUTE get_user(42);
-- Fails: next query may go to different backend connection

-- RIGHT: Use protocol-level prepared statements with parameter
-- In application code, use parameterized queries without explicit PREPARE
-- Most ORMs/drivers handle this automatically

-- WRONG: SET commands don't persist across transactions
SET search_path TO myschema;
-- Next transaction may use a different backend with default search_path

-- RIGHT: Set per-database defaults in PostgreSQL
ALTER DATABASE myapp SET search_path TO myschema, public;

-- WRONG: Advisory locks leak in transaction mode
SELECT pg_advisory_lock(12345);
-- Lock may be held by a different client on the next transaction

-- RIGHT: Use transaction-scoped advisory locks
SELECT pg_advisory_xact_lock(12345);
-- Automatically released at transaction end
```

### Pool Sizing Formula

```
# Optimal PostgreSQL max connections (backend)
# Rule of thumb: 2-4x CPU cores for OLTP workloads
optimal_connections = (cpu_cores * 2) + effective_spindle_count
# Example: 8 cores, SSD → (8 * 2) + 1 = 17 connections

# pgbouncer pool size per database
# Leave headroom for superuser_reserved_connections (default 3)
pool_size = (max_connections - superuser_reserved_connections) / num_pooled_databases

# max_client_conn should be >> pool_size
# This is the whole point: 1000 app connections → 20 PG connections
max_client_conn = expected_peak_app_connections * 1.2
```

## Partitioning Strategies

### Declarative Partitioning (PG10+)

**Range partitioning — the most common pattern (time-series data):**

```sql
-- Parent table (no data stored here)
CREATE TABLE events (
    event_id    bigint GENERATED ALWAYS AS IDENTITY,
    user_id     bigint NOT NULL,
    event_type  text NOT NULL,
    payload     jsonb,
    created_at  timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE events_2025_01 PARTITION OF events
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE events_2025_02 PARTITION OF events
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
-- Repeat for each month

-- Default partition catches rows that don't match any partition
CREATE TABLE events_default PARTITION OF events DEFAULT;

-- Indexes are created per-partition (define on parent, auto-propagated)
CREATE INDEX ON events (created_at);
CREATE INDEX ON events (user_id, created_at);
```

**List partitioning — discrete values:**

```sql
CREATE TABLE orders (
    order_id    bigint GENERATED ALWAYS AS IDENTITY,
    region      text NOT NULL,
    total       numeric(12,2) NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
) PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('us-east', 'us-west');
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('eu-west', 'eu-central');
CREATE TABLE orders_ap PARTITION OF orders FOR VALUES IN ('ap-south', 'ap-east');
CREATE TABLE orders_default PARTITION OF orders DEFAULT;
```

**Hash partitioning — even distribution when no natural range:**

```sql
CREATE TABLE sessions (
    session_id  uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id     bigint NOT NULL,
    data        jsonb,
    created_at  timestamptz NOT NULL DEFAULT now()
) PARTITION BY HASH (session_id);

-- Create N partitions (power of 2 recommended)
CREATE TABLE sessions_p0 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE sessions_p1 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE sessions_p2 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE sessions_p3 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

### Partition Pruning

```sql
-- Verify pruning is enabled
SHOW enable_partition_pruning;  -- Must be 'on' (default)

-- Verify pruning works with EXPLAIN
EXPLAIN SELECT * FROM events
WHERE created_at BETWEEN '2025-03-01' AND '2025-03-31';
-- Should show: "Partitions selected: 1" (only events_2025_03 scanned)

-- Runtime pruning with parameterized queries (PG11+)
PREPARE recent_events(timestamptz) AS
  SELECT * FROM events WHERE created_at > $1;
EXPLAIN ANALYZE EXECUTE recent_events('2025-03-15');
-- Prunes at execution time based on parameter value
```

### Partition Maintenance with pg_partman

```sql
-- Install pg_partman
CREATE SCHEMA partman;
CREATE EXTENSION pg_partman SCHEMA partman;

-- Configure automatic partition creation
SELECT partman.create_parent(
    p_parent_table := 'public.events',
    p_control := 'created_at',
    p_type := 'range',
    p_interval := '1 month',
    p_premake := 3           -- create 3 future partitions
);

-- Configure retention (drop partitions older than 12 months)
UPDATE partman.part_config
SET retention = '12 months',
    retention_keep_table = false  -- actually DROP old partitions
WHERE parent_table = 'public.events';

-- Run maintenance (call via pg_cron or crontab)
-- Creates new partitions and drops expired ones
SELECT partman.run_maintenance();

-- Detach a partition without dropping (for archival)
ALTER TABLE events DETACH PARTITION events_2024_01;
-- Now events_2024_01 is a standalone table you can archive/export

-- Attach an existing table as a partition
ALTER TABLE events ATTACH PARTITION events_2025_04
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');
-- PostgreSQL validates all rows match the constraint (can be slow on large tables)
-- Use CONCURRENTLY (PG14+) to avoid blocking:
ALTER TABLE events ATTACH PARTITION events_2025_04
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');
-- Add constraint first to speed up ATTACH:
ALTER TABLE events_2025_04 ADD CONSTRAINT chk_created_at
    CHECK (created_at >= '2025-04-01' AND created_at < '2025-05-01');
-- Then ATTACH skips validation because constraint already proves compatibility
```

## Advanced Indexing Patterns

### BRIN Indexes (Block Range INdex)

BRIN indexes store min/max values per range of physical blocks. Ideal for large, append-only, naturally ordered tables.

```sql
-- Time-series data: BRIN is 100-1000x smaller than B-tree
CREATE INDEX idx_events_created_brin ON events
  USING BRIN (created_at)
  WITH (pages_per_range = 32);  -- default 128; lower = more precise but larger

-- Check correlation (BRIN requires high correlation to be effective)
SELECT correlation FROM pg_stats
WHERE tablename = 'events' AND attname = 'created_at';
-- correlation > 0.9 → BRIN is excellent
-- correlation < 0.5 → BRIN is useless, use B-tree

-- Multi-column BRIN for correlated columns
CREATE INDEX idx_sensor_brin ON sensor_readings
  USING BRIN (recorded_at, sensor_id)
  WITH (pages_per_range = 64);

-- After bulk loads, summarize new pages
SELECT brin_summarize_new_values('idx_events_created_brin');
```

### Covering Indexes (INCLUDE clause)

Enable index-only scans by including non-key columns in the index.

```sql
-- Query pattern: look up user by email, return name and created_at
-- Without covering index: Index Scan + heap fetch (2 lookups)
-- With covering index: Index Only Scan (1 lookup)

CREATE INDEX idx_users_email_cover ON users (email)
  INCLUDE (name, created_at);

-- Now this query uses Index Only Scan (no table access):
SELECT name, created_at FROM users WHERE email = 'user@example.com';

-- Covering index on composite key
CREATE INDEX idx_orders_user_status_cover ON orders (user_id, status)
  INCLUDE (total, created_at);

-- Index Only Scan for:
SELECT total, created_at FROM orders
WHERE user_id = 42 AND status = 'completed';

-- IMPORTANT: INCLUDE columns are NOT part of the sort key
-- They do NOT help with WHERE clauses or ORDER BY
-- They ONLY avoid the heap fetch
```

### Partial + Expression Index Combos

```sql
-- Partial index: only index rows matching a condition
-- Dramatically smaller for skewed distributions
CREATE INDEX idx_orders_pending ON orders (created_at)
  WHERE status = 'pending';
-- 1M total orders, 5K pending → index is 200x smaller than full index

-- Expression + partial combo: case-insensitive search on active users only
CREATE INDEX idx_active_users_email ON users (lower(email))
  WHERE is_active = true;
-- Query MUST include both: WHERE lower(email) = '...' AND is_active = true

-- Partial unique index: enforce uniqueness on a subset
CREATE UNIQUE INDEX idx_one_active_email ON users (email)
  WHERE deleted_at IS NULL;
-- Allows duplicate emails for soft-deleted rows
```

### Index Maintenance

```sql
-- REINDEX CONCURRENTLY (PG12+): rebuild without blocking reads/writes
REINDEX INDEX CONCURRENTLY idx_users_email;
REINDEX TABLE CONCURRENTLY users;

-- Detect index bloat
SELECT
    schemaname || '.' || indexrelname AS index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    idx_scan AS times_used,
    idx_tup_read AS tuples_read
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 20;

-- Find duplicate indexes (same columns, same table)
SELECT
    indrelid::regclass AS table_name,
    array_agg(indexrelid::regclass) AS index_names,
    count(*) AS num_duplicates
FROM pg_index
GROUP BY indrelid, indkey
HAVING count(*) > 1;

-- Find unused indexes (candidates for removal)
SELECT
    schemaname || '.' || indexrelname AS index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%pkey%'    -- keep primary keys
  AND indexrelname NOT LIKE '%unique%'  -- keep unique constraints
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Vacuum and Autovacuum Tuning

### How Autovacuum Decides to Run

```
vacuum threshold = autovacuum_vacuum_threshold + (autovacuum_vacuum_scale_factor * row_count)
analyze threshold = autovacuum_analyze_threshold + (autovacuum_analyze_scale_factor * row_count)

-- Defaults: threshold=50, scale_factor=0.2
-- 1M row table: vacuum triggers at 50 + (0.2 * 1,000,000) = 200,050 dead tuples
-- That means 20% of the table is dead before vacuum runs!
```

### Per-Table Tuning for Large Tables

```sql
-- Large tables need aggressive autovacuum (lower scale_factor)
ALTER TABLE events SET (
    autovacuum_vacuum_scale_factor = 0.01,     -- 1% instead of 20%
    autovacuum_vacuum_threshold = 1000,
    autovacuum_analyze_scale_factor = 0.005,   -- 0.5% for fresh statistics
    autovacuum_analyze_threshold = 500,
    autovacuum_vacuum_cost_delay = 2           -- faster vacuum (default 2ms PG12+)
);

-- Update-heavy tables: more frequent vacuum, allow more resources
ALTER TABLE user_sessions SET (
    autovacuum_vacuum_scale_factor = 0.02,
    autovacuum_vacuum_cost_limit = 1000,      -- more work per cycle (default 200)
    fillfactor = 90                            -- leave room for HOT updates
);

-- Insert-only tables (PG13+): autovacuum for visibility map updates
-- Needed for index-only scans to work efficiently
ALTER TABLE audit_log SET (
    autovacuum_vacuum_insert_scale_factor = 0.05,
    autovacuum_vacuum_insert_threshold = 10000
);
```

### Monitoring Vacuum Health

```sql
-- Check for tables approaching transaction ID wraparound
-- CRITICAL: wraparound causes forced full-table vacuum (blocks all writes)
SELECT
    c.oid::regclass AS table_name,
    age(c.relfrozenxid) AS xid_age,
    pg_size_pretty(pg_total_relation_size(c.oid)) AS total_size,
    CASE
        WHEN age(c.relfrozenxid) > 1200000000 THEN 'CRITICAL'
        WHEN age(c.relfrozenxid) > 800000000 THEN 'WARNING'
        ELSE 'OK'
    END AS status
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY age(c.relfrozenxid) DESC
LIMIT 20;

-- Check autovacuum worker activity
SELECT
    schemaname || '.' || relname AS table_name,
    n_dead_tup,
    n_live_tup,
    round(100.0 * n_dead_tup / nullif(n_live_tup, 0), 2) AS dead_pct,
    last_autovacuum,
    last_autoanalyze,
    autovacuum_count,
    autoanalyze_count
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;

-- Check currently running vacuums
SELECT pid, query, state, wait_event_type, wait_event,
       now() - query_start AS duration
FROM pg_stat_activity
WHERE query LIKE 'autovacuum:%'
ORDER BY query_start;
```

### Global Autovacuum Tuning

```sql
-- Increase autovacuum parallelism for busy databases
ALTER SYSTEM SET autovacuum_max_workers = 6;           -- default 3
ALTER SYSTEM SET autovacuum_naptime = '15s';            -- default 1min, check more often
ALTER SYSTEM SET maintenance_work_mem = '1GB';          -- more memory for vacuum
ALTER SYSTEM SET autovacuum_work_mem = '512MB';         -- per-worker memory (PG15+, overrides maintenance_work_mem)
SELECT pg_reload_conf();
-- Note: autovacuum_max_workers requires restart
```

## Common Mistakes

### 1. Not Using CONCURRENTLY for Production Index Operations

```sql
-- WRONG: Blocks all writes on the table for minutes/hours
CREATE INDEX idx_events_type ON events (event_type);
DROP INDEX idx_events_type;

-- RIGHT: Non-blocking index creation and removal
CREATE INDEX CONCURRENTLY idx_events_type ON events (event_type);
DROP INDEX CONCURRENTLY idx_events_type;

-- REINDEX also supports CONCURRENTLY (PG12+)
REINDEX INDEX CONCURRENTLY idx_events_type;
```

### 2. Setting work_mem Globally Too High

```sql
-- WRONG: Every sort/hash in every connection uses 1GB
ALTER SYSTEM SET work_mem = '1GB';
-- With 100 connections, 5 sort nodes each → 500GB potential memory usage

-- RIGHT: Set per-session or per-transaction for heavy queries
-- Global: keep low (default 4MB, increase to 16-64MB max)
ALTER SYSTEM SET work_mem = '32MB';

-- Per-session for analytical queries
SET work_mem = '512MB';
SELECT ... complex aggregation ...;
RESET work_mem;

-- Even better: per-transaction
BEGIN;
SET LOCAL work_mem = '256MB';
SELECT ... complex query ...;
COMMIT;  -- work_mem resets automatically
```

### 3. Ignoring Partial Index Opportunities

```sql
-- WRONG: Full index when 99% of queries filter on status = 'active'
CREATE INDEX idx_users_email ON users (email);
-- Indexes all 10M rows including 9.5M inactive

-- RIGHT: Partial index covers only the rows you actually query
CREATE INDEX idx_active_users_email ON users (email)
  WHERE status = 'active';
-- Indexes only 500K active rows — 20x smaller, 20x faster to maintain
```

### 4. Partitioning Without Including Partition Key in PK/Unique

```sql
-- WRONG: Unique constraint without partition key
CREATE TABLE events (
    event_id bigint GENERATED ALWAYS AS IDENTITY,
    created_at timestamptz NOT NULL
) PARTITION BY RANGE (created_at);
-- ERROR: unique constraint must include all partition key columns

-- RIGHT: Include partition key in primary key
CREATE TABLE events (
    event_id bigint GENERATED ALWAYS AS IDENTITY,
    created_at timestamptz NOT NULL,
    PRIMARY KEY (event_id, created_at)
) PARTITION BY RANGE (created_at);
```

### 5. Not Monitoring Table and Index Bloat

```sql
-- Check table bloat estimate (requires pgstattuple extension)
CREATE EXTENSION IF NOT EXISTS pgstattuple;
SELECT * FROM pgstattuple('users');
-- dead_tuple_percent > 20% → manual VACUUM needed
-- free_space > 50% of table_len → consider VACUUM FULL (locks table)

-- Lightweight bloat estimate without pgstattuple
SELECT
    schemaname || '.' || tablename AS table_name,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) AS table_size,
    n_dead_tup,
    n_live_tup,
    round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) AS bloat_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;
```

### 6. Using OFFSET for Deep Pagination on Large Tables

```sql
-- WRONG: Scans and discards 1M rows
SELECT * FROM events ORDER BY created_at DESC LIMIT 20 OFFSET 1000000;

-- RIGHT: Keyset/cursor pagination using the last seen value
SELECT * FROM events
WHERE created_at < '2025-01-15T10:30:00Z'  -- last value from previous page
ORDER BY created_at DESC
LIMIT 20;

-- RIGHT: For composite sort keys
SELECT * FROM events
WHERE (created_at, event_id) < ('2025-01-15T10:30:00Z', 987654)
ORDER BY created_at DESC, event_id DESC
LIMIT 20;
-- Requires index: CREATE INDEX ON events (created_at DESC, event_id DESC);
```
