# Workflow selection and evidence

| Trigger | Evidence to request/use | Review |
|---|---|---|
| SQL correctness or query cost | SQL, schema/cardinality, metric contract, partition metadata | Check grain/results first, then projection, predicates and bytes estimate |
| One slow/failed job | Job ID/location, stage plan, errors, timing and cache state | Find the first evidenced bottleneck; distinguish execution from queueing |
| Usage or capacity trend | Time window, billing model, scoped jobs/slots/storage telemetry | Separate on-demand bytes, capacity consumption and storage; show missing coverage |

## Query checks

- Declare GoogleSQL. Distinguish TIMESTAMP, DATETIME and DATE semantics.
- Confirm one row per expected entity. COUNT after joining order lines counts
  lines unless the query deliberately deduplicates or preaggregates.
- Prefer EXISTS for eligibility-only joins where its semantics match.
- Keep a cohort's original denominator independent of retained activity.
- Bind parameters; do not concatenate untrusted values into query text.
- Use only needed columns. Review repeated scans, large shuffles, skew, and
  materialization candidates using evidence; do not promise a universal fix.
- Construct local-calendar bounds before converting to TIMESTAMP. A wrapped
  partition column may still prune for supported expressions; verify.
- Compare original and proposed results on duplicates, nulls, boundary times,
  zero/partial periods, and applicable access/filter contexts.

## Connected evidence, only when already permitted

For a specific job, scoped job metadata is often a smaller first read than a
warehouse-wide query. Region-qualified INFORMATION_SCHEMA job views require
matching execution location; dataset views have different qualification.
Metadata/query permissions must be established for the actual operation.
Even SELECT and telemetry queries can consume resources.

For an approved dry run, report bytes estimate, project/location and parameters
with the query revision. For executed queries also report cache state, bytes,
elapsed time and result reconciliation. Monetary comparisons require the
applicable billing model, rates and workload context. No billing model means
no substantiated dollar-savings claim.

## Sources

This owner-authored advisory adaptation uses the upstream operations suite as
reference material. It retains no upstream installer or privileged setup branch.
Pinned sources and upstream license are recorded in sources.md.
