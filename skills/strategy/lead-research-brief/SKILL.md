---
name: lead-research-brief
description: >-
  Use when prospecting for consulting clients (automation, Power Platform,
  AI agent buildouts): build and score a prospect list from public signals and
  draft first-touch emails, follow-ups, and warm-lead follow-ups for review.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# Lead Research Brief

Find, score, and prioritize prospects, then draft outreach. Nothing is sent or stored in a CRM without approval.

## Inputs
ICP (industry, size, geography, budget signals), exclusions, pain signals to look for, max prospects, existing relationships and do-not-contact list.

## Workflow
1. **ICP:** a one-paragraph ICP (SMB and mid-market) and 3-5 exclusion rules; confirm before researching.
2. **Source 15-30 candidates (public only):** company sites, job posts mentioning manual processes or Excel reporting, LinkedIn company pages, news (funding, expansion, ops/finance hires), public tech-stack directories, chambers and associations. No scraping of personal emails or phones; respect site terms and rate limits.
3. **Score 1-5** on size fit, pain signals, stack fit (M365, SharePoint, Dynamics), and budget/access; average them. Tier 1 >=4.5, Tier 2 3-4, Tier 3 <3.
4. **Buyer and trigger:** likely buyer role (COO, CFO, VP Ops, IT head) plus a dated trigger with its source URL.
5. **Prospect table** sorted by score, with confidence (verified / single source / speculative, VERIFY before outreach).
6. **Outreach emails** (top 5 Tier 1 only, DRAFT):
   - Write like a peer. Open with their world: the dated trigger, not our services. The personalization must lead into the problem; if removing it leaves the email intact, rewrite.
   - One low-friction, interest-based ask ("worth a look?"); never a 30-minute meeting in email one.
   - 50-110 words, plain text, no links or images. Subject: 2-4 words, lowercase-ish, internal-looking. Cold emails end with a one-line opt-out (CAN-SPAM); warm follow-ups do not.
   - Banned: "I hope this finds you well", feature dumps, fake urgency, fake familiarity ("saw your post" you did not verify).
   - Follow-up plan, each touch a new angle in its own short email: day 3 (a relevant observation), day 7 (one concrete example, anonymized, true), day 14 (polite close, no guilt).
   - Pre-send check: would a peer write this? Every claim true and sourced? One ask? Under 110 words? Clean through slop_check? Fix before showing Aaron.
   - Warm-lead variant (existing relationship, post-meeting): recap their words, the agreed next step, one question. No pitch. Use the contact's stated channel; if they prefer text, draft a text of 320 characters or less.
   - Never write "attached" or "as promised" unless the item exists; list owed items as `[ATTACH: <item>]` for Aaron. Run `slop_check.py --fix-dashes`, then re-check.

## Output
```
# Lead Brief: [ICP]
Summary: X researched; Tier1/2/3 counts; key pattern
| Company | Site | Score | Why fit | Trigger (URL) | Buyer | Tier | Confidence |
DRAFT emails (top 5): subject | body | follow-ups d3/d7/d14 | pre-send check
Next steps
```

## Guardrails
- Drafts only; every email or text needs Aaron's per-message OK; nothing is sent and no one is contacted without it.
- Never add to a CRM or buy data without approval.
- Never contact anyone on a do-not-contact list.
- Mark revenue, headcount, and budget [VERIFY] unless cited. Never promise ROI or invent facts.
- Never print or store API keys.

_Outreach steps adapted from: coreyhaines31/marketingskills (cold-email), MIT. Steps 1-5 carried from the live skill, which credits ComposioHQ/awesome-claude-skills (lead-research-assistant); that repo has no license, so no text from it is reused (6-gram overlap checked)._
