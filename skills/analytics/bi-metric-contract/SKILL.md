---
name: bi-metric-contract
description: Use when defining a KPI, resolving conflicting metric definitions, or changing SQL, DAX, or dashboard calculations whose business meaning is unclear.
metadata:
  version: "0.1.0"
  domain-category: analytics
  last-reviewed: "2026-10-26"
---

# BI Metric Contract

Make the business definition testable before implementing the calculation.
Keep actual organization definitions in their approved workspace; use synthetic
examples in shared skills.

1. Read the supplied definition, approved sources, existing contract, and decision
   being supported. Identify owner and version. An absent owner stays unknown.
2. Fill the [contract](references/contract.md). Label decisions as supplied,
   sourced, proposed, or unresolved. Ask only about ambiguities that change the
   result; a draft with explicit unknowns can still be useful.
3. Fix population and grain before the formula. Distinguish event, entity,
   snapshot, ratio, and cohort metrics; identify join fanout and nonadditivity.
4. Specify date role, timezone, full-period coverage, exclusions, late arrivals,
   deduplication, and null/zero rules. Missing activity is zero only in a
   confirmed complete period. No rows alone never proves completeness.
5. Give small input rows and expected results, including duplicates, empty
   denominators, missing/partial periods, and an applicable security context.
   Derive expected values independently of the implementation.
6. Return the contract, acceptance examples, unresolved decisions with impact,
   and exact next verification. Mark ready only when required semantics and
   evidence are resolved. SQL/DAX syntax success alone does not prove correctness.

For retention, divide distinct retained cohort members by the fixed original
cohort, including inactive members. Ten original customers and two retained
customers means 20%; an uncovered future month remains unknown.

Output a concise contract and test table. Never infer approval, an owner, data
coverage, or a business rule from silence. A profile selects this method; it
does not authorize access, data movement, publication, or metric changes.
