---
name: growth-hacking-engine
description: >
  Genius-level growth engineering covering product-led growth (PLG), viral loops, activation
  optimization, retention mechanics, A/B testing frameworks, referral programs, and the
  mathematical models behind compounding growth. Use this skill whenever the user wants to
  grow faster, increase activation rates, reduce churn, build a referral program, implement
  PLG, design a viral loop, run growth experiments, or understand the metrics that drive
  compounding growth. Also trigger for onboarding optimization, feature adoption, re-engagement
  campaigns, growth model math, CAC reduction, or any question about how to grow from 100
  to 10,000 users efficiently.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: growth
  adjacent-skills: go-to-market-engine, marketing-strategist, micro-saas-builder, financial-model-architect
  last-reviewed: "2026-03-15"
  review-trigger: "New PLG pattern emerges, major growth tool platform change, AI-powered growth tooling breakthrough"
---

# Growth Hacking Engine — Savant-Level Skill

## Philosophy

Growth engineering mastery = **activation before acquisition** (fix the leaky bucket before adding water), **the North Star Metric** (every team, every experiment, optimizes for one number), **compounding loops over linear funnels** (viral coefficient > 1 = infinite returns), and **experiment velocity** (10 small experiments beat 1 big bet, always).

---

## 1. Growth Model Mathematics

### The Growth Equation
```
Net Growth = New Users - Churned Users

New Users = Acquired + Viral/Referred
Churned Users = Active Users × Churn Rate

Expansion:
  MRR Growth = New MRR + Expansion MRR - Churned MRR

The compounding insight:
  If you add 10% new users AND reduce churn 10%, growth compounds.
  Example:
    Start: 1,000 users, 5% monthly churn, 100 new/month
    Without optimization: After 12 months = ~1,285 users
    With 50% churn reduction (5% → 2.5%) + 20% new user increase:
    After 12 months = ~2,100 users (+63% improvement)

  Lesson: Reducing churn is always higher ROI than acquiring more users.
  The "leaky bucket" problem: filling faster never beats fixing the holes.
```

### Viral Coefficient (K-Factor)
```
K = (Invitations sent per user) × (Conversion rate of invitations)

K < 1:  Product grows only through paid/organic acquisition
K = 1:  Each user brings one new user (linear growth, not viral)
K > 1:  Viral growth — each cohort generates more users than itself

Example:
  Each user invites 5 friends (invitations sent = 5)
  10% of invitees convert (conversion rate = 0.1)
  K = 5 × 0.1 = 0.5

  With K = 0.5:
  Start 100 users → 50 invited → 5 converted → 105 total
  This doubles your effective CAC: each paid user brings 0.5 "free" users

  To get K > 1:
  Increase invitations per user (make sharing easier/more valuable)
  OR increase invitation conversion (better invite landing page/offer)

Real-world viral K values:
  < 0.1: Normal SaaS (CAC-funded growth)
  0.1-0.4: Good word-of-mouth
  0.4-0.7: Strong referral program
  > 0.7: Exceptional viral mechanics (rare; Dropbox, Slack early days)
```

---

## 2. Product-Led Growth (PLG)

### PLG Framework
```
PLG = Product is the primary acquisition, retention, and expansion channel

Three PLG motions:
  1. Free-to-Paid:     Freemium model; free value drives acquisition
  2. Trial-to-Paid:    Time-limited free trial; urgency drives conversion
  3. Usage-to-Paid:    Free up to usage limit; power users hit limit and pay

PLG prerequisites:
  ✅ Product delivers value in < 5 minutes (fast aha moment)
  ✅ Core value discoverable without a salesperson
  ✅ Sharing/collaboration creates network effects
  ✅ Free tier is genuinely useful (not crippled)
  ✅ Upgrade trigger is obvious and friction-free

PLG signals you don't have it yet:
  ❌ New users need a demo call before understanding the product
  ❌ Setup requires IT or integration expertise
  ❌ Value only apparent after 2+ weeks of use
  ❌ Sharing/collaboration adds no value to either party
```

### PLG Onboarding Design
```
Aha Moment: The one action that predicts long-term retention
  Find it: Correlate first-week actions with 30-day retention
  Examples:
    Slack: "Send 2,000 messages" (early teams that hit this had 93% retention)
    Twitter: "Follow 30 accounts"
    Dropbox: "Store one file in a shared folder"
    Your product: [Run cohort analysis to find yours]

Onboarding optimization target:
  Time to aha moment (TTAha) < 15 minutes for B2C
  TTAha < 1 day for B2B

Onboarding flow:
  1. Account creation: Minimum friction (SSO preferred)
  2. Intent capture (optional, 1 question): "What brings you here today?"
  3. Progressive profiling: Ask one question at a time, not all upfront
  4. Guided path to aha: Remove all choices except the one critical action
  5. Celebration: Acknowledge the aha moment explicitly ("You just did X!")
  6. Next step nudge: "Most users who do X next get Y result"
```

