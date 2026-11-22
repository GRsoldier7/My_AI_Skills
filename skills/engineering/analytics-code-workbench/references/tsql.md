# Azure SQL and T-SQL reporting

State the row grain and unique key for each table. Decide how duplicates, NULL, late-arriving records, time zones and zero eligibility should affect the metric. Use a half-open period (`>= @start` and `< @end`) with typed parameters. Aggregate facts to their intended grain before joining a one-to-many detail table. Check cardinality separately. A total rate is normally the sum of the numerators divided by the sum of the denominators.

```sql
WITH cohorts AS (
    SELECT 'A' AS area, 1 AS completed, 2 AS eligible
    UNION ALL SELECT 'B', 2, 8
)
SELECT 1.0 * SUM(CAST(completed AS bigint))
       / NULLIF(SUM(CAST(eligible AS bigint)), 0) AS completion_rate
FROM cohorts;
```

Expected rate is 0.30. An empty or zero-eligible group yields NULL. A query that averages 50% and 25% returns 37.5%, which weights the two areas equally. Ask which metric the business defines before choosing. Where counts can be NULL, compare count of rows with count of complete pairs and report incomplete pairs according to the metric contract.

When tuning, request the query, parameter values or distributions, index definitions and an authorized plan. Identify the operator responsible for work before suggesting an index. Include cost to writers. Access to a production plan, schema or permissions is a distinct prerequisite. Supply a read-only diagnostic first. For an approved change, require a bounded predicate, expected affected count, preview and a rollback or recovery plan. The upstream SQL Server reference is optional; check Azure SQL Database feature and permission differences for the target. [NULLIF in T-SQL](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/nullif-transact-sql)
