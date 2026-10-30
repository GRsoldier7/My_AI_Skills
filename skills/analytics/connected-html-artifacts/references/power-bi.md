# Power BI: report embed versus custom data

Secure organizational embed preserves an existing report. Confirm report access,
tenant policy, viewer licensing/capacity and allowed hosting. Supply an approved
report link when iframe/sign-in fails. Do not treat a file:// page or a ChatGPT
preview as a verified OAuth/embed host. Never replace secure embed with Publish
to web for private data: that makes content publicly accessible.

Custom HTML charts need a separate authenticated query service. Execute Queries
requires the tenant setting, read/build permissions and suitable scopes; inspect
row/value/size limits and response errors even when HTTP status is 200. Partial
results must remain labeled incomplete. Use reviewed DAX/query identifiers, not
arbitrary client-submitted expressions. Preserve row-level security and SSO;
service principals are unsupported for datasets with RLS or SSO. Do not bypass
that restriction with a broad shared identity.

Secure embedding generally needs Pro/PPU viewer licensing unless qualifying
capacity covers both report and model. Verify current tenant terms before a real
deployment; the repository example does not establish entitlement.

Sources reviewed 2026-10-29:
- [Secure embed](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-embed-secure)
- [Execute Queries](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries)
- [Publish-to-web exposure](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-publish-to-web)
