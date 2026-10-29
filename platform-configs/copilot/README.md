# GitHub Copilot delivery

Select [work-copilot-coding](../skill-sets/work-copilot-coding.txt) for the
Superpowers coding workflow plus Karpathy guidelines and frontend design.
The same shared workflow is available as home-coding, consulting-coding and
business-coding. Keep actual work, client and personal context in separate projects.

## Skills, agents and prompts

Current [GitHub documentation](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
and [VS Code documentation](https://code.visualstudio.com/docs/agent-customization/agent-skills)
describe skill discovery, including `.github/skills/`, `.claude/skills/`, and
`.agents/skills/`. Check the actual client and version. Preserve each complete
selected skill directory. The existing Bash installer targets Claude/Codex only;
it does not install into Copilot directories.

ECC agent source files are in `agents/ecc/`; Copilot prompt templates are in
`prompts/copilot/`. Use the supported [custom-agent format](https://code.visualstudio.com/docs/agent-customization/custom-agents),
not an unchanged Claude tool list. ECC's Copilot adapter translates agents and
installs selected helpers; it does not install ECC hooks, rules or command shims.

## Full Superpowers plugin option

The upstream [v7.0.1 README](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b#github-copilot-cli)
documents Copilot CLI marketplace installation. Run these only on the intended
approved client when choosing the full plugin instead of duplicate skill copies:

```sh
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

Marketplace installation follows the marketplace's version, not this repository's
pinned snapshot. Use one workflow controller per task; do not stack Superpowers
with the lifecycle router. Optional Superpowers visual-companion code can make an
external logo request; `SUPERPOWERS_DISABLE_TELEMETRY=1` disables that feature.

Library validation is not work-client activation evidence. No Copilot account,
employer repository, hooks, MCP servers or global instructions were changed.
