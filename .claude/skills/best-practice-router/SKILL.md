---
name: best-practice-router
description: Use when a user explicitly requests the legacy best-practice-router command to choose an appropriate project or domain workflow.
disable-model-invocation: true
---

# Choose a workflow

This project-local command is a compatibility entry point. For startup, resumption, rescoping or closeout, hand the request to `skills/aarons-latest/project-router/SKILL.md`. For a domain selection question, use `skills/core/master-orchestrator/SKILL.md` and its canonical registry. Give one owner and the reason it fits. Open the requested specialist directly when the user already named it.

Use Claude project helpers only when they are available and specifically relevant. Leave model settings, installations and shared workspaces under their existing project configuration.
