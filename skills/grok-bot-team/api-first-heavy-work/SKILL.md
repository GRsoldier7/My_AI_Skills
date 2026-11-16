---
name: api-first-heavy-work
description: >-
  Use when the task is to draft, analyze, research, write code, refactor, review
  architecture, build, or fix something: route that heavy work through the
  owner's own API keys, never through a Grok Task or subagent.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# API-first heavy work

Additive. Does not replace other skills.

1. If the job is drafting, analysis, research, or code generation, do it on the owner's APIs, not on Grok.
2. Load keys with `. [REDACTED-PATH]`. Never print or copy the values.
3. Shrink the material first with rg, jq, and tail. Do not send whole files, logs, or host surveys to a model.
4. Call `/home/box/agent-os/scripts/llm.sh` only (it writes the cost ledger). Try OpenRouter free models first (Nemotron or whichever free model is available). Use Haiku for small jobs. For Claude, use llm.sh with the `anthropic` provider. Use Sonnet or OpenAI only if needed, with their own keys, never through OpenRouter.
5. If the API result is weak, retry on the API (different model or tighter prompt). Never redo the work on Grok.
6. Cap retries at two. Stop and report after that.
7. Grok only routes, runs commands, and checks the API result. Send one status update per job, not a ping at every step.
8. Load a coding plugin such as Superpowers only for the one coding skill this task needs.

Hard rule: never launch a Grok Task, subagent, or background executor to do this work. Telling a Grok executor to call the APIs still spends Grok usage.

## History close-out check
Before appending the task's line to `runs/<slug>/history.jsonl`:
- Set a per-task `LLM_BUDGET_LOG=<tmp file>` for every llm.sh call so the task's ledger sum is exact.
- `tokens_est` = sum of `total_tokens` in that file; with no API use, `(input+output chars)/4` plus `"tokens_note":"chars/4"`. `0` only with `"approval_record":true`.
- `cost_est` is numeric whenever an API ran (0 for free models); the key is exactly `cost_est`, never `api_cost_est_usd` or `cost_usd`.
- `approval_record` only for pure approval/confirmation records.
- Classify `user_feedback`: ask/approval (leave status `ok`) vs redirect, change, or rejection (set `corrected` and quote Aaron). The checker's redirect list is a candidate list for review; never auto-rewrite past lines (history is append-only).
- Run `python3 /home/box/agent-os/scripts/history_closeout_check.py <history file>` (proposed; until applied, `proposals/skill-drafts-2026-11-15/history_closeout_check.py`) and fix ERROR flags first.
- Close with `Shipped: <what> · Verified: <how> · Effect: <measured change, or "not measured: <why>">`.
