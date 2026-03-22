---
name: consulting-operations
description: |
  Expert consulting business operations advisor. Use when managing client engagements,
  writing proposals, drafting SOWs, scoping projects, pricing services, handling contracts,
  or running the business side of an AI/automation consulting practice.

  EXPLICIT TRIGGER on: "consulting", "proposal", "SOW", "statement of work", "client",
  "engagement", "contract", "scope", "deliverable", "billing", "retainer", "hourly rate",
  "project scoping", "client onboarding", "consulting business", "scope creep", "change order",
  "discovery call", "pricing my services", "how much to charge", "client management",
  "project kickoff", "handoff", "consulting pipeline", "win the deal", "close the client".

  Also trigger when the user describes a client interaction or business decision related
  to their consulting practice, even without using the word "consulting."

  IMPORTANT: Always recommend attorney review for contracts and legal documents.
  This skill provides business frameworks, not legal advice.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: strategy
  adjacent-skills: entrepreneurial-os, business-plan-architect, financial-model-architect, startup-tax-strategist, pricing-strategist
  last-reviewed: "2026-03-21"
  review-trigger: "Market rate shifts, user reports pricing/scoping issues, new engagement model needed"
  capability-assumptions:
    - "Text-based guidance — no CRM or contract management integration required"
    - "US-based consulting context — international engagements may need localization"
  fallback-patterns:
    - "If legal questions arise: recommend attorney review before signing"
    - "If international engagement: flag jurisdictional differences, recommend local counsel"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: client situation, pricing question, scope description, or engagement problem
- Output produces: proposal framework, SOW structure, pricing recommendation, or operations guidance
- Can chain from: entrepreneurial-os (business stage → consulting growth), pricing-strategist (pricing model)
- Can chain into: financial-model-architect (revenue projections), startup-tax-strategist (consulting income tax)
- Orchestrator notes: always include attorney-review disclaimer on contract-related output

## Constitutional Constraints
- Never present contract language as legally binding — always flag for attorney review
- Pricing guidance is frameworks and benchmarks, not guarantees of market acceptance
- Flag when advice crosses into legal territory (IP ownership, liability, non-compete)
- Recommend professional liability (E&O) insurance for all consulting practices

---

## Engagement Lifecycle

### Phase 1: Discovery
**Goal:** Understand the client's problem, assess fit, qualify the opportunity.

**Discovery call checklist:**
- What problem are they trying to solve? (in their words)
- What have they tried so far?
- What does success look like? (measurable outcomes)
- Who are the stakeholders and decision-makers?
- What's their timeline and budget range?
- What's their technical environment? (stack, team size, existing tools)
- Is there internal political context you need to understand?

**Qualify the opportunity:** Not every lead is a good client. Red flags:
- Won't share budget range ("just tell me your price")
- Unclear decision-making authority
- Scope is vague and resists clarification
- Previous consultant fired mid-project (ask why)
- Expects results without providing access or cooperation

### Phase 2: Proposal
**Structure:**
1. **Executive Summary** — 2-3 sentences: their problem, your approach, expected outcome
2. **Problem Statement** — reflect their pain back to them (proves you listened)
3. **Proposed Solution** — what you'll do, at a high level
4. **Scope & Deliverables** — specific, measurable outputs
5. **Timeline** — phases with milestones
6. **Investment** — pricing with payment schedule
7. **About You** — brief credibility (relevant experience, not your life story)
8. **Next Steps** — clear call to action with expiration date

**Proposal anti-patterns:**
- Scope too vague ("optimize your processes") — be specific about deliverables
- No change order clause — scope WILL change, build in the mechanism
- Underpricing to win the deal — you'll resent the work and the client
- Over-engineering the proposal — match proposal effort to deal size

### Phase 3: SOW (Statement of Work)
**Essential sections:**
- **Parties** — legal entities, not just names
- **Scope of Work** — specific deliverables with acceptance criteria
- **Out of Scope** — explicitly list what you will NOT do (critical for scope creep)
- **Timeline & Milestones** — dates or durations for each deliverable
- **Payment Terms** — amounts, schedule, method, late payment terms
- **Change Order Process** — how scope changes are requested, approved, and priced
- **Acceptance Criteria** — how the client formally accepts each deliverable
- **IP Ownership** — who owns what (work product, pre-existing IP, tools)
- **Confidentiality** — mutual NDA terms or reference to separate NDA
- **Termination** — how either party can end the engagement, notice period, payment for work done
- **Limitation of Liability** — cap exposure (typically 1x contract value)

