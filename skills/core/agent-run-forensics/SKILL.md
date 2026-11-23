---
name: agent-run-forensics
description: >-
  Use when diagnosing why a bot failed, behaved unexpectedly, or produced wrong
  results; analyzing patterns across bot sessions; or validating that a bot
  change fixed a failure.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Agent Run Forensics

Diagnose bot failures from transcripts and run logs: build a timeline, classify the root cause, propose minimal fixes, and define regression tests. Never edit the bot until the user approves.

## Inputs
1. Transcripts or logs from 5-10 representative failures
2. Expected behavior and success criteria
3. Bot config snapshot (prompt, skills, tools, approval rules)
4. Error messages or user complaints

## Workflow
1. **Index runs.** For each: run id, time, task, outcome (error/wrong result/timeout/loop), failing phase (understanding, planning, tool choice, execution, verification). Redact secrets and personal data.
2. **Timeline one representative failure.** Number each action: intent, action, result, expected. Separate recorded facts from inferred causes. Mark the divergence point.
3. **Classify** each run: WRONG_TOOL, MISSING_CONTEXT, AMBIGUOUS_INSTRUCTION, INSTRUCTION_CONFLICT, HALLUCINATED_FACT, PREMATURE_STOP, LOOPING, APPROVAL_BREACH, TOOL_AUTH_ERROR, COST_BLOWUP. The most common is the primary diagnosis.
4. **Root cause:** PROMPT, TOOL, DATA, or MODEL, with confidence HIGH/MEDIUM/LOW.
5. **Propose 1-3 minimal fixes** with change, expected impact, effort, and risk. Rank by (impact x confidence)/(effort x risk). Try prompt/tool/data fixes before model changes.
6. **Regression tests:** 3-5 cases (input, current failing behavior, expected behavior); at least one critical case replicates the original failure.

## Output
```
# Bot Failure Forensics: [bot] | [date] | [N] runs
Summary: [mode, root cause, top fix]
Primary mode: [category] (X/N) | Root cause: [type] ([confidence])
Fixes (ranked): A) [summary] effort/risk
Regression tests: 1) [name] CRITICAL - input / expected
```

## Guardrails
- Proposals only; never edit bot config without explicit approval.
- Never invent facts; mark unverified claims VERIFY.
- Redact all secrets and personal data.
- Read-only analysis; no destructive commands.
- Never call a fix proven until regression tests pass.

_Adapted from: alirezarezvani/claude-skills (agent-run-forensics, agent-regression-evals), MIT._
