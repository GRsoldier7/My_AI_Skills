# Analysis and SQL evidence contract

1. State decision, metric definition, grain, schema, source, SQL dialect, business
   timezone, coverage and supplied permissions before generating a candidate.
2. Keep numerator and denominator populations explicit. Check join cardinality,
   duplicate/null keys, inactive entities, and dimension attribution.
3. Report missingness and data-quality exceptions before proposing cleaning.
   Never silently drop rows, impute values, or convert errors to zero.
4. Supply parameters and expected-result fixtures. Separate syntax checks,
   synthetic execution, source reconciliation and live authorization.
5. Compare original/proposed control totals, distinct keys, date windows, null
   behavior and security context. State tolerance and unexplained differences.
6. Report only required aggregates by default. Preview raw source rows only when
   permitted and necessary. Keep employer/client context in approved storage.
7. Return decision, evidence, findings, candidate code, expected/observed results,
   uncertainty, and next verification. Never label generated SQL production-ready
   merely because it looks plausible.

## Dialects

- GoogleSQL: explicit timestamp timezone conversion, DATE_TRUNC(date, MONTH),
  SAFE_DIVIDE for an agreed null-on-zero policy, scoped metadata and dry runs.
- PostgreSQL: DATE_TRUNC('month', timestamp), explicit timezone handling and
  floating-point/numeric division. AGE's month component is not total months.
- SQL Server: declare T-SQL; use its actual date/parameter syntax and inspect
  real plans/statistics before index claims.
- Do not substitute one dialect's interval, cast, date or plan syntax for another.

## Cohort fixture

Use [cohort-retention.sql](cohort-retention.sql) after normalizing source dates
into integer month indices in the agreed timezone: year * 12 + month.
GoogleSQL normalization uses EXTRACT(YEAR FROM local_date) * 12 +
EXTRACT(MONTH FROM local_date); PostgreSQL uses the equivalent EXTRACT calls.

A reporting-month input must say whether the complete local interval is covered.
Ten original users and two active users produce 0.2. Duplicate activity does
not change the result. No activity in a complete month is zero; no activity in
an incomplete month is null. Subtract full month indices across year boundaries.
The executable tests cover this portable calculation in SQLite. They do not
certify source timestamp normalization or native BigQuery/PostgreSQL execution.
