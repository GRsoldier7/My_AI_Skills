---
name: micro-saas-builder
description: >
  Genius-level micro-SaaS development covering niche identification, validation before
  building, MVP scoping, tech stack selection for speed, distribution strategy, pricing
  and packaging, the path from $0 to $10K MRR, churn reduction, and exit options. Use
  this skill whenever the user wants to build a SaaS product, is evaluating SaaS ideas,
  wants to validate before coding, needs to scope an MVP, is choosing a tech stack for a
  small product, wants to productize an existing workflow or service, or is trying to grow
  a solo SaaS from early revenue to sustainable income. Also trigger for micro-SaaS
  acquisition, no-code SaaS tools, SaaS bootstrapping vs fundraising decisions.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: product
  adjacent-skills: entrepreneurial-os, go-to-market-engine, pricing-strategist, growth-hacking-engine, cloud-migration-playbook
  last-reviewed: "2026-03-15"
  review-trigger: "New no-code platform changes build economics, AI coding tools change solo developer capacity, major SaaS acquisition market shift"
---

# Micro-SaaS Builder — Savant-Level Skill

## Philosophy

Micro-SaaS mastery = **niche relentlessly** (a $5M TAM owned fully beats a $5B TAM owned at 0.001%), **validate payment before code** (get $1 before writing a line), **distribution first, product second** (the best product with no distribution is a hobby), and **boring is beautiful** (the most profitable SaaS businesses are the least exciting ones).

---

## 1. Niche Identification Framework

### The Micro-SaaS Niche Matrix
```
Profitable micro-SaaS characteristics:
  ✅ Clear, specific pain (not a "nice to have")
  ✅ Audience that pays (existing budget for this category)
  ✅ Small enough to dominate (TAM $1M-$50M, you can be the best)
  ✅ Underserved (large players don't bother; small pain for them, huge for niche)
  ✅ Recurring need (problem doesn't go away)
  ✅ You have unfair insight (domain expertise, community access, lived experience)

Niche identification sources:
  1. Reddit goldmine: Search r/entrepreneur, r/SaaS, r/software for "I wish there was..."
  2. App store reviews: Read 1-star reviews of category leaders. What do they miss?
  3. Your own workflow: What do YOU manually do that software doesn't solve?
  4. Job postings: What skills does your ICP hire for? Can you automate that job?
  5. Adjacent to known: What does [existing tool] NOT do? Build the add-on.
  6. Community pain: What question gets asked 10x/week in your niche community?

Evaluation scorecard (score each idea 1-5):
  Pain severity:          Is this a vitamin (nice) or painkiller (must-have)?
  Willingness to pay:     Evidence of paying for solutions in this category?
  Market size:            $1M-$50M SAM (enough to matter; not too big)
  Competition:            Some competition (validates market); not dominated
  Founder fit:            Do you understand this customer deeply?
  Distribution access:    Can you reach this customer cheaply?
  ─────────────────────────────────────────
  Composite score:        ≥20/30 = green light to validate
```

### Niche Examples by Approach
```
Vertical SaaS (serve a specific industry):
  "Project management for tattoo studios"
  "Client portal for solo accountants"
  "Inventory management for food trucks"
  → Take a horizontal tool (ClickUp, HubSpot) and build the vertical-specific version

Workflow automation SaaS (automate a manual process):
  "Auto-populate reports from Google Sheets to PDF and email"
  "Sync customer feedback from Zendesk to Notion automatically"
  → The process is known; the automation is the product

Integration SaaS (connect two things that don't talk):
  "Sync Shopify orders to Airtable"
  "Pull Stripe MRR metrics into Notion"
  → Glue products. Simple to build; huge demand.

API wrapper SaaS (add UX to a complex API):
  "Simple email address verification for non-developers" (wraps ZeroBounce API)
  → Makes something powerful accessible to a less technical audience
```

---

## 2. Validation Before Code

### The $1 Test
```
Goal: Get one person to commit money before you build the full product.

Step 1: Landing page (2-3 hours to build)
  - One clear problem + one clear solution
  - Price and "Join Waitlist" or "Early Access: $X"
  - Use: Carrd ($19/yr), Framer, or Webflow

Step 2: Traffic (48 hours)
  - Post in 3 communities where your ICP hangs out
  - LinkedIn/Twitter post about the problem (not the product)
  - Cold email 20 ICP contacts with the link and a personal note

Step 3: Interpret results
  If 0 sign-ups from 100 visits: Problem framing or wrong audience. Iterate.
  If sign-ups but 0 payments: Value prop not compelling. Iterate.
  If 1+ payment on pre-launch: Green light. Build the MVP.

// Rule: Don't build until you have 3 paying customers or 50+ email sign-ups
// AND at least 3 interviews confirming they'd pay.
```

