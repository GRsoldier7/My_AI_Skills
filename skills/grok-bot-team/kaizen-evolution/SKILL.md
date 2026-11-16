---
name: kaizen-evolution
description: "Budgeted self-improvement routine that mines run histories and Foundry ReadTranscript inbox extracts for user corrections and tool errors, proposes quoted, quality-gated repo edits, verifies them, and commits only if CI passes. Use when running the Kaizen routine under Foundry, or when a bot repeats a mistake a user has already corrected."
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---

# Kaizen Evolution

Kaizen is a small, budgeted, repeatable routine. It reads what went wrong recently (user corrections and tool errors), proposes minimal edits to the files that shape bot behavior, verifies them, and commits only if everything passes. The loop is generate, verify, refine. It has a budget and a stop condition, and it never works from whole transcripts.

## Who runs it

Foundry is the routine runner. Invoke it with `bash scripts/kaizen.sh`.

## Principles

- generate, verify, refine: draft an edit, check it with a second-model quality gate plus verifiers and CI, refine or discard.
- Routines have a budget and a stop. Every run has a hard cost cap of $0.50 and exits cleanly when it is reached or when there is nothing to do.
- Send extracts and references, not whole transcripts.

## Step 1: Collect recent signal (primary path)

The primary transcript path is Foundry's native ReadTranscript tool. Foundry reads recent bot transcripts, extracts only corrections and tool errors, and writes them to `runs/_inbox/<date>.jsonl` (one JSON object per line). Kaizen then reads that inbox together with `runs/*/history.jsonl` via `jq`.

`gbot` / `gbot thread` is optional and is not used on this box. There is no `gbot_thread` command. Do not log in to gbot and do not treat a missing gbot session as a defect. If a live Grok Bot app session is already present on a registered machine, `scripts/kaizen.sh --try-gbot` may use `gbot thread` as an extra source; that path is optional.

Canonical history fields in `runs/<slug>/history.jsonl`:

- `ts`: ISO 8601 timestamp
- `task`: short description of the task
- `status`: one of `ok`, `corrected`, `failed`
- `user_feedback`: the user's correction text, if any
- `tokens_est`: estimated tokens used

## Step 2: Extract

Keep only user corrections (`status` is `corrected`, or a non-empty `user_feedback`) and tool errors (`status` is `failed`, or an explicit tool error). Record each extract with its source reference.

## Step 3: No-op check

If there are no new corrections or errors since the last run, this is a no-op. Exit 0 without calling any model, without editing any file, and without committing. Still write a short no-op digest to `runs/kaizen/<date>.md`.

## Step 4: Propose edits, then quality-gate them

Send only the extracts to `scripts/llm.sh` (OpenRouter `:free` first, then quality: Claude Sonnet, then GPT-4.1). Each proposal must quote the source correction in `source_correction` and name an allowed file.

Then a second API call, using a different model from the proposer, grades each proposal with a JSON verdict `{"on_target": true|false, "reason": "..."}`. Reject the edit when `on_target` is false or when `source_correction` is missing. Off-target examples include proposing an unrelated checklist when the correction was about not presenting prior work as newly run.

### Allowed edit targets

- `bots/<slug>/CONTEXT.md`
- `bots/<slug>/PROFILE.md`
- `skills/*/SKILL.md`

### Forbidden targets

- Never touch a live bot UI or live bot configuration. Kaizen edits repository files only.
- Never edit `APPROVALS.md`. It is forbidden.
- Never edit `scripts/approvals.lock`.

## Step 5: Verify

After applying on-target edits, run `bash scripts/verify.sh` and `npm run ci`. If either fails, revert the edits, do not commit, and note the failure in the digest.

## Step 6: Commit

When verification passes, commit with `evolve(<bot>): <reason>` (one commit per bot).

## Step 7: Digest

Write `runs/kaizen/<date>.md` every run, including no-op runs: bots upgraded and why, quoted corrections, rejected off-target proposals, API cost, and anything that needs Aaron.

## Budget

The per-run API cost cap is $0.50 (`--cost-cap`, also exported as `LLM_BUDGET_USD`). Stop before exceeding it.

## Exit behavior

- Edits verified and committed: exit 0.
- No-op (no new corrections/errors, or none on-target): exit 0 with a short no-op digest.
- Budget reached: stop, write digest, exit 2.
- CI failure: revert, do not commit, record in the digest, exit 1.

## Safety notes

- No credentials are read, printed, or stored by this routine.
- Do not log in to gbot.
- Redact secrets from extracts before sending them to `scripts/llm.sh`.
- Verify this skill with `bash skills/kaizen-evolution/verify.sh`.
