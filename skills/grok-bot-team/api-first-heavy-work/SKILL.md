---
name: api-first-heavy-work
description: >-
  Use when the task is to draft, analyze, research, write code, refactor, review
  architecture, build, or fix something: route that heavy work through the
  owner's own API keys, never through a Grok Task or subagent.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# API-first heavy work

Additive. Does not replace other skills.

1. If the job is drafting, analysis, research, or code generation, do it on the owner's APIs, not on Grok.
2. Load keys with `. [REDACTED-PATH]`. Never print or copy the values.
3. Shrink the material first with rg, jq, and tail. Do not send whole files, logs, or host surveys to a model.
4. Call `/home/box/agent-os/scripts/llm.sh` (or `/workspace/claude/ask.py` for Claude). Try OpenRouter free models first (Nemotron or whichever free model is available). Use Haiku for small jobs. Use Sonnet or OpenAI only if needed, with their own keys, never through OpenRouter.
5. If the API result is weak, retry on the API (different model or tighter prompt). Never redo the work on Grok.
6. Cap retries at two. Stop and report after that.
7. Grok only routes, runs commands, and checks the API result. Send one status update per job, not a ping at every step.
8. Load a coding plugin such as Superpowers only for the one coding skill this task needs.

Hard rule: never launch a Grok Task, subagent, or background executor to do this work. Telling a Grok executor to call the APIs still spends Grok usage.
