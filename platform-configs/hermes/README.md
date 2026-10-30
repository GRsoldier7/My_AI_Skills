# Hermes Teams source selection

The expanded selections, staged exports, runtime limits and receiving-host checks
are in the [Platform Delivery Guide](<../../docs/20261029 - My AI Skills - Platform Delivery Guide.md>).
The source catalog separates skills, personas and prompts; importing files does
not register or activate them on this host.

[hermes-teams](../skill-sets/hermes-teams.txt) selects ECC's portable team-agent
orchestration, agent-harness construction and Hermes import guidance. Four
candidate personas live under `agents/ecc/`; they need Hermes-compatible tool
mapping and one synthetic team run before use. This import installs no runtime.

`team-builder` is stored as reference-only because upstream discovers agents using
`claude agents` and Claude directories. ECC's agentic-patterns module does not
currently declare Hermes as an install target, and its orchestration runtime
supports other hosts. Do not treat a minimal Hermes install as complete team setup.

Sources pinned to ECC `91b5f6a371f7b06d2c3e0c208147c559e11f022c`:

- [Hermes adapter](https://github.com/affaan-m/ECC/blob/91b5f6a371f7b06d2c3e0c208147c559e11f022c/.hermes/README.md)
- [Hermes setup](https://github.com/affaan-m/ECC/blob/91b5f6a371f7b06d2c3e0c208147c559e11f022c/docs/HERMES-SETUP.md)
- [Opt-in Hermes hooks](https://github.com/affaan-m/ECC/blob/91b5f6a371f7b06d2c3e0c208147c559e11f022c/docs/HERMES-HOOKS.md)

ECC Memory Vault requires its separate runtime; the vendored skills do not supply
it. Hooks and configuration need a separate target-specific setup. Preserve Hermes
config, credentials and memory on their existing private host.

Superpowers also offers a Hermes plugin which injects its bootstrap and registers
skills. Choose it deliberately as the workflow owner; do not enable it alongside
another automatic controller. No Hermes service, listener, hook or config was
changed by this library import.
