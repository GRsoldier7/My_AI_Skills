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

The unmodified vendored entries below are byte-identical to upstream at the pinned commit; each skill directory also carries the
upstream `LICENSE` (MIT). Keep those entries byte-identical; deliberate local adaptations are recorded separately below. Control exposure per machine instead (see
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

## Curated profile operation

The curated manifest covers only the selected pilot packages, not the entire
source library. The legacy generated master registry remains the full canonical
catalog. The 44 Claude-specific definitions are an additional source population,
not assumed duplicates or generated outputs.

The named profiles opt into trial packages. They are not added to global.txt
and do not grant tools, accounts or data access. The work-parallon set is generic;
actual employer definitions stay in employer-approved storage. Use a fresh
scoped workspace/session when changing client or domain.

Validate after a source change:
~~~bash
python3 scripts/skill-sets.py
~~~
After reviewing package changes, explicitly refresh hashes and regenerate:
~~~bash
python3 scripts/skill-sets.py --write --refresh-hashes
~~~
Preview a selected profile with the existing installer:
~~~bash
bash scripts/install-skills.sh --project /path/to/approved-workspace --set platform-configs/skill-sets/analytics.txt
~~~
The target directory must already exist. Dry-run exit 3 means changes are pending;
0 means in sync; 1 or 2 indicates an error. Repeat with --apply only for an
authorized target, then rerun without --apply to confirm In sync.

Install multiple required profiles as a deduplicated union; the consulting and
work-parallon profiles already include analytics. Do not use --prune on a subset
of profiles: it can remove links belonging to other sets. No new installer owns
the seven project-router packages.

For account skills/plugins, native discovery and updates require a separate
supported export/upload and actual-host verification. A repo push does not
install an account plugin. Check unmanaged/global/plugin identities on the
target for collisions before claiming isolation; manifest validation covers
only its selected canonical packages.

### Deliberate local adaptations

The two phuryn packages pm-sql-queries and pm-sprint-plan now intentionally differ
from upstream: added validation/capacity contracts and removed unconditional
readiness/persistence claims. Each package records the exact matching upstream
baseline in references/provenance.md and retains the upstream MIT LICENSE.
Their declared names remain sql-queries and sprint-plan; folder-name aliases
are explicit in the manifest. An upstream sync must preserve/review local changes.

Google BigQuery and Anthropic synthesis sources inform concise owner-authored
advisory adaptations. Their exact source revisions and upstream licenses are
recorded in the packages and manifest; upstream installers, servers and broad
permissions are not imported. Licensing for owner-authored repository content
remains unspecified until the owner chooses terms.

### Maintenance and recovery

Keep the prior reviewed Git commit and manifest. Revert a reviewed change on a
branch to restore source procedures, hashes and set files together; compare
managed links before applying any restoration. Do not reset/clean a dirty
device checkout. Other devices and uploaded account packages require their own
verified update/rollback. Review meaningful upstream changes and due trials;
do not auto-activate new upstream main.

The new package hash uses exact bytes. .gitattributes now fixes LF endings for
Markdown, JSON, YAML, SQL and both license filenames as well as script/text rules, so fresh
Windows, macOS and Linux checkouts can compute the same content hash.

The generator reserves global.txt and refuses collisions with other unmanaged
set files before writing. Removing or renaming a profile requires explicit
retirement of its old generator-owned .txt file: checks report orphaned files
and preserve them for review. Use a scoped reviewed Git removal for an obsolete
generated set, then regenerate. No automatic deletion or target pruning occurs.

<!-- CURATED-SETS:START -->
## Curated pilot profiles

Generated from `manifest.json`. All trial profiles require deliberate selection; `global.txt` is unchanged.

| Profile | Packages | Trial | Selection |
|---|---:|---:|---|
| [addy-controller](addy-controller.txt) | 1 | 1 | using-agent-skills |
| [addy-engineering](addy-engineering.txt) | 22 | 22 | api-and-interface-design, ci-cd-and-automation, code-review-and-quality, code-simplification, constraint-driven-development, context-engineering, debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs, frontend-ui-engineering, git-workflow-and-versioning, idea-refine, incremental-implementation, interview-me, observability-and-instrumentation, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, source-driven-development, spec-driven-development, addy-test-driven-development |
| [agent-deep-review](agent-deep-review.txt) | 1 | 1 | doubt-driven-development |
| [agent-team-design](agent-team-design.txt) | 5 | 5 | impeccable, design-taste-frontend, emil-design-eng, mobile-native, break-ui |
| [agent-team-research](agent-team-research.txt) | 2 | 2 | bounded-agent-research, reverse-engineer-anything |
| [analytics](analytics.txt) | 5 | 5 | data-analytics-engine, power-bi, sql-queries, bi-metric-contract, bigquery-review |
| [browser-qa](browser-qa.txt) | 1 | 1 | playwright-cli |
| [business-coding](business-coding.txt) | 17 | 17 | brainstorming, diagnosing-superpowers, dispatching-parallel-agents, requesting-code-review, executing-plans, finishing-a-development-branch, receiving-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills, karpathy-guidelines, anthropic-frontend-design |
| [business-operations](business-operations.txt) | 8 | 8 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, consulting-operations, pricing-strategist, professional-communicator, internal-comms |
| [connected-artifacts](connected-artifacts.txt) | 4 | 4 | connected-html-artifacts, dogum-html-artifacts, theme-factory, bi-metric-contract |
| [consulting](consulting.txt) | 13 | 13 | data-analytics-engine, power-bi, sql-queries, bi-metric-contract, bigquery-review, humanizer, theme-factory, web-artifacts-builder, discernment-nudge, consulting-operations, knowledge-synthesis, professional-communicator, internal-comms |
| [consulting-coding](consulting-coding.txt) | 17 | 17 | brainstorming, diagnosing-superpowers, dispatching-parallel-agents, requesting-code-review, executing-plans, finishing-a-development-branch, receiving-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills, karpathy-guidelines, anthropic-frontend-design |
| [consulting-web-integration](consulting-web-integration.txt) | 7 | 7 | firecrawl-developer-index, firecrawl-research-index, firecrawl-build, firecrawl-build-interact, firecrawl-build-onboarding, firecrawl-build-scrape, firecrawl-build-search |
| [consulting-web-research](consulting-web-research.txt) | 15 | 15 | firecrawl-scrape, firecrawl, firecrawl-agent, firecrawl-alexandria, firecrawl-crawl, firecrawl-developer-index, firecrawl-download, firecrawl-interact, firecrawl-map, firecrawl-parse, firecrawl-research-index, firecrawl-search, firecrawl-competitive-intel, firecrawl-lead-research, firecrawl-market-research |
| [continued-learning](continued-learning.txt) | 6 | 6 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, academy-guide, teach |
| [design-general](design-general.txt) | 1 | 1 | impeccable |
| [design-marketing](design-marketing.txt) | 1 | 1 | design-taste-frontend |
| [design-polish](design-polish.txt) | 3 | 3 | emil-design-eng, mobile-native, break-ui |
| [design-product-ui](design-product-ui.txt) | 2 | 2 | interface-design, ui-ux-pro-max |
| [e7](e7.txt) | 8 | 8 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, internal-comms, consulting-operations, pricing-strategist, professional-communicator |
| [e7-web-integration](e7-web-integration.txt) | 7 | 7 | firecrawl-developer-index, firecrawl-research-index, firecrawl-build, firecrawl-build-interact, firecrawl-build-onboarding, firecrawl-build-scrape, firecrawl-build-search |
| [e7-web-research](e7-web-research.txt) | 15 | 15 | firecrawl-scrape, firecrawl, firecrawl-agent, firecrawl-alexandria, firecrawl-crawl, firecrawl-developer-index, firecrawl-download, firecrawl-interact, firecrawl-map, firecrawl-parse, firecrawl-research-index, firecrawl-search, firecrawl-competitive-intel, firecrawl-lead-research, firecrawl-market-research |
| [emil-toolkit](emil-toolkit.txt) | 16 | 16 | animate-expo, animate, animation-performance, animation-vocabulary, apple-design, ask-sonner, break-ui, emil-design-eng, find-animation-opportunities, improve-animations, mobile-native, pick-ui-library, emil-prototype, remove-animations, review-animations, write-swift |
| [engineering-planning](engineering-planning.txt) | 4 | 0 | setup-matt-pocock-skills, to-spec, to-tickets, domain-modeling |
| [faith-learning](faith-learning.txt) | 12 | 12 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, bible-study-theologian, faith-life-integration, sunday-school-teacher, prayer-and-reflection, group-study-leader, bible-study-publisher, social-media-apologetics, teach |
| [faith-personal](faith-personal.txt) | 7 | 7 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, bible-study-theologian, prayer-and-reflection, faith-life-integration |
| [faith-publishing](faith-publishing.txt) | 7 | 7 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, bible-study-theologian, bible-study-publisher, social-media-apologetics |
| [faith-teaching](faith-teaching.txt) | 8 | 8 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, bible-study-theologian, group-study-leader, sunday-school-teacher, prayer-and-reflection |
| [government-contracting](government-contracting.txt) | 5 | 5 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, internal-comms |
| [hermes-teams](hermes-teams.txt) | 7 | 7 | team-agent-orchestration, agent-harness-construction, hermes-imports, hermes-agent, context-engineering, code-review-and-quality, constraint-driven-development |
| [home-coding](home-coding.txt) | 17 | 17 | brainstorming, diagnosing-superpowers, dispatching-parallel-agents, requesting-code-review, executing-plans, finishing-a-development-branch, receiving-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills, karpathy-guidelines, anthropic-frontend-design |
| [home-life](home-life.txt) | 6 | 6 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, knowledge-management, personal-productivity |
| [html-artifacts](html-artifacts.txt) | 3 | 3 | dogum-html-artifacts, theme-factory, humanizer |
| [html-artifacts-offline](html-artifacts-offline.txt) | 2 | 2 | html-artifacts-offline, humanizer |
| [interview](interview.txt) | 4 | 2 | grilling, grill-me, domain-modeling, grill-with-docs |
| [maintainer](maintainer.txt) | 2 | 2 | skill-builder, skill-sentinel |
| [parallon-artifacts](parallon-artifacts.txt) | 6 | 6 | interface-design, dogum-html-artifacts, theme-factory, humanizer, connected-html-artifacts, bi-metric-contract |
| [productivity](productivity.txt) | 7 | 7 | grilling, grill-me, handoff, teach, to-questionnaire, wait-what, writing-for-agents |
| [reverse-engineering](reverse-engineering.txt) | 1 | 1 | reverse-engineer-anything |
| [shared-artifacts](shared-artifacts.txt) | 4 | 4 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge |
| [shared-writing](shared-writing.txt) | 1 | 1 | humanizer |
| [skill-maintenance](skill-maintenance.txt) | 3 | 3 | skill-builder, skill-sentinel, skill-inspector |
| [superpowers](superpowers.txt) | 15 | 15 | brainstorming, diagnosing-superpowers, dispatching-parallel-agents, requesting-code-review, executing-plans, finishing-a-development-branch, receiving-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills |
| [web-product](web-product.txt) | 6 | 6 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, brand-website-strategy, anthropic-frontend-design |
| [work-analytics](work-analytics.txt) | 7 | 7 | humanizer, theme-factory, web-artifacts-builder, discernment-nudge, data-analytics-engine, power-bi, professional-communicator |
| [work-copilot-coding](work-copilot-coding.txt) | 17 | 17 | brainstorming, diagnosing-superpowers, dispatching-parallel-agents, requesting-code-review, executing-plans, finishing-a-development-branch, receiving-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills, karpathy-guidelines, anthropic-frontend-design |
| [work-parallon](work-parallon.txt) | 13 | 13 | data-analytics-engine, power-bi, sql-queries, bi-metric-contract, bigquery-review, humanizer, theme-factory, web-artifacts-builder, discernment-nudge, knowledge-synthesis, sprint-plan, professional-communicator, internal-comms |

| Skill | Canonical path | Status |
|---|---|---|
| academy-guide | skills/learning/academy-guide | trial |
| addy-test-driven-development | skills/engineering/addy-test-driven-development | trial |
| agent-harness-construction | skills/engineering/agent-harness-construction | trial |
| animate | skills/design/animate | trial |
| animate-expo | skills/design/animate-expo | trial |
| animation-performance | skills/design/animation-performance | trial |
| animation-vocabulary | skills/design/animation-vocabulary | trial |
| anthropic-frontend-design | skills/engineering/anthropic-frontend-design | trial |
| api-and-interface-design | skills/engineering/api-and-interface-design | trial |
| apple-design | skills/design/apple-design | trial |
| ask-sonner | skills/design/ask-sonner | trial |
| bi-metric-contract | skills/analytics/bi-metric-contract | trial |
| bible-study-publisher | skills/faith/bible-study-publisher | trial |
| bible-study-theologian | skills/faith/bible-study-theologian | trial |
| bigquery-review | skills/analytics/bigquery-review | trial |
| biohacking-data-pipeline | skills/product/biohacking-data-pipeline | reference |
| bounded-agent-research | skills/research/bounded-agent-research | trial |
| brainstorming | skills/engineering/brainstorming | trial |
| brand-website-strategy | skills/product/brand-website-strategy | trial |
| break-ui | skills/design/break-ui | trial |
| browser-testing-with-devtools | skills/engineering/browser-testing-with-devtools | trial |
| ci-cd-and-automation | skills/engineering/ci-cd-and-automation | trial |
| clean-project | skills/aarons-latest/clean-project | trial |
| code-review-and-quality | skills/engineering/code-review-and-quality | trial |
| code-simplification | skills/engineering/code-simplification | trial |
| connected-html-artifacts | skills/analytics/connected-html-artifacts | trial |
| constraint-driven-development | skills/engineering/constraint-driven-development | trial |
| consulting-operations | skills/strategy/consulting-operations | trial |
| context-engineering | skills/engineering/context-engineering | trial |
| continuing-alm-work | skills/aarons-latest/continuing-alm-work | trial |
| data-analytics-engine | skills/engineering/data-analytics-engine | trial |
| debugging-and-error-recovery | skills/engineering/debugging-and-error-recovery | trial |
| deprecation-and-migration | skills/engineering/deprecation-and-migration | trial |
| design-taste-frontend | skills/design/design-taste-frontend | trial |
| diagnosing-superpowers | skills/engineering/diagnosing-superpowers | trial |
| directory-cleanup | skills/aarons-latest/directory-cleanup | trial |
| discernment-nudge | skills/core/discernment-nudge | trial |
| dispatching-parallel-agents | skills/engineering/dispatching-parallel-agents | trial |
| docker-infrastructure | skills/engineering/docker-infrastructure | trial |
| documentation-and-adrs | skills/engineering/documentation-and-adrs | trial |
| dogum-html-artifacts | skills/design/dogum-html-artifacts | trial |
| domain-modeling | skills/engineering/domain-modeling | active |
| doubt-driven-development | skills/engineering/doubt-driven-development | trial |
| emil-design-eng | skills/design/emil-design-eng | trial |
| emil-prototype | skills/design/emil-prototype | trial |
| executing-plans | skills/engineering/executing-plans | trial |
| fact-checker | skills/core/fact-checker | reference |
| faith-life-integration | skills/faith/faith-life-integration | trial |
| find-animation-opportunities | skills/design/find-animation-opportunities | trial |
| finishing-a-development-branch | skills/engineering/finishing-a-development-branch | trial |
| firecrawl | skills/research/firecrawl | trial |
| firecrawl-agent | skills/research/firecrawl-agent | trial |
| firecrawl-alexandria | skills/research/firecrawl-alexandria | trial |
| firecrawl-build | skills/engineering/firecrawl-build | trial |
| firecrawl-build-interact | skills/engineering/firecrawl-build-interact | trial |
| firecrawl-build-onboarding | skills/engineering/firecrawl-build-onboarding | trial |
| firecrawl-build-scrape | skills/engineering/firecrawl-build-scrape | trial |
| firecrawl-build-search | skills/engineering/firecrawl-build-search | trial |
| firecrawl-competitive-intel | skills/research/firecrawl-competitive-intel | trial |
| firecrawl-crawl | skills/research/firecrawl-crawl | trial |
| firecrawl-developer-index | skills/research/firecrawl-developer-index | trial |
| firecrawl-download | skills/research/firecrawl-download | trial |
| firecrawl-interact | skills/research/firecrawl-interact | trial |
| firecrawl-lead-research | skills/research/firecrawl-lead-research | trial |
| firecrawl-map | skills/research/firecrawl-map | trial |
| firecrawl-market-research | skills/research/firecrawl-market-research | trial |
| firecrawl-monitor | skills/research/firecrawl-monitor | reference |
| firecrawl-parse | skills/research/firecrawl-parse | trial |
| firecrawl-research-index | skills/research/firecrawl-research-index | trial |
| firecrawl-scrape | skills/research/firecrawl-scrape | trial |
| firecrawl-search | skills/research/firecrawl-search | trial |
| frontend-ui-engineering | skills/engineering/frontend-ui-engineering | trial |
| git-workflow-and-versioning | skills/engineering/git-workflow-and-versioning | trial |
| grill-me | skills/aarons-latest/grill-me | trial |
| grill-with-docs | skills/aarons-latest/grill-with-docs | active |
| grilling | skills/aarons-latest/grilling | trial |
| group-study-leader | skills/faith/group-study-leader | trial |
| handoff | skills/productivity/handoff | trial |
| health-biohacking-protocol | skills/product/health-biohacking-protocol | reference |
| hermes-agent | skills/engineering/hermes-agent | trial |
| hermes-imports | skills/engineering/hermes-imports | trial |
| html-artifacts-offline | skills/design/html-artifacts-offline | trial |
| humanizer | skills/core/humanizer | trial |
| idea-refine | skills/engineering/idea-refine | trial |
| impeccable | skills/design/impeccable | trial |
| improve-animations | skills/design/improve-animations | trial |
| incremental-implementation | skills/engineering/incremental-implementation | trial |
| interface-design | skills/design/interface-design | trial |
| internal-comms | skills/growth/internal-comms | trial |
| interview-me | skills/engineering/interview-me | trial |
| karpathy-guidelines | skills/engineering/karpathy-guidelines | trial |
| knowledge-management | skills/core/knowledge-management | trial |
| knowledge-synthesis | skills/core/knowledge-synthesis | trial |
| mobile-native | skills/design/mobile-native | trial |
| n8n-workflow-architect | skills/engineering/n8n-workflow-architect | reference |
| observability-and-instrumentation | skills/engineering/observability-and-instrumentation | trial |
| performance-optimization | skills/engineering/performance-optimization | trial |
| personal-productivity | skills/core/personal-productivity | trial |
| pick-ui-library | skills/design/pick-ui-library | trial |
| planning-and-task-breakdown | skills/engineering/planning-and-task-breakdown | trial |
| playwright-cli | skills/engineering/playwright-cli | trial |
| power-bi | skills/microsoft/power-bi | trial |
| prayer-and-reflection | skills/faith/prayer-and-reflection | trial |
| pricing-strategist | skills/strategy/pricing-strategist | trial |
| professional-communicator | skills/growth/professional-communicator | trial |
| project-router | skills/aarons-latest/project-router | trial |
| projectplan-builder | skills/aarons-latest/projectplan-builder | trial |
| projectplan-rescope | skills/aarons-latest/projectplan-rescope | trial |
| projectplan-roadmap | skills/aarons-latest/projectplan-roadmap | trial |
| receiving-code-review | skills/engineering/receiving-code-review | trial |
| remove-animations | skills/design/remove-animations | trial |
| requesting-code-review | skills/engineering/requesting-code-review | trial |
| research_adaptive | skills/aarons-latest/research_adaptive | reference |
| reverse-engineer-anything | skills/engineering/reverse-engineer-anything | trial |
| review-animations | skills/design/review-animations | trial |
| security-and-hardening | skills/engineering/security-and-hardening | trial |
| setup-matt-pocock-skills | skills/engineering/setup-matt-pocock-skills | active |
| shipping-and-launch | skills/engineering/shipping-and-launch | trial |
| skill-builder | skills/core/skill-builder | trial |
| skill-inspector | skills/security/skill-inspector | trial |
| skill-sentinel | skills/core/skill-sentinel | trial |
| social-media-apologetics | skills/faith/social-media-apologetics | trial |
| source-driven-development | skills/engineering/source-driven-development | trial |
| spec-driven-development | skills/engineering/spec-driven-development | trial |
| sprint-plan | skills/product/pm-sprint-plan | trial |
| sql-queries | skills/product/pm-sql-queries | trial |
| subagent-driven-development | skills/engineering/subagent-driven-development | trial |
| sunday-school-teacher | skills/faith/sunday-school-teacher | trial |
| systematic-debugging | skills/engineering/systematic-debugging | trial |
| teach | skills/aarons-latest/teach | trial |
| team-agent-orchestration | skills/aarons-latest/team-agent-orchestration | trial |
| team-builder | skills/engineering/team-builder | reference |
| test-driven-development | skills/engineering/test-driven-development | trial |
| theme-factory | skills/design/theme-factory | trial |
| to-questionnaire | skills/productivity/to-questionnaire | trial |
| to-spec | skills/engineering/to-spec | active |
| to-tickets | skills/engineering/to-tickets | active |
| ui-ux-pro-max | skills/design/ui-ux-pro-max | trial |
| using-agent-skills | skills/engineering/using-agent-skills | trial |
| using-git-worktrees | skills/engineering/using-git-worktrees | trial |
| using-superpowers | skills/core/using-superpowers | trial |
| verification-before-completion | skills/engineering/verification-before-completion | trial |
| wait-what | skills/productivity/wait-what | trial |
| web-artifacts-builder | skills/engineering/web-artifacts-builder | trial |
| workbetter | skills/aarons-latest/workbetter | trial |
| write-swift | skills/engineering/write-swift | trial |
| writing-for-agents | skills/productivity/writing-for-agents | trial |
| writing-plans | skills/engineering/writing-plans | trial |
| writing-skills | skills/engineering/writing-skills | trial |
<!-- CURATED-SETS:END -->

## October 29 library import

The canonical compiler is `scripts/skill-sets.py`; the older local catalog's
unique profiles were reconciled here. `reference_profiles` retains core policy,
the separate lifecycle distributor and existing blocked domains without emitting
misleading installer sets. Domain profiles combine shared capabilities once.

[Import record](../../docs/20261029%20-%20My%20AI%20Skills%20-%20Library%20Imports%20and%20Sync.md)
contains all upstream pins and local adaptations. Non-skill assets use
[artifact-sources.json](../artifact-sources.json). The four restricted document
packages are [references only](../../skills/documents/README.md).

Imported skill text remains subordinate to the user's readiness gate and host
permissions. In particular, discernment-nudge's suggested questions do not add
blanket clarification or approval requirements. None of these trial selections
was installed globally by this import.
