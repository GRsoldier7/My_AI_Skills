# Skill-Candidate Proposal

A workflow is a credible skill candidate when it is repeated or predictably recurring, follows a stable sequence, has clear inputs and outputs, is error-prone or time-consuming, contains durable knowledge, or would materially improve consistency across projects.

Do not build hidden scaffolding, implementation files, or a materially complete skill before approval.

## Proposal format

1. **Name and trigger:** proposed kebab-case name and concrete activation conditions.
2. **Problem and evidence:** repeated failure, recurrence, or expected reuse.
3. **Value:** quality, time, risk, or token savings; avoid false precision.
4. **Users and scope:** intended workflows plus explicit non-goals.
5. **Inputs and outputs:** required context, artifacts, and output contract.
6. **Workflow and routing:** core steps; tools, connectors, agents, and permissions actually needed.
7. **Guardrails:** approval boundaries, safe defaults, failure handling, retry, and recovery.
8. **Acceptance and evaluation:** positive, negative, and edge cases; evidence of success.
9. **Ownership:** versioning, maintenance, deprecation, and observability.
10. **Decision:** ask exactly, `Should I build this skill based on the proposal above?`

Continue the current project while approval is pending unless the proposed skill is itself a critical dependency. After approval, build production-quality behavior rather than wrapping the repeated prompt unchanged.
