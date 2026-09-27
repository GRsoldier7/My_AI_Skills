# projectplan-builder v1.0.0

Create the first delivery baseline from an idea, brief, feature, or unplanned codebase. The runtime is entirely in [SKILL.md](SKILL.md); this folder installs independently. No scripts, MCP servers, model subscriptions, framework dependencies, automatic shell commands, or tool pre-approvals are bundled.

## Use

Claude Code:

```text
/projectplan-builder Plan the smallest complete release from this brief. Planning only.
/projectplan-builder Use the current repository and supplied requirements. Do not implement.
/projectplan-builder Build the plan and save only the planning artifact at the path I specify.
```

In Codex, use `$projectplan-builder` followed by the same request. Natural-language discovery uses the frontmatter description; do not expect identical trigger behavior from every model. An invocation without additional arguments uses the active project context, not an invented brief.

Use `projectplan-rescope` for the other planning mode. Neither skill implements its plan. An explicit save request may authorize saving the planning artifact, not code changes, commits, spending, migrations, or deployment. Read-only rules are behavioral instructions, not enforced tool isolation; retain host approval controls and use a read-only/plan-mode session for stronger protection.

## Install from this repository

Run this in a local checkout's **repository root**. It links the canonical folder rather than making a second editable copy and leaves any existing installation untouched.

```bash
skill="projectplan-builder"
source_dir="$PWD/skills/aarons-latest/$skill"
target="$HOME/.claude/skills/$skill"
# For Codex instead, set: target="$HOME/.agents/skills/$skill"
if [ ! -f "$source_dir/SKILL.md" ]; then
  printf 'Run from the My_AI_Skills repository root.\n' >&2
elif [ -e "$target" ] || [ -L "$target" ]; then
  printf 'Existing installation left unchanged: %s\n' "$target"
else
  mkdir -p "$(dirname "$target")" && ln -s "$source_dir" "$target"
fi
```

For project-local use, copy the whole folder into `.claude/skills/` for Claude Code or `.agents/skills/` for Codex, after checking that the destination is not an existing installation. Do not install two competing copies with the same name. Keep a linked repository checkout at its original location. If the skill does not appear, reload skills or restart the session as supported by the host.

Adding this folder to the GitHub library does **not** install it into your local clients.

## What is preserved and improved

Derived from Aaron's supplied principal-project-planner prompt. Preserves the project contract, strict leanness test, conditional current research, smallest coherent architecture, outcome phases, compact task contracts, dependency-safe parallelism, honest estimation, A–F output order, first execution handoff, and final quality gate. Rescope-specific KEEP/SIMPLIFY/MERGE/DEFER/REMOVE and approval rules live in the rescoping skill rather than bloating the builder.

Packaging improvements: separate trigger boundaries, focused repository inspection, portable frontmatter, no forced agent/model framework, explicit baseline/approval provenance, and independently installable runtime instructions. Rescoping adds delta-first updates, transitive dependency repair, superseded-ID continuity, and a no-material-change outcome. These are design choices, not benchmarked speedup claims.

## Regression evaluation

[evals/evals.json](evals/evals.json) contains 8 self-contained prompts, expected outputs, and assertions. No external fixture files or paid evaluation service are required by the package. Running models may incur your normal usage costs.

**Fresh-model behavioral evaluation: not run in the authoring environment.** Claude Code and Codex executables were unavailable. Static packaging checks are not behavioral benchmarks, and self-review is not independent verification.

Run cases in isolated read-only sessions using the same model/settings both without the skill and with it. For routing cases, test natural-language discovery rather than forcing the wrong skill. Inspect outputs **and tool calls**, score every assertion, and record passed/failed/not run. Repeat safety-critical cases to detect inconsistent behavior. Do not treat word matches or merely repeating a rule as evidence of compliance.

## Packaging references

Checked September 27, 2026; these describe packaging/discovery, not measured delivery gains:

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Agent Skills specification](https://agentskills.io/specification)
