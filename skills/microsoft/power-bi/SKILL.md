---
name: power-bi
description: >
  Genius-level Power BI expertise covering DAX, Power Query (M), data modeling, performance optimization,
  report design, deployment pipelines, and governance. Use this skill whenever the user mentions Power BI,
  DAX, Power Query, M language, .pbix files, semantic models, measures, calculated columns, star schemas,
  report performance, RLS, incremental refresh, composite models, DirectQuery, Import mode, aggregations,
  paginated reports, dataflows, deployment pipelines, workspace management, or any BI/analytics task
  involving Microsoft's analytics stack. Also trigger for questions about data modeling best practices,
  slowly changing dimensions, many-to-many relationships, calculation groups, field parameters, or
  XMLA endpoints. Even if the user just says "dashboard" or "report" in a Microsoft context, use this skill.
---

# Power BI — Savant-Level Skill

## Philosophy

Power BI mastery requires three pillars: **data modeling** (the foundation), **DAX** (the engine), and **report design** (the delivery). Most problems stem from modeling mistakes. Always fix the model before writing complex DAX.

---

## 1. Data Modeling (Star Schema First)

### Core Principles
- **Always use star schema**: Fact tables (events/transactions) surrounded by dimension tables (descriptors)
- **One-way relationships only** unless absolutely unavoidable; cross-filter direction = Single
- **Avoid bi-directional filters** — they kill performance and create ambiguity
- **Role-playing dimensions**: Create separate date tables for OrderDate, ShipDate, etc. — never multiple relationships to one table with USERELATIONSHIP as the primary pattern
- **Bridge tables** for many-to-many: Fact → Bridge → Dimension, with bridge table filtered by dimension only
- **Junk dimensions**: Combine low-cardinality flags (IsActive, Status, Priority) into one table
- **Degenerate dimensions**: Keep single-use attributes (OrderNumber) in the fact table

### Relationship Checklist
```
✅ Dimension → Fact (1:many, single direction)
✅ Date table marked as Date Table
✅ No circular dependencies
✅ No calculated columns on fact tables for relationships
❌ Many-to-many without bridge table
❌ Bi-directional unless explicitly required and documented
❌ Snowflake chains deeper than 2 hops
```

### Slowly Changing Dimensions (SCD)
- **Type 1** (overwrite): Default for most dims. Simple, use Power Query to merge/update.
- **Type 2** (history): Add SurrogateKey, ValidFrom, ValidTo, IsCurrent. Fact FK = SurrogateKey.
  ```
  DimCustomer: CustomerSK | CustomerID | Name | City | ValidFrom | ValidTo | IsCurrent
  ```
- **Type 3** (previous value column): Add PreviousCity column. Rarely used.
- For SCD2 in Power Query: Group by natural key, sort by effective date, add index, self-join for ValidTo.

---

## 2. DAX Mastery

### Evaluation Context — The #1 Concept
- **Filter context**: Comes from slicers, filters, rows/columns of visuals, and CALCULATE filter arguments
- **Row context**: Exists inside iterators (SUMX, FILTER, ADDCOLUMNS) and calculated columns
- **Context transition**: CALCULATE converts row context into filter context. This is what makes measures work inside iterators.

### Essential Patterns

#### Time Intelligence (requires a proper Date table)
```dax
// YTD
Sales YTD = TOTALYTD([Sales Amount], 'Date'[Date])

// Prior Year
Sales PY = CALCULATE([Sales Amount], SAMEPERIODLASTYEAR('Date'[Date]))

// YoY %
Sales YoY% = DIVIDE([Sales Amount] - [Sales PY], [Sales PY])

// Rolling 12 Months
Sales R12M =
CALCULATE(
    [Sales Amount],
    DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -12, MONTH)
)

// Parallel Period (flexible)
Sales Prior Period =
CALCULATE(
    [Sales Amount],
    DATEADD('Date'[Date], -1, MONTH)
)
```

#### Semi-Additive Measures (Snapshots/Balances)
```dax
// Last non-blank balance
Current Balance =
CALCULATE(
    LASTNONBLANK('Date'[Date], [Balance Amount]),
    ALLSELECTED('Date'[Date])
)

// Proper snapshot pattern
Headcount =
CALCULATE(
    SUM(FactHeadcount[EmployeeCount]),
    LASTDATE('Date'[Date])
)
```

