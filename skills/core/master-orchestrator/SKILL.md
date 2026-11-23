---
name: master-orchestrator
description: Use when someone explicitly asks which available skill should own an unfamiliar task, several specialists appear to overlap, or they need a short handoff between domains. Return one recommendation with its canonical path, required resources and reason.
metadata:
  author: aaron-deyoung
  version: "2.0.0"
  domain-category: core
  adjacent-skills: project-router
  last-reviewed: "2026-11-21"
  review-trigger: "A change to registry fields, curated sets, agent fences, or project lifecycle ownership."
---

# Select a skill

Use this skill to answer a selection question. A clear request for a known specialist goes directly to that skill. For starting, resuming, rescoping or closing a project, hand ownership to the project router.

1. Identify the deliverable, intended audience, available tool and private workspace. A work task, family study and client deliverable each have their own context.
2. From a full checkout, use `python scripts/skill-picks.py list` or look up the canonical entry in [the skill registry](../../../registry/skills.json). Use the current agent's index when it has one. In a standalone installation, select from the host's visible skills or ask for the relevant entry. Use the skill's complete package and required sibling references.
3. Prefer an eligible core or optional skill whose trigger matches the outcome. Check host scope, review status and manual-only policy. Recommend a manual-only skill by name for the user to select. For a fenced skill, identify its required host. A useful answer can also be “the available general instructions are sufficient.”
4. Return the primary skill, its source path and a one-sentence reason. Add a supporting skill only if it supplies a necessary input or a distinct next deliverable. Name the artifact passed between them. Use the permissions already granted for the task.

For example, a teacher who needs discussion questions can start with the group-study leader and its Bible study foundation. A request for a publishable summary starts a separate public draft using only the approved study material. A second client receives a fresh consulting context.

## Failure behavior

If the canonical package or required material is unavailable, identify the missing resource. If the tool cannot invoke it directly, offer its accessible instructions as a manual workflow. A routing decision alone does not start an installation, external action or public post.
