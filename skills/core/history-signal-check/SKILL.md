---
name: history-signal-check
description: Use when running a daily or weekly read-only check of bot history.jsonl ledgers to detect silent failures: error rate, missed schedules, zero tokens, missing fields, vault loop gaps, usage spikes, and repeated corrections. Produces normalized findings with evidence, threshold, and done-criteria. Detects only; never diagnoses or fixes.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-26"
---

# History signal check

Read-only. Source of truth is each bot's `runs/<bot>/history.jsonl`, the registered checks in `proposals/watchdog-checks.jsonl`, and the signal list in the Watchdog CONTEXT. Do not edit any ledger.

## Signals

| Signal | Fire when | Evidence to quote |
|---|---|---|
| error_rate | non-ok lines exceed the CONTEXT threshold in 7 days | the failed line timestamps and count of total lines |
| missed_schedule | a routine's expected run has no history line within its window | routine name, expected time, last line seen |
| tokens_zero | a line has `tokens_est` of 0 and no later superseding correction line | the line timestamp |
| missing_fields | a line lacks `vault`, `tokens_est`, `cost_est`, or the close-out text | the field name and line timestamp |
| vault_loop | a bot has substantive tasks in 7 days and no vault read or write, with no valid `skipped: <reason>` | task count and the bot slug |
| usage_spike | a bot's share of weekly usage exceeds the CONTEXT multiple of its own mean | the share and the baseline used |
| repeated_corrected | two or more correction lines target the same cause | the superseded timestamps |

## Rules

1. Baseline first: on a bot's first check, or when fewer than 7 days of history exist, report usage_spike as `baseline-pending`, not as an alert.
2. A correction line with `supersedes_ts`, matching status, and `tokens_est` above 0 clears the earlier line. Do not fire on a cleared line.
3. Report only findings. A clean run writes one history line and sends nothing.
4. State thresholds as written in CONTEXT. If a threshold is not written there, mark it UNVERIFIED and do not invent one.
5. Never name a root cause. Name the signal, the evidence, and the owning bot. Hand diagnosis to the owner through Chief of Staff.

## Finding format

One JSON object per finding, appended to `proposals/open-findings.jsonl`:

```
{"signal":"","bot":"","evidence":["<path or quoted line>"],"threshold":"","observed":"","done_criteria":"","owner":""}
```

## Close-out

One history line per run with real `tokens_est` and `cost_est`, a valid `vault` value, and Shipped / Verified / Effect. Route each finding to its owner via Chief of Staff and note what was routed.

