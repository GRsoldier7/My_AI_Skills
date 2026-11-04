# Contract fields and acceptance

Record each field's evidence or mark it unresolved.

| Field | Required content |
|---|---|
| Identity | Metric ID, version, business question, accountable owner |
| Formula | Numerator, denominator, unit, rounding and aggregation behavior |
| Population | Inclusion, exclusion, deduplication key and acquisition rules |
| Grain | Evaluation grain, permitted dimensions, join cardinality |
| Time | Date role, business timezone, period boundaries and comparison logic |
| Coverage | Watermark, complete/provisional periods and late-arrival handling |
| Edge cases | Nulls, blanks, zero denominator, negative values, missing activity |
| Source | Authoritative source, lineage, freshness and unresolved conflicts |
| Access | Applicable row/filter security; approved context and destination |
| Acceptance | Input rows, expected results, reconciliation query/tolerance |
| State | Draft/ready/blocked, unresolved decisions, next check and evidence |

## Example: cohort retention

Proposed business meaning: customers in a fixed acquisition cohort with at
least one approved qualifying activity in a later business-calendar month.
Activity qualification and acquisition rules need the owner's agreement.

| Input condition | Expected result |
|---|---|
| 10 original customers, 2 retained in a complete month | 20% |
| One retained customer has 5 activity rows | Count that customer once |
| Complete month, no cohort activity | 0% |
| Incomplete month, no activity rows | Unknown/provisional; never final 0% |
| Empty original cohort | Undefined/null; label the denominator condition |
| Data complete only through February 28 UTC | Check the year and full local-month boundary before calling February complete |

Coverage through a UTC date does not establish the end of the corresponding
America/Chicago calendar month. Resolve the precise watermark, not just its
displayed date. A sample can establish arithmetic while publication remains
blocked on unresolved qualification, timezone, coverage, or ownership.
