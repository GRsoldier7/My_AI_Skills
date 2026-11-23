---
name: work-instruction-review
description: Improve a work prompt, reusable SKILL.md or ChatGPT plugin specification when outputs drift, activation is unreliable, or instructions are expensive to use. Return the smallest tested revision, the correct delivery format and release criteria for the intended workspace.
metadata:
  version: "1.0.0"
  domain-category: core
  last-reviewed: "2026-11-21"
  adjacent-skills: prompt-master, skill-creator, agent-regression-evals
  review-trigger: "A failed work fixture, changed host permissions or changed upstream guidance."
---

# Optimize a prompt, skill or plugin

Start with one real failure described using synthetic content, the intended host, and an example of an acceptable answer. If there is no baseline, label the first version a design proposal and keep an untouched copy. Select one path.

| User needs | Path |
| --- | --- |
| Better results from a specific request | [Prompt revision](references/prompt-review.md) |
| A reusable procedure that triggers correctly | [Skill evaluation](references/skill-evaluation.md) |
| A new ChatGPT workflow, project brief or Space page system | [ChatGPT authoring and Spaces](references/chatgpt-spaces.md) |
| Better ChatGPT plugin discovery, tool selection or instructions | [Plugin evaluation](references/plugin-evaluation.md) |

Use the available workspace. An instructions-only ChatGPT Enterprise project can draft and evaluate text manually. GitHub Copilot can review supplied project files. Keep tool execution, tenant connections, publishing, and installation outside a drafting task. Return the revised artifact, a short change rationale, and a small table of observed or expected results.

For a general prompt-writing reference, the catalog already contains Prompt Master. The skill creator and agent regression evaluation packages are available for deeper authoring or engineering work in an approved environment.
