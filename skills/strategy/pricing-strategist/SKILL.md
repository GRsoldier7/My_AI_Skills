---
name: pricing-strategist
description: >
  Genius-level pricing strategy covering value-based pricing methodology, packaging psychology,
  SaaS pricing models, willingness-to-pay research, the $100M Offers value equation, price
  increase playbooks, and competitive pricing analysis. Use this skill whenever the user asks
  about how to price their product or service, how to structure pricing tiers, whether to charge
  more, how to test prices, packaging strategy, freemium vs paid, usage-based vs subscription
  pricing, or why customers are churning due to price. Also trigger for annual vs monthly billing,
  price anchoring, decoy pricing, discount policy, and enterprise pricing strategy.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: strategy
  adjacent-skills: financial-model-architect, go-to-market-engine, business-plan-architect, micro-saas-builder
  last-reviewed: "2026-03-15"
  review-trigger: "Major SaaS pricing shift, new pricing model popularized (usage-based surge), inflation impact on B2B pricing"
---

# Pricing Strategist — Savant-Level Skill

## Philosophy

Pricing mastery = **value-based, not cost-plus** (charge what it's worth, not what it cost), **packaging as product** (good packaging sells itself), **price as positioning** (cheap = low quality in buyers' minds), and **test before optimizing** (your intuition about price is almost always wrong).

---

## 1. The Value Equation ($100M Offers Framework)

### Alex Hormozi's Value Equation
```
Value = (Dream Outcome × Perceived Likelihood of Achievement)
        ÷ (Time Delay × Effort and Sacrifice)

To increase perceived value:
  ↑ Dream Outcome:     Make the result feel bigger, more transformative
  ↑ Likelihood:        Show proof (testimonials, guarantees, case studies)
  ↓ Time Delay:        Speed up time-to-value (onboarding, quick wins)
  ↓ Effort/Sacrifice:  Reduce friction, automate work, done-for-you elements

Example applications:
  "Save 10 hours/week" > "Streamline your workflow"     (↑ Dream + ↓ Effort)
  "Get results in 48h" > "See results quickly"          (↓ Time Delay)
  "Or your money back" > implied faith in product       (↑ Likelihood)
  "We do it for you" > "Easy to use"                    (↓ Effort)
```

### Willingness-to-Pay (WTP) Research
```
Methods (by validity):

1. Van Westendorp Price Sensitivity Meter (most rigorous):
   Ask 4 questions to identify acceptable price range:
   Q1: "At what price would this seem too cheap to be quality?"
   Q2: "At what price would this seem expensive but still acceptable?"
   Q3: "At what price would this feel like a bargain?"
   Q4: "At what price would this be too expensive to consider?"
   Output: Acceptable price range (overlap of Q1-Q2 and Q3-Q4)

2. Direct Ask (best for B2B):
   Customer interview: "If this solved X for you, what would you expect to pay?"
   Follow-up: "Would you pay $[50% more]?" → observe reaction
   Target: Get 20+ responses before drawing conclusions

3. Competitor Benchmarking:
   Map every competitor's pricing page
   Identify: floor (cheapest option), ceiling (most expensive used)
   Position: at 1.2-2x if you have differentiation; at parity if not

4. A/B Price Test:
   Show different prices to different user cohorts
   Measure: Conversion rate AND revenue per visitor (not just conversion)
   Minimum: 100 conversions per variant before declaring winner
```

---

## 2. SaaS Pricing Models

### Model Comparison
```
Per-Seat (User) Pricing:
  Revenue = Seats × Price per seat
  Best for: Collaboration tools, project management
  Examples: Slack, Notion, Figma
  Pros: Scales with org growth (land-and-expand)
  Cons: Customers minimize seats; usage doesn't correlate with value

Flat-Rate Subscription:
  Revenue = Fixed fee per period
  Best for: Broad value delivery, unlimited usage products
  Examples: Basecamp, many media subscriptions
  Pros: Simple to sell and predict; customers love unlimited
  Cons: Heavy users subsidized by light users; leaves money on table

Usage-Based (UBP):
  Revenue = Units consumed × Rate
  Best for: APIs, AI inference, data processing, cloud infra
  Examples: Stripe (0.3%+), OpenAI ($0.002/1K tokens), Twilio
  Pros: Low barrier to entry; scales with customer success
  Cons: Unpredictable revenue; customers optimize to reduce spend

Hybrid (Base + Usage):
  Revenue = Base subscription + overage charges
  Best for: Mature products with predictable base + variable spikes
  Examples: Most modern SaaS (HubSpot, Salesforce)
  Pros: Predictable base + upside on power users
  Cons: Complex to communicate; billing surprises cause churn

Outcome-Based:
  Revenue = % of value generated or results achieved
  Best for: Professional services, performance marketing, HR tech
  Examples: Percentage of salary for recruiting platforms
  Pros: Perfectly aligned incentives
  Cons: Hard to measure; customers dispute attribution

// 2026 recommendation: Usage-based with commitment discounts
// (annual commitment at seat/usage floor → discounts → no ceiling)
// The model that's eating pure per-seat and pure flat-rate.
```

