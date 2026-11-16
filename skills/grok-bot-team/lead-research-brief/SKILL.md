---
name: lead-research-brief
description: >-
  Use when prospecting for consulting clients (automation, Power Automate, Power
  BI, agentic workflows): build and score a prospect list from public signals
  and draft first-touch emails for review.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Lead Research Brief

Find, score, and prioritize prospects, then draft outreach. Nothing is sent or stored in a CRM without approval.

## Inputs
ICP (industry, size, geography, budget signals), exclusions, pain signals to look for, max prospects, existing relationships and do-not-contact list.

## Workflow
1. **ICP:** a one-paragraph ICP and 3-5 exclusion rules; confirm before researching.
2. **Source 15-30 candidates (public only):** company sites, job posts mentioning manual processes or Excel reporting, LinkedIn company pages, news (funding, expansion, ops/finance hires), public tech-stack directories, chambers and associations. No scraping of personal emails or phones; respect site terms and rate limits.
3. **Score 1-5** on size fit, pain signals, stack fit (M365, SharePoint, Dynamics), and budget/access; average them. Tier 1 >=4.5, Tier 2 3-4, Tier 3 <3.
4. **Buyer and trigger:** likely buyer role (COO, CFO, VP Ops, IT head) plus a dated trigger with its source URL.
5. **Prospect table** sorted by score, with confidence (verified / single source / speculative, VERIFY before outreach).
6. **Draft emails for the top 5 Tier 1 only:** 70-120 words, a short internal-looking subject, a specific trigger reference, one low-friction ask, a one-line opt-out (CAN-SPAM). Marked DRAFT.

## Output
```
# Lead Brief: [ICP]
Summary: X researched; Tier1/2/3 counts; key pattern
| Company | Site | Score | Why fit | Trigger (URL) | Buyer | Tier | Confidence |
DRAFT emails (top 5) | Next steps
```

## Guardrails
- Drafts only; the user sends from their own client. Never add to a CRM or buy data without approval.
- Never contact anyone on a do-not-contact list.
- Mark revenue, headcount, and budget VERIFY unless cited. Never promise ROI.
- Never print or store API keys.

_Adapted from: ComposioHQ/awesome-claude-skills (lead-research-assistant), alirezarezvani/claude-skills (cold-email)._
