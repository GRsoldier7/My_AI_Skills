---
name: data-analytics-engine
description: |
  Data analytics and business intelligence expert. Use when analyzing data, building reports,
  creating visualizations, designing dashboards, writing SQL queries, performing statistical
  analysis, or making data-driven business decisions.

  EXPLICIT TRIGGER on: "analyze data", "data analysis", "SQL query", "dashboard", "report",
  "visualization", "chart", "graph", "metrics", "KPIs", "business intelligence", "BI",
  "Power BI", "pandas", "dataframe", "pivot table", "trend analysis", "cohort analysis",
  "funnel analysis", "A/B test", "statistical significance", "correlation", "regression",
  "data cleaning", "ETL", "data pipeline", "BigQuery", "data warehouse",
  "executive summary from data", "what does this data tell us".

  Also trigger when the user shares a dataset or asks questions that require quantitative
  reasoning, even without explicitly saying "analytics."
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: database-design, power-bi, financial-model-architect, market-intelligence
  last-reviewed: "2026-03-21"
  review-trigger: "New analytics tools, library updates, user reports incorrect analysis patterns"
  capability-assumptions:
    - "Python with pandas, numpy, matplotlib/plotly available"
    - "SQL access via SQLAlchemy or direct database connection"
    - "Power BI for enterprise dashboards, Python for ad-hoc analysis"
  fallback-patterns:
    - "If no Python: provide SQL-only analysis approach"
    - "If no database access: work with CSV/JSON files the user provides"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: data question, dataset, report request, or dashboard design need
- Output produces: analysis, SQL queries, Python scripts, visualization specs, or insight summary
- Can chain from: database-design (schema → queries), market-intelligence (research → analysis)
- Can chain into: power-bi (analysis → dashboard), financial-model-architect (data → model)
- Orchestrator notes: always clarify the business question before writing queries

---

## Analysis Framework

### Step 1: Clarify the Question
Before touching data, ensure you understand:
- **What decision** will this analysis inform?
- **What would change** if the answer were X vs Y?
- **Who is the audience** — executive (high-level), manager (actionable), analyst (detailed)?
- **What data is available** and where does it live?

### Step 2: Explore the Data
```python
import pandas as pd

df = pd.read_csv("data.csv")  # or pd.read_sql(query, engine)
print(df.shape)                # rows, columns
print(df.dtypes)               # column types
print(df.describe())           # statistical summary
print(df.isnull().sum())       # missing values per column
print(df.head(10))             # sample rows
```

### Step 3: Clean and Prepare
- Handle missing values: drop, fill (mean/median/mode), or flag
- Fix data types: dates as datetime, categories as categorical
- Remove duplicates: `df.drop_duplicates(subset=['key_column'])`
- Validate ranges: are values within expected bounds?

### Step 4: Analyze
Choose the right technique for the question:

| Question Type | Technique |
|--------------|-----------|
| What happened? | Descriptive stats, aggregation, time series |
| Why did it happen? | Segmentation, correlation, drill-down |
| What will happen? | Trend extrapolation, regression, forecasting |
| What should we do? | A/B test analysis, scenario modeling, optimization |

### Step 5: Communicate
- **Lead with the insight**, not the methodology
- **One key finding per visualization** — don't overload charts
- **Include the "so what"** — what should the audience DO with this information?
- **Confidence level** — flag uncertainty, sample sizes, caveats

---

## SQL Patterns

### Aggregation with Context
```sql
-- Revenue by month with running total and month-over-month change
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(revenue) AS monthly_revenue,
    SUM(SUM(revenue)) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS running_total,
    ROUND(
        (SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY DATE_TRUNC('month', order_date)))
        / NULLIF(LAG(SUM(revenue)) OVER (ORDER BY DATE_TRUNC('month', order_date)), 0) * 100,
    1) AS mom_change_pct
FROM orders
GROUP BY 1
ORDER BY 1;
```

