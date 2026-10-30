# Google Cloud / BigQuery recipe

Confirm that BigQuery is the actual GCP source. Use an approved backend with
workload identity/Application Default Credentials and least-privilege dataset
access. BigQuery does not accept API-key authentication. Never embed service
account credentials in HTML.

Use reviewed, parameterized read-only queries; restrict project, dataset, region,
returned fields, maximum bytes billed, timeout and result size. Keep metric/query
review in the existing bigquery-review and bi-metric-contract skills. Query costs
and data access require the authorized project's policy, not library defaults.

Sources reviewed 2026-10-29:
- [Authentication](https://docs.cloud.google.com/bigquery/docs/authentication/getting-started)
- [Running queries](https://docs.cloud.google.com/bigquery/docs/running-queries)