---

## 3. Packaging Psychology

### The Three-Tier Framework
```
Structure:
  Starter  → Entry point. Removes risk. Captures hesitant buyers.
  Pro      → Your real product. Best value at target margin.
  Business → Upsell/enterprise. Higher ARPU. White-glove framing.

Pricing anchors:
  - Business tier anchors Pro as the "reasonable" choice
  - Pro should be ~3-4x Starter (not 2x — too close reduces upgrades)
  - Business should be 3-5x Pro for enterprise positioning

Feature allocation rules:
  - Core value: available in ALL tiers (proves it works)
  - Collaboration: Pro and above (team adoption drives expansion)
  - Admin/security/compliance: Business tier (enterprise buyers need these)
  - API/integrations: Pro or above (power users, retention)
  - Support: Level up with tier (chat → priority → dedicated CSM)

// Rule: The feature that makes you "must-have" should NOT be gated
// behind a paid tier. Let them experience the aha moment first.
```

### Decoy Pricing
```
Classic decoy effect:
  Option A: Small $5 (digital only)
  Option B: Large $10 (digital + physical) ← TARGET
  Decoy C:  Physical only $10 (same price as B, less value)
  → C makes B feel like obvious value; B conversion jumps 20-40%

Applied to SaaS tiers:
  Starter: $29/mo — 1 user, 3 projects
  Pro: $79/mo — 5 users, unlimited projects ← TARGET
  Pro+: $75/mo — 5 users, 10 projects (decoy — same price, less value)
  → Decoy makes $79 Pro look obviously better

// Use annual pricing with monthly equivalent display:
  "Save 20% with annual → $63/mo billed $756/yr"
  Always show monthly equivalent. $63 feels less than $756.
```

### Price Anchoring Patterns
```
1. Show the "before" price prominently:
   ~~$149/mo~~  $79/mo (first 3 months)
   → Anchors on $149; $79 feels like a deal

2. ROI anchoring:
   "This saves 8 hours/week. At $50/hr, that's $1,600/month saved.
   We charge $149/mo. You keep $1,451/month in value."

3. Per-unit anchoring:
   $79/mo = "$2.63/day — less than a coffee"
   (Especially effective for consumer products)

4. Competitor anchoring:
   "Salesforce charges $300/seat. We charge $79/seat with [X advantage]."
```

---

## 4. Price Increase Playbook

### When to Raise Prices
```
Strong signals to raise prices immediately:
  □ Closing >70% of deals without price negotiation
  □ Churn is low (<3%/mo) even among lower-tier customers
  □ New competitor with similar product charges 50% more
  □ Customers proactively cite "best value" in NPS comments
  □ CAC payback < 3 months (leaving money on the table)
  □ WTP research shows average WTP 40%+ above current price

// Rule of thumb: If you're not losing 20% of deals on price, you're too cheap.
```

### How to Raise Prices Without Losing Customers
```
Strategy: Grandfather-New Pricing

1. Raise prices for all new customers immediately (no announcement)
2. Notify existing customers 60 days before their price changes:
   "We're updating our pricing on [DATE]. As a loyal customer since
   [DATE], you'll be grandfathered at your current rate until [90 days].
   After that, your new rate will be $X (up from $Y)."
3. Offer annual lock-in at current rate:
   "Lock in your current price for 12 months by switching to annual billing."
4. Measure: Track churn at the 90-day mark. If <5% additional churn, success.

// Typical outcome: 80-90% of customers stay. Annual revenue jumps immediately.
// The customers you lose are usually the lowest-tier, highest-support users.
```

### B2B Enterprise Pricing
```
Enterprise pricing is NOT listed publicly. Why:
  - Deal size varies 10-100x by org size
  - Procurement requires custom contracts
  - Price anchoring works against you in enterprise (anchors low)
  - Legal and security requirements drive custom scope

Enterprise pricing approach:
  1. Discovery call: Understand org size, use case, and budget signals
  2. ROI framing: Build a business case in the customer's language
  3. Champion coaching: Give internal champion the math to sell to their boss
  4. Quote custom: Annual commitment, multi-year option, volume discount
  5. Negotiate on scope, not on price: Add features before reducing price

// Champion's ROI template:
"If [product] saves each of your 50 engineers 2 hours/week,
at a blended rate of $120/hr, that's $624K/year recovered.
Our proposal is $180K/year — a 3.5:1 ROI in year 1."
```

