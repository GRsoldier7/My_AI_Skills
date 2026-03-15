---
name: business-plan-architect
description: >
  Genius-level business plan construction engine for founders, investors, and operators. Covers
  executive summary writing, market opportunity sizing (TAM/SAM/SOM), competitive moat analysis
  (7 Powers framework), business model design, financial projections, traction narratives,
  and investor-ready deck structure. Use this skill whenever the user needs to write a business
  plan, pitch deck, investor memo, one-pager, or executive summary. Also trigger for questions
  about how to present a business opportunity, frame a go-to-market strategy for investors,
  model unit economics for a pitch, or structure a narrative around traction data.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: strategy
  adjacent-skills: financial-model-architect, market-intelligence, entrepreneurial-os, go-to-market-engine
  last-reviewed: "2026-03-15"
  review-trigger: "Investor landscape shift, new fundraising format popularized, Y Combinator application format changes"
---

# Business Plan Architect — Savant-Level Skill

## Philosophy

Business plan mastery = **narrative before numbers** (investors fund stories with proof), **BLUF structure** (bottom line up front — your best point in the first sentence), **assumption transparency** (show your work and defend it), and **traction is the only currency that matters** (everything else is storytelling support).

---

## 1. Executive Summary (The Most Important 250 Words)

### BLUF Formula
```
[Company Name] is a [category] for [ICP] that [core value prop].
Unlike [incumbent/alternative], we [key differentiation].
We've achieved [traction proof point] in [timeframe].
We're raising $[amount] to [specific use of funds] to reach [milestone].

Example:
"Helix is a biohacking data platform for self-optimizers that generates
personalized health protocols from bloodwork and supplement data using AI.
Unlike generic wellness apps, we connect lab results, supplement intake,
and biomarker tracking to produce evidence-based protocols, not generic advice.
We have 47 beta users with 89% weekly retention. We're raising $500K to
build the ingestion pipeline and reach 500 paying customers."
```

### What Investors Read (In Order)
```
1. Executive summary (pass/fail filter — 90 seconds)
2. Traction slide (is this real?)
3. Team slide (can they actually do this?)
4. Market size (is it worth my time?)
5. Product (is it real and differentiated?)
6. Financials (do they understand their business?)
7. Everything else
```

---

## 2. Market Opportunity Sizing

### TAM / SAM / SOM Framework
```
TAM (Total Addressable Market):
  - The total global revenue opportunity if you captured 100%
  - Use for: Establishing ceiling, proving space is worth entering
  - Method: Bottom-up (units × price) OR top-down (industry report × %)
  - Target: $1B+ for venture; $50M+ is fine for bootstrap/SMB

SAM (Serviceable Addressable Market):
  - The portion you can realistically reach with your model and geography
  - Use for: Proving you know your customer
  - Should be 1–20% of TAM

SOM (Serviceable Obtainable Market):
  - What you can realistically capture in 3–5 years
  - Use for: Setting credible revenue targets
  - Should be 1–10% of SAM

// Bottom-up sizing example:
"There are 2.3M personal trainers in the US (IBISWorld).
Approximately 400K run independent practices (SAM).
At $79/mo, that's $380M SAM.
We're targeting 5K in year 3 = $47M SOM."

// Red flag: Top-down only with "we only need 1% of a $10B market."
// This is not sizing. It's a math trick. Build bottom-up.
```

### Market Sizing Inputs
```
Primary research signals (most credible):
  - Customer interviews quantifying annual spend on the problem
  - Survey data on willingness to pay
  - Comparable cohorts from similar markets

Secondary research signals:
  - IBISWorld, Statista, Grand View Research (industry reports)
  - LinkedIn Sales Navigator filters (count of ICP companies/roles)
  - Job posting data (demand signal)
  - Keyword search volume × CPC (paid demand proxy)
```

---

## 3. Competitive Moat Analysis (7 Powers Framework)

