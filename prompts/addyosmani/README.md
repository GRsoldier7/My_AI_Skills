# Addy workflow prompts

Nine workflow prompts are adapted from Addy Osmani release 0.6.14 at `eb07f19f52c2669f2364897aaa293e2aaddd7b1c`.
Original source: https://github.com/addyosmani/agent-skills/tree/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/.claude/commands
MIT attribution is retained in LICENSE.

The prompts are manual task entrypoints, not globally installed slash commands.
The agent-skills plugin prefix was removed so they reference canonical library
skills. Addy's TDD identity is `addy-test-driven-development`; Superpowers retains
`test-driven-development`. `$ARGUMENTS` means the current user's explicit prompt
arguments when the receiving host has no command substitution.

Hermes remains the coordinator. Select one prompt for the current phase and
only the specialists it needs. Never stack automatic controllers. A ship prompt
prepares a review/rollout recommendation; it does not grant deployment authority.
For Parallon, browser checks use approved Playwright CLI or supplied evidence.
Do not activate the Chrome DevTools MCP package, session hooks, automatic package
downloads, or a competing meta-skill. ChatGPT can draft/review but must label
runtime checks it could not execute.
