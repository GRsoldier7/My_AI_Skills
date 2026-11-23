---
name: outcome-effect-closeout
description: >-
  Use when any bot starts or finishes a job, or when Chief of Staff assembles the
  weekly Scoreboard: record a baseline before the change, re-measure the same way
  after, write an `effect` field to the history line, and close with the
  Shipped/Verified/Effect line.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-15"
---
# Outcome-effect closeout

Shared procedure; each bot supplies its metric from the adapter table. Logging rules (tokens_est, cost_est, status, approval_record) live in `api-first-heavy-work`; follow them and run `history_closeout_check.py` before appending.

1. **Baseline first.** Before changing anything, run the adapter command and note metric, value, source command/file, date. Keep it in the working notes; it becomes `effect.before`. No new baseline files unless the bot already keeps one.
2. **Do the job** under its own skill.
3. **Re-measure the same way.** Same command, same file, same host. Numbers come from commands or files, never model judgment. Label each reading `freshly measured` or `reused (<date>)`.
4. **Write `effect` into the history line:** `{"metric","before","after","source","measured_at"}`, or the string `"not measured: <reason>"`. History is append-only; never rewrite past lines.
5. **Close the job:** `Shipped: <what> · Verified: <how> · Effect: <measured change, or "not measured: <why>">`.
6. **Weekly rollup (Chief of Staff).** Read the latest `effect` in each `runs/<slug>/history.jsonl`; emit one row per bot. If none exists, write `Baseline missing: <metric>, owner <bot>` and list it under Decisions.

## Adapter table (measurable today)
| Bot | Metrics and sources |
|---|---|
| Foundry | verify checks: `python3 /home/box/agent-os/scripts/no_regress.py check` ("N verify checks"); drift findings: nightly report `runs/health/<date>.md`; kaizen reverts: `git -C /home/box/agent-os log --since=7.days --grep=revert --oneline \| wc -l`; cost: that run's ledger lines |
| Chief of Staff | weekly Scoreboard row per bot from latest `effect`; missing list per step 6 |
| Optimizer | per-bot usage share and tokens from ledger/usage, before vs after each Wednesday tweak; 7-day history counts by status and ok-with-redirect (via checker); no_regress PASS/FAIL pre and post; FAIL means roll back the tweak and log it |
| Code Cheese | read-only host commands named in the job: `df -h` used/free on the target host, `uptime` load, active alerts via `amtool alert query \| wc -l` or the alert digest count, router spend from its own report, test pass count |
| GovCon | per weekly summary: notices reviewed, screens run, briefs drafted, responses approved, responses submitted (week over week); `delivered: tool\|plain-text` for the user-facing summary (must be tool); NAICS-in-SAM = `blocked: D1` |
| E7 | per active deal: stage, amount + source (or UNVERIFIED), next action + date, open questions count; surface the 4 [REDACTED-NAME] questions in a blocker list, do not wait on them |
| SEO | per site ([REDACTED-NAME].com, templeprotocol.ai): home status `curl -s -o /dev/null -w '%{http_code}'`; sitemap URLs `curl -s <site>/sitemap.xml \| grep -o '<loc>' \| wc -l`; robots.txt reachable + Sitemap line; home title and meta description present; GSC indexed/clicks/impressions = `blocked: D2` |

## Output
```
Shipped: <what> · Verified: <command/file> · Effect: <metric before -> after (source, measured_at)> | not measured: <why>
Scoreboard row: <bot> | <latest Effect, freshly measured|reused (date)> | Baseline missing: <metric>, owner <bot>
```

## Guardrails
- Baseline and re-measure must use the identical source.
- Never invent metrics, paths, or dates; if the source is unavailable, write `not measured: <reason>`.
- API-backed fields not yet provisioned read `blocked: D1` (SAM_API_KEY) or `blocked: D2` (GSC service account); do not assume access.
- Drafts and reports only; no external sends without approval.