```
Hamilton Helmer's 7 Powers — the only defensible business advantages:

1. Scale Economies
   Definition: Per-unit costs decrease as volume increases
   Example: AWS — infrastructure cost per GB drops with scale
   Build when: Fixed costs dominate; variable costs minimal

2. Network Effects
   Definition: Product becomes more valuable as more users join
   Example: Slack, WhatsApp, LinkedIn
   Build when: User data or interactions improve the product for others

3. Counter-Positioning
   Definition: New business model incumbents can't copy without damaging themselves
   Example: Netflix vs. Blockbuster (streaming vs. late fees)
   Build when: Your model would cannibalize an incumbent's cash cow

4. Switching Costs
   Definition: Customers face pain/cost/risk when switching away
   Example: Salesforce CRM — years of data, integrations, workflows
   Build when: You can embed in customer workflows or data stores

5. Branding
   Definition: Durable perception that commands premium pricing
   Example: Apple, Patagonia, Porsche
   Build when: Long-term reputation building is feasible; premium market

6. Cornered Resource
   Definition: Preferential access to a valuable resource
   Example: Exclusive data sets, patents, talent pools, licenses
   Build when: Resource is scarce and you can acquire it first

7. Process Power
   Definition: Embedded organizational processes others can't replicate quickly
   Example: Toyota Production System
   Build when: Years of iteration create operational excellence

// For a startup pitch: Identify your primary power + the path to build it.
// Claiming all 7 reads as naive. Focus on 1-2 that are defensible.
```

---

## 4. Business Model Design

### Revenue Model Options
```
Subscription (SaaS):
  MRR × 12 = ARR
  Best for: Recurring value delivery, predictable revenue
  Metrics that matter: Churn, expansion MRR, LTV:CAC

Transactional:
  Revenue = Volume × Take Rate
  Best for: Marketplaces, payment processing, commerce
  Metrics: GMV, take rate, repeat purchase rate

Usage-Based:
  Revenue = Units consumed × Price per unit
  Best for: APIs, cloud infra, AI inference
  Metrics: DAU, API calls, expansion from usage growth

Freemium → Paid:
  Free tier drives acquisition; premium features drive conversion
  Conversion benchmark: 2–5% freemium → paid is healthy
  Metrics: Free-to-paid conversion rate, time to convert

Services → Product:
  Start with high-margin services, productize the repeatable parts
  Best for: Solo founders who can sell before building
  Metrics: Service revenue (bridge), product revenue (destination)

Licensing:
  IP or technology licensed to third parties
  Best for: Research-heavy innovations, enterprise software
```

### Unit Economics Template
```
Customer Acquisition Cost (CAC):
  CAC = Total Sales & Marketing Spend / New Customers Acquired
  Target: CAC Payback < 12 months (< 6 for VC-backable)

Lifetime Value (LTV):
  LTV = ARPU / Monthly Churn Rate
  Or: LTV = ARPU × Average Contract Length × Gross Margin
  Target: LTV:CAC > 3:1 (> 5:1 for great businesses)

Gross Margin:
  GM% = (Revenue - COGS) / Revenue
  SaaS target: 70–85%
  Marketplace target: 40–70%
  Physical product: 30–60%

Payback Period:
  Payback = CAC / (ARPU × Gross Margin)
  < 12 months = venture-fundable
  < 24 months = bootstrappable

// Example unit economics block for pitch:
"CAC: $180 (paid social + content). LTV: $1,080 (18-month avg contract × $60/mo).
LTV:CAC = 6:1. Payback: 4.5 months. Gross margin: 78%."
```

---

## 5. Traction Narrative

### Traction Hierarchy (Most → Least Credible)
```
Tier 1 — Revenue proof:
  - MRR with growth curve (best: consistent month-over-month %)
  - Paying customers with logos (named = more credible)
  - Revenue retention / net revenue retention > 100%

Tier 2 — Strong demand signals:
  - Waitlist with high engagement (email open rate > 50%)
  - LOIs or signed contracts (pre-revenue but binding)
  - Beta users with deep engagement (daily/weekly active, low churn)

Tier 3 — Weak signals (use only if nothing better):
  - Downloads, signups, social followers
  - Inbound media coverage
  - Advisor commitments

// Traction frame: "We went from X to Y in Z days using only channel A,
// and we're seeing [retention metric] which tells us customers are getting value."

// Anti-frame: "We have 10,000 downloads" (meaningless without engagement)
```

### The Traction Slide
```
Show these elements (in this order):
1. MRR graph (last 12 months or since launch)
2. User count + growth rate (if meaningful)
3. Key cohort metric: retention at 30/60/90 days
4. 1-2 customer logos (if enterprise) or NPS (if consumer)
5. One sentence: "This growth came from [channel], which costs us $X to acquire a customer."
```

---

## 6. Investor-Ready Pitch Deck Structure