---

## 3. Activation Optimization

### Activation Funnel Analysis
```
Measure the drop-off at each step:

Sign Up → Email Confirmed → Profile Completed → First Key Action → Aha Moment
  100%        72%                  48%               31%              18%

In this example:
  Email confirmation: 28% drop — fix with frictionless SSO
  Profile completion: 24% drop — reduce fields; delay optional data
  First key action: 17% drop — simplify the UI; add empty state guidance
  Aha moment: 13% drop — more in-app guidance to reach aha

// Rule: Fix the biggest drop-off step first. Always.
// Every 10% improvement in activation at early stages compounds.
```

### Activation Tactics
```
Empty State Design:
  - Never show a blank screen; show what's possible
  - Template library: Let users start with prebuilt examples
  - Demo mode: Let them explore a populated version before entering data

In-App Guidance:
  - Tooltips on first visit to key features
  - Progress bar: "Complete 3 steps to get started" (completion bias)
  - Checklist in sidebar: "Your setup is 2/5 complete"

Email Activation Sequence:
  Day 0: "Here's how to get started" (with the ONE action they must do)
  Day 1: "Most [users] do this first" (with direct link to that action)
  Day 3: "You're missing out on [specific feature]" (if not activated)
  Day 7: "Let's chat" (founder email for non-activated trial users — 20-30% reply rate)
```

---

## 4. Retention Engineering

### Retention Curve Analysis
```
Plot retention by cohort:
  - X axis: Days since signup (Day 0, 7, 14, 30, 60, 90)
  - Y axis: % of cohort still active
  - One line per monthly cohort

Healthy curve: Flattens to non-zero plateau (retained users stay)
Unhealthy curve: Continuous decline toward zero

Interpretation:
  If Day 30 retention < 30%: Product isn't delivering enough value
  If Day 7-30 drop is steep: Onboarding failure; users can't find value
  If plateau is high (>40% at Day 90): Strong PMF

Target benchmarks by product type:
  Consumer: 40% Day 1, 20% Day 7, 10% Day 30
  B2B SaaS: 60% Day 7, 50% Day 30, 40% Day 90
  Mobile: 30% Day 1, 10% Day 7, 5% Day 30 (high churn expected)
```

### Retention Tactics
```
Habit formation:
  - Weekly digest email: "Here's what happened this week" (brings them back)
  - Personalized dashboard: "Based on your activity, here's what to do next"
  - Progress notifications: "Your [project] is 75% complete"

Value reinforcement:
  - Monthly ROI report: "You saved X hours last month with [product]"
  - Milestone celebrations: "You've processed 1,000 records!" (gamification)
  - Feature spotlight: "New: [feature] — here's how it helps your workflow"

Re-engagement before churn:
  - 14-day inactive: In-app message ("We miss you. Here's what's new.")
  - 30-day inactive: Email with personal touch (founder email)
  - 45-day inactive: Discount offer or new feature as reason to return
  - 60-day inactive: "Are you still interested?" + unsubscribe path
```

---

## 5. Growth Experiment Framework

### ICE Scoring (Prioritize Experiments)
```
Score each experiment on 3 dimensions (1-10):
  I = Impact:     If successful, how much will this move the North Star Metric?
  C = Confidence: How confident are you this will work? (1-10)
  E = Ease:       How easy/fast is it to implement?

ICE Score = (I + C + E) / 3

Example experiment backlog:
  Experiment                     | I  | C  | E  | ICE
  ─────────────────────────────────────────────────────
  Simplify onboarding to 1 step  | 8  | 7  | 8  | 7.7 ← Run first
  Add referral program           | 7  | 5  | 6  | 6.0
  Email activation at Day 3      | 6  | 8  | 9  | 7.7 ← Run first
  Add social login               | 5  | 8  | 7  | 6.7
  New pricing page layout        | 9  | 4  | 5  | 6.0

// Run 2-3 experiments per sprint. Prioritize by ICE score.
// Log every experiment with: hypothesis, metric, result, decision.
```

### A/B Test Design
```
A/B test requirements:
  [ ] One variable changed (headline, CTA, layout — never multiple)
  [ ] Primary metric defined before test starts
  [ ] Sample size calculated: Use a statistical significance calculator
      Minimum: 100 conversions per variant for a conversion test
  [ ] Duration: Minimum 2 weeks (captures weekly patterns)
  [ ] Winner criteria: ≥95% statistical significance

Tools:
  Web: Optimizely, VWO, or Google Optimize (deprecated — use Statsig)
  Email: Klaviyo built-in A/B, ConvertKit A/B
  In-product: LaunchDarkly (feature flags), PostHog (free, open-source)

// 80% of A/B tests should be boring (headline test, CTA copy, button color).
// Run the boring ones because they run fast and give clean signal.
// Save creative experiments for monthly moonshots.
```

