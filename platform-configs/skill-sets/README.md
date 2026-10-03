# Skill sets: one repo, Claude Code and Codex, every device

This repository is the only source for skills. Each device installs a **small global set** at user
scope; every other skill in `skills/` stays out of sessions until you install it by name. Nothing here
copies skills between projects by hand.

## What is installed where

| Mechanism | Skills | Claude Code | Codex | Install model |
|---|---|---|---|---|
| `scripts/install-skills.sh` + [`global.txt`](global.txt) | the global set below | `~/.claude/skills/` | `~/.agents/skills/` | symlinks into this repo; `git pull` updates them |
| `scripts/project-router.py` | Aaron's 7 project skills (`skills/aarons-latest/`) | not covered by this script | `~/.agents/skills/` | hash-checked copies; re-run after `git pull` ([guide](../openai/project-router/README.md)) |
| On demand | any other skill in `skills/` | `./scripts/install-skills.sh --apply <dir-name>` | same command, except `skills/aarons-latest/*` (skipped; `project-router.py` owns those) | symlink |

Rule: **two installers never manage the same skill name.** That is why `global.txt` does not list
`skills/aarons-latest/*`, and why `install-skills.sh` skips them on the Codex side even when asked by name.

Discovery paths were checked on 2026-10-03: Claude Code 2.1.283 reads personal skills from
`~/.claude/skills/` and follows symlinked skill directories ([docs](https://code.claude.com/docs/en/skills);
Aaron's homelab already loads 50+ symlinked skills). Codex 0.145.0 reads `~/.agents/skills/`
([docs](https://developers.openai.com/codex/skills)), verified by a live session listing the skills installed there.

## Global set: index

| Skill | Purpose | Use when | Invocation | Prerequisites |
|---|---|---|---|---|
| [setup-matt-pocock-skills](../../skills/engineering/setup-matt-pocock-skills/SKILL.md) | Configure a repo for `to-spec`/`to-tickets`: issue tracker (GitHub, GitLab or local markdown), triage labels, domain-doc layout | Once per project, before the first spec or tickets | Manual: `/setup-matt-pocock-skills` (Claude Code), `$setup-matt-pocock-skills` (Codex) | Git repo; `gh` or `glab` only for a GitHub/GitLab tracker. **Edits the project's existing `CLAUDE.md` or `AGENTS.md`** (adds `## Agent skills`) and writes `docs/agents/*.md` |
| [to-spec](../../skills/engineering/to-spec/SKILL.md) | Turn the current conversation into a spec and publish it to the tracker, without re-interviewing | Discovery is done and the decisions are already in the conversation | Manual: `/to-spec`, `$to-spec` | Setup has run. Publishing to GitHub/GitLab is outward-facing; the local-markdown tracker keeps it in the repo |
| [to-tickets](../../skills/engineering/to-tickets/SKILL.md) | Break a plan, spec or conversation into tracer-bullet vertical tickets with blocking edges; you approve the breakdown before anything is published | A spec or plan is approved | Manual: `/to-tickets`, `$to-tickets` | Setup has run; same tracker note as `to-spec` |
| [domain-modeling](../../skills/engineering/domain-modeling/SKILL.md) | Keep a `CONTEXT.md` glossary and ADRs so code and conversations use one domain language | Discussing terminology, editing `CONTEXT.md`, recording an ADR | Automatic (model-invoked) | None. It names ADRs `docs/adr/0001-<slug>.md`; on Aaron's homelab the doc-naming guard refuses that name inside `workspace/docs` and `hermes-deploy/docs`, so name ADRs `YYYYMMDD - Project - Description.md` there |

All four work in Claude Code and Codex: each ships `agents/openai.yaml`, and the three manual-only
skills set both `disable-model-invocation: true` and `allow_implicit_invocation: false`.

## Provenance (third-party, vendored)

Files are byte-identical to upstream at the pinned commit; each skill directory also carries the
upstream `LICENSE` (MIT). Never edit vendored files; control exposure per machine instead (see
[Keeping context lean](#keeping-context-lean)).

| Skill | Upstream | Commit | Upstream path | Upstream files | Security scan (2026-10-03, SkillSpector, static) |
|---|---|---|---|---|---|
| setup-matt-pocock-skills | [mattpocock/skills](https://github.com/mattpocock/skills) | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | `skills/engineering/setup-matt-pocock-skills` | 7 | ALLOW, 2/100 |
| to-spec | same | same | `skills/engineering/to-spec` | 2 | ALLOW, 2/100 |
| to-tickets | same | same | `skills/engineering/to-tickets` | 2 | NOTIFY, 27/100; findings reviewed and judged false positives: TM2 at `SKILL.md:40` is ticket-sequencing prose (no tool chaining, and the user approves the breakdown before publishing); EA3 at `LICENSE:16` is MIT warranty text |
| domain-modeling | same | same | `skills/engineering/domain-modeling` | 4 | ALLOW, 2/100 |

## Candidates considered and not vendored

The 2026-09-26 skill-rating reports ranked about 60 candidates from `mattpocock/skills`,
`davidondrej/skills`, `affaan-m/ECC` and `msitarzewski/agency-agents`. Everything not vendored above is
accounted for here.

**Reference — vendor when a project needs it** (procedure below):
`resolving-merge-conflicts` (its last step is "Stage everything and commit"; vendor as manual-only per machine if wanted),
`writing-for-agents`, `wayfinder` (needs `research`, `prototype`, `grilling`), `codebase-design`,
`improve-codebase-architecture`, `prototype`, `triage` (mattpocock);
`contract-first`, `database-migrations`, `api-design`, `backend-patterns`, `deployment-patterns`,
`e2e-testing`, `eval-harness` (needs ECC runtime scripts), `context-budget`, `workspace-surface-audit`,
`spec-miner` agent (ECC); `create-readonly-db-role` (davidondrej); the agency-agents role contracts
`multi-agent-systems-architect`, `sre`, `security-architect`, `product-feedback-synthesizer`,
`finops-engineer`, `devops-automator`, `codebase-onboarding-engineer`.

**Excluded — already covered on Aaron's setup** (git-worktree, code-review, handoff, tdd, diagnosing-bugs,
effective-agent-skills, team-agent-orchestration, parallel-execution-optimizer, goal-loop, loop-operator,
research, mcp-server-patterns, browser-qa, verification-loop, strategic-compact, memory-persistence,
continuous-learning v1/v2, security-review, senior-secops, architecture-decision-records,
minimal-change-engineer, software-architect, build-error-resolver, harness-optimizer, fable-review,
codex-subagent, security-scan/AgentShield, git-guardrails-claude-code, global-agent-guardrails and
deny-dangerous). Two of these names already exist in this repo (`code-review`, `git-worktree`).

**Excluded — hazard, or rejected by the reports themselves:** repo-sync (auto-commits and pushes every 60 s),
davidondrej's global `AGENTS.md`, fable-safe-prompt (rewrites prompts to evade safety classifiers), gpt-review,
distribute-skill-to-all-agents (`rsync --delete` into five home dirs; replaced by `install-skills.sh`),
mattpocock `implement` (auto-commits), ECC `tdd-workflow` and `delivery-gate`, deepapi/deep-research/deep-scrape
(paid external API, self-updater, undefined credentials variable), agency `code-reviewer`, NEXUS,
agents-orchestrator, incident-response-commander, infrastructure-maintainer, reality-checker,
sprint-prioritizer, autonomous-optimization-architect.

## Set up a new device

Linux or macOS (needs git, bash, python3):

```sh
git clone https://github.com/GRsoldier7/My_AI_Skills.git ~/My_AI_Skills
cd ~/My_AI_Skills
./scripts/install-skills.sh                        # preview; writes nothing (exit 3 = changes pending)
./scripts/install-skills.sh --apply                # link the global set into Claude Code and Codex
python3 scripts/project-router.py install          # preview Aaron's project skills for Codex
python3 scripts/project-router.py install --apply  # details: platform-configs/openai/project-router/README.md
```

Then restart Codex. Claude Code picks up new skills without a restart. The installers work from any
clone path; `lint-skills.py`, `generate-skill-registry.py` and `build-bundle.sh` still assume
`/root/My_AI_Skills`.

Windows: **untested here (no Windows host).** In PowerShell, directory junctions need no admin rights:

```powershell
$repo = "$HOME\My_AI_Skills"
Get-Content "$repo\platform-configs\skill-sets\global.txt" | ForEach-Object { ($_ -split '#')[0].Trim() } | Where-Object { $_ } | ForEach-Object {
  $name = Split-Path $_ -Leaf
  foreach ($t in "$HOME\.claude\skills", "$HOME\.agents\skills") {
    New-Item -ItemType Directory -Force $t | Out-Null
    if (Test-Path "$t\$name") { "SKIP $t\$name (exists)" }
    else { New-Item -ItemType Junction -Path "$t\$name" -Target (Join-Path $repo $_) | Out-Null; "ADD  $t\$name" }
  }
}
```

**Machine-local, never committed:** Claude Code `skillOverrides` in `~/.claude/settings.json` (for example
`"continuing-alm-work": "user-invocable-only"`), Codex `[[skills.config]]` in `~/.codex/config.toml`,
and tracker credentials (`gh auth login`, `glab auth login`).

## Update and sync

```sh
cd ~/My_AI_Skills
git pull --ff-only
./scripts/install-skills.sh --apply           # add new entries; repair links to skills moved within this clone
python3 scripts/project-router.py install      # preview; reconcile reported differences, then --apply
```

To remove skills that left `global.txt`, run `./scripts/install-skills.sh --apply --prune` deliberately: it
removes every absolute symlink into this repo's `skills/` that is not in the set, **including skills you
installed by name**, however the link was made. It never touches real directories, links that point
elsewhere, or relative links. Links left behind by an old clone path are reported as SKIP (dangling ones
are marked) and must be removed by hand.

## Verify

| Check | Command | Expected |
|---|---|---|
| Installed set matches `global.txt` | `./scripts/install-skills.sh` | `In sync.`, exit 0 (a "skipped" note means some entries are not managed by this repo) |
| Installer behaviour | `./scripts/test-install-skills.sh` | `passed=55 failed=0` |
| Claude Code sees the skills | `claude -p "Reply OK" --max-turns 1 --output-format stream-json --verbose < /dev/null \| grep '"subtype":"init"'` | the skill names appear in `skills` |
| Codex sees the skills | in a new Codex session, type `$` or ask it to list its available skills | the four names appear |
| Library quality | `./scripts/validate-skills.sh` · `python3 scripts/lint-skills.py --config scripts/lint-config.json` | no new FAIL or WARN |

## Add or update a third-party skill

1. Pin the source: clone upstream and record `git rev-parse HEAD`.
2. Copy byte-identical: `mkdir skills/<category>/<name>`, then
   `git -C <upstream> archive <commit> <path> | tar -x -C skills/<category>/<name> --strip-components=<depth of path>`,
   then copy upstream's `LICENSE` into the directory. Confirm every file's sha256 matches `git -C <upstream> show <commit>:<path>/<file>`.
3. Add the directory to `scripts/lint-config.json` `vendored_paths`. That marks it third-party for the
   validator, the linter and the security scan.
4. Scan the exact bytes before installing anywhere: on Aaron's homelab, `/root/bin/skill-scan <dir>`.
   ALLOW proceeds; NOTIFY needs the findings read and an explicit opt-in; BLOCK means do not vendor.
   Re-scan whenever upstream changes (trust on first use is not trust forever).
5. Add a provenance row above. Add the skill to `global.txt` only if it must load everywhere; prefer
   manual-only skills there.
6. Run `./scripts/validate-skills.sh`, the linter and `./scripts/test-install-skills.sh`; commit with
   the upstream URL and commit in the message.

## Default workflow

| Step | Do | Skills and commands | Done when |
|---|---|---|---|
| 1. Environment setup | Clone, run both installers | [Set up a new device](#set-up-a-new-device) | `install-skills.sh` says `In sync.` |
| 2. Project creation or onboarding | Configure the tracker and domain docs once; establish the glossary | `/setup-matt-pocock-skills`, `domain-modeling`; for project lifecycle questions (start, next step, resume, rescope, cleanup) start with `project-router` | `docs/agents/*.md` and `CONTEXT.md` exist |
| 3. Skill selection | Let one controller pick the workflow; install library skills only when needed | `project-router` or your host's router (one controller, never nested); `./scripts/install-skills.sh --apply <name>` | the next workflow is named |
| 4. Execution | Spec, then tickets, then one ticket per branch or worktree | `/to-spec` → `/to-tickets` → implement (test-first where it fits); `workbetter` or `continuing-alm-work` to execute or resume | ticket acceptance checks pass |
| 5. Validation and review | Run the project's checks; an independent, read-only reviewer reviews the frozen diff against the ticket | project test/lint commands; a different model or session than the author | findings fixed or answered; a human merges |
| 6. Reusable improvements | When a pattern repeats, capture it once | propose an owner-authored skill, or vendor a reference skill ([procedure](#add-or-update-a-third-party-skill)); change `global.txt` only for things needed everywhere | the repo has the improvement, scanned and validated |
| 7. Sync and update | Pull and re-run the installers on each device | [Update and sync](#update-and-sync) | every device reports `In sync.` |

## One agent or a team

- **Default: one agent, one ticket, one branch.** Most work is sequential, and splitting it only adds handoffs.
- **Use a team only** when two or more tickets have no blocking edge between them and touch disjoint
  files. Give each writer its own worktree; never put two writers in one tree.
- **Handoffs** are the ticket itself (objective, acceptance checks, blocking edges) plus a pointer to the
  branch. The receiver checks branch and state before acting and does not trust a summary on faith.
- **Review:** the author never approves its own work. Reviewers are read-only and report findings; the
  author fixes; a human merges in dependency order.
- **Skip coordination** when tickets share a schema, migration chain or generated file, or when
  explaining the task costs more than doing it.

## Keeping context lean

- Only the global set loads at session start. Manual-only skills (`to-spec`, `to-tickets`, `setup-…`)
  add no description to the model's context until invoked.
- Claude Code: `skillOverrides` per machine in `~/.claude/settings.json`, values `on`, `name-only`,
  `user-invocable-only`, `off` (official docs; this host already uses `user-invocable-only`).
- Codex: disable a skill per machine with `[[skills.config]]`, `path = "<…>/SKILL.md"`, `enabled = false`
  in `~/.codex/config.toml` ([docs](https://developers.openai.com/codex/skills); untested here).
- Both tools cap skill descriptions (Claude Code about 1% of the context window, Codex about 2%, per their
  docs; not measured here), so keep model-invoked entries in `global.txt` few and their descriptions short.
