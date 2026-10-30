---
name: playwright-cli
description: Plan and review browser checks using Playwright CLI concepts without assuming a local CLI in ChatGPT.
---

# Playwright CLI — ChatGPT browser-check guidance

Instruction-only adaptation of Microsoft's Playwright CLI skill, Apache-2.0, reviewed CLI 0.1.22 and source revision `b85c7a736bb473bf55b584e54a09ffa698d6d871`. ChatGPT skill installation does not supply a terminal, browser executable, extension or MCP server. Never install those, invent execution results, or claim that a written test plan ran.

If this host already exposes an approved browser tool, follow that tool's documented controls. Otherwise prepare the verification plan and interpret evidence the user supplies.

For an authorized page or synthetic local artifact:

1. Identify the exact URL/file and expected behavior. Prefer a new disposable session; do not reuse authenticated accounts without task authorization.
2. Capture page structure, then select stable accessible names/roles or fresh observed element references. Refresh references after navigation or meaningful DOM changes.
3. Exercise the main path and an edge case: empty/invalid inputs, no results, long text, failed request or denied access as applicable. Verify visible outcomes, not merely that an action returned.
4. Check desktop and mobile layouts, keyboard operation, focus, labels, overflow, errors and reduced-motion behavior.
5. Capture only necessary evidence. Cookies, authentication state, tokens, private payloads, browser profiles and sensitive traces stay out of published artifacts and Git.
6. Report the tested target, actual actions, observations and remaining unknowns. Distinguish executed checks from proposed test steps.

For a Copilot handoff, the separate full package uses an approved installed CLI/browser and `NO_UPDATE_NOTIFIER=1`; project fallback commands retain `npx --no-install`. This guidance never authorizes runtime acquisition, global configuration or account actions.

[Complete pinned CLI skill/reference](https://github.com/microsoft/playwright-cli/tree/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli).
