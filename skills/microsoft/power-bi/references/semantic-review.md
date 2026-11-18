# Semantic model and report review

Identify the live model or exported artifact revision, connection/storage mode,
authoritative metric contract and permitted operation. With a connected model,
inspect that model; do not assume stale local files describe its current state.

Review fact/dimension grain, relationship cardinality and filter paths, date
roles, measure semantics, blank/zero behavior, report filters and row security.
Prefer a suitable star schema; document justified exceptions to recipe defaults.

For each changed measure, preserve old/new definitions and compare expected
values across representative filters, blank periods, empty populations and
applicable RLS identities. Syntax success is not numerical, performance, or
access-control proof. Compare before/after timings on equivalent cache/context
only when a real execution tool is available.

For reports, check model binding, visual totals, labels/units, date/filter
defaults, accessibility and performance; compare displayed values to query
results. Draft PBIR/TMDL changes separately from publishing them.

## Balance regression cases

Current Balance uses LASTNONBLANKVALUE to return the balance expression, rather
than the date returned by LASTNONBLANK. Respect the current date/filter context.

| Ordered balances in the visible period | Expected last nonblank balance |
|---|---:|
| 100, blank, 150 | 150 |
| 100, blank, blank | 100 |
| 100, 0, blank | 0 |
| blank, blank | blank |

Execute these against an actual model before promotion; static inspection here
does not establish a DAX runtime result. If the business wants a balance carried
from before the visible period, specify that separate date-context rule first.

## Reference source

Microsoft skills-for-fabric semantic-model-authoring is a useful upstream source
for model inspection, TMDL/PBIP, DAX validation and tool selection. The curated
manifest pins the reviewed reference revision. Its MCP, CLI, publish and delete
operations are not installed or inherited by this advisory package.
