---
name: startup-tax-strategist
description: |
  Expert tax strategist for business founders, solo entrepreneurs, and consultants. Use when
  you have questions about business taxes, self-employment tax, entity structure, deductions,
  quarterly estimated payments, S-corp election, LLC taxation, business startup costs,
  home office deduction, equipment/tech deductions, contractor vs employee classification,
  bookkeeping for taxes, or how to minimize your tax burden legally as a business owner.
  Trigger on: "business taxes", "tax strategy", "self-employment tax", "quarterly estimates",
  "LLC vs S-corp", "business deductions", "can I deduct", "home office deduction", "1099",
  "contractor taxes", "startup tax", "what can I write off", "tax planning", "CPA question",
  "business entity for taxes", "how to pay myself", "owner's draw vs salary", "SE tax",
  "estimated taxes", "tax efficient", "business expense", "depreciation", "Section 179",
  "QBI deduction", "pass-through taxation", "fiscal year", "payroll taxes".
  Also trigger when the user describes their business setup and asks how to structure it
  for minimal tax liability. Works for consultants, solo founders, SaaS builders, and
  freelancers — not for large corporations or international tax law.
  IMPORTANT: Always recommend verifying strategy with a licensed CPA or tax attorney
  before implementation. This skill provides frameworks and education, not legal tax advice.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: legal-financial
  adjacent-skills: financial-model-architect, entrepreneurial-os, business-plan-architect, micro-saas-builder
  last-reviewed: "2026-03-21"
  review-trigger: "Annual tax law changes (review each January), IRS rule changes, user reports outdated info"
  capability-assumptions:
    - "Tax guidance based on US federal law as of training cutoff August 2025"
    - "State tax rules not covered — US federal only"
    - "No external tools required — text guidance only"
  fallback-patterns:
    - "If question involves state taxes: flag and recommend state-specific CPA"
    - "If question post-dates August 2025: flag knowledge cutoff, recommend IRS.gov verification"
    - "Always: recommend CPA/tax attorney verification before implementation"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: business structure description, income situation, or specific tax question
- Output produces: tax strategy framework, entity analysis, deduction checklist, or planning roadmap
- Can chain from: entrepreneurial-os (stage gates → tax structure decision), business-plan-architect
- Can chain into: financial-model-architect (tax assumptions → financial model)
- Orchestrator notes: always flag CPA verification requirement in output

## Constitutional Constraints
- Never present tax strategies as guaranteed outcomes or legal tax advice
- Always include: "Verify with a licensed CPA or tax attorney before implementing any strategy here"
- Never recommend illegal tax avoidance — only legal tax minimization
- Flag when a question exceeds the scope of general tax education (e.g., international, estate, complex M&A)
- Be explicit about the tax year these strategies apply to (2025/2026 as of this writing)

---

## Entity Structure Decision Framework

### The Core Question: How Should Your Business Be Taxed?

| Entity | Taxation | SE Tax | Best For |
|--------|---------|--------|---------|
| Sole Proprietor | Pass-through (Schedule C) | Full 15.3% on all profit | Side hustle / pre-revenue |
| Single-Member LLC | Same as sole prop by default | Full 15.3% on all profit | Liability protection, same tax |
| Multi-Member LLC | Partnership (Form 1065) | Full 15.3% on all profit | Multiple founders |
| LLC taxed as S-Corp | Pass-through (Form 1120-S) | Only on "reasonable salary" | Profit > ~$50K/year |
| C-Corp | Double taxation (entity + dividend) | N/A (W-2 employee) | VC funding, retained earnings play |

### The S-Corp Sweet Spot

An S-Corp election (via Form 2553) is often the highest-leverage tax move for a solo consultant
or founder once annual profit consistently exceeds ~$50,000-60,000.

**How it works:**
- You pay yourself a "reasonable salary" (subject to payroll taxes — FICA/SECA)
- Remaining profit flows through as a distribution (NOT subject to self-employment tax)
- Savings: 15.3% SE tax avoided on the distribution portion

**Example:**
- Profit: $120,000
- Reasonable salary: $60,000 (subject to payroll taxes ~$9,180 employer + employee)
- Distribution: $60,000 (no SE tax — saves ~$9,180 vs sole prop)
- Net annual savings: ~$8,000-9,000 (offset by payroll setup costs of ~$1,500-2,500/year)

**Cautions:**
- IRS scrutinizes "reasonable salary" — it must reflect market rate for your role
- Requires payroll setup (Gusto, QuickBooks Payroll, etc.) — adds cost and complexity
- Not worth it below ~$50K profit; sweet spot is $70K-$500K net income
- Requires Form 2553 filing within deadline (75 days of entity formation or tax year start)

---

## Key Deduction Categories for Founders and Consultants

### Home Office Deduction
Two methods — choose the one that gives the larger deduction:

**Simplified method:** $5 per square foot, max 300 sq ft = max $1,500/year. Easy but capped.

**Actual expense method:** Calculate % of home used exclusively for business:
(Office sq ft / Total home sq ft) × home expenses (mortgage interest/rent, utilities,
insurance, repairs, depreciation) = deductible amount. More work, often larger deduction.

**Requirements:** The space must be used *regularly and exclusively* for business.
A desk in your bedroom doesn't qualify. A dedicated office does.

