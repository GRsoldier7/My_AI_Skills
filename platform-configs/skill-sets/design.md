# Design skill set

Status: **reviewed and installed on the owner's Mac on 2026-11-01**. Raw scanner
findings and their dispositions are documented in the
[intake review](../../docs/20261101%20-%20My%20AI%20Skills%20-%20Design%20Intake%20Review.md)
and [approval scope](../../docs/20261101%20-%20My%20AI%20Skills%20-%20Design%20Approval%20Scope.md).
The owner approved proceeding after being notified of the review. Future updates
must be rescanned; this acceptance applies to the recorded pins only.
The default `global.txt` is unchanged.

| Skill | Primary role | Invocation |
| --- | --- | --- |
| [Impeccable](../../skills/design/impeccable/SKILL.md) | Default frontend design, critique and finishing | `$impeccable polish` in Codex; `/impeccable polish` in Claude |
| [Taste Skill](../../skills/design/design-taste-frontend/SKILL.md) | Distinctive art direction and screenshot refinement | `$design-taste-frontend` / `/design-taste-frontend` |
| [UI/UX Pro Max](../../skills/design/ui-ux-pro-max/SKILL.md) | Searchable product design guidance and design systems | `$ui-ux-pro-max` / `/ui-ux-pro-max` |

Use one primary design approach per task. Default to Impeccable for improving an
existing interface; choose Taste for a new site where a distinctive visual concept
is central; use UI/UX Pro Max for dashboard/product patterns and targeted reference
queries. Preserve the project's brand, stack, content and behavior. Load specialist
references only for the current pass. Inspect desktop and mobile rendering before
claiming completion. Native skill descriptions may overlap; availability does not
mean loading all three bodies into every conversation.

## Installation after intake approval

Use a persistent local clone. The existing installer creates symlinks; deleting or
moving that clone breaks installed skills. Preview first:

```sh
python3 scripts/verify-design-imports.py
bash scripts/install-skills.sh --set platform-configs/skill-sets/design.txt
# After owner intake approval:
bash scripts/install-skills.sh --set platform-configs/skill-sets/design.txt --apply
bash scripts/install-skills.sh --set platform-configs/skill-sets/design.txt
```

Targets are `~/.claude/skills/` and `~/.agents/skills/` (Codex). Do not also copy
the same skills into `~/.codex/skills/`: duplicate discovery can obscure which
package is active. Do not use `--prune`; it removes links installed by other sets.
Existing unmanaged files must be reviewed rather than overwritten. Reload the
host's skill catalog in a new session; this does not install tools into an already
running ChatGPT session or into other devices.

Impeccable's engine is a separate checksum-verified download on first use, pinned
by `scripts/VERSION` and `engine-checksums.txt`. Its optional hooks are not installed
by this set. Taste needs Node 22+ and a Chrome-family browser; its scripts support
Brave on macOS and use temporary profiles. UI/UX Pro Max's retrieval uses Python 3
without third-party runtime dependencies. Public image/font search can contact
external services: do not pass private project details as search queries.

## Provenance and adaptation

[design-sources.json](design-sources.json) records full upstream commits, source
paths, versions, licenses and SHA-256 for every file. Packages include all scripts,
references, data and assets. Impeccable and Taste retain upstream bytes. UI/UX Pro
Max retains all upstream code/data; only its `SKILL.md` replaces Claude-plugin-only
paths with an explicit absolute skill-directory placeholder. Its original and
adapted hashes are recorded. The verifier can compare all files against a supplied
directory containing the three upstream Git clones.

The older `.claude/skills/frontend-design` and `design-*` project-local skills are
unchanged. They are legacy alternatives, not aliases for these packages. When
working in this repository, explicitly select the new named skill to avoid their
incomplete command chain. No seven-skill Project Router bundle changes are needed.

Chrome DevTools MCP is a separate [tool configuration](../mcp/chrome-devtools/README.md),
not an extra design skill.
