---
name: outcome-effect-closeout
description: >-
  Use when any bot starts or finishes a job, or when Chief of Staff assembles the
  weekly Scoreboard: run the four-question preflight before the first action,
  record a baseline before the change, re-measure the same way after, write an
  `effect` field to the history line, close with the Shipped/Verified/Effect
  line, and write the vault entry (or log skipped/none) after.
metadata:
  version: "1.1.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-26"
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

## Task preflight

Spend under a minute. Write the block into your working notes before the first action.

```
Preflight:
1. Already done? <yes|no> - <how checked>
2. Access path exists? <yes|no> - <probe used>
3. Approval in hand? <yes|no|not needed> - <quote, time, card id>
4. Done-criteria and rollback? <yes|no> - <check and revert step>
```

Stop on "already done" or on any no. Output one line: `BLOCKER: <question> - <detail>`.

### 1. Already done?

Check your own `history.jsonl`, other bots' lines where relevant, the last week of the vault log, and repo or PR state. If a client deliverable may exist, ask Aaron. Case: 2026-11-16, a bot drafted a written proposal and Aaron replied "I already did this and sent it".

### 2. Access path exists?

Run one read-only probe of the credential, scope, host, or connector permission before building anything. Case: 2026-11-17, a task failed because no root path to the lab hosts existed from the box. Case: 2026-11-16, a bot hit three Cloudflare connector failures (missing `page.read`, missing `page.write`, then 403 code 8000013).

### 3. Approval in hand?

Production deploys, merges, sends, deletes, and public posts each need Aaron's per-action yes, as set in APPROVALS.md. This skill never replaces that file. Quote his exact words, with time and card id if any, in the history line before acting. A past yes for another action does not cover this one. If no gated action is involved, answer "not needed".

### 4. Done-criteria and rollback

Write what confirms success and how to revert, before starting. Example for a deploy: 200 on key URLs, titles and H1, JSON-LD parses, API `OPTIONS` returns 204; rollback is the prior production deployment id.

### Rule of thumb

One question answered "no" costs a line of report. A wrong "yes" costs the task.

## Vault write-after

### Access (hard limits)

- Only the approved vault S3 connection, via the approved S3 piece and its list/read/metadata/upload actions.
- Allowed actions, nothing else: `list_files`, `read_file`, `get_file_metadata`, `upload_file`. Any other action needs Aaron's yes per action.
- Never delete a vault file without Aaron's yes per file. No credentials in the vault.

### A. Monthly log entry (append to an existing key)

This is the only case where `doNotOverwrite` is `false`, because the key already exists.

1. Read the current part file and note its etag via `list_files` or `get_file_metadata`. Do not trust a stale pointer in docs; list the log folder and use the current part file.
2. Build the new content: existing text plus your entry at the end. Never change earlier text.
3. Re-read the etag immediately before upload. If it changed, abort, re-read, and rebuild.
4. `upload_file` with `doNotOverwrite: false`.
5. Read back and confirm your entry is present.

Do not rewrite files over about 18 KB. If the part would exceed that, start the next part as a new key (see B), first line `Continuation of [[<previous-part>]]`.

### B. New notes and new part files (new keys)

Use `upload_file` with `doNotOverwrite: true`, so an existing key is never clobbered. Put deliverables in the existing project folder. Frontmatter and the four-question value test follow `Notes-Standard.md`, read it first. Corrections are new linked superseding notes, never in-place rewrites.

### Foundry exception

Overwrite only its own `98_Agents/Bot-Health-<date>.md` to set `status: superseded` and `updated:`, nothing else.

### Entry format

```
## YYYY-MM-DD HH:MM CT - <Agent> - <topic> [<kind>]
- Date: YYYY-MM-DD HH:MM CT
- Agent: <Agent>
- Topic: <topic>
- What: <one sentence>
- Outcome: <result>
- Confidence: <verified|likely|unverified>
- Supersedes: <note path or none>
- Cost: <USD or tokens>
- Links: <[[wikilinks]] or repo paths>
- Next: <action or none>
```

### Record it

Set the `vault` field on every `history.jsonl` line: `read`, `wrote`, `read+wrote`, `skipped: <reason>`, or `none` when the vault was not touched. Never leave it out. Trivial or no-op tasks write nothing and log `skipped: <reason>`. The nightly health check flags a bot with substantive tasks and no vault reads or writes as drifting.

### Credit

Aaron's My_AI_Skills `skills/aarons-latest/2nd-brain` v2.0.0: read at most 3 notes, re-read before upload and abort if the etag changed, read back, one log entry per piece of work.
