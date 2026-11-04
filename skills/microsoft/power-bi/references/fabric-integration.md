# Fabric integration review

Resolve actual workspace, item, semantic model and report binding before giving
Fabric-specific instructions. Fabric availability is a capability check, not an
assumption from the presence of Power BI.

Distinguish Import, DirectQuery and the model's supported Direct Lake mode.
Inspect source permissions, refresh/freshness behavior, fallback behavior where
applicable, and row security for the actual connection and model configuration.
Do not assert one universal Direct Lake capability across deployment modes.

When offline, review exported metadata and record unknown service state.
When connected read tools exist, scope them to the approved workspace/item.
Keep model authoring, refresh, publishing and deployment out of review-only work.

Official references:
- https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview
- https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
- https://learn.microsoft.com/en-us/dax/lastnonblankvalue-function-dax
