---
name: database-design
description: |
  Expert PostgreSQL schema designer and query architect. Designs normalized schemas that
  survive requirements changes, writes queries that perform at scale, and identifies the
  data integrity issues that corrupt production systems silently. Specializes in: normalization
  decisions, index strategy, constraint design, JSONB usage, provenance and temporal versioning
  patterns, and query optimization using EXPLAIN ANALYZE. Use when designing a new schema,
  reviewing an existing one, writing complex queries, diagnosing slow queries, or deciding
  between normalization options. Trigger phrases: "design a schema for", "database design",
  "how should I model this", "slow query", "index this", "EXPLAIN ANALYZE", "normalize this",
  "is this schema right", "foreign key design", "JSONB vs column", "temporal data".
  Also activates when user says "how do I store X in the database" or "query is too slow".
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: testing-strategy, biohacking-data-pipeline, cloud-migration-playbook
  last-reviewed: "2026-03-15"
  review-trigger: "PostgreSQL major version release, new JSONB operator availability"
  capability-assumptions:
    - "Python 3.12+, FastAPI, SQLAlchemy 2.0, PostgreSQL"
    - "Bash tool for running commands"
  fallback-patterns:
    - "If no code execution: provide code as text for user to run"
  degradation-mode: "graceful"
---

## Purpose and Scope

This skill designs PostgreSQL schemas and writes queries that are correct, performant, and
maintainable. Focus is on production PostgreSQL — not ORMs, not generic SQL, not other databases.

It does NOT cover: ORM configuration (SQLAlchemy patterns are in the broader stack), data
migration execution, or database infrastructure (Cloud SQL setup is in `cloud-migration-playbook`).
For testing database code, use `testing-strategy`. For biohacking-specific schema patterns
(provenance, temporal versioning), this skill provides the foundations and `biohacking-data-pipeline`
provides the domain-specific application.

---

## Section 1 — Core Knowledge

### The Three Laws of Schema Design

**Law 1: Normalize to 3NF by default, denormalize by evidence.**
Start with a fully normalized schema. Denormalize only when you have `EXPLAIN ANALYZE` output
showing that the join cost is causing a real problem. Premature denormalization is the most
common source of data inconsistency in production databases.

**Law 2: Constraints are documentation that the database enforces.**
Every constraint you put in the schema is a rule the database guarantees. Every constraint
you omit is a rule you're trusting the application to enforce — and applications fail.
`NOT NULL`, `UNIQUE`, `CHECK`, and `FOREIGN KEY` constraints are not optional polish.
They are the difference between a database and a CSV file.

**Law 3: Design for the query pattern, not the entity model.**
The most normalized schema in the world is useless if the queries against it cause full table
scans. For each table, ask: what are the three most common queries? Design indexes for those
queries. If the query pattern and the normalization conflict, the index can usually resolve it.

### The Normalization Decision Tree

```
Has repeated groups of columns? → Move to a child table (1NF)
Has non-key columns depending on part of a composite key? → Separate table (2NF)
Has non-key column A determining non-key column B? → Separate table for A→B (3NF)
Have two tables that reference the same lookup value? → Shared reference table
```

Stop at 3NF unless performance requires otherwise. BCNF and 4NF are rarely necessary
and add join complexity without proportional benefit in OLTP systems.

---

## Section 2 — Advanced Patterns

### Pattern 1: Covering Indexes for Foreign Keys
Every foreign key column should have an index unless the table is tiny.
PostgreSQL does not automatically index foreign keys (unlike some databases).
A missing FK index causes a sequential scan of the child table on every cascade or join.
The symptom: DELETE on a parent table takes 30+ seconds because PostgreSQL is scanning
the entire child table for references.

```sql
-- Always add this when you add a foreign key:
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Pattern 2: Partial Indexes for Filtered Queries
A partial index covers only rows matching a WHERE clause. It is smaller, faster, and
more selective than a full index. Use whenever a query filters on a column with a highly
skewed distribution.

```sql
-- Only index active records (90% of queries) instead of all records
CREATE INDEX idx_users_email_active ON users(email) WHERE is_active = true;