### 12-Slide Format (Investor Deck)
```
Slide 1:  Title — Company name, tagline, contact
Slide 2:  Problem — The specific pain. Make them feel it.
Slide 3:  Solution — Your product/service. One clear thing.
Slide 4:  Why Now — What changed that makes this possible today?
Slide 5:  Market Size — TAM/SAM/SOM with bottom-up sizing
Slide 6:  Product — Screenshots, demo GIF, or architecture
Slide 7:  Business Model — How you make money, unit economics
Slide 8:  Traction — Revenue/growth graph + key metrics
Slide 9:  Go-to-Market — How you will acquire the next 1,000 customers
Slide 10: Competition — Honest 2×2 matrix or feature table
Slide 11: Team — Why you + why now + relevant credentials
Slide 12: Ask — Amount, use of funds, milestones to be hit
```

### Investor Memo Format (For Deeper Due Diligence)
```
Section 1: Executive Summary (1 page — the BLUF)
Section 2: Problem & Market Opportunity (2 pages)
Section 3: Solution & Product (2 pages)
Section 4: Business Model & Unit Economics (1 page)
Section 5: Traction & Validation (1 page)
Section 6: Go-to-Market Strategy (1 page)
Section 7: Competitive Analysis & Moats (1 page)
Section 8: Team & Advisors (1 page)
Section 9: Financial Projections (3-year model, 1 page)
Section 10: The Ask & Use of Funds (0.5 page)
```

---

## Anti-Patterns

**Anti-Pattern 1: Vanity Metrics as Traction**
Presenting total downloads, social followers, email list size, or press mentions as primary traction indicators. These metrics don't predict revenue or retention. Sophisticated investors know the difference; using them signals naivety.
Fix: Lead with revenue or revenue-predictive metrics: MRR, paying customers, monthly active users with engagement rates, NPS from a real cohort. If you have no revenue, show willingness-to-pay signals: LOIs, waitlist conversion rates, beta retention.

**Anti-Pattern 2: "We Have No Competition" Claim**
Stating you have no competitors. This signals either that you haven't done market research (alarming) or that there is no market (also alarming). Every business has competition — direct, indirect, or the status quo.
Fix: Acknowledge competition honestly. The best competitive slide shows a 2×2 matrix where your company sits in the quadrant no one else occupies. Frame: "Incumbents do X well but fail at Y. We're built to win at Y because [structural reason]."

**Anti-Pattern 3: Bottom-Up Financial Projections With No Driver Logic**
Showing a revenue chart that goes "up and to the right" with no explanation of what drives the growth. Projections without CAC, conversion rates, churn assumptions, and headcount costs are fiction. Investors will ask about every assumption — if you can't defend it, the number is worthless.
Fix: Build the financial model starting from drivers: How many new customers per month? At what CAC? With what churn? What ARPU? What headcount is required to support that? The revenue number falls out of the model — it's not the input.

---

## Quality Gates

- [ ] Executive summary uses BLUF format — best point is in the first sentence
- [ ] TAM/SAM/SOM built bottom-up, not top-down percentage math
- [ ] Primary competitive moat identified from 7 Powers framework
- [ ] Unit economics block present: CAC, LTV, LTV:CAC, payback, gross margin
- [ ] Traction slide leads with revenue or revenue-predictive metric (not downloads/followers)
- [ ] Financial projections are driver-based with explicit assumptions for every input

---

## Failure Modes and Fallbacks

**Failure: Business plan written for the wrong audience**
Detection: Investor feedback is "too detailed/technical" (written for operators) or "not enough substance" (written for consumers). Wrong tone, wrong depth.
Fallback: Identify the reader first. Seed investor memo vs. bank loan vs. accelerator application vs. internal planning doc each have different formats, metrics, and depths. Rewrite with the reader's decision criteria explicit at the top of the document.

**Failure: Financial projections rejected as unrealistic**
Detection: Investors or advisors push back hard on growth assumptions. "How do you go from $0 to $5M in year 2?"
Fallback: Build the model backwards from the milestone. If $5M requires X customers at Y ARPU, that requires Z new customers/month, which requires A in marketing spend and B conversion rate. Show the chain. If any link is implausible, adjust the projection to what the model can support. A slower, believable projection beats an aggressive, indefensible one.

---

## Composability

**Hands off to:**
- `financial-model-architect` — for detailed 3-statement financial model and scenario planning
- `market-intelligence` — for deep competitive research and TAM validation
- `go-to-market-engine` — for the GTM section of the business plan

**Receives from:**
- `entrepreneurial-os` — stage context determines which sections need depth
- `business-genius` — top-level orchestrator that routes business planning requests here
