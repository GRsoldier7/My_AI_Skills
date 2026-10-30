---
description: Start spec-driven development — write a structured specification before writing code
disable-model-invocation: true
---

This is a portable task prompt adapted from an upstream Claude command. Use the current host's skill mechanism or read the named canonical skill explicitly. Command names are labels; importing this file does not register a slash command. Preserve current task authorization, repository policy, and one workflow owner.


Invoke the spec-driven-development skill.

Begin by understanding what the user wants to build. Ask clarifying questions about:
1. The objective and target users
2. Core features and acceptance criteria
3. Tech stack preferences and constraints
4. Known boundaries (what to always do, ask first about, and never do)

Then generate a structured spec covering all six core areas: objective, commands, project structure, code style, testing strategy, and boundaries.

If the request bundles several independently testable capabilities, first propose a capability map (module ids, dependency direction, build order) per the skill's Phase 0 and get it approved, then spec each module in dependency order.

Save the spec as SPEC.md in the project root and confirm with the user before proceeding.