### The Concierge MVP
```
Concierge: Manually do the thing the software will eventually do.
Works for: Any product that transforms inputs → outputs

Example: "AI-generated market research reports for consultants"
  Instead of building the AI tool:
  → Offer "done for you" market research for $297
  → If 5 people pay, the demand is validated
  → Use the payments to fund building the automated version
  → Then migrate manual customers to the product

Benefits:
  - Zero code, zero risk
  - Learn the exact inputs/outputs customers need
  - Pays for itself (you earn while validating)
  - Customers become first product users

When it doesn't work: Products that need to be automated from day 1 to be useful (real-time alerts, background sync, etc.)
```

---

## 3. MVP Scoping

### MVP Definition (Real MVP, Not CRUDware)
```
MVP = The minimum product that creates the aha moment for your ICP.

MVP definition process:
  1. Identify the core job: What ONE thing does the customer hire this for?
  2. Remove everything not in the critical path to the aha moment
  3. For everything remaining: Can we delay or simplify?

The test:
  "If we shipped only [this thing], would customers pay and stay?"
  If yes → That's your MVP
  If no → You need to add [missing piece] to reach aha moment

Common MVP over-scoping:
  ❌ Built-in analytics (use third-party for v1)
  ❌ Team collaboration features (single user first)
  ❌ Multiple export formats (one format first)
  ❌ Admin panel (manage via database for first 10 customers)
  ❌ Custom branding/white label (add at month 3)

MVP minimum to ship:
  ✅ Core workflow: Input → Process → Output that delivers the job
  ✅ Account creation + auth (even just email/password; SSO is v2)
  ✅ Basic billing (Stripe checkout; no pricing tiers yet)
  ✅ One channel for support (email or Intercom widget)
```

### Tech Stack Choices for Speed (Solo Founder)
```
SaaS starter stack (2025):
  Frontend:   Next.js (React) with Tailwind CSS + shadcn/ui
  Backend:    Next.js API routes (simple) OR FastAPI (Python if ML involved)
  Database:   Supabase (Postgres + auth + storage + realtime in one)
  Auth:       Clerk or Supabase Auth (never build custom auth for v1)
  Payments:   Lemon Squeezy (simpler than Stripe; handles EU VAT)
              OR Stripe Billing (more powerful, more setup)
  Deployment: Vercel (frontend) + Railway or Render (backend)
  AI/LLM:     Anthropic SDK / OpenAI SDK (direct) or Vercel AI SDK

No-code SaaS stack (for non-developers):
  UI:         Bubble or WeWeb
  Backend:    Xano or Supabase
  Auth:       Clerk
  Automations: Zapier or Make
  Payments:   Lemon Squeezy
  AI:         Make + Claude API (via webhook)

Rule: If it's been done before, use a tool. Build only your unique core.
If auth took 2 weeks, that's 2 weeks not building the core product.
```

---

## 4. From $0 to $10K MRR

### The Growth Stages
```
$0 → $1K MRR (Survival → First 12 customers):
  Focus: Find the customer who LOVES it.
  Method: Manual outreach to everyone who might benefit.
         Do not market broadly. Find the 12 people individually.
  Spend: $0 on paid acquisition. Time only.
  Learn: Why did they buy? What do they do in the product?
         What would make them cancel? What would they tell their peers?

$1K → $3K MRR (12 → 35 customers):
  Focus: Make the product easy to discover.
  Method: Write about the problem your product solves.
         Post in communities where customers hang out.
         Launch on Product Hunt and relevant directories.
  Learn: What's your primary acquisition channel at zero cost?

$3K → $10K MRR (35 → 120 customers):
  Focus: Scale the working channel.
  Method: If content is working → invest in more content.
         If referrals work → launch a formal referral program.
         If outbound works → build a systematic outreach cadence.
  Spend: Invest 20% of MRR back into the working channel.
  Hire: First contractor hire (support or content) at ~$5K MRR.

$10K MRR → sustainability:
  Focus: Fix churn before scaling acquisition.
  Method: Analyze churn cohorts. What makes customers stay 12+ months?
         What causes churn in month 3-6? Fix the pattern.
```

### Launch Checklist for Micro-SaaS
```
Pre-launch (2 weeks before):
  [ ] Landing page with clear value prop and early-bird pricing
  [ ] Email waitlist collecting (target: 200+ before launch)
  [ ] 3 beta customers running the product for feedback
  [ ] Product Hunt scheduled (Tuesday-Thursday, 12:01 AM PT)
  [ ] 3 communities identified to post in on launch day

Launch day:
  [ ] Post on Product Hunt
  [ ] Share in 3 communities (personal tone, not press release)
  [ ] Email waitlist
  [ ] Personal DM to 20 network contacts who match ICP
  [ ] Monitor all channels and respond within 1 hour

Post-launch:
  [ ] Follow up personally with every trial user in first 48h
  [ ] Fix the top 3 friction points from first-user feedback
  [ ] Document what drove traffic (for future launches)
```