### Technology and Equipment
- Computers, monitors, tablets, phones (business use %) — fully deductible
- Software subscriptions (Claude Code, Cursor, GitHub, n8n, Notion, etc.) — fully deductible
- SaaS tools used for business — fully deductible
- **Section 179:** Deduct full cost of qualifying equipment in the year of purchase (vs. depreciation over years). Applies to computers, office furniture, equipment.
- **Bonus Depreciation:** 100% first-year deduction for eligible property (phase-down began 2023 — verify current year %)

### Vehicle
- **Actual expense method:** Track all car expenses × business use percentage
- **Standard mileage rate:** IRS-published rate per business mile (67 cents/mile in 2024 — verify current)
- Keep a mileage log — IRS requires documentation

### Health Insurance Premiums
Self-employed individuals can deduct 100% of health insurance premiums paid for themselves
and family as an above-the-line deduction (Schedule 1, not Schedule C). This directly reduces
AGI. One of the most valuable deductions available to founders.

### Retirement Contributions
- **SEP-IRA:** Up to 25% of net self-employment income, max $69,000 (2024). Simple to set up.
- **Solo 401(k):** Employee contributions up to $23,000 ($30,500 if 50+) PLUS employer contributions up to 25% of compensation. Higher ceiling than SEP-IRA if maxing employee contribution.
- **SIMPLE IRA:** Available for small businesses with employees
- Retirement contributions reduce taxable income dollar-for-dollar. This is among the most powerful tools available.

### Business Meals
50% deductible when there is a genuine business purpose and you document: who, what, where, why.
Keep receipts and notes. Business entertainment (sporting events, concerts) is no longer deductible.

### Professional Development
Courses, books, conferences, coaching, and subscriptions directly related to maintaining or
improving your current business skills — fully deductible.

### QBI Deduction (Section 199A)
Qualified Business Income deduction: up to 20% of qualified business income for pass-through
entities (sole props, LLCs, S-corps, partnerships). Subject to income limits and restrictions
for certain "specified service trades or businesses" (SSTBs). Consult a CPA for eligibility.

---

## Quarterly Estimated Tax Payments

Self-employed individuals must pay taxes quarterly (IRS does not withhold from self-employment).

**Safe harbor rule:** Pay 100% of prior year's tax liability (110% if prior year AGI > $150K)
OR 90% of current year's actual liability — whichever is smaller. This avoids underpayment penalties.

**Due dates (approximate — verify annually):**
- Q1: April 15
- Q2: June 15
- Q3: September 15
- Q4: January 15 (following year)

**Calculation approach:**
1. Estimate annual gross revenue
2. Subtract business deductions → estimated net profit
3. Calculate SE tax (15.3% on 92.35% of net profit)
4. Calculate income tax on (net profit - half of SE tax - QBI deduction - other deductions)
5. Add SE tax + income tax = total estimated annual tax
6. Divide by 4 → quarterly payment

**Tools:** IRS Form 1040-ES, or use tax software (TurboTax Self-Employed, TaxAct, or your CPA's system)

---

## Startup Cost Deductions

Business startup costs can be deducted:
- **First $5,000** of startup costs deducted in year of business launch
- **First $5,000** of organizational costs (LLC/corp formation fees)
- Remaining costs amortized over 180 months (15 years)

Startup costs include: market research, legal fees for entity formation, initial advertising,
travel to investigate the business, training before opening.

---

## Bookkeeping Minimum for Tax Readiness

You need at minimum:
1. **Separate business bank account and credit card** — never mix personal and business funds
2. **Accounting software** — QuickBooks Self-Employed, Wave (free), or FreshBooks
3. **Receipt capture** — Dext, Hubdoc, or just a dedicated email folder + monthly folder in Google Drive
4. **Mileage log** — MileIQ, TripLog, or a simple spreadsheet
5. **Quarterly reconciliation** — match books to bank statements every quarter, not just at tax time

---

## Tax Planning Calendar (Founder Edition)

| Month | Action |
|-------|--------|
| January | Prior year bookkeeping close; gather 1099s; review entity structure |
| February-March | Work with CPA on prior year return; plan current year strategy |
| April | File/extend prior year return; Q1 estimated payment due |
| June | Q2 estimated payment due; mid-year profit check |
| September | Q3 estimated payment due; year-end planning begins |
| October-November | Max out retirement contributions; accelerate deductions if profitable year |
| December | Final year-end moves (equipment purchases, prepay expenses, delay income if possible) |
| January 15 | Q4 estimated payment due |

---

## Self-Evaluation (run before presenting output)

Before presenting, silently check:
[ ] Is the CPA/tax attorney verification disclaimer present?
[ ] Are all strategies legal tax minimization — not tax evasion?
[ ] Are dollar figures labeled as approximate / subject to current IRS rules?
[ ] Is the advice calibrated to the user's business stage and income level?
[ ] Are the most high-leverage moves presented first (entity structure, retirement, health insurance)?
If any check fails, revise before presenting.

---

## Read references/ for:
- Extended S-Corp vs LLC comparison scenarios
- State tax considerations by state (coming soon)
- Contractor vs employee classification guide (1099 vs W-2)
- Consulting business deduction checklist (print-and-use)
