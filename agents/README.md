# Agents

Each agent has one entry-point index in this folder. Each index lists at most 12 curated skills in a generated table between agent-index markers. Regenerate the table with `python3 scripts/generate-skill-registry.py --registry`. Never hand-edit it.

## Index files

| Agent | Index | What it is |
| --- | --- | --- |
| Muse | `agents/muse.md` | Aaron's self-hosted personal chief-of-staff agent |
| Grok Bot | `agents/grok-bot.md` | Team of specialist bots on one Linux box |
| Watchdog | `agents/watchdog.md` | Grok Bot specialist: silent-failure checks |
| Hermes Manager | `agents/hermes-manager.md` | Grok Bot specialist: Hermes prompts, evals, cost |
| Hermes UX | `agents/hermes-ux.md` | Grok Bot specialist: Hermes console closeout |
| Growth Architect | `agents/growth-architect.md` | Grok Bot specialist: offer, pricing, lead magnets, claims |
| Dot | `agents/dot.md` | OpenAI ChatGPT dot, an always-on work agent |
| Duet | `agents/duet.md` | Duet CLI agent harness (identity unconfirmed) |
| Nod | `agents/nod.md` | n8n Labs personal agent |

## Point an agent at its index

- Muse: point it at `agents/muse.md`, or symlink the listed folders into the skills directory its runtime reads. The runtime loader is not confirmed.
- Grok Bot: skills load on demand from `/home/box/agent-data/workflows`. Restore a fenced skill by copying `agents/grok-bot/skills/<name>/` into that box path (Aaron's yes required for each skill).
- Watchdog, Hermes Manager, Hermes UX, and Growth Architect: same box path and fenced-skill restore rule as Grok Bot. These are Grok specialist indexes (`registry/curation.json` `grok_indexes`) and may list fenced skills.
- Dot: install the listed skills on the connected computer with `scripts/install-skills.sh` (Codex target).
- Duet: install the listed skills to `~/.agents/skills` with `scripts/install-skills.sh`. Duet reads that path.
- Nod: copy only the skills listed in `agents/nod.md` into a self-hosted checkout's `src/runtime/skills/` (restart required).

## Rules for every agent

- Load a skill only when its name and description match the task.
- Never install the whole library.
- Keep each agent's list at 12 skills or fewer.
- Use Superpowers-style coding skills only in coding agents.

## Fenced folder

`agents/grok-bot/skills/` holds 9 Grok Bot-only skills. They depend on the box roster, lanes, agent-os scripts, `history.jsonl` ledgers, and approvals files. They sit outside `skills/`, so `install-skills.sh`, `deploy.sh`, and any agent that scans `skills/` never load them.

The source of truth is `/home/box/agent-data/workflows`. This folder is a scrubbed backup written by agent-os `scripts/backup_skills.sh` through a pull request. See `agents/grok-bot/README.md`.
