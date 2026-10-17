# projectplan-roadmap v1.0.0

Save an existing or approved plan into the project as one concise, prescriptive roadmap file named `YYYYMMDD - <Project Name> - <Title>.md`. The runtime is entirely in [SKILL.md](SKILL.md); this folder installs independently.

## Use

Claude Code:

```text
/projectplan-roadmap Write this plan to the project with the proper naming convention, then stop.
/projectplan-roadmap Save the rescope output as the roadmap next to the existing ALM docs.
```

In Codex, use `$projectplan-roadmap` followed by the same request.

Family: `projectplan-builder` creates a first plan, `projectplan-rescope` revises one, `projectplan-roadmap` saves it as an executable file, `workbetter` executes it.

## Naming convention

```text
YYYYMMDD - <Project Name> - <Title>.md
20261017 - Job Scraper - Owner Feedback Loop Roadmap.md
```

The H1 inside the file equals the filename without `.md`. Placement follows the project's existing dated-doc folder (for example `docs/alm/`), else `docs/plans/`, else `docs/`.

## Install

From the repository root:

```bash
(
skill="projectplan-roadmap"
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

On Windows without symlink rights, copy the folder instead of linking it.
