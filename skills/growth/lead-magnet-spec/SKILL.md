---
name: lead-magnet-spec
description: >-
  Use when specifying a single lead magnet (format, promise, audience,
  fulfillment, success metric, and build handoff) as a draft for Aaron.
  Does not launch, send, or collect data.
metadata:
  version: "1.0.0"
  domain-category: growth
  last-reviewed: "2026-11-26"
  origin: coreyhaines31/marketingskills
  origin-path: skills/lead-magnets/SKILL.md
  origin-sha: "2bf95edb4ebd37198ab7fd18b99ba95c2145ec64"
  license: MIT
---

# Lead magnet spec

TempleProtocol.ai magnets stay with `growth-architect`. Echelon Seven consulting magnets stay with `e7-client-growth`. Do not cross lanes.

## Guardrails

- Drafts only. Never send, post, publish, email, or launch the magnet.
- One clear promise. No treat, cure, or prevent language, and no outcome guarantees.
- Health-adjacent promises or any field that could collect health data must pass `claims-guardrail-check` before the spec reaches Aaron.
- Minimize data: email is the default required field. Flag any health field for review and remove it unless Aaron explicitly keeps it.
- Build work is a spec handed to `code-cheese` through `chief-of-staff`. This skill builds nothing.
- No secrets, credentials, RFC1918 or tailnet IPs, lab hostnames, lab paths, connection IDs, surnames, or private client names.
- Heavy prose goes through `/home/box/agent-os/scripts/llm.sh` (OpenRouter `:free` first, then Claude or OpenAI on their own keys, never through OpenRouter). Grok only routes and checks.

## Workflow

1. Confirm scope and lane. Read the owning bot's CONTEXT for brand voice, offers, and any "no regular campaigns" or data-minimization promises. Confirm this is one asset, not a content calendar or series.
2. Write one promise sentence: the problem it solves and what the user walks away with. If it touches supplements, peptides, therapies, or biomarkers, mark `[HEALTH-ADJACENT]`.
3. Specify audience and entry point: one buyer stage (awareness / consideration / decision) and a traffic source, or "unspecified." A single optional qualifying question is allowed only if it does not ask for conditions, medications, lab values, or symptoms. Otherwise flag `[HEALTH-DATA]` and replace it.
4. Choose one format: checklist, cheat sheet, template, interactive tool, or short guide. Target consumption time is 10 minutes or less, 30 minutes at most. It must be usable on a phone without special software.
5. Design fulfillment, but do not send anything. Delivery is one of: an email with a download link, a gated download page, or a tool access link, all pending Aaron's yes. Consent is an explicit opt-in for this magnet. If the site promises no regular campaigns, do not bundle "occasional updates" or a newsletter into the same checkbox. A tool may use a magic link; do not require an account for first use.
6. Data collection: required field is email only (plus a token if the tool needs one). Optional: first name. Prohibited by default: phone, company, role, health conditions, medications, supplement stack, lab results, symptoms, and open-ended health goals. Any extra field needs a written justification and a `[HEALTH-DATA]` flag.
7. One primary success metric: unique completions or tool starts divided by unique visitors to the magnet page. Optionally one secondary metric (completion rate, share rate, or reply rate). Do not put revenue or pipeline targets in this spec. Do not invent a baseline.
8. Write a one-page build brief for `code-cheese` via `chief-of-staff`: slug, format and promise, fields and validation, a text description of the flow (visitor, form, consent, delivery after approval), and tracking events (`page_view`, `form_submit`, `consent_given`, `delivery_queued`, `delivery_opened`, `tool_start`, `tool_complete`). No raw email in event payloads. Staging first; production only after Aaron approves a staging preview.
9. Assemble steps 1-8 as a Markdown spec. If any `[HEALTH-ADJACENT]` or `[HEALTH-DATA]` flag is set, run `claims-guardrail-check` before delivering the draft to Aaron.

## Credit

Adapted from Corey Haines, [marketingskills](https://github.com/coreyhaines31/marketingskills) (`skills/lead-magnets/SKILL.md`), commit `2bf95edb4ebd37198ab7fd18b99ba95c2145ec64`, MIT License. Copyright (c) 2025 Corey Haines. This text is a rewrite for Aaron's Grok Bot team, not a copy of the upstream skill. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. The Software is provided "AS IS", without warranty of any kind.