---

## 5. Churn Prevention

### Churn Root Cause Analysis
```
Churn reasons by frequency (typical SaaS):
  1. Product doesn't solve the problem well enough (40%)
  2. Found a better alternative (20%)
  3. Business circumstance changed (15%) — budget cuts, company closed
  4. Didn't achieve the expected outcome (15%)
  5. Bad support experience (10%)

Actions:
  Reasons 1 + 4: Product/onboarding problem. Fix the aha moment path.
  Reason 2: Competitive analysis. What does the competitor do better?
  Reason 3: Target less fragile customers. Avoid pre-revenue startups if you can.
  Reason 5: Improve support response time and quality.

Churn interview template:
  "Before you go, can I ask you 2 questions? What led to your decision to cancel?
   And what would have had to be different for you to stay?"
  → 40-60% of churned users will respond if asked personally (not via survey).
```

---

## Anti-Patterns

**Anti-Pattern 1: Scope Creep Before Revenue**
Adding features before the core works. Building team features, API access, advanced analytics, and integrations before a single customer has paid. This delays launch by months and delivers a complex product to a market that hasn't validated the core value.
Fix: Ruthlessly cut scope. Define the one thing the product must do to create the aha moment. Ship only that. Add features only when customers ask for them specifically — and only when 3+ customers request the same feature.

**Anti-Pattern 2: Building in Secret**
Spending 6 months building before talking to a single potential customer. The product is launched, no one buys, and the builder discovers the problem they solved wasn't important enough.
Fix: The Concierge MVP approach. Build nothing for the first 30 days — just talk to potential customers and manually do the work. When you have 3 paying customers for the manual service, you've validated. Start building.

**Anti-Pattern 3: Underpricing Forever**
Launching at $9/mo or $19/mo "to get customers" and never raising prices. At $9/mo you need 1,111 customers to reach $10K MRR. At $79/mo you need 127. The pricing decision is a leverage decision.
Fix: Price for your best customers. The ideal customer for a $79/mo tool is not the same as the ideal customer for a $9/mo tool. Charge more, acquire fewer customers, provide better service, and learn from customers who value what you've built.

---

## Quality Gates

- [ ] Niche validation score ≥20/30 before any code is written
- [ ] At least 3 paying customers (or 50+ waitlist signups + 5 customer interviews) before MVP build
- [ ] MVP scoped to ONLY the core aha moment workflow — all extras deferred
- [ ] Tech stack decision documented with reason (use tools for solved problems)
- [ ] Launch checklist complete: communities, waitlist, Product Hunt timing, beta customers ready
- [ ] Churn rate tracked by cohort from day 1 (not just "total active users")

---

## Failure Modes and Fallbacks

**Failure: MVP launched, 0 paying customers after 60 days**
Detection: Product built. Waitlist converted to trial users. 60 days later: zero paying customers, high trial drop-off.
Fallback: Zero-conversion after 60 days is almost always one of: (1) Wrong audience reached in launch (validate: who actually signed up? Does it match your ICP?), (2) Too much friction between signup and aha moment (user tests: watch 5 users try to get started), (3) Pricing too high for discovered value, or (4) Value isn't clear enough on pricing/upgrade page. Priority order: fix activation first → then pricing → then positioning → then acquisition.

**Failure: Revenue plateau at $3K-5K MRR for 6+ months**
Detection: MRR stuck. New customers exactly replacing churned customers. Founder feeling trapped.
Fallback: $3-5K MRR plateaus happen when churn equals acquisition and neither is improving. Diagnose: (1) Is churn the problem? (Calculate: If churn was 0%, what would MRR be in 6 months?), (2) Is acquisition the problem? (Calculate: If acquisition doubled, would MRR grow or would churn neutralize it?). Fix the binding constraint. Usually it's churn — and churn is usually an activation/aha moment problem. Fix the customer journey before investing in marketing.

---

## Composability

**Hands off to:**
- `go-to-market-engine` — product-market fit triggers the GTM motion
- `growth-hacking-engine` — PLG design and viral loops for the SaaS
- `cloud-migration-playbook` — infrastructure for moving from local to production-grade GCP

**Receives from:**
- `entrepreneurial-os` — stage-gate model governs when to build vs. validate vs. scale
- `pricing-strategist` — pricing and packaging must be set before launch
