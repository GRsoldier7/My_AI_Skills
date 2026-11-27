---
name: case-study-draft
description: >-
  Use when drafting a one-page case study or proof asset from a real,
  approved client engagement for e7-client-growth. Drafts only; never
  sends, publishes, or contacts a prospect. Stops if there is no approved
  engagement or if Aaron has said there are no past clients.
metadata:
  version: "1.0.0"
  domain-category: strategy
  last-reviewed: "2026-11-26"
  origin: coreyhaines31/marketingskills
  origin-path: "skills/sales-enablement/SKILL.md; skills/copywriting/SKILL.md"
  origin-sha: "2bf95edb4ebd37198ab7fd18b99ba95c2145ec64"
  license: MIT
---

# Case study draft

## Guardrails

- Drafts only. Never send, post, publish, email, or contact a prospect or client.
- Never invent clients, logos, revenue figures, percentages, timelines, or quotes.
- If there is no real, approved engagement, or Aaron has said there are no past clients of the firm, do not draft a real case study. Say that no approved case is available and stop. A labeled `[HYPOTHETICAL TEMPLATE - NOT A REAL CASE]` with placeholder sections only is optional; it must not present invented facts as real.
- A pending or unwon deal is not a case study. A deal brief or discovery plan is not a case study. Do not name a private prospect; refer to "the named prospect in the bot's CONTEXT" if needed.
- Client approval is required before any real case is used, even when anonymized. Record approval status (pending, granted, or denied). Do not proceed if denied.
- Every metric needs a source; otherwise tag `[VERIFY]` or omit it.
- Check CONTEXT and history before drafting so work Aaron already completed is not redone.
- No secrets, credentials, RFC1918 or tailnet IPs, lab hostnames, lab paths, connection IDs, surnames, or private client names.
- Heavy prose goes through `/home/box/agent-os/scripts/llm.sh` (OpenRouter `:free` first, then Claude or OpenAI on their own keys, never through OpenRouter). Grok only routes and checks.

## Workflow

1. Read the bot's CONTEXT and history for existing deal records, delivery records, and any statement that there are no past clients.
2. If no approved engagement exists, output: "No approved case study engagement available. Cannot draft a case study without a real, client-approved engagement." Optionally attach the labeled hypothetical template. Stop.
3. If an approved engagement exists, record "Client approval: pending / granted / denied." Pull scope, timeline, and delivered outcomes only from CONTEXT, history, or files Aaron pointed to. Do not infer unrecorded results.
4. Draft at most one page, about 300 words:
   - Headline: a specific outcome, not a generic "Case Study" title
   - Situation: 2-3 sentences on the problem before the engagement, using the client's language where it is on record
   - Approach: 3-4 bullets on what was done in the engagement
   - Results: 3-4 quantified outcomes, each with a source, or omitted
   - Client voice, only if approved: one short quote with attribution scope, never invented
5. Footer: "Draft, not sent, not published. Client approval: [status]. All metrics [VERIFY] unless sourced."
6. Return the draft to Aaron only.

## Credit

Adapted from Corey Haines, [marketingskills](https://github.com/coreyhaines31/marketingskills) (`skills/sales-enablement/SKILL.md` and `skills/copywriting/SKILL.md` (no dedicated upstream case-study skill; proof-asset and one-pager ideas only)), commit `2bf95edb4ebd37198ab7fd18b99ba95c2145ec64`, MIT License. Copyright (c) 2025 Corey Haines. This text is a rewrite for Aaron's Grok Bot team, not a copy of the upstream skill. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. The Software is provided "AS IS", without warranty of any kind.