-- Only index unprocessed jobs instead of the entire job history
CREATE INDEX idx_jobs_pending ON jobs(created_at) WHERE status = 'pending';
```

### Pattern 3: JSONB for Semi-Structured Extension Data
JSONB (not JSON) is correct for semi-structured data. The difference: JSONB is stored in
a decomposed binary format that supports GIN indexes and operators. JSON is stored as text
and must be parsed on every read.

Use JSONB when: the structure varies per row, the fields aren't known at schema design time,
or you're storing user-defined attributes. Use it in addition to columns, not instead of them:
the primary identifier, foreign keys, and frequently queried fields should always be columns.

```sql
-- GIN index on the entire JSONB column (supports containment queries @>)
CREATE INDEX idx_supplements_metadata ON supplements USING GIN (metadata);

-- Functional index on a specific JSONB field (supports equality queries)
CREATE INDEX idx_supplements_source ON supplements((metadata->>'source'));
```

### Pattern 4: Provenance Columns as First-Class Citizens
Every table that stores data from an external source should carry its origin.
Without provenance, you cannot answer: "where did this value come from?", "when was it
ingested?", or "which version of the source data does this reflect?"

```sql
-- Minimum provenance for any external data:
source_id          TEXT NOT NULL,  -- identifier in the source system
source_name        TEXT NOT NULL,  -- which source (e.g., 'pubchem', 'examine')
ingested_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
source_version     TEXT,           -- API version or dataset version
```

---

## Section 3 — Standard Workflow

1. **Define the entities and their relationships.** List nouns (things you're storing) and
   the verbs between them (how they relate). Draw the ER diagram before writing DDL.

2. **Identify cardinality.** For every relationship: 1:1, 1:N, or M:N?
   M:N always requires a junction table. Never use comma-separated IDs in a column.

3. **Apply normalization.** Work through the decision tree. Write the normalized DDL.

4. **Add constraints.** For every column: NOT NULL unless null is meaningful. For every
   relationship: FOREIGN KEY. For every business rule that can be expressed as a CHECK or
   UNIQUE constraint: add it.

5. **Design indexes for the 3 most common queries.** Write the queries in plain English first,
   then design indexes for them. Test with EXPLAIN (ANALYZE, BUFFERS) before and after.

6. **Document the schema.** Add COMMENT ON TABLE and COMMENT ON COLUMN for anything non-obvious.
   Schema documentation in the DDL is the only documentation that stays in sync with the code.

---

## Section 4 — Edge Cases

**Edge Case 1: Temporal / historical data**
Data that changes over time and you need both the current value and the history.
Mitigation: Add `valid_from TIMESTAMPTZ NOT NULL` and `valid_until TIMESTAMPTZ` columns.
A NULL `valid_until` means "currently valid." Use a partial unique index on the natural key
where `valid_until IS NULL` to enforce "only one current record."

```sql
CREATE UNIQUE INDEX idx_biomarker_current
  ON biomarker_values(user_id, biomarker_id)
  WHERE valid_until IS NULL;
