---
name: offer-and-pricing-review
description: >-
  Use when reviewing an existing offer, price, and packaging (TempleProtocol.ai
  primary; Echelon Seven experiments secondary) and producing a ranked
  recommendation plus an experiment spec. Drafts only.
metadata:
  version: "1.0.0"
  domain-category: growth
  last-reviewed: "2026-11-26"
  origin: coreyhaines31/marketingskills
  origin-path: "skills/pricing/SKILL.md; skills/offers/SKILL.md"
  origin-sha: "2bf95edb4ebd37198ab7fd18b99ba95c2145ec64"
  license: MIT
---

# Offer and pricing review

Review an existing offer and price against alternatives, live-checked competitor prices, and cited willingness-to-pay evidence. Output a ranked recommendation and an experiment spec. The library also has `pricing-strategist` and `pricing-strategy`; use this skill for a concrete offer and packaging review, not a pricing-theory essay.

Health-adjacent offer copy must pass `claims-guardrail-check` before it reaches Aaron.

## Guardrails

- Drafts only. Never send, post, publish, email, purchase, change a live price, or start payment or ad spend.
- Never invent prices, metrics, quotes, or citations. Mark unverified items `[VERIFY]`.
- If no payment flow is live, say so. Do not design a charge as if money is already being collected.
- No secrets, credentials, RFC1918 or tailnet IPs, lab hostnames, lab paths, connection IDs, surnames, or private client names.
- Route comparison tables and long writeups through `/home/box/agent-os/scripts/llm.sh` (OpenRouter `:free` models first, then Claude or OpenAI on their own keys, never through OpenRouter). Grok only routes and checks.

## 1. Input gathering

1. Read the current offer from the bot's CONTEXT: product name, price point, billing interval, refund or guarantee terms, cohort caps, and what is included at launch.
2. Capture the stated value proposition and the primary alternatives customers consider (from CONTEXT or PROFILE).
3. Note whether a payment flow is live. If not, record "no live payment flow" and continue to the recommendation only.
4. List competitor names to scan. Do not assume prices; re-verify them in step 2.

## 2. Competitor price re-verification

1. For each competitor, fetch the public pricing or product page with `trafilatura` or `/workspace/tools/bin/webtext`. Record the published price, interval, and any promotional rate, plus the URL and fetch date (America/Chicago).
2. Mark every competitor price `[VERIFY]` with that date.
3. If a price is not on a public page, record "not publicly listed." Do not invent a number.
4. Route the comparison table to `llm.sh` for formatting if it exceeds 10 rows.

## 3. Value vs alternatives

1. Map the offer's included items (library access, evidence reviews, tools, community, updates) to the primary alternatives.
2. Note gaps in both directions.
3. Cite willingness-to-pay evidence only from CONTEXT (survey responses, sales calls, usage data). If none exists, record "no cited WTP evidence" and do not invent it.
4. Summarize in 5-7 bullets.

## 4. Packaging review

1. Evaluate any founding-cohort cap against demand signals in CONTEXT.
2. Review refund or guarantee terms for clarity.
3. Check what is included at launch versus promised later additions; flag a "future promise" as a risk.
4. Assess whether the pricing metric (per year, flat, per seat) matches the value described.

## 5. Ranked recommendation

1. Produce three options: Hold, Adjust, Test New. Each option must include a one-sentence rationale tied to steps 2-4, a specific price or packaging change (or "no change"), a risk level (Low / Medium / High), and the key assumption.
2. Rank the options 1-3 with the top recommendation first.
3. If no payment flow is live, label Adjust and Test New as pre-launch hypotheses only.

## 6. Experiment spec

For the top-ranked option that involves a change (or Test New if Hold is first), write a spec of at most 12 lines:

- Hypothesis: If we [change X], then [metric Y] will [move Z] because [reason].
- Metric: primary and a guardrail (for example refund rate or support volume).
- Traffic allocation: percentage or cohort definition.
- Duration: minimum days or sample size, plus a stop rule.
- Analysis plan: how to decide, including a statistical threshold if one is given.
- Rollback: how to revert if the guardrail triggers.

Do not invent a baseline metric. If none is in CONTEXT, write `[PLACEHOLDER - REQUIRES INPUT]`.

## 7. Output format

Produce exactly these sections, in order:

1. Current Offer Snapshot (price, interval, cap, inclusions, live payment Y/N)
2. Competitor Price Table (name, price, interval, promo, `[VERIFY]` date, source URL)
3. Value vs Alternatives (5-7 bullets)
4. Packaging Risks (3-5 bullets)
5. Ranked Recommendations (Hold / Adjust / Test New with rationale, change, risk)
6. Experiment Spec
7. Notes (any `[VERIFY]` items, missing WTP evidence, no live payment flow)

## Credit

Adapted from Corey Haines, [marketingskills](https://github.com/coreyhaines31/marketingskills) (`skills/pricing/SKILL.md` and `skills/offers/SKILL.md`), commit `2bf95edb4ebd37198ab7fd18b99ba95c2145ec64`, MIT License. Copyright (c) 2025 Corey Haines. This text is a rewrite for Aaron's Grok Bot team, not a copy of the upstream skill. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. The Software is provided "AS IS", without warranty of any kind.
