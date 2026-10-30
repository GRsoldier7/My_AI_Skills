# REA runtime reference

The canonical procedure is `skills/engineering/reverse-engineer-anything`. REA is an external runtime, not vendored application code.

- Source: https://github.com/morluto/rea/tree/160d821ac9a0310afcb8d1fc427862dd6508add5
- Reviewed version: 6.8.0; immutable source revision `160d821ac9a0310afcb8d1fc427862dd6508add5`.
- Core CLI package `rea-agents` 6.8.0 requires Node `^22.23.4 || ^24.22.1 || >=26.12.1`; individual operations need approved engines such as Ghidra/JADX or native SQLite support. Check the selected operation and pinned upstream package requirements before installing.
- Parallon: approved CLI only, no MCP, automatic setup, engine acquisition, policy repair, or hooks.
- ChatGPT: supplied evidence review only, via the explicit adapter.
- Store analysis artifacts in the authorized project/private workspace; no binaries, credentials, process dumps or private evidence belong in this public library.

This import did not install or activate REA. Retain its MIT license and disclaimer with the skill. Target-specific execution requires a selected authorized artifact and actual-host verification.
