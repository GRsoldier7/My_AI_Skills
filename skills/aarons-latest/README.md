# Aaron's newest project skills

For multi-step project lifecycle work, start with **project-router**. It chooses
one justified workflow; this table is not a pipeline to execute in full.

| Skill | Responsibility |
|---|---|
| [project-router](project-router/SKILL.md) | Select the next workflow from evidence of phase, maturity, exposure, and permissions. |
| [projectplan-builder](projectplan-builder/SKILL.md) | Create the first delivery baseline for a defined scope; planning only. |
| [projectplan-rescope](projectplan-rescope/SKILL.md) | Revise an existing baseline when evidence or constraints justify it; planning only. |
| [continuing-alm-work](continuing-alm-work/SKILL.md) | Reconstruct uncertain state and resume authorized work. |
| [workbetter](workbetter/SKILL.md) | Execute a ready bounded task with proportionate verification. |
| [clean-project](clean-project/SKILL.md) | Investigate lifecycle/security/usage and manage approved cleanup with optimizeproject.md. |
| [directory-cleanup](directory-cleanup/SKILL.md) | Organize directories and archives without unrelated refactoring or permanent deletion. |
| [grill-me](grill-me/SKILL.md) | Manual entry point (`/grill-me`) to a relentless interview that sharpens a plan or design; delegates to `grilling`. Vendored from mattpocock/skills. |
| [grilling](grilling/SKILL.md) | The interview primitive: asks the open frontier of design questions in numbered rounds with a recommended answer each, looks up facts itself, leaves decisions to you. Vendored from mattpocock/skills. |
| [grill-with-docs](grill-with-docs/SKILL.md) | Manual entry point (`/grill-with-docs`): the same interview, but stateful; runs `grilling` plus `domain-modeling` so decisions land in `GLOSSARY.md` and ADRs. Use it when working inside a repo. Vendored from mattpocock/skills. |
| [teach](teach/SKILL.md) | Manual (`/teach <topic>`): multi-session tutoring in the current directory as a teaching workspace (MISSION.md, RESOURCES.md, lessons, reference sheets, learning records). Vendored from mattpocock/skills. |
| [discount-codes](discount-codes/SKILL.md) | Find legitimate website or product discounts, compare actual costs, and label verification evidence. |
| [adaptive-research](adaptive-research/SKILL.md) | Research questions and compare options through broad discovery, verified evidence, and concise recommendations. |

`grill-me`, `grilling`, `grill-with-docs` and `teach` are third-party (MIT, byte-identical to upstream at a pinned commit; provenance in
[platform-configs/skill-sets/README.md](../../platform-configs/skill-sets/README.md#provenance-third-party-vendored)).
They are not part of the project-router workflow set and are not packaged by `scripts/project-router.py`.

Reuse existing specialists for diagnosis, review, verification, release, and
checkpointing. Their presence is checked at runtime; they are not new required
installations. One active execution owner, no recursive controller chains.

[ChatGPT/Codex installation and updates](../../../platform-configs/openai/project-router/README.md)
