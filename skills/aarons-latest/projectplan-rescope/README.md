# projectplan-rescope v1.1.0

Revise an existing delivery baseline after scope, deadline, capacity, evidence, blockers, approvals, or implementation findings change. The runtime is entirely in [SKILL.md](SKILL.md); this folder installs independently.

## Use

Claude Code:

```text
/projectplan-rescope Rescue this overbuilt plan while preserving mandatory outcomes.
/projectplan-rescope Update the approved baseline for this change request. Preserve unaffected IDs.
/projectplan-rescope Reconcile current evidence with the plan and show only the affected delta.
/projectplan-rescope Audit the baseline; keep it unchanged if no material improvement is justified.
```

In Codex, use `$projectplan-rescope` followed by the same request. Use `projectplan-builder` when there is no delivery baseline for the requested scope.

The skill plans; it does not implement. A save request can authorize the specified planning artifact only, not code changes, deletion, commits, purchases, migrations, agent launches, or deployment.

## Install

From the repository root:

```bash
(
skill="projectplan-rescope"
source_dir="$PWD/skills/aarons-latest/$skill"
target="$HOME/.claude/skills/$skill"
# Codex: target="$HOME/.agents/skills/$skill"

if [ ! -f "$source_dir/SKILL.md" ]; then
  printf 'Run from the My_AI_Skills repository root.\n' >&2
  exit 1
elif [ -e "$target" ] || [ -L "$target" ]; then
  printf 'Existing installation left unchanged: %s\n' "$target"
else
  mkdir -p "$(dirname "$target")" && ln -s "$source_dir" "$target"
fi
)
```

For project-local use, copy the whole folder into `.claude/skills/` or `.agents/skills/`. Avoid competing installations with the same skill name.

## Design

The skill is intentionally **delta-first**. It treats the current approved baseline plus newer verified evidence as the starting point and changes only what the new evidence or constraint justifies.

It preserves the source prompt's strict leanness, KEEP/SIMPLIFY/MERGE/DEFER/REMOVE disposition, stable IDs, dependency-safe parallelism, honest estimation, A–F structure, release gates, and execution handoff.

### v1.1.0 refinements

- Establishes an authoritative baseline instead of silently blending conflicting plans.
- Separates reported status from verified evidence and preserves useful history when evidence is invalidated.
- Computes change trigger and blast radius before rewriting tasks.
- Optimizes the real release bottleneck rather than general plan aesthetics.
- Repairs transitive dependencies and superseded-ID references.
- Explicitly budgets switching, migration, coexistence, review, integration, and rollback costs.
- Caps active parallel lanes by implementation plus review/integration capacity.
- Produces an unblock request when nothing is genuinely executable.
- Stops with **no material change** when the baseline is already the strongest defensible path.

These are architecture choices, not claims of measured speedup.

## Evaluation

The existing regression suite at [evals/evals.json](evals/evals.json) covers overbuild rescue, approval boundaries, evidence invalidation, ID-preserving merges, delta-only updates, no-change outcomes, transitive dependencies, missing baselines, unsafe parallelism, and approved scope reductions.

Fresh-model behavioral evaluation is not claimed unless actually run. Evaluate in isolated read-only sessions using the same model/settings with and without the skill. Inspect outputs and tool calls; record assertions as passed, failed, or not run.

## Packaging references

Checked September 27, 2026:

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Agent Skills specification](https://agentskills.io/specification)