---

## 6. Referral Program Design

### Referral Program Architecture
```
Components:
  1. Trigger: When to show the referral prompt (30 days after aha moment, not at signup)
  2. Incentive: Reward for referrer AND referee (double-sided)
  3. Mechanism: 1-click sharing (not a form or copy-paste flow)
  4. Tracking: Unique referral links per user; dashboard showing status

Incentive patterns:
  SaaS: Free month for each referral (scales with their spend)
  Marketplace: $10-25 credit for each side (low cost, high perceived value)
  Consumer app: Premium feature unlock (zero marginal cost to you)
  B2B: "Get 10% off your invoice for 1 year" (meaningful for enterprise)

Timing:
  ❌ Don't ask for referrals at signup (they don't know the product yet)
  ❌ Don't ask for referrals after support tickets (bad timing)
  ✅ Ask after: NPS 9-10 response, milestone achieved, renewal, feature adoption

Referral benchmarks:
  K contribution from referral: 0.1-0.3 for well-designed programs
  Referral-to-paid conversion: Typically 2-4x higher than paid acquisition
  (Referred users convert better, churn less, and LTV is 16% higher on average)
```

---

## Anti-Patterns

**Anti-Pattern 1: Optimizing Acquisition Before Fixing Retention**
Spending $10K/month on ads or content to acquire users while 40% churn within 30 days. Every dollar spent on acquisition is partially wasted if the bucket is leaking.
Fix: Measure Day 7, Day 30, and Day 90 retention before investing in any paid acquisition. If Day 30 retention is below 30% for a B2B tool, you don't have enough product value to justify acquisition spend. Fix retention first. Every 10% retention improvement is worth more than doubling acquisition spend.

**Anti-Pattern 2: Running Too Many Experiments Simultaneously**
Running 5-10 A/B tests at the same time. Overlapping experiments corrupt each other's results — a user in Test A also sees Test B, C, and D, creating confounds that make all results unreliable.
Fix: Run a maximum of 2-3 non-overlapping experiments simultaneously. Allocate each experiment to non-overlapping user segments. Prioritize by ICE score; finish and record results from each experiment before starting the next one on the same page or flow.

**Anti-Pattern 3: Copying Growth Tactics Without Context**
Reading about a growth tactic (viral loops, referral programs, plg freemium) and implementing it without understanding why it worked in its original context. A tactic that worked for Dropbox in 2008 (refer a friend, get free storage) worked because Dropbox had genuine free tier value, an active user base, and a product with natural sharing behavior.
Fix: Before implementing any growth tactic, ask: (1) Do I have the prerequisites? (Enough active users to seed a referral program? Enough free-tier value to justify PLG?), (2) Is the mechanism compatible with my product's natural behavior? (3) What evidence do I have that my ICP would actually use this feature?

---

## Quality Gates

- [ ] North Star Metric defined: one metric that best predicts long-term revenue and customer value
- [ ] Aha moment identified: specific action that correlates with Day 90 retention in your cohort data
- [ ] Activation funnel mapped with drop-off rates at each step
- [ ] Retention curve plotted by cohort (not just overall average active users)
- [ ] ICE-scored experiment backlog maintained and reviewed weekly
- [ ] Referral program live with double-sided incentive and post-aha-moment trigger

---

## Failure Modes and Fallbacks

**Failure: Viral loop designed but K-factor near zero**
Detection: Referral program live for 60 days. <5% of users have ever sent an invite. Referred user conversion < 10%.
Fallback: Three failure modes to diagnose: (1) Wrong timing — showing the referral prompt before users get value; fix by triggering after aha moment. (2) Wrong incentive — the reward isn't valuable enough to motivate sharing; increase or change to something your users actually want. (3) Wrong friction — the sharing mechanism requires too many steps; rebuild to 1-click or integrate with the most-used sharing method in your app.

**Failure: Growth experiment backlog infinite, zero decisions made**
Detection: 30+ experiments in the backlog. Team debates which to run. Weeks pass with no tests shipped.
Fallback: Backlog paralysis usually means the North Star Metric is unclear (everyone is optimizing for something different) or ICE scoring hasn't been done (no prioritization). Fix: (1) Define one North Star Metric, (2) ICE score the top 10 backlog items in a 30-minute session, (3) Run the top 2 ICE-scored experiments immediately regardless of whether they're "perfect" hypotheses. Velocity beats perfection.

---

## Composability

**Hands off to:**
- `marketing-strategist` — when acquisition channels need to be scaled beyond PLG and referral
- `financial-model-architect` — growth levers (activation, retention) feed revenue model

**Receives from:**
- `go-to-market-engine` — PMF signal and channel data informs which experiments to prioritize
- `micro-saas-builder` — PLG design integrates with product architecture decisions
