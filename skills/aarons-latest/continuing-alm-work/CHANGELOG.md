# Changelog

## 2.0.0 - 2026-09-30

- Rebuilt the original 553-line ALM continuation directive as a native Claude Code skill.
- Reduced always-loaded instructions while preserving evidence, execution, safety, continuity, and verification requirements.
- Added progressive-disclosure references for approvals, delegation, checkpoints, and skill proposals.
- Added explicit compatibility with the separate `context-checkpoint` workflow.
- Added dirty-working-tree protection, plan-only behavior, evidence-scope completion rules, and non-blocked-work continuation.
- Replaced the earlier custom evaluation layout with Anthropic skill-creator's current `evals/evals.json` schema.
- Added a dependency-free package validator.

## 1.0.0

- Initial evaluation concept and ALM continuation prompt.
