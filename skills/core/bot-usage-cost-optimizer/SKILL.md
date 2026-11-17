---
name: bot-usage-cost-optimizer
description: >-
  Use when reviewing bot or routine costs, credits are running low, bot sprawl
  is suspected, or designing new automation with cost controls.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Bot Usage Cost Optimizer

Cut bot and routine usage substantially without losing value. Draft a plan; change nothing without approval.

## Workflow
1. **Inventory** each bot and routine: purpose, schedule, cost per run, runs per month, monthly cost, last useful output, value (critical/useful/optional/unknown). Never invent usage numbers; pull them from the usage dashboard or ask.
2. **Find the 20% driving 80% of spend** and start there. Red flags: hourly where weekly would do, no useful output in 30+ days, overlapping bots.
3. **Classify** each item: keep, reduce frequency, merge, make event-driven, use a cheaper model, or retire (approval required).
4. **Scan for waste:** re-reading big context every run, polling without change detection, duplicate bots, verbose outputs, browser use where an API or connector exists, loops without max iterations, oversized context.
5. **Rank fixes by ROI:**
   - Model routing: small or free models (or outside API keys) for classification, extraction, formatting, and first drafts; large models only for hard reasoning.
   - Schedule: hourly to daily or event-triggered; daily to weekly or on-demand.
   - Change detection: check a hash, timestamp, or count first and exit if unchanged.
   - Context and output caps: summarize history, cap max_tokens, use structured output.
   - Dedupe and batch: merge overlapping routines and share fetched data.
6. **Cost controls for new automation:** per-routine budget caps (alert at 80%, stop at 100%), iteration and time limits, graceful degradation (smaller model, then cache, then queue, then pause and notify).

## Output
```
# Cost Optimization Plan
Current spend: [amount or VERIFY] | Top drivers: [list, % share]
1. [Change] - target, current cost, proposed action, est. savings, confidence, risk, [ ] approve
Start here: [one recommendation]
```

## Guardrails
- Never disable, reschedule, retire, or switch models without explicit approval.
- Mark unverified numbers [VERIFY]; rate risk and confidence for every change.
- Deliver a plan, not executed changes.

_Adapted from: alirezarezvani/claude-skills (llm-cost-optimizer), MIT._
