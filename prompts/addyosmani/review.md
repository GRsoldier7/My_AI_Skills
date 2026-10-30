---
description: Conduct a five-axis code review — correctness, readability, architecture, security, performance
disable-model-invocation: true
---

This is a portable task prompt adapted from an upstream Claude command. Use the current host's skill mechanism or read the named canonical skill explicitly. Command names are labels; importing this file does not register a slash command. Preserve current task authorization, repository policy, and one workflow owner.


Invoke the code-review-and-quality skill.

Review the current changes (staged or recent commits) across all five axes:

1. **Correctness** — Does it match the spec? Edge cases handled? Tests adequate?
2. **Readability** — Clear names? Straightforward logic? Well-organized?
3. **Architecture** — Follows existing patterns? Clean boundaries? Right abstraction level?
4. **Security** — Input validated? Secrets safe? Auth checked? (Use security-and-hardening skill)
5. **Performance** — No N+1 queries? No unbounded ops? (Use performance-optimization skill)

Categorize findings as Critical, Required, Optional, or Nit.
Output a structured review with specific file:line references and fix recommendations.
