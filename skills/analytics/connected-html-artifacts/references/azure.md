# Azure database recipe

Identify Azure SQL/PostgreSQL/Cosmos or the actual service before adapting a
connection. HTML calls an approved authenticated API over read-only views or
parameterized queries. Use managed identity from service to database where
supported; browser code never receives database credentials.

Azure Data API builder is one possible REST layer, not a required service. Require
authenticated read roles, row/field restrictions, allowed origins, bounded queries
and applicable private networking. Do not copy example anonymous or write-enabled
permissions into a private-data artifact. Test unauthorized and cross-user access
with synthetic identities on an approved target before release.

Sources reviewed 2026-10-29:
- [Entra authentication](https://learn.microsoft.com/en-us/azure/data-api-builder/concept/security/authenticate-entra)
- [Authorization](https://learn.microsoft.com/en-us/azure/data-api-builder/concept/security/authorization-overview)
