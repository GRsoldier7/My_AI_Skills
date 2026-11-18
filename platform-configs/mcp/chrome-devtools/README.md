# Chrome DevTools MCP

Status: **reviewed, installed and smoke-tested on the owner’s Mac**.
The latest published package checked on 2026-11-01 is `chrome-devtools-mcp@1.12.0`.
The scanner flagged its Zod dependency, but the current
[primary CVE record](https://github.com/CVEProject/cvelistV5/blob/main/cves/2023/54xxx/CVE-2023-54404.json)
marks CVE-2023-54404 REJECTED on October 28. Earlier active-vulnerability language
was incorrect. See the [corrected review](../../../docs/20261101%20-%20My%20AI%20Skills%20-%20Design%20Intake%20Review.md).
The inspected bundle contains Zod 4.6.5; a source lockfile resolving 4.6.7 does not
change the published bytes. No patched-release requirement follows from the rejected
CVE. Raw scanner outcomes are preserved with their reviewed dispositions and owner proceed authorization.

[source.json](source.json) records the inspected upstream commit and exact npm
tarball integrity. Preserve the Apache-2.0 license when redistributing the package.
The runtime is not vendored into this repository.

## Intended configuration

The [Codex template](codex.toml) is an example server table. The
[Claude template](claude.json) is a merge fragment, not an active configuration.
Use one isolated, headless browser instance for task pages, with MCP usage metrics
and CrUX requests disabled. Do not use `--autoConnect`, a debugging URL, the
everyday browser profile or a persistent `--user-data-dir`.

After the inspected release passes intake, retain its exact version in both templates and
set an absolute `--executablePath` appropriate to the device. On the inspected Mac,
the installed browser is `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser`;
Node is already present. Brave compatibility still requires a live smoke test.
Use an absolute `npx` path if the desktop host does not inherit the shell PATH.

Merge only the new `chrome-devtools` server into each host's existing user config,
preserving every other entry and making a local backup first. Use `codex mcp add`
and `claude mcp add-json --scope user` when practical; do not replace whole config
files. No credentials are required. Reconnecting/restarting the host is a separate
step from writing configuration.

## Verification required before reporting operational

1. Confirm the exact runtime version, tarball integrity and the current disposition of dependency findings.
2. Initialize MCP and list tools; verify the new entry through each host CLI.
3. Open a benign local HTML fixture in the isolated browser, inspect it, and save a screenshot.
4. Confirm normal browser windows/profile were not attached to or changed.
5. Report whether tools are available in a new session; do not imply the current
   conversation gained live tools just because config was written.

## Verified installation on 2026-11-01

The Mac uses the integrity-verified extracted npm package under
`~/.local/share/my-ai-design-tools/chrome-devtools-mcp/1.12.0/`, launched with an
absolute Node path. Both hosts have user-scope registration. Claude's connection
check succeeded; the direct MCP handshake exposed 32 tools. Navigation, a button
interaction and screenshot writing passed against a benign local page. The client
negotiated a narrow workspace root; unrestricted filesystem access was not enabled.
The current chat's live tool catalog is separate from these host registrations.

Startup update checks are also disabled with `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS=1`.
Use a new host session to load the changed configuration.
