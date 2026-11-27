---
name: financial-model-architect
description: >
  Genius-level financial modeling covering SaaS unit economics, three-statement models,
  runway calculation, investor-ready metrics, scenario planning (base/bull/bear), and
  bootstrapper-specific financial strategies. Use this skill whenever the user needs to
  model financials, calculate runway, understand their unit economics, build investor
  projections, analyze burn rate, plan for profitability, or stress-test their business
  assumptions. Also trigger for questions about MRR/ARR, churn modeling, LTV:CAC analysis,
  cohort revenue analysis, cash flow planning, operating expenses, or when to hire.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: strategy
  adjacent-skills: business-plan-architect, pricing-strategist, entrepreneurial-os
  last-reviewed: "2026-03-15"
  review-trigger: "SaaS benchmarks update (OpenView, Bessemer), interest rate environment shift, major bootstrap financial tool released"
  capability-assumptions:
    - "No external tools required — text-based frameworks and guidance"
  fallback-patterns:
    - "If financial specifics needed: recommend CPA or financial advisor verification"
  degradation-mode: "graceful"
---

# Financial Model Architect — Savant-Level Skill

## Philosophy

Financial modeling mastery = **drivers before outputs** (model the machine, not the wish), **scenario planning as standard** (base case is wrong; bull and bear cases bracket reality), **cash before GAAP** (cash is fact, profit is opinion), and **simple enough to defend** (a model with 100 tabs you can't explain is worse than a 10-row spreadsheet you can).

---

## 1. SaaS Metrics Master Reference

### The Core SaaS Metric Stack
```
Revenue Metrics:
  MRR (Monthly Recurring Revenue)
    = Sum of all active monthly subscriptions
    = New MRR + Expansion MRR - Churned MRR - Contraction MRR

  ARR (Annual Recurring Revenue) = MRR × 12

  MRR Decomposition (every month):
    New MRR:        From new customers acquired
    Expansion MRR:  From upgrades/upsells of existing customers
    Churned MRR:    From cancelled customers (negative)
    Contraction MRR: From downgrades (negative)
    Net New MRR:    = New + Expansion - Churned - Contraction

Retention Metrics:
  Logo Churn Rate:  % of customers who cancel
    Monthly: (Churned customers / Start of period customers) × 100
    Target: < 1%/mo (enterprise), < 3%/mo (SMB), < 5%/mo (consumer)

  Revenue Churn Rate:  % of MRR lost from existing customers
    = (Churned MRR + Contraction MRR) / Start MRR × 100

  Net Revenue Retention (NRR):  Holy grail metric
    NRR = (Start MRR + Expansion - Churn - Contraction) / Start MRR × 100
    > 100% = customers spending MORE over time (expansion > churn)
    > 120% = exceptional (product growing without new customers)
    Benchmarks: 105% (good), 115% (great), 130%+ (elite — Snowflake territory)

Efficiency Metrics:
  CAC (Customer Acquisition Cost)
    = (Sales + Marketing Spend) / New Customers

  LTV (Lifetime Value)
    = ARPU × Gross Margin / Monthly Churn Rate
    Or: ARPU × Average Customer Lifetime (in months)

  LTV:CAC Ratio
    < 3:1 = Struggling
    3:1   = Sustainable
    5:1   = Healthy
    > 7:1 = Potential underinvestment in growth

  CAC Payback Period
    = CAC / (ARPU × Gross Margin)
    < 6 months  = Aggressive (invest more)
    6-12 months = Healthy SaaS
    12-24 months = Bootstrappable but tight
    > 24 months = Needs restructuring

  Magic Number
    = (Net New ARR × Gross Margin) / Prior Quarter S&M Spend
    > 0.75 = Good efficiency; spend more
    < 0.5  = Fix CAC before scaling spend
```

---

## 2. Three-Statement Financial Model

### Statement Hierarchy
```
Income Statement (P&L):
  Revenue
  - COGS (Cost of Goods Sold)
  = Gross Profit
  - Operating Expenses (S&M, R&D, G&A)
  = EBITDA
  - D&A, interest, taxes
  = Net Income

Balance Sheet:
  Assets: Cash, AR, Prepaid, PP&E
  Liabilities: AP, Deferred Revenue, Debt
  Equity: Invested capital + Retained earnings

Cash Flow Statement:
  Operating: Net income ± working capital changes
  Investing: CapEx, acquisitions
  Financing: Debt, equity raises, dividends
  = Net change in cash

// For early-stage startups: Income Statement + Cash Flow only.
// Full 3-statement becomes relevant at Series A+.
```

### SaaS Revenue Model (Driver-Based)
```
Monthly Cohort Model Structure:

Inputs (drivers):
  New customers/month:     [Seed value → growth rate]
  Monthly churn rate:      [Constant or improving over time]
  ARPU at signup:          [Constant or with expansion model]
  Expansion rate:          [Monthly % increase for retained customers]
  Gross margin:            [COGS as % of revenue]

Cohort calculation (per month):
  Active customers = Prior active + New customers - Churned customers
  MRR = Active customers × ARPU
  Expansion MRR = Active customers (retained) × ARPU × Expansion rate

Revenue build:
  Month 1: 10 new customers × $79/mo = $790 MRR
  Month 2: 10 new + 9.7 retained (3% churn) × $79 = $1,576 MRR
  Month 3: 10 new + 19.1 retained × $79 = $2,358 MRR
  ...continuing with compounding retained base

// Golden rule: Model revenue bottom-up from cohorts, not as
// "% growth per month." Cohort model is auditable and defensible.
```

---

## 3. Operating Expense Model

### OPEX Categories for SaaS
```
COGS (Direct costs to deliver the product):
  - Hosting/infrastructure (AWS, GCP, Azure)
  - Third-party APIs consumed per customer
  - Customer success (post-sale support)
  - Payment processing fees
  Target: 15-30% of revenue for software

R&D (Product development):
  - Engineering salaries
  - Contractor/freelance development
  - Dev tooling and licenses
  Target: 20-30% of revenue at growth stage

S&M (Sales & Marketing):
  - Paid acquisition (ads, SEO tools)
  - Marketing content and tools
  - Sales team (if applicable)
  - Affiliate/referral costs
  Target: 20-40% of revenue (higher when investing in growth)

G&A (General & Administrative):
  - Founder salary (pay yourself)
  - Legal, accounting, insurance
  - Office/remote tools
  - Admin and back-office
  Target: 10-20% of revenue

// Unit economics target:
// Gross Margin > 70% → COGS < 30%
// CAC Payback < 12mo → S&M < ~40% of first-year revenue per customer
// Operating profitable target: EBITDA > 0% (bootstrap), or
//   Rule of 40: Revenue Growth% + EBITDA% > 40% (venture)
```

---

## 4. Runway & Cash Management

### Runway Calculation
```
Burn Rate (Monthly):
  Gross Burn = Total cash out per month (all expenses)
  Net Burn   = Gross Burn - Revenue collected

Runway:
  Runway (months) = Cash Balance / Net Monthly Burn

Example:
  Cash: $150,000
  Monthly expenses: $18,000
  Monthly revenue: $8,000
  Net burn: $10,000/mo
  Runway: 15 months

// Target: Always maintain 12+ months runway.
// At 6 months: Raise, cut burn, or accelerate revenue — not a time to choose.

Default Alive vs. Default Dead:
  Default Alive: At current burn and growth rate, revenue reaches
                 break-even before cash runs out
  Default Dead:  Cash runs out before break-even at current trajectory

// Paul Graham test: Plot your projected MRR and projected cash simultaneously.
// Do they cross? If not, you are Default Dead and must act.
```

### The Bootstrapper's Cash Rules
```
1. Revenue before expense: Only hire or spend when revenue supports it.
2. Monthly threshold rule:
   Hire when: Role would directly create/protect $3x the salary in annual value.
3. Emergency reserve: Keep 3 months of expenses in a separate account always.
4. Pay yourself: Set a non-zero founder salary from month 1 (even $1,500/mo).
   Reason: Unpaid founders make desperate decisions.

Cash flow accelerators:
  - Annual billing: Collect 12 months upfront → immediate cash injection
  - Retainers/consulting: Bridge revenue while product matures
  - Prepay discounts: Offer 1-3 months free for annual prepay
  - Customer deposits: For implementation projects

Cash flow drains to watch:
  - Deferred revenue timing (ARR collected upfront → recognized monthly)
  - Accounts receivable aging (enterprise customers pay Net 30-60)
  - Contractor timing mismatches
```

---

## 5. Scenario Planning

### Three-Scenario Model
```
Build three explicit models:

Bear Case (survive scenario):
  Assumption: Growth 50% of base case; churn 2x base case
  Question: Does the company survive? At what funding requirement?
  Action: Minimum viable team, minimum viable burn, revenue focus

Base Case (expected scenario):
  Assumption: Current conversion rates, current churn, trend-line growth
  Question: Is this a good business at these assumptions?
  Action: Standard operating plan

Bull Case (outperformance scenario):
  Assumption: Growth 2x base case; churn 50% of base
  Question: What investment would accelerate to here?
  Action: Hiring plan, capex, marketing investment

// Investors know the base case is wrong.
// The bear case shows you're not delusional.
// The bull case shows upside potential.
// Present all three. It signals rigor.
```

### Key Assumption Sensitivity Table
```
Variable               Base    Sensitivity Unit    Revenue Impact
─────────────────────────────────────────────────────────────────
Monthly churn rate     3%      per 1% change       ±$XXK ARR
New customers/month    25      per 5 customer Δ    ±$XXXK ARR
ARPU                   $79     per $10 change       ±$XXK ARR
Expansion rate         2%/mo   per 1% change       ±$XXK ARR
Gross margin           75%     per 5% change       ±$XXK GP

// Build this table explicitly. It shows which levers matter most.
// Usually: Churn > New Customers > ARPU > Expansion > Margin
```

---

## 6. Investor-Ready Financial Metrics

### The Metrics Dashboard (Seed/Series A)
```
Monthly report — 12 metrics every investor wants:

1.  MRR ($) + MoM growth (%)
2.  ARR ($)
3.  Net Revenue Retention (%)
4.  Gross MRR Churn (%)
5.  New MRR added this month ($)
6.  Customers (count + MoM growth)
7.  CAC ($) — trailing 3-month average
8.  LTV:CAC (ratio)
9.  Gross Margin (%)
10. Burn Rate ($ net/month)
11. Runway (months at current burn)
12. Cash Balance ($)

// Format: Metric | Current | Last Month | 3-Month Trend
// Present at every board meeting and monthly investor update.
```

### Financial Projection Format for Pitch
```
Three-year P&L summary:

                   Year 1     Year 2     Year 3
Revenue            $180K      $720K      $2.2M
COGS               ($45K)    ($144K)    ($396K)
Gross Profit       $135K      $576K     $1.80M
Gross Margin       75%        80%        82%

S&M                ($72K)    ($216K)    ($440K)
R&D                ($60K)    ($144K)    ($330K)
G&A                ($30K)     ($72K)    ($110K)
EBITDA            ($27K)      $144K     $924K
EBITDA Margin      -15%       20%        42%

Headcount          2          5          12
MRR (exit)         $25K       $80K       $215K
ARR (exit)         $300K     $960K      $2.58M

Key assumptions: [List every material assumption here]
```

---

## Anti-Patterns

**Anti-Pattern 1: Hockey Stick Without Inflection Explanation**
Financial projections that are flat for 18 months then suddenly explode upward in year 2-3 with no explanation for what causes the inflection. This is the most common pitch deck sin. The model shows a hockey stick; the narrative doesn't explain the blade.
Fix: Every inflection in the model must map to a specific business event: hiring a sales rep, launching a new channel, a platform partnership going live, or a product feature that changes retention. If you can't explain the inflection, remove it from the projection.

**Anti-Pattern 2: Modeling Revenue Without Modeling COGS**
Showing only revenue and headcount in projections while ignoring COGS, hosting costs, customer success costs, and payment processing fees. This produces artificially high margins that collapse when a real accountant reviews them.
Fix: Model COGS as a percentage of revenue from day one. Include: infrastructure (usually 5-15% of revenue for SaaS), third-party API costs (varies wildly for AI products), and direct support cost per customer. If you have AI inference in your product, model token costs explicitly — they can be 20-40% of revenue at early stage.

**Anti-Pattern 3: Single-Scenario Projections**
Building only a base case and presenting it as "the plan." This signals that you haven't stress-tested your assumptions and don't understand the variables that drive your business.
Fix: Build three scenarios explicitly. Use the bear case to identify the minimum viable business and the point at which you must raise, cut burn, or pivot. The discipline of building a bear case is the entire point — it forces you to find the failure modes before they find you.

---

## Quality Gates

- [ ] Revenue model is driver-based (cohort model) not "X% growth per month"
- [ ] All three scenarios modeled: bear, base, bull with explicit assumption differences
- [ ] CAC, LTV, LTV:CAC, CAC payback period explicitly calculated
- [ ] Runway calculated; default alive vs. default dead status explicitly determined
- [ ] COGS modeled as a percentage of revenue (not ignored)
- [ ] Sensitivity table built showing impact of ±1% churn, ±10% new customers, ±$10 ARPU

---

## Failure Modes and Fallbacks

**Failure: Model complexity exceeds ability to explain it**
Detection: Advisor or investor asks "how do you get to $720K year 2?" and the answer requires 10 minutes of tab-by-tab explanation.
Fallback: Rebuild the model with a single-page summary tab. The summary shows the 12 key metrics in three scenarios. All complexity lives in supporting tabs. The presentation layer is always the summary. If you can't explain the model in 3 minutes, it's too complex.

**Failure: AI product COGS blow up unit economics**
Detection: As usage scales, infrastructure and LLM API costs grow faster than revenue. Gross margin compresses below 50%.
Fallback: AI inference cost management: (1) Cache aggressively — repeat queries hit the cache at minimal cost; (2) Right-size models — use the smallest model capable of the task, reserve flagship models only where quality requires it; (3) Batch non-real-time requests at off-peak pricing; (4) Build pricing with usage floors — minimum commit per month means low-usage customers are profitable.

---

## Composability

**Hands off to:**
- `business-plan-architect` — financial model feeds into the pitch deck and investor memo
- `pricing-strategist` — model outputs (LTV, CAC payback) inform pricing decisions

**Receives from:**
- `entrepreneurial-os` — stage context determines which metrics to prioritize
- `market-intelligence` — TAM/SAM data feeds market share projections in the model
