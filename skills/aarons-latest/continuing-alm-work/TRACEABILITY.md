# Source Directive Traceability

This release preserves the original directive's behavioral requirements while moving infrequently needed detail out of the always-loaded `SKILL.md`.

| Source requirement area | v2 implementation |
|---|---|
| Role and mission | `SKILL.md` overview, modes, non-negotiables, and six-stage workflow |
| Runtime inputs and missing evidence | `SKILL.md` baseline capture plus `references/state-and-evidence.md` discovery and missing-evidence rules |
| Evidence before assumption | `SKILL.md` non-negotiables and `references/state-and-evidence.md` authority, evidence order, status model, and reconstruction checklist |
| Execute rather than merely advise | `SKILL.md` resume mode, execute-by-default rule, and next-unit selection |
| Optimize for leverage, not activity | `SKILL.md` smallest-sufficient-orchestration rule plus `references/execution-routing.md` priority and over-orchestration rules |
| Preserve continuity | `SKILL.md` persistence stage, `assets/execution-state-template.md`, and exact `RESUME FROM` contract |
| Ask only necessary questions | `SKILL.md` one decision-changing-question rule and independent-work continuation |
| Discover and reconcile state | `SKILL.md` stages 1–2 and `references/state-and-evidence.md` |
| Normalize and improve the plan | `SKILL.md` stage 3 and `references/execution-routing.md` task contract, priority, and lifecycle lens |
| Dependency-aware execution map | `references/execution-routing.md` parallel, sequential, and integration classifications |
| Best-fit capability assignment | `SKILL.md` specialist-skill routing and `references/execution-routing.md` capability/delegation contracts |
| Execute highest-leverage work | `SKILL.md` stage 4 and `references/execution-routing.md` priority and recovery rules |
| Verify and challenge work | `SKILL.md` stage 5 plus `references/verification-and-safety.md` claim-to-evidence and quality-gate rules |
| Approval and safety boundaries | `SKILL.md` approval boundary plus `references/verification-and-safety.md` work preservation, approval request, and trust controls |
| Skill-candidate detection and approved builds | `references/checkpoints-and-skill-candidates.md` proposal gate and post-approval production contract |
| Required response structure | `SKILL.md` compact normal iteration and conditional full checkpoint; `references/checkpoints-and-skill-candidates.md` preserves all material checkpoint fields |
| Communication standards | `SKILL.md` compact output/no-fabrication rules and all references' evidence-first wording |

## Intentional Efficiency Changes

- The original seven-part response remains available at real handoff boundaries, but routine turns use four delta fields so reporting does not crowd out execution.
- Detailed evidence, routing, verification, checkpoint, and skill-authoring rules load only when their conditions apply.
- The bundled state-capture utility discovers evidence locations and Git state without reading arbitrary project source or modifying the workspace.
- Focused specialist skills own planning, testing, debugging, review, deployment, and domain execution; this skill coordinates rather than duplicating them.

These changes alter frequency and placement, not the directive's safety, evidence, execution, continuity, or approval requirements.