#### Virtual Relationships & Advanced Filtering
```dax
// TREATAS — virtual relationship
Sales by Manager =
CALCULATE(
    [Sales Amount],
    TREATAS(VALUES(DimManager[EmployeeID]), FactSales[SalesPersonID])
)

// Disconnected parameter table
Selected Metric =
SWITCH(
    SELECTEDVALUE(MetricSelector[Metric]),
    "Revenue", [Revenue],
    "Profit", [Profit],
    "Units", [Units Sold]
)
```

#### Ranking & TopN
```dax
Product Rank =
RANKX(
    ALLSELECTED(DimProduct[ProductName]),
    [Sales Amount],
    ,
    DESC,
    Dense
)

// Dynamic TopN with "Others"
Sales TopN =
VAR TopN = 10
VAR CurrentRank = [Product Rank]
RETURN
IF(CurrentRank <= TopN, [Sales Amount])

Sales Others =
CALCULATE(
    [Sales Amount],
    FILTER(
        ALLSELECTED(DimProduct[ProductName]),
        [Product Rank] > 10
    )
)
```

#### Calculation Groups (Tabular Editor)
```
// Time Calculation Group — eliminates dozens of duplicate measures
Calculation Items:
  - Current: SELECTEDMEASURE()
  - YTD: TOTALYTD(SELECTEDMEASURE(), 'Date'[Date])
  - PY: CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
  - YoY%: VAR CY = SELECTEDMEASURE()
          VAR PY = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
          RETURN DIVIDE(CY - PY, PY)
```

### DAX Anti-Patterns to Avoid
| ❌ Anti-Pattern | ✅ Correct Approach |
|---|---|
| Calculated columns for aggregation | Use measures |
| FILTER(ALL(Table)) on large tables | Use KEEPFILTERS or specific columns |
| Nested CALCULATE without understanding | Break into variables |
| IF(HASONEVALUE(...)) | Use SELECTEDVALUE with alternate |
| DISTINCTCOUNT on high-cardinality | Consider approximate (APPROXIMATEDISTINCTCOUNT) |
| Mixing implicit/explicit measures | Always use explicit measures |

### Variables — Always Use Them
```dax
// Variables evaluate ONCE in their context, then are referenced as constants
Profit Margin =
VAR TotalRevenue = [Revenue]
VAR TotalCost = [Total Cost]
VAR Margin = DIVIDE(TotalRevenue - TotalCost, TotalRevenue)
RETURN
IF(TotalRevenue > 0, Margin, BLANK())
```

---

## 3. Power Query (M Language)

### Performance Rules
1. **Fold everything possible** — keep transformations in the "foldable zone" (before any non-foldable step)
2. **Check query folding**: Right-click step → "View Native Query". If grayed out, folding broke.
3. **Common fold-breakers**: Table.AddColumn with custom functions, Table.Buffer, most List operations
4. **Filter early, select columns early** — reduce data volume before complex transforms

### Key Patterns
```m
// Incremental load with parameters
let
    Source = Sql.Database(Server, Database),
    Filtered = Table.SelectRows(Source, each [ModifiedDate] >= RangeStart
                                          and [ModifiedDate] < RangeEnd)
in
    Filtered

// Dynamic date table
let
    StartDate = #date(2020, 1, 1),
    EndDate = Date.From(DateTime.LocalNow()),
    DateList = List.Dates(StartDate, Duration.Days(EndDate - StartDate) + 1, #duration(1,0,0,0)),
    ToTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    Typed = Table.TransformColumnTypes(ToTable, {{"Date", type date}}),
    Year = Table.AddColumn(Typed, "Year", each Date.Year([Date]), Int64.Type),
    Month = Table.AddColumn(Year, "MonthNum", each Date.Month([Date]), Int64.Type),
    MonthName = Table.AddColumn(Month, "Month", each Date.ToText([Date], "MMM"), type text),
    Quarter = Table.AddColumn(MonthName, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    FiscalYear = Table.AddColumn(Quarter, "FiscalYear", each if Date.Month([Date]) >= 10 then Date.Year([Date]) + 1 else Date.Year([Date]), Int64.Type)
in
    FiscalYear

// Unpivot pattern for normalized data
let
    Source = Excel.Workbook(File.Contents(FilePath)),
    Data = Source{[Name="Sheet1"]}[Data],
    Promoted = Table.PromoteHeaders(Data),
    Unpivoted = Table.UnpivotOtherColumns(Promoted, {"ID", "Name"}, "Attribute", "Value")
in
    Unpivoted

// Error handling
Table.ReplaceErrorValues(PreviousStep, {{"Column1", null}, {"Column2", 0}})
```

