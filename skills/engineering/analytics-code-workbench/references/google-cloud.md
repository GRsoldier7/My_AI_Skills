# Google Cloud analytics and BigQuery

Use this when an analyst needs a GoogleSQL draft, a BigQuery bill or runtime investigation, or a read-only diagnosis across Cloud Storage, BigQuery and Power BI. Start with approved project aliases, region, dataset/table grain, reporting window, data freshness, a cost ceiling and the available evidence. Never assume console, CLI or service account access. Keep source rows, credentials and actual project identifiers in the authorized environment.

## Draft and reconcile a query

Use named, typed parameters and a half-open partition range. Select needed columns, partition-filter the actual partition field and aggregate each fact to the intended grain before joining. Verify distinct keys and parent-to-child row counts. A LIMIT on output is insufficient as a cost control. Use SAFE_DIVIDE for undefined denominators and label the result. Supply a separate query or report for rejected/incomplete rows.

```sql
WITH cohorts AS (
  SELECT * FROM UNNEST([
    STRUCT('A' AS area, 1 AS completed, 2 AS eligible),
    STRUCT('B' AS area, 2 AS completed, 8 AS eligible),
    STRUCT('C' AS area, 0 AS completed, 0 AS eligible)
  ])
)
SELECT area, SUM(completed) AS completed, SUM(eligible) AS eligible,
       SAFE_DIVIDE(SUM(completed), SUM(eligible)) AS completion_rate
FROM cohorts
GROUP BY GROUPING SETS ((area), ());
```

The total is 3/10 (30%), B is 2/8 (25%), and C has a NULL rate. Match the warehouse result, Power BI measure and reporting timezone at the same grain. A discrepancy at a join often means the measure has counted a fact twice.

## Investigate a slow, costly or stale report

1. Trace the freshest approved object metadata in Cloud Storage, the BigQuery load or external table, the last successful query job and the Power BI semantic-model refresh in order. Compare region, partition date and business timestamp. For an access error, identify the failing identity and resource boundary from supplied evidence. Object metadata or a log snippet need not expose row contents.
2. For cost, distinguish on-demand scan bytes from reservations/slot usage. Request the redacted query plan and the specific job's bytes processed/billed, cache status, slot milliseconds and elapsed time. Look for unpruned partitions, cross joins and repeated scans. Use the caller's own job history if sufficient. Avoid project-wide job visibility unless the operator already has it.
3. Propose a dry run and, for on-demand pricing, a maximum bytes billed limit set by the authorized operator. Confirm the billing project and matching dataset location. Dry run bytes are estimates and may be unavailable for some source types. If the estimate exceeds the limit, return a narrower query and leave execution to the owner. Distinguish permission to create a query job from permission to read dataset rows. Do not provision IAM, run a billed query or change retention.
4. Return a finding with evidence, confidence, a proposed check and expected result. If no cloud access exists, use the synthetic query or supplied job statistics and label the rest unverified.

[Google's BigQuery skill](https://github.com/google/skills/tree/4bb21ebfa085f6307d5d62bc21765e1d3433f11d/skills/cloud/bigquery-basics) · [Dry runs](https://cloud.google.com/bigquery/docs/running-queries#dry-run) · [Controlling costs](https://cloud.google.com/bigquery/docs/best-practices-costs) · [Job metadata](https://cloud.google.com/bigquery/docs/information-schema-jobs-by-user)
