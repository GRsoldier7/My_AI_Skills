---
name: discovery-call-prep
description: >-
  Use when preparing for, running, or following up on a consulting discovery
  call: research a prospect, build a call brief, qualify an opportunity,
  summarize a call or transcript, or draft a follow-up.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Discovery Call Prep

## Before the call
1. **Company research (public only):** industry, size, locations, tech signals (M365, job posts), recent news, leadership changes. Tag each fact [PUBLIC SOURCE: link].
2. **Attendees:** role, tenure, link to automation decisions. Unknowns are [VERIFY IN CALL]; never invent.
3. **Three hypothesized opportunities:** signal, likely volume [ASSUMPTION], tier fit (Recon/Architect/Commander), 2-3 validation questions each.
4. **12-15 open-ended questions:** current state (3), volume and pain (3), decision process (4: success metrics, decision makers, budget/timeline, alternatives), technical and risk (2: compliance, who owns M365/automation).
5. **MEDDIC-lite grid:** Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion, each scored 0-3.

## After the call (from notes or transcript)
6. **Summary:** 2-3 sentence exec summary, confirmed pains with frequency and cost, decision context, technical needs, objections, commitments, next steps. Unknowns are [NOT DISCUSSED]; inferences are [INFERRED].
7. **Score the grid:** >=15 strong, 12-14 qualified, 8-11 weak, <8 disqualify.
8. **Pain-to-value map:** volume [STATED] x time per unit [ASSUMPTION] x cost gives annual cost; the automation share gives estimated savings, prefaced with "Based on these assumptions...". Never guarantee ROI.
9. **Recommend a tier** with rationale.
10. **Follow-up email as a DRAFT only:** thanks, priorities heard, opportunity with caveats, recommended next step, action items, proposed time.

## Output
```
Discovery Brief: [company] | [date] | attendees
Overview [sources] | Attendees | 3 opportunities | Questions | MEDDIC grid
(post-call) Summary | Score | Value map | Tier rec | DRAFT follow-up
```

## Guardrails
- Never send or submit anything without explicit approval; all communications are drafts.
- Never invent data; label [VERIFY], [ASSUMPTION], [INFERRED], [NOT DISCUSSED].
- Cite public sources. Respect any 'do not contact' instruction for a prospect.

_Adapted from: alirezarezvani/claude-skills (sales-engineer, product-discovery), ComposioHQ/awesome-claude-skills (meeting-insights-analyzer)._
