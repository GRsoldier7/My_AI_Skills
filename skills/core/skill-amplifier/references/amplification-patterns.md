# Amplification Patterns Reference

Extended examples, templates, and chain maps for the skill-amplifier.

---

## Table of Contents
1. Pass-by-Pass Examples (applied to real skills)
2. Domain-Specific Constitutional Constraint Templates
3. Composability Chain Map — Master_Skills Library
4. Batch Mode Scoring Template

---

## 1. Pass-by-Pass Examples

### Pass 1 — Metacognitive Scaffolding (example: financial-model-architect)

**Before:**
> Build the financial model, output the Excel file.

**After:**
> Build the financial model. Before presenting the file, silently verify:
> [ ] All formulas reference correct cells — no hard-coded values where dynamic is needed
> [ ] Three scenarios (base / bull / bear) are all populated, not just base
> [ ] Unit economics (CAC, LTV, churn) are internally consistent across tabs
> [ ] The summary tab matches the detail tabs — no orphaned numbers
> If any check fails, fix before outputting.

---

### Pass 2 — Adaptive Context Injection (example: database-design)

**Before:**
> Generate the PostgreSQL schema DDL.

**After:**
> Generate the PostgreSQL schema DDL.
> - If running in Claude Code with Bash available: write the DDL to `schema.sql` and run
>   `psql -c "\d"` to verify table creation.
> - If no Bash available: output as a fenced SQL code block and note that the user should
>   run it manually.
> - If the user's message mentions an ORM (SQLAlchemy, Prisma, Drizzle): generate both the
>   raw DDL and the ORM model file in the appropriate format.

---

### Pass 3 — Composability Contract (example: market-intelligence)

```
## Composability Contract
- Input expects: target market/industry name, optional competitor list, optional geography
- Output produces: TAM/SAM/SOM analysis, competitor matrix, opportunity scoring report (Markdown)
- Can chain into: business-plan-architect, go-to-market-engine, pricing-strategist
- Receives from: business-genius (as orchestrator), entrepreneurial-os (as research phase)
- Orchestrator notes: output is always Markdown — downstream skills can parse directly
```

---

### Pass 4 — Self-Evaluation Hooks (domain-specific templates)

**For code-generation skills:**
```
Before presenting code, silently verify:
[ ] Code runs without syntax errors (mentally trace or actually execute if Bash available)
[ ] Edge cases handled: empty input, null values, out-of-range parameters
[ ] No hardcoded credentials, paths, or environment-specific values
[ ] Tests would pass with this implementation
```

**For writing/content skills:**
```
Before presenting the content, silently verify:
[ ] Directly addresses the user's stated goal — no scope drift
[ ] Tone matches the context (formal/informal, technical/general)
[ ] No claims made without basis — hypotheticals labeled as such
[ ] Actionable: the user knows what to do next after reading this
```

**For analysis/research skills:**
```
Before presenting the analysis, silently verify:
[ ] Conclusions are supported by the data/research presented
[ ] Counterarguments or alternative interpretations are acknowledged
[ ] Confidence level is stated for each major claim
[ ] Sources or reasoning chains are visible, not just conclusions
```

---

### Pass 7 — Trigger Precision (before/after: power-bi)

**Before:**
> Expert in Power BI, DAX, and data visualization.

**After:**
> Deep Power BI and DAX expert. Use when the user needs help with: Power BI report design,
> DAX formula writing or debugging, Power Query / M language, data model relationships,
> row-level security, calculated columns vs measures, report performance optimization,
> publishing to Power BI Service, or building dashboards for business stakeholders.
> Trigger phrases: "Power BI", "DAX formula", "Power Query", "CALCULATE function",
> "measure vs column", "my report is slow", "data model", "build a dashboard in BI".
> Also trigger when user shares a DAX error or describes a visualization problem without
> naming Power BI explicitly — infer from context.
> Do NOT use for Excel pivot tables, Tableau, Looker, or general SQL — use database-design
> or the relevant specialist instead.

---

## 2. Domain-Specific Constitutional Constraint Templates

### For financial skills (financial-model-architect, pricing-strategist, startup-tax-strategist):
- "Do not present financial projections as guaranteed outcomes. Label all forward-looking
  statements as estimates based on stated assumptions."
- "Before recommending a tax strategy, state that the user should verify with a licensed CPA
  or tax attorney before implementation."
- "Never output specific investment advice (buy/sell/hold). Provide analysis frameworks only."

### For technical/code skills (database-design, code-review, testing-strategy):
- "Before suggesting schema changes to an existing database: flag that migrations require
  backup verification and staging environment testing first."
- "Do not generate or output credentials, API keys, connection strings, or secrets — even
  as examples. Use placeholder syntax instead (e.g., YOUR_API_KEY)."

### For business strategy skills (business-genius, go-to-market-engine, market-intelligence):
- "If the user's plan involves a regulated industry (healthcare, finance, legal, food/drug),
  flag the regulatory dimension explicitly before proceeding with strategy."
- "Do not make specific claims about competitor financials, internal strategies, or
  confidential information. Base competitive analysis on publicly available data only."

### For Microsoft Power Platform skills:
- "Before recommending a Power Automate flow that involves production data or shared
  environments: recommend testing in a dev/sandbox environment first."
- "Flag licensing requirements when recommending Premium connectors — user may not have
  the license tier required."

### For faith/theology skills:
- "Present theological positions with respect for diverse Christian traditions. When
  multiple credible interpretations exist, acknowledge them rather than presenting one
  as the only valid reading."
- "Distinguish between exegesis (what the text says) and application (what it means for
  the user's situation). Do not conflate the two."

---

## 3. Composability Chain Map — Master_Skills Library

```
business-genius (orchestrator)
  ├─> market-intelligence
  │     └─> business-plan-architect
  │           └─> financial-model-architect
  │                 └─> pricing-strategist
  ├─> go-to-market-engine
  │     ├─> marketing-strategist
  │     │     └─> copywriting-conversion
  │     │           └─> content-marketing-machine
  │     └─> sales-closer
  └─> entrepreneurial-os

polychronos-team (master orchestrator)
  └─> [any skill in the library]

skill-amplifier (meta layer — operates on skills, not on tasks)
  └─> [any SKILL.md in the library]

skill-builder (creation layer)
  └─> skill-amplifier (run after creation for maximum output)

biohacking-data-pipeline
  └─> cloud-migration-playbook
        └─> database-design

faith/bible-study-theologian
  └─> faith/sunday-school-teacher (research → curriculum)
  └─> faith/faith-life-integration (theology → application)
```

---

## 4. Batch Mode Scoring Template

When running in batch mode, output this table for each skill assessed:

| Skill | P1 Meta | P2 Adaptive | P3 Compose | P4 Self-Eval | P5 Disclosure | P6 Future | P7 Trigger | P8 Constitutional | Score | Priority |
|-------|---------|------------|-----------|-------------|--------------|----------|-----------|------------------|-------|---------|
| skill-name | 1-5 | 1-5 | 1-5 | 1-5 | 1-5 | 1-5 | 1-5 | 1-5 | avg | H/M/L |

**Priority tiers:**
- **High (score < 3.0):** Rewrite now — these skills are underperforming and hurting productivity
- **Medium (3.0–3.9):** Rewrite next sprint — solid but leaving performance on the table
- **Low (4.0–4.4):** Polish pass — minor improvements only
- **Optimal (4.5+):** No action needed — monitor on next Claude major version

Output full rewrites for all High priority skills in the same batch run.
Output the scoring table + offer to rewrite for Medium priority.
Output a one-line note for Low and Optimal.
