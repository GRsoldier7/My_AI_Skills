# Power BI model, measure and refresh review

Use for a KPI, report design, Power Query review, slow visual or failed refresh. Return a design or diagnostic brief in ChatGPT Enterprise or GitHub Copilot from a supplied schema, formula, redacted error or synthetic fixture. This pack has no Power BI service connection. Assign any Desktop/service verification, release or rollback to the authorized model owner.

## Establish the metric and model

1. Identify the decision, authoritative source, row grain, business key, reporting period/time zone, exclusions, units, freshness target and reconciliation total. Confirm the owner and definitions of numerator and denominator. Distinguish an unknown count from a true zero.
2. Reuse a governed semantic model if it already supplies the required measures, grain, dimensions, freshness and RLS. A thin report can reference that model. Confirm Build permission and existing definitions through the owner. For a supplied `INFO.VIEW.MEASURES()` export, formula text requires model write permission and is unavailable in Desktop live connection. If the expression is unavailable, report visible results and the missing definition. Never reconstruct private DAX from an output value.
3. For a model change proposal, state the fact grain and unique dimension keys. Define one-to-many relationships from dimensions to facts with an intentional filter direction. Compare source and loaded row counts, unique keys, unmatched dimensions and additive control totals before and after joins. Keep facts with different grains separate unless an explicit allocation or aggregation reconciles them.

## Synthetic example: on-time completion rate

Source grain is **one row per queue per day**. `OnTime` is a subset of `Eligible`. Zero eligible means the rate is undefined. Reject duplicate date/queue rows, negative counts, null counts and OnTime > Eligible for owner investigation. Use this stand-alone Power Query M fixture as the table named `QueueDay`:

```powerquery
let
    Fixture = #table(
        type table [Day = date, Queue = text, OnTime = Int64.Type, Eligible = Int64.Type],
        {
            {#date(2026, 11, 2), "North", 9, 10},
            {#date(2026, 11, 2), "South", 1, 2},
            {#date(2026, 11, 3), "North", 1, 2},
            {#date(2026, 11, 3), "South", 0, 0}
        }
    )
in
    Fixture
```

For a source-quality check, draft a second Power Query query referencing `QueueDay`. It returns exception groups for review. The fixture should return zero rows. Copying the first fixture row should flag North on November 2 with two rows. A 3-of-2 count should flag the affected day/queue. Gate publication on owner reconciliation. Silently dropping exceptions changes the rate.

```powerquery
let
    ByKey = Table.Group(QueueDay, {"Day", "Queue"}, {
        {"Rows", each Table.RowCount(_), Int64.Type},
        {"InvalidCounts", each Table.RowCount(Table.SelectRows(_, each
            [OnTime] = null or [Eligible] = null or [OnTime] < 0 or
            [Eligible] < 0 or [OnTime] > [Eligible])), Int64.Type}
    }),
    Exceptions = Table.SelectRows(ByKey, each
        [Day] = null or [Queue] = null or [Rows] <> 1 or [InvalidCounts] > 0)
in
    Exceptions
```

Define each DAX measure separately and format the rate as a percentage:

```dax
On-time completions = SUM(QueueDay[OnTime])
```

```dax
Eligible completions = SUM(QueueDay[Eligible])
```

```dax
On-time rate = DIVIDE([On-time completions], [Eligible completions])
```

| Visual context | Expected numerator / denominator | Expected rate |
|---|---|---|
| Grand total | 11 / 14 | 78.57% |
| November 2 | 10 / 12 | 83.33% |
| November 2 → North / South | 9 / 10 and 1 / 2 | 90% and 50% |
| November 3 → South | 0 / 0 | BLANK() |
| North across both days | 10 / 12 | 83.33% |

If a grand total shows the unweighted mean of queue percentages, inspect the numerator and denominator in the total filter context. Use the matrix drilldown and a single-queue slicer to verify aggregation and relationship propagation. If the blank leaf is hidden by the visual, enable “Show items with no data” in the test matrix or display the denominator beside the rate.

## Diagnose and hand off

| Symptom | Evidence and decision |
|---|---|
| Slow visual | Capture one reproducible slicer/drill action and Performance Analyzer timings. Distinguish DAX query, source/DirectQuery, rendering and other time where reported. Simplify the slow visual or model/query step, then compare the same interaction under comparable cache conditions. |
| Late or failed refresh | Record storage mode, last successful refresh, history/error stage, source's last update and business data-through date. Check credential/gateway or schema changes, partition window and timezone first where relevant. For supported connectors inspect query folding after early filters and projections. Report suspected cause separately from verified cause. |
| Wrong audience or rollout | Draft a role matrix for permitted queue, other queue and unmapped consumer. Test with representative Viewer access. Admin, Member and Contributor workspace roles bypass RLS. Check detail, drillthrough and totals for each role. Agree release owner, acceptance total, freshness target, baseline timing and version to restore if any gate fails. |

**Handoff.** Supply metric contract, source/grain and relationship sketch, M/DAX draft, expected fixture results, discrepancies, role/refresh checks and rollback decision. Label calculations based on synthetic rows separately from tests observed in Desktop or the service.

[Microsoft Learn: governed model reuse](https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-across-workspaces) · [star schema and grain](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax) and [measure expression visibility](https://learn.microsoft.com/en-us/dax/info-view-measures-function-dax) · [query folding](https://learn.microsoft.com/en-us/power-query/query-folding-basics) · [RLS and workspace roles](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security) · [Performance Analyzer](https://learn.microsoft.com/en-us/power-bi/create-reports/performance-analyzer) · [refresh troubleshooting](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-troubleshooting-refresh-scenarios)