### Dataflows Best Practices
- Use dataflows for **shared data prep** across multiple reports
- Linked entities for cross-dataflow references (Premium only)
- Computed entities for transformations on linked entities
- Standard dataflows for most cases; Analytical (CDM) only when feeding Azure Synapse

---

## 4. Performance Optimization

### The Optimization Hierarchy
1. **Model first**: Reduce cardinality, remove unused columns, optimize data types
2. **DAX second**: Use variables, avoid iterators on large tables, minimize CALCULATE nesting
3. **Visuals third**: Limit visuals per page (<8), avoid high-cardinality slicers

### Specific Techniques
- **Disable Auto Date/Time** (always — create your own date table)
- **Integer keys** for relationships (never text/GUID)
- **Remove columns** not used in any visual, measure, or relationship
- **Split high-cardinality text columns** into separate dimension tables
- **Use aggregations** for DirectQuery over large tables (user-defined or automatic)
- **Incremental refresh**: Partition by date, keep X months live, archive rest
- **Composite models**: Import for dimensions, DirectQuery for large facts

### Performance Analyzer
1. Clear cache: DAX Studio → `CALL [DaxStudioClearCache]`
2. Run Performance Analyzer in Desktop
3. Look for: DAX query time > 500ms, visual render > 200ms
4. Copy DAX query → DAX Studio → Server Timings for SE/FE breakdown

### DAX Studio Diagnostics
```dax
// Check model size
SELECT [TABLE_NAME], [ROWS_COUNT], [DICTIONARY_SIZE], [DATA_SIZE]
FROM $SYSTEM.DISCOVER_STORAGE_TABLES
ORDER BY [DATA_SIZE] DESC

// Identify expensive measures
EVALUATE
SUMMARIZECOLUMNS(
    DimProduct[Category],
    "Sales", [Expensive Measure]
)
// Then check Server Timings: SE (storage engine) vs FE (formula engine)
```

---

## 5. Row-Level Security (RLS)

```dax
// Static RLS
[Region] = USERPRINCIPALNAME()

// Dynamic RLS with security table
CONTAINS(
    SecurityTable,
    SecurityTable[UserEmail], USERPRINCIPALNAME(),
    SecurityTable[Region], DimGeography[Region]
)

// Manager hierarchy (parent-child)
PATHCONTAINS(
    DimEmployee[OrgPath],
    LOOKUPVALUE(DimEmployee[EmployeeID], DimEmployee[Email], USERPRINCIPALNAME())
)
```

---

## 6. Deployment & Governance

### Deployment Pipeline Pattern
```
Dev Workspace → Test Workspace → Production Workspace
  - Use Power BI deployment pipelines (Premium/PPU)
  - Parameter rules: Change connection strings per stage
  - Dataset rules: Rebind reports to stage-specific datasets
  - Automate via Power BI REST API + service principal
```

### REST API Automation (PowerShell)
```powershell
# Refresh dataset
Invoke-PowerBIRestMethod -Url "groups/{workspaceId}/datasets/{datasetId}/refreshes" -Method Post

# Export report
Invoke-PowerBIRestMethod -Url "groups/{workspaceId}/reports/{reportId}/ExportTo" -Method Post -Body @{format="PDF"}

# Get refresh history
Invoke-PowerBIRestMethod -Url "groups/{workspaceId}/datasets/{datasetId}/refreshes" -Method Get
```

### Governance Checklist
- [ ] Endorsement: Certified vs Promoted datasets
- [ ] Sensitivity labels applied (Microsoft Purview)
- [ ] Lineage documented in workspace
- [ ] Shared datasets with Build permission (not full copies)
- [ ] Monitoring via Admin API / Activity Log

---

## 7. Semantic Model Best Practices (Post-Nov 2023 Naming)

The "dataset" is now officially a **semantic model**. Key implications:
- XMLA endpoint for external tooling (Tabular Editor, DAX Studio, ALM Toolkit)
- Default semantic model created with each report; prefer standalone semantic models
- Live-connect reports for thin-report/thick-model architecture
- Direct Lake (Fabric): Semantic model reads Parquet directly from OneLake — no import/DQ needed

---

## Reference Files

For extended patterns, read these files from `references/`:
- `references/dax-patterns-advanced.md` — Complex DAX scenarios (basket analysis, ABC, budget allocation, parent-child hierarchies)
- `references/power-query-patterns.md` — M code recipes for common ETL scenarios
- `references/fabric-integration.md` — Fabric lakehouse, Direct Lake, notebooks + PBI integration
