# continuing-alm-work v2.0.0

A Claude Code skill for safely resuming and advancing an established multi-step project from verified evidence. It reconstructs the real checkpoint, reconciles the plan with implementation state, executes the next safe high-leverage task, verifies claims, and leaves a precise resume marker.

## Why this version is leaner

The original 553-line directive has been reduced to a compact operating contract. Detailed approval, delegation, checkpoint, and skill-proposal rules load only when relevant. The skill grants no broad tool permissions and does not force a large status table for simple continuations.

## Install

### Personal skill

macOS or Linux:

```bash
mkdir -p ~/.claude/skills
cp -R continuing-alm-work ~/.claude/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME/.claude/skills" | Out-Null
Copy-Item -Recurse -Force ".\continuing-alm-work" "$HOME/.claude/skills/continuing-alm-work"
```

### Project skill

Copy the folder to:

```text
<project>/.claude/skills/continuing-alm-work/
```

Commit it when the team should share the workflow. Avoid installing duplicate copies at personal and project scopes unless you intentionally want the personal copy to take precedence.

## Invoke

```text
/continuing-alm-work Resume this project from the last verified checkpoint and continue the next safe task.
```

Claude may also load the skill automatically for clear project-resumption requests that match its description.

## Companion boundary

- `continuing-alm-work`: reconstructs state and continues execution.
- `context-checkpoint`: freezes new work under context pressure, audits integrity, writes the handoff, and stops.

When both apply, `context-checkpoint` takes priority. The next fresh session can then invoke `continuing-alm-work` to resume.

## Validate

```bash
python scripts/validate_skill.py .
```

The validator uses only Python's standard library. It checks frontmatter, naming, description quality, referenced files, line count, eval schema, and obvious placeholders.

## Evaluate

`evals/evals.json` follows Anthropic skill-creator's current schema. Run behavior comparisons in fresh sessions with and without the skill, then grade the listed expectations. Trigger accuracy should also be tested with realistic resume requests and unrelated one-off tasks.

## Maintenance rule

Keep `SKILL.md` focused. Add detailed conditional guidance to `references/`, not to the always-loaded core. Change behavior only with a version bump, updated evals, and fresh verification.
