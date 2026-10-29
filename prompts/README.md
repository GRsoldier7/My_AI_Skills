# Reusable prompts

`copilot/` contains five upstream ECC prompt templates: plan, build-fix, refactor,
security-review, and tdd. Their MIT license is bundled. Pins and hashes live in
[artifact-sources.json](../platform-configs/artifact-sources.json).

Prompts are reusable task starters. Multi-step procedures with supporting assets
belong in `skills/`; personas and specialist roles belong in `agents/`.
Keep embedded prompts required by a skill inside that skill package.

To use a template with a supported Copilot client, copy the selected `.prompt.md`
file to the approved project's `.github/prompts/` directory and verify discovery.
No employer repository or tool settings were changed by this library import.
