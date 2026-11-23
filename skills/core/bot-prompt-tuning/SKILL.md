---
name: bot-prompt-tuning
description: >-
  Use when auditing, improving, or versioning a bot's system prompt,
  instructions, or skill descriptions, e.g. inconsistent answers, skills not
  triggering, bloated or contradictory instructions.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Bot Prompt Tuning

Every line must earn its place; clarity beats cleverness. Every change is measured, versioned, and approved before it's applied.

## Inputs
Current instruction text, concrete problem examples, success criteria, and permission to run 5-10 test prompts.

## Workflow
1. **Baseline audit.** Flag vague verbs, missing output templates, contradictions, redundancy, missing approval gates (send/post/delete/purchase), skill under-triggering, and loops without stop conditions. Write 5-10 test prompts (happy path, edge, near-miss, adversarial), run them, and record pass/fail. Report and **ask approval to rewrite**.
2. **Rewrite (after approval).** Structure: role (1-2 sentences), scope (do / don't), exact output contract, numbered concrete workflow, guardrails (never-actions, VERIFY markers, stop conditions). For skills, put real trigger phrases in the description. Trim aggressively. Save the diff and rationale.
3. **A/B test (after approval).** Same test set; compare pass rate, token count, trigger accuracy, format compliance, and new failure modes.
4. **Version & rollback (after approval).** Snapshot the baseline, record version/date/changes/pass rate, and give exact rollback steps. Define rollback triggers (metric drops, new error types).

## Output
```
Tuning Report: [bot/skill]
Baseline: X/Y (Z%) | Critical issues: [list]
Changes: [removed/added], token delta
A/B: baseline -> revised | Status: pending/approved/deployed
Rollback: [steps]
```

## Guardrails
- Never apply changes without explicit approval; show diff and rationale first.
- Never invent test results; say so if a test couldn't run.
- Keep rollback snapshots.
- Mark unsure claims (VERIFY). One high-impact change at a time.

_Adapted from: anthropics/skills (skill-creator), alirezarezvani/claude-skills (prompt-governance, senior-prompt-engineer)._
