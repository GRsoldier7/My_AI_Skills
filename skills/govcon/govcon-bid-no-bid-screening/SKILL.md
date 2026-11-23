---
name: govcon-bid-no-bid-screening
description: >-
  Use when a federal opportunity (SAM.gov sources sought, RFI, presolicitation,
  or solicitation) needs a disciplined bid/no-bid decision for a small
  veteran-owned firm before committing pursuit effort.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# GovCon Bid/No-Bid Screening

Answer four questions: eligible? can perform? can win? should pursue?

## Inputs
**From the notice:** ID, agency/POC, NAICS and size standard, set-aside, contract type, value and period, deadlines, place of performance, incumbent, scope, evaluation basis (LPTA or best value), past-performance needs, clearance/CMMC/FedRAMP needs.
**From the firm:** SAM status and expiry, VOSB/SDVOSB certification, NAICS on profile, clearances, past performance (3 years, CPARS), current workload, agency relationships, teaming partners.

## Workflow
1. **Eligibility gate (PASS/GAP):** set-aside matches certification; under the size standard (VERIFY at sba.gov); SAM active through award; clearances held or obtainable in time; CMMC/FedRAMP achievable. Any unclosable GAP means NO-BID (eligibility); stop.
2. **Score (total 100):** capability 20, past performance 15, competitive position 20 (incumbent strength + relationship), price-to-win 15 (LPTA: 0-5 unless confident within 10% of the low bid), capacity 10 (account for a one-principal firm; pursuit costs 20-100 hours), strategic value 10, risk 10 (higher = safer).
3. **Decide:** 75+ BID; 55-74 TEAM (only with a named partner closing the gaps); 35-54 SHAPE (answer the RFI/sources sought, skip the solicitation unless it changes); <35 NO-BID.
   Forced NO-BID: eligibility gap; mandatory past performance = 0; LPTA with price = 0; no capacity and no sub; high risk with no bond or insurance.
4. **Capture calendar:** work backward from the due date: questions due, teaming agreement, internal review (-3 to -5 days), a complete draft by about 80% of the window.
5. **Gaps table:** every dimension at or under 50% of max, with mitigation, owner, and date.

## Output
```
BID/NO-BID: [ID - title] | agency | set-aside | NAICS (VERIFY) | value | due [date time TZ]
Eligibility: [PASS / NO-BID - gap]
Scorecard: [7 rows score/max/notes] TOTAL ## | overrides
DECISION: [BID/TEAM/SHAPE/NO-BID] - 2-4 sentence rationale
Actions | Calendar | Gaps | VERIFY list
```

## Guardrails
- Drafts only; never submit, email, or post to SAM.gov, a CO, or partners without explicit approval.
- No commitments, pricing negotiations, or signed agreements.
- Mark public-database facts and size standards VERIFY (standards change; check the current fiscal year).
- No credentials or proprietary cost data beyond what scoring needs.

_Adapted from: alirezarezvani/claude-skills (rfp-responder, deal-desk), MIT._
