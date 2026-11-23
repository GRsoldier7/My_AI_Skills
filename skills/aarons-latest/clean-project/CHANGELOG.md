# Changelog

## 2.0.0 - 2026-10-03

- Rebuilt to the Agent Skills format: trigger-first description, metadata block, and a SKILL.md cut to the operating contract.
- Register schema 2: local-offset timestamps, an `Outcome` row, and a three-value output contract; one-edit migration from schema 1.
- Added `scripts/register.py` (read-only check and next ID), `agents/openai.yaml`, and five evals.
- Audit is change-aware by default; scheduled-run rules moved to `references/runner-contract.md`; dropped the tool-research section.

## 1.0.0

- Initial audit, apply, and verify skill with the root `optimizeproject.md` register.
