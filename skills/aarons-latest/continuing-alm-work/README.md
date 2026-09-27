# Continuing ALM Work v2.0.0

A Claude Code skill for resuming interrupted plans from the last verified state, executing the next safe high-leverage unit, verifying progress, and preserving an exact handoff.

## Why v2

The original directive was strong but too expensive to load and repeat every cycle. v2 keeps the evidence-first and execution-first behavior while reducing the main runtime instructions from 1,786 to under 900 words (about 50% smaller), moving deep rules into on-demand references, and replacing seven-section routine reporting with a four-item delta update.

The package also adds:

- Read-only deterministic project-state capture
- Resume, reconcile, and checkpoint modes
- Explicit specialist-skill routing instead of duplicated workflows
- Official `evals/evals.json` compatibility
- Standard-library validation and unit tests
- A canonical execution-state template
- Strict dirty-worktree, destructive-action, prompt-injection, secret-path, and no-fabrication protections
- Requirements traceability back to the full source directive

## Install

### Personal skill

```bash
mkdir -p ~/.claude/skills
unzip continuing-alm-work-v2.0.0.zip -d ~/.claude/skills
```

### Project skill

```bash
mkdir -p .claude/skills
unzip continuing-alm-work-v2.0.0.zip -d .claude/skills
```

If the skills directory was created after the session began, run `/reload-skills`.

## Use

```text
/continuing-alm-work
/continuing-alm-work resume "current approved plan"
/continuing-alm-work reconcile "phase 2 only"
/continuing-alm-work checkpoint "end this session"
```

With no arguments, mode defaults to `resume` and scope defaults to the current project. Claude may also invoke the skill automatically when a request matches its description.

### Optional manual-only mode

To prevent automatic invocation without editing the shared skill, add this to `.claude/settings.local.json` or the applicable Claude Code settings file:

```json
{
  "skillOverrides": {
    "continuing-alm-work": "user-invocable-only"
  }
}
```

## State Capture

The skill can run:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/capture_project_state.py \
  --root ${CLAUDE_PROJECT_DIR} --format markdown --max-items 30
```

The utility is offline, read-only, timeout-bounded for Git commands, and scan-bounded for state-file discovery. It reports Git-status completeness, secret-path omissions, candidate plan/checkpoint files, recognized manifests, and likely verification commands. It excludes secret-like filenames and reads only recognized manifests such as `package.json` when command inference requires it.

If Python, git, Claude substitutions, or the bundled script are unavailable, the skill falls back to manual source inspection. The script works most predictably from a local personal or project skill; synced and non-Claude runtimes may not support Claude Code substitutions or bundled-script permissions.

## Package Layout

```text
continuing-alm-work/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── MAINTENANCE.md
├── TRACEABILITY.md
├── assets/
│   └── execution-state-template.md
├── references/
│   ├── state-and-evidence.md
│   ├── execution-routing.md
│   ├── verification-and-safety.md
│   └── checkpoints-and-skill-candidates.md
├── scripts/
│   ├── capture_project_state.py
│   └── validate_package.py
├── evals/
│   ├── README.md
│   └── evals.json
└── tests/
    ├── test_capture_project_state.py
    ├── test_skill_contract.py
    └── test_validate_package.py
```

## Verify Locally

```bash
python3 scripts/validate_package.py .
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
```

## Behavioral Evaluation

The package ships 16 official-format cases covering evidence conflicts, missing inputs, ambiguous ALM meaning, unsafe parallelism, destructive production changes, blocked workstreams, dirty trees, skill-creation approval, verification scope, checkpoint quality, negative activation, compact reporting, capability unavailability, prompt injection, and plan optimization.

Run them with the official Claude Code skill-creator plugin as described in `evals/README.md`. This build environment does not include Claude Code or a clean-context model runner, so generated behavioral benchmarks are intentionally not fabricated.

## Recommended Operating Model

Use this skill as the continuity and orchestration layer. Let focused skills own planning, TDD, debugging, review, security, deployment, and domain work. That separation avoids giant overlapping prompts and keeps the coordinator small enough to remain useful after many turns.