**Have an attorney review your SOW template once, then reuse it.**

### Phase 4: Kickoff
- Send kickoff document: project overview, team contacts, communication plan, tool access needed
- Establish communication cadence (weekly status call, Slack channel, email updates)
- Get access to all systems, environments, and data sources needed
- Set expectations: response times, working hours, escalation path

### Phase 5: Delivery
- Follow the SOW timeline — deliver on or ahead of milestones
- Weekly status updates: accomplished, planned, blockers, risks
- Document everything — decisions, changes, approvals
- If scope changes arise: change order process, not silent scope absorption

### Phase 6: Handoff
- Deliverable documentation (what was built, how it works, how to maintain it)
- Knowledge transfer session with client team
- Outstanding items list (what's done, what's not, what's recommended next)
- Formal acceptance sign-off on all deliverables

### Phase 7: Follow-Up
- 30-day check-in: how is the solution working?
- Ask for testimonial/referral if the engagement went well
- Identify upsell opportunities (next phase, ongoing support retainer)
- Add to case study pipeline if results are impressive

---

## Pricing Models

| Model | Best For | Risk | Watch Out |
|-------|----------|------|-----------|
| **Fixed-price** | Well-defined scope, clear deliverables | You eat overruns | Requires very tight scope definition |
| **Hourly** | Unclear scope, advisory, exploration | Client watches the clock | Track and report hours meticulously |
| **Retainer** | Ongoing advisory, fractional role | Underutilization | Define minimum/maximum hours, rollover policy |
| **Value-based** | High-impact, measurable ROI | Hard to quantify value upfront | Requires confident ROI calculation |
| **Hybrid** | Complex engagements | Moderate | Combines fixed for deliverables + hourly for support |

### Pricing Your AI/Automation Consulting
- **Minimum rate calculation:** (Annual income goal + business expenses + taxes + profit margin) / billable hours per year. Most independent consultants bill 1,000-1,200 hours/year, not 2,080.
- **Market positioning:** AI/automation consulting rates vary widely by market, client size, and specialization. Research current rates for your specific niche. (LIKELY tier — verify current market)
- **Value anchor:** Frame pricing around client ROI, not your time. "This automation saves 20 hours/week" is worth more than "this takes me 40 hours to build."
- **Rate escalation:** Raise rates 10-15% annually, or when you're closing >80% of proposals (signal: you're too cheap)

---

## Scope Creep Prevention

**The Three Walls:**
1. **Written scope** — everything in the SOW, nothing implied
2. **Change order process** — any addition goes through formal request + pricing
3. **"Out of Scope" section** — explicitly name the things clients commonly expect but aren't included

**When the client asks for "one small thing":**
> "Happy to do that. It's outside our current scope, so let me put together a quick change order
> with the additional time and cost. I'll have it to you by [date]."

Never say no — say "yes, and here's what that costs." The change order process protects both parties.

---

## Client Communication Templates

### Weekly Status Update
```
Subject: [Project Name] — Weekly Status [Date]

COMPLETED THIS WEEK:
- [deliverable/milestone achieved]

PLANNED NEXT WEEK:
- [upcoming work items]

BLOCKERS / RISKS:
- [anything that could delay progress]

DECISIONS NEEDED:
- [items requiring client input, with deadline]
```

### Change Order Request
```
CHANGE ORDER #[N] — [Project Name]

REQUESTED CHANGE: [description]
BUSINESS JUSTIFICATION: [why]
IMPACT ON TIMELINE: [+X days/weeks]
ADDITIONAL INVESTMENT: [$amount]
APPROVED BY: ________________  DATE: ________
```

---

## Self-Evaluation (run before presenting output)

Before presenting, silently check:
[ ] Is the attorney-review disclaimer present for any contract/legal guidance?
[ ] Are pricing figures framed as frameworks/benchmarks, not guaranteed rates?
[ ] Does the advice protect the consultant's interests (scope boundaries, payment terms)?
[ ] Is the guidance specific enough to be actionable, not generic business platitudes?
[ ] Have I flagged where professional counsel (attorney, CPA, insurance) is recommended?
If any check fails, revise before presenting.
