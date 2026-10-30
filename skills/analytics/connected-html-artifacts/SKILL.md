---
name: connected-html-artifacts
description: Build HTML reports and tools from Excel/CSV snapshots, secure Power BI embeds, or approved read-only APIs for Power BI, BigQuery and Azure data. Use when a visual artifact needs business data, refresh behavior or authenticated connectivity.
---

# Connected HTML artifacts

Own the connection between verified data and the HTML presentation. Reuse the
selected design/artifact skill and existing analytics procedures for metric and
query correctness. One creator owns layout; this skill owns data access, source
identity, freshness, failure states, and safe delivery.

## Choose the delivery mode

| Mode | Use when | Load |
|---|---|---|
| Snapshot | A portable file is sufficient or the host cannot authenticate | [Snapshots](references/snapshots.md) |
| Secure Power BI embed | The existing report should retain its own interactions and permissions | [Power BI](references/power-bi.md) |
| Authenticated live API | Custom HTML charts need refreshable private data | [Live APIs](references/live-apis.md), then the provider recipe |

Prefer one HTML frontend. Approved external services/libraries are permitted;
record their hosts and pinned versions. Explicit offline requests require all
essential assets/data inline and zero network calls. Live authenticated delivery
may need an approved hosted backend; a standalone HTML file does not supply one.

## Establish the data contract

Resolve the audience, source, metric definitions, permitted columns/rows, refresh
expectation and approved hosting/authentication from context. Ask only when an
unknown changes the implementation. Distinguish observed results from synthetic
examples. Show source, retrieval time, data-as-of time and freshness separately
where they differ. Never label a workbook export as a live workbook connection.

Default to synthetic or explicitly supplied data while connectivity is unverified.
Do not put employer/client data, report IDs, tenant details, credentials, tokens,
cookies or signed download URLs in the public library. Never use Power BI Publish
to web for private reports. Short-lived user tokens may exist in memory only
through an approved authentication flow; never prefill them in exported HTML.

## Implement and verify

1. Select one mode and load only its references. For GCP, BigQuery is a recipe,
   not an assumption about the actual service. For Azure, identify the database
   before choosing an adapter.
2. Use semantic HTML, accessible data tables, visible focus and labeled controls.
   Treat all source content as untrusted: textContent/DOM text nodes, safe JSON
   serialization, and formula-safe CSV export. No arbitrary browser-supplied
   SQL/DAX, secret-bearing URLs or direct database credentials.
3. Implement loading, empty, invalid data, denied/expired authorization, timeout,
   offline and stale states. Never silently substitute demo values after failure.
4. Verify numbers against the source and metric contract. Test the final delivered
   HTML, keyboard operation, narrow screens, exports and failure paths. Follow the
   [acceptance checklist](references/acceptance.md).
5. Deliver the artifact, source/refresh instructions, dependency list, verified
   checks and remaining limits. Actual-host authentication and licensing remain
   unverified until exercised on the authorized target.

## Host boundaries

ChatGPT skills-only mode can author files and interpret supplied data using the
capabilities actually available. Do not claim previews permit arbitrary iframes,
OAuth or network calls. Copilot may implement/test with approved project tools;
no MCP server is required. Account registration, deployment, permissions changes
and live credentials are separate target-specific actions.

## Resources

- [Google Cloud / BigQuery](references/bigquery.md)
- [Azure databases](references/azure.md)
- [Synthetic CSV](examples/sample.csv)
- [Portable CSV snapshot example](examples/snapshot.html)

The example is a synthetic CSV demonstration, not an Excel parser or live-data
connector. Never present its data as a business result.
