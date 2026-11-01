# Skill sets: one repo, Claude Code and Codex, every device

This repository is the only source for skills. Each device installs a **small global set** at user
scope; every other skill in `skills/` stays out of sessions until you install it by name. Nothing here
copies skills between projects by hand.

## What is installed where

| Mechanism | Skills | Claude Code | Codex | Install model |
|---|---|---|---|---|
| `scripts/install-skills.sh` + [`global.txt`](global.txt) | the global set below | `~/.claude/skills/` | `~/.agents/skills/` | symlinks into this repo; `git pull` updates them |
| `scripts/project-router.py` | Aaron's 7 project skills (the `SKILLS` list in `scripts/project-router.py`) | not covered by this script: link them by name per device ([Set up a new device](#set-up-a-new-device)) | `~/.agents/skills/` | hash-checked copies; re-run after `git pull` ([guide](../openai/project-router/README.md)) |
| On demand | any other skill in `skills/` | `./scripts/install-skills.sh --apply <dir-name>` | same command, except Aaron's 7 (skipped; `project-router.py` owns those) | symlink |

Rule: **two installers never manage the same skill name.** That is why `global.txt` does not list the
project-router skills, and why `install-skills.sh` links them into Claude Code only and skips exactly those
names on the Codex side, whether from a set file or by name. It reads the names from `scripts/project-router.py`
(needs python3). Every other skill in `skills/aarons-latest/`, such as `grill-me` or `projectplan-roadmap`,
installs into both tools like any library skill.

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
| [domain-modeling](../../skills/engineering/domain-modeling/SKILL.md) | Keep a `GLOSSARY.md` glossary and ADRs so code and conversations use one domain language | Discussing terminology, editing `GLOSSARY.md`, recording an ADR | Automatic (model-invoked) | None. It names ADRs `docs/adr/0001-<slug>.md`; on Aaron's homelab the doc-naming guard refuses that name inside `workspace/docs` and `hermes-deploy/docs`, so name ADRs `YYYYMMDD - Project - Description.md` there |

All four work in Claude Code and Codex: each ships `agents/openai.yaml`, and the three manual-only
skills set both `disable-model-invocation: true` and `allow_implicit_invocation: false`.

