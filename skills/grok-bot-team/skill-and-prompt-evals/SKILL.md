---
name: skill-and-prompt-evals
description: Use when about to propose or apply a new or changed skill, prompt, routine, or model swap, or when asked "is the new version better?". Builds a small eval set from real history, runs paired trials against the baseline, and gates the change on a decision rule.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# Skill and Prompt Evals

Replaying 1-2 past tasks once is not evidence. Outputs vary; compare arms over repeated runs.

## 1. Build the eval set
1. Pull 3-8 cases per change from `runs/<slug>/history.jsonl` tasks plus their saved deliverables.
2. Include at least one case where the change should NOT trigger or alter behavior.
3. Scrub client names, emails, phones, hosts, and personal data before saving any case.
4. Save to the proposal's `tests/<change-slug>/cases.json` (L1 bots never write to `evals/`, which Foundry owns): id, input, expected facts, critical flag.

## 2. Write assertions before any run
Deterministic first:
- required facts present; forbidden claims absent
- format and word cap
- `slop_check.py` exit 0; `quote_check.py` exit 0

Model-graded rubric only for what scripts cannot check. The grader must be a different model than the one that produced the output. Mark each assertion critical or not.

## 3. Run paired trials
1. Arms: change vs baseline (current skill/prompt, or no skill if new). Same model, same inputs.
2. At least 2 runs per case per arm.
3. Bulk trials on free models. Add one quality-model arm for client-facing outputs.
4. Route heavy calls through `scripts/llm.sh`. Respect `LLM_BUDGET_USD`; stop and report if the cap would be exceeded.
5. Record tokens and cost per arm.

## 4. Aggregate
Compute per arm: pass rate, delta, tokens, cost. List new failures (pass in baseline, fail in change). A case with a pass/fail mix across runs is FLAKY: report it in its own row, never drop it.

## 5. Decision rule
Recommend shipping only if all hold:
- change pass rate >= baseline
- no new failure on a critical assertion
- cost within the bot's cap

Otherwise recommend revise or reject. State the rule result plainly.

## 6. Description/trigger check
Write 5 should-trigger and 5 should-not-trigger requests, including near-misses. Confirm the description routes each correctly. Fix the description and rerun if any misroute.

## 7. Record
- Write `TEST-RESULTS.md` in the proposal folder using the template below.
- Add to the history line: `tokens_est`, `cost_est`, effect = pass-rate delta (e.g. `+12pp`).

## 8. After apply (Foundry only)
Run `scripts/no_regress.py` (floors in `evals/baseline.json`) and CI. Revert on any failure and report it.

## Output template
```
Change: <slug> | Arms: baseline vs change | Model: <id> | Runs/case: N
| case | assertion | baseline pass | change pass | notes |
|------|-----------|---------------|-------------|-------|
Pass rate: baseline X% -> change Y% (delta Zpp)
Tokens/cost: baseline A / $B -> change C / $D
New failures: <list or none> | Flaky: <list or none>
Trigger check: 10/10 routed correctly | [VERIFY] items
Verdict: SHIP / REVISE / REJECT (rule: <which clause>)
```

## Guardrails
- L1 propose only: never apply to the live library; never edit another bot's prompt.
- Applying is Foundry's job and needs Aaron's per-action approval.
- Never invent results; if a trial could not run, say so and mark [VERIFY].
- No secrets or unscrubbed client data in eval sets.

_Adapted from: anthropics/skills (skill-creator), Apache-2.0; alirezarezvani/claude-skills (agent-regression-evals), MIT; live bot-prompt-tuning._
