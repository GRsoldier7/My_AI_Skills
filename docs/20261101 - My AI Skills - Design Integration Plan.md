# 20261101 - My AI Skills - Design Integration Plan

**Goal:** Add Impeccable, Taste Skill, UI/UX Pro Max and Chrome DevTools MCP to the repository and install for this Mac's Codex and Claude hosts.

**Architecture:** Keep canonical skill packages under skills/design, an additive design.txt set, per-file pinned provenance and a separate MCP configuration. Preserve the existing network-volume checkout, default global set and project-router bundle.

**Tech stack:** Existing Bash installer, Python 3, Node 26, installed Brave browser.

- [x] Copy complete pinned skill packages with upstream licenses. Adapt only UI/UX Pro Max's plugin-only search path for portable user-scope use; record original and adapted hashes.
- [x] Review exact package bytes, security findings and references before global installation.
- [x] Add separate design usage/routing documentation and isolated Chrome DevTools MCP configuration with telemetry and CrUX disabled.
- [x] Run provenance/reference verification, repo validators and installer tests; smoke-test local retrieval and browser tooling.
- [x] Install globally without pruning or replacing unmanaged skills/configuration. Verify discovery and MCP launch; report session reload boundary.
- [x] Present concrete checked diff for the repository's explicit commit/push/PR approval gate. Do not merge.

**Review focus:** Existing skill names and unmanaged directories; platform-specific search paths; missing references/assets; browser-profile separation; integrity of upstream code and licenses. Global setup is authorized by the user. Publishing remains subject to the repository's explicit gate.

## Current disposition

Static and runtime checks are complete. The owner approved proceeding; all four items are installed globally. GitHub publication is recorded separately after it succeeds. See Installation Results.