Aaron's 7 project skills are installed per device, not from `global.txt`: Claude Code by name
([Set up a new device](#set-up-a-new-device)), Codex from `scripts/project-router.py`. `continuing-alm-work` is manual-only in both tools: Codex
reads its `agents/openai.yaml`, and Claude Code needs the machine-local override in
[Set up a new device](#set-up-a-new-device), because the skill's own validator accepts only the open
Agent Skills frontmatter fields.

## Provenance (third-party, vendored)

Files are byte-identical to upstream at the pinned commit; each skill directory also carries the
upstream `LICENSE` (MIT). Never edit vendored files; control exposure per machine instead (see
[Keeping context lean](#keeping-context-lean)).

| Skill | Upstream | Commit | Upstream path | Upstream files | Security scan (SkillSpector, static; 2026-10-03 unless a later date is given) |
|---|---|---|---|---|---|
| setup-matt-pocock-skills | [mattpocock/skills](https://github.com/mattpocock/skills) | `49dd158d1076134a641b33efb035946536778336` (re-synced 2026-10-17 from `c55ee46`; follows the `CONTEXT.md` → `GLOSSARY.md` rename) | `skills/engineering/setup-matt-pocock-skills` | 7 | SAFE, 0/100 (2026-10-17) |
| to-spec | same | `c55ee46` (content identical at `49dd158d`, checked 2026-10-17) | `skills/engineering/to-spec` | 2 | ALLOW, 2/100 |
| to-tickets | same | `49dd158d1076134a641b33efb035946536778336` (re-synced 2026-10-17 from `c55ee46`) | `skills/engineering/to-tickets` | 2 | CAUTION, 25/100 (2026-10-17); one TM2 at `SKILL.md:40`, the same expand/contract ticket-sequencing prose judged a false positive on 2026-10-03 (no tool chaining; the user approves the breakdown before publishing) |
| domain-modeling | same | `49dd158d1076134a641b33efb035946536778336` (re-synced 2026-10-17 from `c55ee46`; upstream renamed `CONTEXT.md` to `GLOSSARY.md`, which `grill-with-docs` expects) | `skills/engineering/domain-modeling` | 4 | SAFE, 0/100 (re-scanned 2026-10-17 at `49dd158d`) |
| grill-me | same | `49dd158d1076134a641b33efb035946536778336` (2026-10-09) | `skills/productivity/grill-me` → vendored at `skills/aarons-latest/grill-me` | 2 | SAFE, 0/100 (scanned 2026-10-17) |
| grilling | same | same | `skills/productivity/grilling` → vendored at `skills/aarons-latest/grilling` | 2 | SAFE, 10/100 (2026-10-17); one MEDIUM EA2 at `SKILL.md:28` judged a false positive: "don't ask the user for anything you could look up yourself" is about fact-finding, and the skill forbids acting before the user confirms |
| grill-with-docs | same | same (`49dd158d`) | `skills/engineering/grill-with-docs` → vendored at `skills/aarons-latest/grill-with-docs` | 2 | SAFE, 0/100 (2026-10-17). Two-line wrapper: calls `grilling` and `domain-modeling`, so both must be installed with it |
| teach | same | same (`49dd158d`) | `skills/productivity/teach` → vendored at `skills/aarons-latest/teach` | 6 | SAFE, 0/100 (2026-10-17) |

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
python3 scripts/project-router.py install --global-guidance          # preview Aaron's 7 for Codex
python3 scripts/project-router.py install --apply --global-guidance  # details: platform-configs/openai/project-router/README.md
./scripts/install-skills.sh --tool claude --apply project-router projectplan-builder projectplan-rescope \
    continuing-alm-work workbetter clean-project directory-cleanup  # Aaron's 7 for Claude Code
```

`--global-guidance` appends the project-router routing block to `~/.codex/AGENTS.md` without replacing
what is there. With a custom `CODEX_HOME`, omit it and merge the block by hand (same README).

Keep `continuing-alm-work` manual-only in Claude Code. If `~/.claude/settings.json` does not exist, create
it with this content; if it exists, merge the `skillOverrides` key into it:

```json
{ "skillOverrides": { "continuing-alm-work": "user-invocable-only" } }
```

Per device, install the interview, tutoring and roadmap skills by name into both tools:
`./scripts/install-skills.sh --apply grill-me grilling grill-with-docs teach projectplan-roadmap`. Neither
these nor Aaron's 7 (the last command above) are in `global.txt`, because model-invoked skills cost
context in every session. `grill-me` and `grill-with-docs` call `grilling`; `grill-with-docs` also needs
`domain-modeling` (global set). `--prune` removes every by-name link, so re-run both by-name commands after
any prune.

Then restart Codex. Claude Code picks up new skills without a restart. The installers work from any
clone path; `lint-skills.py`, `generate-skill-registry.py` and `build-bundle.sh` still assume
`/root/My_AI_Skills`.

Windows: Aaron's Windows device ran `install-skills.sh` itself under Git Bash with `MSYS=winsymlinks:nativestrict`
set (2026-10-17; real symlinks), which is the preferred path. Creating symlinks needs Developer Mode or an
elevated shell; otherwise `ln -s` fails under `nativestrict`. The PowerShell fallback below is **untested**;
directory junctions need no admin rights:

```powershell
$repo = "$HOME\My_AI_Skills"
$router = python -I -c "import ast,sys;t=ast.parse(open(sys.argv[1],encoding='utf-8-sig').read()).body;v=[n.value for n in t if isinstance(n,(ast.Assign,ast.AnnAssign)) and n.value and 'SKILLS' in [getattr(x,'id','') for x in getattr(n,'targets',[getattr(n,'target',None)])]];s=ast.literal_eval(v[-1]);assert isinstance(s,tuple) and all(isinstance(x,str) for x in s);print(*s,sep=chr(10))" "$repo\scripts\project-router.py"
if ($LASTEXITCODE -ne 0 -or -not $router -or @($router | Where-Object { $_ -cnotmatch '^[a-z0-9-]+$' }).Count) { throw "cannot read SKILLS from scripts\project-router.py" }
Get-Content "$repo\platform-configs\skill-sets\global.txt" | ForEach-Object { ($_ -split '#')[0].Trim() } | Where-Object { $_ } | ForEach-Object {
  $name = Split-Path $_ -Leaf
  foreach ($t in "$HOME\.claude\skills", "$HOME\.agents\skills") {
    if ($t -like '*\.agents\skills' -and $_ -like 'skills/aarons-latest/*' -and $router -contains $name) { "SKIP $t\$name (Codex copy: project-router.py)"; continue }
    New-Item -ItemType Directory -Force $t | Out-Null
    if (Test-Path "$t\$name") { "SKIP $t\$name (exists)" }
    else { New-Item -ItemType Junction -Path "$t\$name" -Target (Join-Path $repo $_) | Out-Null; "ADD  $t\$name" }
  }
}
```

Then run the two `project-router.py` commands above with `python` and add the `skillOverrides` entry. For the
by-name skills, run the loop again with `'skills/aarons-latest/project-router','skills/aarons-latest/projectplan-builder',
'skills/aarons-latest/projectplan-rescope','skills/aarons-latest/continuing-alm-work','skills/aarons-latest/workbetter',
'skills/aarons-latest/clean-project','skills/aarons-latest/directory-cleanup','skills/aarons-latest/grill-me',
'skills/aarons-latest/grilling','skills/aarons-latest/grill-with-docs','skills/aarons-latest/teach',
'skills/aarons-latest/projectplan-roadmap'` in place of the `Get-Content … | Where-Object { $_ }` part (its
`$router` test skips Aaron's 7 on the Codex side).

**Machine-local, never committed:** Claude Code `skillOverrides` in `~/.claude/settings.json` (the
`continuing-alm-work` entry above), Codex `[[skills.config]]` in `~/.codex/config.toml`,
and tracker credentials (`gh auth login`, `glab auth login`).

## Update and sync

```sh
cd ~/My_AI_Skills
git pull --ff-only
./scripts/install-skills.sh --apply           # add new entries; repair links to skills moved within this clone
python3 scripts/project-router.py install --global-guidance   # preview; reconcile reported differences, then --apply --global-guidance
```

A clone made before `.gitattributes` existed (2026-10-17) with `core.autocrlf=true`, the Git for Windows
default, can keep CRLF copies of the scripts (bash then fails with `$'\r': command not found`). Check with
`git ls-files --eol scripts/install-skills.sh`: `w/lf` is fine; `w/crlf` needs one refresh. Commit or stash
local work first, then run `git rm -r -q --cached . && git reset --hard` (this refresh is untested here).

With a custom `CODEX_HOME`, drop `--global-guidance` (see setup). A device set up before this guide also
needs the `skillOverrides` entry from [Set up a new device](#set-up-a-new-device).

If `install-skills.sh` reports a real directory as `SKIP … same content as repo`, move it away and run
`--apply`. If it reads `DIFFERS from repo`, compare first; a copy that lacks only `agents/openai.yaml` is
safe to replace the same way.

To remove skills that left `global.txt`, run `./scripts/install-skills.sh --apply --prune` deliberately: it
removes every absolute symlink into this repo's `skills/` that is not in the set, **including skills you
installed by name**, however the link was made. It never touches real directories, links that point
elsewhere, or relative links. Links left behind by an old clone path are reported as SKIP (dangling ones
are marked) and must be removed by hand.

## Verify

| Check | Command | Expected |
|---|---|---|
| Installed set matches `global.txt` | `./scripts/install-skills.sh` | `In sync.`, exit 0. `N change(s) pending`, exit 3, means something is missing or needs relinking; a SKIP line means a skill there is not managed by this repo |
| Installer behaviour | `./scripts/test-install-skills.sh` | `passed=98 failed=0` |
| Aaron's 7 in Claude Code | `./scripts/install-skills.sh --tool claude project-router projectplan-builder projectplan-rescope continuing-alm-work workbetter clean-project directory-cleanup` | `In sync.`, exit 0 (a skill held back on purpose shows as pending; a hand-installed real directory as SKIP) |
| Per-device skills | `./scripts/install-skills.sh grill-me grilling grill-with-docs teach projectplan-roadmap` | `In sync.`, exit 0, no SKIP lines (both tools) |
| Codex has Aaron's 7 | `python3 scripts/project-router.py install` | `0 new skills; 7 already match` |
| Codex routing block | `grep -c 'project-router:user-guidance:end' ~/.codex/AGENTS.md` | `1` (if `~/.codex/AGENTS.override.md` exists, grep that file instead; with a custom `CODEX_HOME`, grep `$CODEX_HOME/AGENTS.md`; a missing file means the block is missing) |
| `continuing-alm-work` manual-only in Claude Code | `python3 -c 'import json,os; print(json.load(open(os.path.expanduser("~/.claude/settings.json"))).get("skillOverrides",{}).get("continuing-alm-work"))'` · Windows PowerShell (untested): `(Get-Content -Raw "$HOME\.claude\settings.json" \| ConvertFrom-Json).skillOverrides.'continuing-alm-work'` | `user-invocable-only` (`None` = key missing; `FileNotFoundError` = no settings.json) |
| Claude Code sees the skills | `claude -p "Reply OK" --max-turns 1 --output-format stream-json --verbose < /dev/null \| grep '"subtype":"init"'` | all 16 names appear in `skills` (4 global, Aaron's 7, grill-me, grilling, grill-with-docs, teach, projectplan-roadmap) |
| Codex sees the skills | in a new Codex session, type `$` | all 16 names appear |
| Codex offers only model-invocable skills | in a new Codex session, ask it to list its available skills | `domain-modeling`, Aaron's 6 model-invocable project skills, `grilling` and `projectplan-roadmap`; the 7 manual-only skills are absent (invoke them with `$name`) |
| Library quality | `./scripts/validate-skills.sh` · `python3 scripts/lint-skills.py --config scripts/lint-config.json` | no new FAIL or WARN |

## Add or update a third-party skill

1. Pin the source: clone upstream and record `git rev-parse HEAD`.
2. Copy byte-identical: `mkdir skills/<category>/<name>`, then
   `git -C <upstream> archive <commit> <path> | tar -x -C skills/<category>/<name> --strip-components=<depth of path>`,
   then copy upstream's `LICENSE` into the directory. Confirm every file's sha256 matches `git -C <upstream> show <commit>:<path>/<file>`.
   `.gitattributes` commits `*.sh`, `*.py` and `*.txt` with LF endings: if upstream ships one of them with
   CRLF, the committed copy is not byte-identical, so say so in its provenance row.
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
| 2. Project creation or onboarding | Configure the tracker and domain docs once; establish the glossary | `/setup-matt-pocock-skills`, `domain-modeling`; for project lifecycle questions (start, next step, resume, rescope, cleanup) start with `project-router` | `docs/agents/*.md` and `GLOSSARY.md` exist |
| 3. Skill selection | Let one controller pick the workflow; install library skills only when needed | `project-router` or your host's router (one controller, never nested); `./scripts/install-skills.sh --apply <name>` | the next workflow is named |
| 4. Execution | Spec, then tickets, then one ticket per branch or worktree | `/to-spec` → `/to-tickets` → implement (test-first where it fits); `workbetter` or `continuing-alm-work` to execute or resume | ticket acceptance checks pass |
| 5. Validation and review | Run the project's checks; an independent, read-only reviewer reviews the frozen diff against the ticket | project test/lint commands; a different model or session than the author | findings fixed or answered; a human merges |
| 6. Reusable improvements | When a pattern repeats, capture it once | propose an owner-authored skill, or vendor a reference skill ([procedure](#add-or-update-a-third-party-skill)); change `global.txt` only for things needed everywhere | the repo has the improvement, scanned and validated |
| 7. Sync and update | Pull and re-run the installers on each device | [Update and sync](#update-and-sync) | every device reports `In sync.`, and both by-name commands report `In sync.` |

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

- Every installed model-invocable skill loads its description at session start: the global set plus the
  by-name ones (Aaron's 6, `grilling`, `projectplan-roadmap`). Manual-only skills (`to-spec`, `to-tickets`,
  `setup-…`, `continuing-alm-work`, `grill-me`, `grill-with-docs`, `teach`) add nothing until invoked.
- Claude Code: `skillOverrides` per machine in `~/.claude/settings.json`, values `on`, `name-only`,
  `user-invocable-only`, `off` (official docs; this host already uses `user-invocable-only`).
- Codex: disable a skill per machine with `[[skills.config]]`, `path = "<…>/SKILL.md"`, `enabled = false`
  in `~/.codex/config.toml` ([docs](https://developers.openai.com/codex/skills); untested here).
- Both tools cap skill descriptions (Claude Code about 1% of the context window, Codex about 2%, per their
  docs; not measured here), so keep model-invoked entries in `global.txt` few and their descriptions short.