### Cohort Analysis
```sql
-- User retention by signup month
WITH user_cohort AS (
    SELECT user_id, DATE_TRUNC('month', created_at) AS cohort_month
    FROM users
),
activity AS (
    SELECT user_id, DATE_TRUNC('month', activity_date) AS active_month
    FROM user_activity
)
SELECT
    uc.cohort_month,
    EXTRACT(MONTH FROM AGE(a.active_month, uc.cohort_month)) AS months_since_signup,
    COUNT(DISTINCT a.user_id) AS active_users,
    COUNT(DISTINCT a.user_id)::FLOAT / COUNT(DISTINCT uc.user_id) AS retention_rate
FROM user_cohort uc
JOIN activity a ON uc.user_id = a.user_id
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Funnel Analysis
```sql
SELECT
    COUNT(CASE WHEN visited THEN 1 END) AS visitors,
    COUNT(CASE WHEN signed_up THEN 1 END) AS signups,
    COUNT(CASE WHEN activated THEN 1 END) AS activated,
    COUNT(CASE WHEN paid THEN 1 END) AS paid,
    ROUND(COUNT(CASE WHEN paid THEN 1 END)::FLOAT
        / NULLIF(COUNT(CASE WHEN visited THEN 1 END), 0) * 100, 1) AS overall_conversion
FROM user_journey;
```

---

## Visualization Guide

### Chart Selection
| Data Relationship | Chart Type |
|------------------|------------|
| Change over time | Line chart (continuous), bar chart (discrete periods) |
| Comparison across categories | Horizontal bar chart |
| Part of a whole | Stacked bar (over time), donut/pie (single point, max 5 segments) |
| Distribution | Histogram, box plot |
| Correlation between two variables | Scatter plot |
| Geographic | Choropleth map |
| Flow/process | Sankey diagram |

### Visualization Rules
- **Title = insight**, not description ("Revenue grew 23% in Q4" not "Q4 Revenue Chart")
- **Remove chartjunk** — no 3D, no unnecessary gridlines, minimal decoration
- **Consistent colors** — same metric = same color across all charts
- **Label directly** — labels on the data, not in a legend the reader has to cross-reference
- **Start y-axis at zero** for bar charts (truncated axes mislead)

---

## Python Analysis Patterns

### Quick Pivot Analysis
```python
# Revenue by product category and quarter
pivot = df.pivot_table(
    values='revenue',
    index='product_category',
    columns=pd.Grouper(key='order_date', freq='Q'),
    aggfunc='sum',
    fill_value=0
)
```

### Time Series Decomposition
```python
from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(df['metric'], model='additive', period=12)
result.plot()  # trend, seasonal, residual components
```

### Statistical Testing
```python
from scipy import stats

# A/B test: is the difference significant?
group_a = df[df['group'] == 'control']['conversion']
group_b = df[df['group'] == 'treatment']['conversion']
t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"p-value: {p_value:.4f} — {'Significant' if p_value < 0.05 else 'Not significant'}")
```

---

## Reporting Templates

### Executive Summary Format
```
TITLE: [What was analyzed]
KEY FINDING: [One sentence — the most important insight]
IMPACT: [What this means for the business in dollars, users, or risk]
RECOMMENDATION: [What to do about it]
SUPPORTING DATA: [2-3 charts or tables that prove the finding]
CAVEATS: [Data limitations, sample size, confidence level]
```

### KPI Dashboard Design
- **Top row:** 3-5 headline KPIs with trend arrows (up/down/flat)
- **Middle:** Time series of key metrics (filterable by date range)
- **Bottom:** Breakdown tables and drill-down charts
- **Every metric needs:** definition, data source, refresh frequency, owner

---

## Self-Evaluation (run before presenting analysis)

Before presenting, silently check:
[ ] Did I clarify the business question before diving into data?
[ ] Is the analysis answering the question that was asked, not a different one?
[ ] Are statistical claims supported (sample size, significance, confidence)?
[ ] Does the visualization type match the data relationship?
[ ] Have I included the "so what" — actionable recommendation, not just numbers?
[ ] Are caveats and limitations disclosed?
If any check fails, revise before presenting.