```

**Edge Case 2: Multi-tenant schemas**
Every table needs `tenant_id`. Either add it explicitly to every table, or use PostgreSQL
row-level security (RLS) policies. RLS is the safer approach — it cannot be bypassed by
a missed WHERE clause in application code.

**Edge Case 3: Soft deletes conflicting with unique constraints**
A UNIQUE constraint on `email` prevents a deleted user's email from being reused.
Mitigation: Use a partial unique index excluding soft-deleted rows.
```sql
CREATE UNIQUE INDEX idx_users_email_active ON users(email) WHERE deleted_at IS NULL;
```

**Edge Case 4: Very wide JSONB documents causing bloat**
Large JSONB values (>8KB) cause TOAST decompression overhead on every read of any column
in that row. Mitigation: Split large semi-structured blobs into a separate table with a 1:1
relationship to the parent, so they're only fetched when needed.

---

## Section 5 — Anti-Patterns

**Anti-Pattern 1: The EAV (Entity-Attribute-Value) Table**
A table with `(entity_id, attribute_name, attribute_value TEXT)` used to store arbitrary
attributes. Looks flexible. Is actually a performance disaster and a constraint nightmare.
You cannot enforce types, foreign keys, or NOT NULL on values stored as text. Every query
requires a pivot. Every index is useless for attribute-specific queries.
Fix: JSONB with GIN indexes for genuinely variable attributes. Typed columns for anything
queried frequently.

**Anti-Pattern 2: Missing Indexes on Foreign Keys**
Creating a foreign key constraint without a corresponding index on the child table column.
PostgreSQL creates an index on the PRIMARY KEY automatically. It does not create an index
on the FOREIGN KEY column. The result: every DELETE or UPDATE on the parent table causes
a full sequential scan of the child table.
Fix: After every `REFERENCES parent_table(id)`, immediately write:
`CREATE INDEX idx_child_parent_id ON child_table(parent_id);`

**Anti-Pattern 3: Storing Lists in a Column**
Using a comma-separated text column, a TEXT[] array column, or a JSONB array to store a
list of values that need to be queried, filtered, or joined on. The moment you need to find
"all records containing value X", you have an unindexable full-table scan.
Fix: Normalize to a junction table. Arrays are appropriate only for data that is always
consumed together and never filtered on individually.

**Anti-Pattern 4: Using TEXT for Everything**
Storing dates as TEXT, storing numbers as TEXT, storing booleans as TEXT "true"/"false".
The database cannot enforce format, perform range queries, or use numeric/date-specific
index types. You end up with invalid dates, locale-dependent number formatting, and
unexplainable sort orders.
Fix: Use the most specific type available. `TIMESTAMPTZ` for timestamps (always with TZ).
`NUMERIC` for money (never FLOAT). `UUID` for identifiers.

---

## Section 6 — Quality Gates

- [ ] Every foreign key has a corresponding index on the child table column
- [ ] No nullable columns exist without explicit documentation of why NULL is meaningful
- [ ] Every external-data table has source_id, source_name, ingested_at provenance columns
- [ ] No comma-separated values or arrays used for data that needs to be filtered or joined
- [ ] TEXT type is not used for dates, numbers, booleans, or enumerated values
- [ ] EXPLAIN ANALYZE confirms no sequential scans on tables >1000 rows for primary queries
- [ ] All business-rule constraints that can be expressed as CHECK or UNIQUE are in the schema

---

## Section 7 — Failure Modes and Fallbacks

**Failure: Schema migration causes table lock in production**
Detection: `ALTER TABLE` runs for >1 second on a table with active writes.
Fallback: Use `ALTER TABLE ... ADD COLUMN ... DEFAULT NULL` (lock-free in PG 11+). Add the
NOT NULL constraint in a separate step after backfilling. Use `CREATE INDEX CONCURRENTLY`
instead of `CREATE INDEX` for index additions.

**Failure: Query is slow after adding data volume**
Detection: Query takes <100ms in dev (1k rows) but >5s in staging (1M rows).
Fallback: Run `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` in staging. Look for:
Seq Scan on large tables → needs index. Nested loop on large rowsets → needs hash join (may
need to set `enable_nestloop = off` to force planner decision for diagnosis).

---

## Section 8 — Composability

**Hands off to:**
- `testing-strategy` — for testing constraints, migrations, and query correctness
- `cloud-migration-playbook` — when schema is finalized and needs Cloud SQL deployment
- `biohacking-data-pipeline` — for domain-specific schema patterns (temporal, provenance)

**Receives from:**
- `biohacking-data-pipeline` — when designing the health data schema
- `code-review` — when a review identifies a schema or query design issue

---

## Section 9 — Improvement Candidates

- `references/migration-patterns.md` covering Alembic migration patterns, lock-free changes,
  and rollback strategies for common DDL operations
- `references/query-optimization.md` with EXPLAIN ANALYZE interpretation guide and common
  planner hints
- A JSONB decision rubric: when to use JSONB, when to use typed columns, when to use both
