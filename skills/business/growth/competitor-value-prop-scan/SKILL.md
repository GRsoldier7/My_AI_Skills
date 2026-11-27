---
name: competitor-value-prop-scan
description: >-
  Use when scanning public competitor pages to extract value propositions,
  offers, pricing, proof signals, and billing posture, then comparing them
  to the subject's stated positioning and listing gaps with experiment ideas.
  Drafts only. This is a marketing positioning scan, not a product-management
  SWOT or sales battlecard (see competitor-analysis and competitive-battlecard
  for those).
metadata:
  version: "1.0.0"
  domain-category: growth
  last-reviewed: "2026-11-26"
  origin: coreyhaines31/marketingskills
  origin-path: "skills/competitors/SKILL.md; skills/competitor-profiling/SKILL.md"
  origin-sha: "2bf95edb4ebd37198ab7fd18b99ba95c2145ec64"
  license: MIT
---

# Competitor value-prop scan

## Guardrails

- Drafts only. Never send, post, publish, email, or contact a competitor.
- Public pages only. Do not authenticate, bypass a paywall, or evade a block.
- Cite a URL and fetch date (America/Chicago) for every fact. Mark unverified or promotional prices `[VERIFY]`. Do not treat third-party complaint digests as verified findings.
- No secrets, credentials, RFC1918 or tailnet IPs, lab hostnames, lab paths, connection IDs, surnames, or private client names.
- If billing language touches negative-option or auto-renew terms, or if copy is health-adjacent, run `claims-guardrail-check` before the writeup reaches Aaron.
- Heavy synthesis goes through `/home/box/agent-os/scripts/llm.sh` (OpenRouter `:free` first, then Claude or OpenAI on their own keys, never through OpenRouter). Grok only routes and checks.

## Workflow

1. Take the scan brief: the subject's positioning statement, a competitor list with homepage URLs, and any hypotheses to test. If a required element is missing, ask Aaron for it before proceeding.
2. For each competitor URL, fetch public page text with `trafilatura` or `/workspace/tools/bin/webtext`. Save the extracted text to a dated file under the bot's work directory (for example `work-<YYYY-MM-DD>/competitors/<slug>/page.txt`). If a page blocks the fetch, record the block and move on. Do not retry with evasion.
3. Extract, with a script where possible:
   - Primary value proposition (hero or first heading)
   - Core offer: what is sold, the unit, and any stated outcome promise
   - Price: any dollar amount; note if it is labeled promotional, founding, introductory, or limited-time; tag `[VERIFY]`
   - Proof signals: testimonials, logos, study citations, reviewer counts, trust badges; record exact wording
   - Cancellation and billing posture: auto-renew language, trial terms, "cancel anytime" claims, refund policy; record verbatim snippets
   - URL and fetch date for every fact
4. Run a synthesis pass through `llm.sh` (free model first) with the positioning statement and the extracted competitor data. Ask for a comparison on value-prop clarity, offer specificity, price transparency, proof density, and billing posture; a ranked gap list; and two or three experiment ideas per gap. Require sources to be preserved. Do not let the model invent prices or complaints.
5. Review the model output. Add `[VERIFY]` where a price, claim, or legal term is promotional or unchecked.
6. Deliver a Markdown draft to Aaron with:
   - Table: Competitor | Value Prop | Offer | Price `[VERIFY]` | Proof Signals | Billing Posture | Fetch Date
   - Ranked gap list with experiment ideas
   - Cross-competitor summary: top 3 positioning opportunities for the subject
   - Paths to the saved page extracts

## Credit

Adapted from Corey Haines, [marketingskills](https://github.com/coreyhaines31/marketingskills) (`skills/competitors/SKILL.md` and `skills/competitor-profiling/SKILL.md`), commit `2bf95edb4ebd37198ab7fd18b99ba95c2145ec64`, MIT License. Copyright (c) 2025 Corey Haines. This text is a rewrite for Aaron's Grok Bot team, not a copy of the upstream skill. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. The Software is provided "AS IS", without warranty of any kind.
