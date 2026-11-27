---
name: retention-loop-design
description: >-
  Use when designing a retention loop that matches the product's actual
  promises, including a "no regular campaigns" commitment, and producing
  an experiment spec (trigger, action, reward, reinvestment, measurement,
  and a do-not-do list). Drafts only; does not send or launch.
metadata:
  version: "1.0.0"
  domain-category: growth
  last-reviewed: "2026-11-26"
  origin: coreyhaines31/marketingskills
  origin-path: "skills/marketing-loops/SKILL.md"
  origin-sha: "2bf95edb4ebd37198ab7fd18b99ba95c2145ec64"
  license: MIT
---

# Retention loop design

## Guardrails

- Drafts only. Never send, post, publish, email, or launch a campaign or notification.
- Honor a documented "no regular campaigns" (or similar) promise with opt-in, topic-specific notices, not a newsletter cadence.
- Do not invent retention metrics or benchmarks. Mark missing numbers `[VERIFY]` or `[PLACEHOLDER - REQUIRES INPUT]`.
- If billing is not live, design renewal and cancellation transparency for a future payment flow and flag it for `claims-guardrail-check` and counsel. Do not assume renewal behavior.
- No secrets, credentials, RFC1918 or tailnet IPs, lab hostnames, lab paths, connection IDs, surnames, or private client names.
- Heavy prose goes through `/home/box/agent-os/scripts/llm.sh` (OpenRouter `:free` first, then Claude or OpenAI on their own keys, never through OpenRouter). Grok only routes and checks.

## Workflow

1. Read the product promises in the bot's CONTEXT. Extract any explicit "no regular campaigns," "no newsletter," or similar commitment. If none exists, still default to opt-in, topic-specific design.
2. Define the trigger. Use one of: a new evidence review published on a topic the user voted for; a major update to a review the user bookmarked or engaged with; or a membership renewal approaching (only if billing is live; otherwise design it and flag it). Do not use a weekly or monthly cadence as the primary trigger.
3. Define the action: a single short notification draft, for example "New review on [topic] is live. [One-sentence finding.]" plus a direct link. No promotional language, cross-sell, or "you might also like."
4. Define the reward: the review itself (immediate access to the new evidence summary). Do not add discounts, credits, or badges unless the product already has them documented.
5. Define reinvestment: the user's next vote or bookmark on the new review refines future triggers. Log topic and engagement to the preference profile. No external sharing prompts.
6. Define measurement only: opt-in rate (users with at least one active topic preference / total members); notification open or in-app view rate; review completion rate after the click; and, if billing is live, churn at the next renewal, marked `[VERIFY]` until real data exists.
7. Write the do-not-do list:
   - Do not send on a fixed schedule (no weekly digest).
   - Do not send for topics the user has not opted into.
   - Do not include unrelated content, upsells, or partner offers.
   - Do not auto-opt-in existing members; require explicit consent per topic.
   - Do not launch or send any notification from this skill; output the spec only.
   - If billing is not live, do not assume renewal behavior; flag the renewal-notice design for `claims-guardrail-check` and counsel before any payment flow exists.
8. Output one Markdown experiment spec with fields: trigger, action, reward, reinvestment, measurement, do_not_do, and flags (include `billing_not_live_renewal_requires_claims_guardrail_and_counsel` when applicable).

## Credit

Adapted from Corey Haines, [marketingskills](https://github.com/coreyhaines31/marketingskills) (`skills/marketing-loops/SKILL.md` (churn-prevention and referrals consulted for loop mechanics only)), commit `2bf95edb4ebd37198ab7fd18b99ba95c2145ec64`, MIT License. Copyright (c) 2025 Corey Haines. This text is a rewrite for Aaron's Grok Bot team, not a copy of the upstream skill. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. The Software is provided "AS IS", without warranty of any kind.
