---
name: list-skills
description: List the current library's recommended skill sets or find a named specialist by domain, using the canonical registry.
---

# List available skills

For a broad request, show the current profile names, purposes and sizes using `python scripts/skill-picks.py list`. For a domain or name, read `registry/skills.json` and return the matching name, status, canonical path and scope. If the user asks for the full inventory, show the registry totals and direct them to that file or list the requested domain.

Use `agents/README.md` to find an agent's curated index. Report separately what the current Claude session actually exposes. A repository entry alone does not establish native installation.
