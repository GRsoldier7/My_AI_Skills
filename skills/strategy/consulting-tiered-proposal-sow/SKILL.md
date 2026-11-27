---
name: consulting-tiered-proposal-sow
description: >-
  Use when drafting a tiered consulting proposal or Statement of Work for
  automation work (Power Automate, Power BI, agents, dashboards), e.g.
  Recon/Architect/Commander tiers. Also use when reviewing whether a written
  proposal should be drafted at all, or how a Recon offer converts to Architect.
  Draft only.
metadata:
  version: "1.1.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-26"
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


## Recon-to-Architect conversion preflight

Use this section before drafting or redrafting a proposal. It does not replace the workflow above. If the decision is GO, continue with the Inputs and Workflow sections (or stop if Aaron already sent the proposal).

1. Load CONTEXT for the named prospect in the bot's CONTEXT, any existing proposal files, and this skill.
2. Already sent? Search CONTEXT, history, and available workspace files for evidence Aaron already created and sent a proposal for this prospect and scope. If found, output "STOP: proposal already sent. Confirm with Aaron before any redraft." and do not draft.
3. Open questions recorded in CONTEXT block a written proposal until Aaron answers them.
4. Conversion review. From CONTEXT or the latest draft, identify Recon and Architect scope, price, and deliverables, or `[PLACEHOLDER - REQUIRES INPUT]`. List friction points and a recommended wording or offer change for each, without inventing a credit percentage, deadline, win rate, or conversion rate:
   - Scope gap: what Recon delivers versus what Architect needs in order to start
   - Value gap: whether Recon output naturally creates demand for Architect (evidence, roadmap, prioritized backlog)
   - Pricing continuity: whether the Recon fee credits toward Architect, or `[VERIFY]` if undecided
   - Timing: whether a decision window is defined
   - Decision-maker access: whether Recon includes a stakeholder readout with the Architect buyer
5. Measurement plan (draft only). Define the conversion event (signed Architect SOW within N days of Recon delivery; default N = 30, marked `[VERIFY]`). Define leading indicators. If no historical rate is in CONTEXT, write "Baseline conversion rate: [PLACEHOLDER - REQUIRES INPUT]."
6. Go or no-go:
   - GO if Recon scope and price are confirmed, an Architect scope outline exists, Aaron has not already sent a proposal for this scope, and no open CONTEXT questions block the draft. Continue with the proposal workflow above.
   - NO-GO if any open question blocks the draft. Output "NO-GO: resolve open questions first:" plus the list.

Never contact a prospect. Never send, post, publish, or email. Heavy prose goes through `/home/box/agent-os/scripts/llm.sh` (OpenRouter `:free` first, then Claude or OpenAI on their own keys, never through OpenRouter). Grok only routes and checks.

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

The Recon-to-Architect conversion preflight (v1.1.0) was rewritten from Corey Haines, [marketingskills](https://github.com/coreyhaines31/marketingskills) (`skills/cro/SKILL.md` and `skills/sales-enablement/SKILL.md`), commit `2bf95edb4ebd37198ab7fd18b99ba95c2145ec64`, MIT License. Copyright (c) 2025 Corey Haines. It is a rewrite, not a copy. The Software is provided "AS IS", without warranty of any kind.
