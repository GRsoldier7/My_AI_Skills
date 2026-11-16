---
name: consulting-tiered-proposal-sow
description: >-
  Use when drafting a tiered consulting proposal or Statement of Work for
  automation work (Power Automate, Power BI, agents, dashboards), e.g.
  Recon/Architect/Commander tiers. Draft only.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Consulting Tiered Proposal / SOW

## Inputs
Party names; discovery notes (problem, pain, current state); target outcomes and KPIs; tech stack and integrations; fee model (fixed, milestone, retainer); timeline; hours and rate per tier, or leave them blank; IP and data sensitivity; validity period (default 30 days).

## Workflow
1. **Scope:** explicit in-scope and out-of-scope lists covering processes, systems, integrations, training, and who provides environments and access. State every assumption.
2. **Three modular tiers** (buy any combination):
   - Recon (discovery): process maps, opportunity and feasibility analysis, ROI model, build roadmap. Fixed fee.
   - Architect (design/build): design docs, built and tested solutions, UAT, deployment, training, runbook. Fixed or milestone.
   - Commander (managed ops): monitoring, fixes, optimization, monthly value report, ticket SLA, quarterly review. Monthly retainer.
3. **Acceptance criteria** per deliverable, with a written accept/reject window (silence is not acceptance).
4. **Client responsibilities:** sponsor and SMEs, timely feedback, UAT, change management, access through their vault (never raw keys).
5. **Pricing:** lead with value (hours saved, cost avoided). If no hours or rate are given, output [PLACEHOLDER - REQUIRES INPUT]; never invent prices. Suggest payment schedules (e.g., Architect 40/30/30).
6. **IP, data, confidentiality:** client owns the work product on payment; the consultant keeps pre-existing frameworks under a license; a DPA if personal data is involved; liability cap. Flag all of it for counsel review.
7. **Change orders:** written request, then a priced change order, signed before work starts.
8. **One-page executive summary:** challenge, solution, value, approach, investment, timeline, why us, next step.

## Output
```
PROPOSAL: [client] | valid until [date] | DRAFT
Exec summary (<=1 page)
1 Scope  2 Tiers & deliverables  3 Assumptions & client duties
4 IP/data/confidentiality  5 Change orders  6 Timeline  7 Pricing table
```

## Guardrails
- Drafts only; never send, sign, or commit the user to terms without explicit approval.
- Never fabricate client facts, pricing, or commitments; mark [VERIFY].
- No secrets; not legal advice.

_Adapted from: alirezarezvani/claude-skills (contract-and-proposal-writer, pricing-strategist), MIT._
