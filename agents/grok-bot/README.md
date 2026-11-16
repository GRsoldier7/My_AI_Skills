# Grok Bot fenced skills

This folder holds 9 Grok Bot-only skills. They are not portable and work only on the Grok Bot team's box.

## Skills

| Skill | What it does |
| --- | --- |
| `api-first-heavy-work` | Routes heavy drafting, analysis, and code through the owner's API keys via the box's `llm.sh`. Grok only routes and checks. |
| `bot-team-review` | Reviews a team of Grok Bots: purpose, recent work, duplicate ownership, and gaps. |
| `chief-of-staff-intake-routing` | Routes new requests to the right specialist bot and sequences multi-bot work. |
| `evidence-before-claims` | Requires proof before claiming work is done, fixed, or sent. References the box's run ledgers. |
| `govcon-sources-sought-response` | Builds a sources-sought or RFI response from the firm's verified facts file. |
| `kaizen-evolution` | Runs a budgeted self-improvement loop over run histories and corrections. |
| `outcome-effect-closeout` | Records a baseline before and the measured effect after, then closes with a Shipped/Verified/Effect line. |
| `skill-and-prompt-evals` | Runs paired evals before applying a skill, prompt, or model change. |
| `skill-scout` | Finds public skills, license-gates them, then adapts and tests them for the bot library. |

## Why fenced

These skills depend on the box: the bot roster and lanes, agent-os scripts such as `scripts/llm.sh`, `history.jsonl` ledgers, and approvals files. They sit outside `skills/`, so `install-skills.sh`, `deploy.sh`, and any agent that scans `skills/` never load them.

Never add them to `platform-configs/skill-sets/global.txt` or to any index other than `agents/grok-bot.md`.

## Restore to the box

Copy `agents/grok-bot/skills/<name>/` into `/home/box/agent-data/workflows/<name>/`. Do this only with Aaron's yes for that skill. Foundry applies the change and runs CI.

## How backups arrive

The source of truth is `/home/box/agent-data/workflows`. Agent-os `scripts/backup_skills.sh` scrubs those folders, writes them here, and opens a pull request. This folder is that scrubbed backup.