---

## 5. Discount Policy

### Discount Rules
```
Never offer discounts proactively. Only respond to explicit requests.

Acceptable discount scenarios:
  1. Annual prepay: 15-20% off. Improves cash flow. Fair trade.
  2. Non-profit / startup: 30-50% off. Goodwill + future upgrade.
  3. Volume: 10% per 10-seat increment, max 30% off.
  4. Pilot/POC: 60-day reduced rate to prove value before full commit.

Unacceptable discount scenarios:
  1. "Can you do better?" with no justification → Hold the price.
  2. Discounting to close a deal before quarter end → Trains bad behavior.
  3. Matching a competitor's lower price on the spot → Re-anchor on value.

// Pushback script for price objections:
"I understand price is a consideration. Help me understand —
is it that the price exceeds your budget, or is it that you're
not yet sure the value justifies the investment? Because those
have different solutions."
```

---

## Anti-Patterns

**Anti-Pattern 1: Cost-Plus Pricing**
Calculating cost to deliver the product and adding a percentage markup. This is factory thinking applied to software and services. Your cost to serve has no relationship to the value you create. A tool that saves a customer $10K/year is worth $1K/year regardless of whether it cost $50 or $5,000 to build.
Fix: Start with WTP research. Find out the value your product delivers in customer terms (time saved, revenue generated, risk reduced). Price at 10-30% of that value. Your cost is a floor, not a ceiling.

**Anti-Pattern 2: Too Many Tiers**
Offering 5-7 pricing tiers plus add-ons and custom bundles. Choice paralysis is real — more options reduce conversion. B2B buyers who see 7 tiers experience anxiety about picking wrong; many leave without buying.
Fix: 3 tiers maximum for self-serve. 4 if enterprise is a distinct motion. Each tier must have a clearly defined ICP so the buyer self-selects without help. If you can't describe the customer for each tier in one sentence, you have too many tiers.

**Anti-Pattern 3: Permanent Discounts as Default**
Always being "on sale" or having a lifetime deal running continuously. Permanent discounts train customers to wait for deals, devalue your product, and create two customer classes (LTD customers who paid $49 one-time and monthly customers paying $49/month) that require different support at different cost-to-serve.
Fix: Discounts are events, not states. Run limited-time promotions with hard end dates. Lifetime deals, if used for launch, should have a hard cap (first 200 customers) and never be repeated. Price the product for the long term from day one.

---

## Quality Gates

- [ ] Pricing is value-based: WTP research conducted or competitor benchmarking done before setting price
- [ ] Value equation audit: Dream outcome, likelihood, time delay, and effort are explicitly framed in pricing page copy
- [ ] Three-tier maximum with clear ICP for each tier (or explicit reason for more)
- [ ] Annual discount offered and incentivized (15-20% off, prominently displayed)
- [ ] Discount policy documented: what's acceptable, what's not, what sales can offer without approval
- [ ] Price increase protocol ready: 60-day notice, grandfather option, annual lock-in offer

---

## Failure Modes and Fallbacks

**Failure: High-traffic pricing page with low conversion**
Detection: Pricing page analytics show high scroll depth but low "start trial" / "buy" clicks. Session recordings show hesitation, back-navigation, or FAQ clicks on pricing.
Fallback: Run Van Westendorp survey on existing trial users. Add comparison table (vs. competitor). Add testimonials near CTA. Reduce the number of tiers. Add money-back guarantee or free trial (reduces risk). A/B test: same product at 20% lower price to quantify price elasticity.

**Failure: Enterprise deals stalling at procurement**
Detection: Champion says "yes" but deal goes dark after being sent to procurement. Months pass. No decision.
Fallback: Enterprise deals stall for three reasons: budget not pre-approved, security/legal blockers, or missing executive sponsor. Solution: Ask champion who controls the budget, what the security review process looks like, and who the executive champion needs to be. Provide a security overview doc, a standard MSA, and a business case template for the champion to present internally.

---

## Composability

**Hands off to:**
- `financial-model-architect` — when price changes need to be modeled for revenue impact
- `go-to-market-engine` — pricing is a GTM lever; coordinate with launch sequencing
- `copywriting-conversion` — pricing page copy must translate value equation into conversion

**Receives from:**
- `market-intelligence` — competitor pricing data and market positioning inform price setting
- `business-genius` — orchestrator routes pricing questions here for full-framework analysis
