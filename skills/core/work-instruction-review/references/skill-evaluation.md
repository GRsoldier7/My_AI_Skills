# Optimize reusable skills

Keep the trigger description close to what the user would say. Identify the input, expected deliverable, tools actually needed, and what to return when a tool or source is missing. Split long examples from the SKILL.md entry point. Check that the distribution includes each required reference and license.

Use a tiny labeled set before editing: a direct request, an implied request, two near misses that belong to adjacent skills, missing evidence, and an empty input. Record expected activation and expected output for each. Run baseline and candidate separately using the same model and host settings when available. Manually supplying instructions tests output quality; automatic discovery requires a host trial with the skill registered.

Score correct activation, false activation, verified task checks, unsupported claims, and effort to correct the result. Rewrite one weak trigger or step at a time. Hold back a new example until after the edit. Keep the previous package if any high-impact near miss begins activating. A small sample supports a pilot decision. [Agent Skills specification](https://agentskills.io/specification)
