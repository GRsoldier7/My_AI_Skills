# 20261101 - My AI Skills - Design Approval Scope

Owner approved proceeding with the four requested items after notice that intake findings were being reviewed. The following review dispositions explain why no undisclosed material security finding remains established. Raw scanner reports and scores are preserved; scanner rules were not disabled. Authorization covers the requested local global installation, verification, commit/push and draft PR; it does not cover merging or attaching to an everyday authenticated browser.

## Impeccable: 29 scanner findings

- `scripts/live-browser.js:7431` and `:7553` (E1): executable POST requests to `http://localhost:<PORT>` carry target results/claims to its local preview server. This is actual local browser communication, not the claimed external exfiltration. It runs during the live design workflow, not simply by linking the skill.
- `reference/document.md:411`, `reference/delight.md:55`, `reference/audit.md:139` and `reference/audit.native.md:139` (EA2): negative instructions forbid overwriting context without asking, sound without consent, and unverified false-positive reports. These are instruction text, not destructive execution.
- `reference/new-work.md:55`: changes a standing design default without re-asking only when the user explicitly requests that change. `reference/init.md:112` says one answer is not consent for another decision.
- `agents/impeccable_finish_reviewer.toml:21,22,36` and `reference/degraded/finish-reviewer.md:19,20,34`: reviewer checks identify unapproved design additions; no separate permissions are granted.
- `reference/critique.md:722` identifies absent UI action confirmation as a usability problem. `reference/colorize.md:23` and `reference/mode-operate.md:15` concern visual identity/interface state. `scripts/live-browser.js:1031` is a comment about persistent CSS selectors, not model memory modification.
- `reference/visualize.md:31,37`: actual workflow text permits choosing a design direction if both question mechanisms fail, while requiring disclosure. Host/user approval rules retain precedence; a tool failure is never user consent for a protected action.
- `reference/hooks.md:49` (RA2): optional project hook installation guidance. No hooks are enabled by this integration.
- `scripts/modern-screenshot.umd.js:14` (SC3): bundled screenshot encoding uses `String.fromCharCode`, not evidence of a hidden payload.
- Four Apache license phrase matches and missing scanner-specific permissions metadata (LP3) do not execute anything.

Actual extra capability: `scripts/impeccable:154–256` downloads a pinned engine from the project's GitHub release and verifies its packaged SHA-256 before execution. This is explicitly included in installation verification; it does not install arbitrary latest code.

## Taste Skill: 63 scanner findings

- `scripts/assets.mjs:15,63` (TM1 HIGH) document `--no-check`. Actual behavior at `:145,618` skips testing whether asset URLs load. It does not disable TLS validation, browser security, or the intake scanner. Default is to check.
- `scripts/assets.mjs:329,422,720,727` (E1) performs actual public image-provider GET requests; query text is sent to Openverse and Art Institute APIs. Downloads and credits are written at `:714,742,751,755`. Do not place private details in public search queries.
- Forty-eight E1 matches in `library/type.json` are font URLs stored as design data. They are not executed by scanning or installing, though a built page can request those fonts.
- `library/sites.json:1946,2664,2673,2697,2698` (PE3): descriptions of physical keyring/keychain imagery, not credential-store access. `library/photos.json:2632` (TM1): wave alt text containing the word curl, not a shell command.
- `library/sites.json:8271` (EA4) describes looping motion in a reference site. MIT-license wording and absent permissions metadata are non-executable matches.
- Actual browser behavior is in `scripts/lib/cdp.mjs:77–104`: create a temporary profile, launch a Chrome-family browser, terminate that child and remove its own temporary directory. No everyday user profile is selected.

Disposition: the HIGH findings do not represent security-control bypass. Accept the pinned candidate after this documented review and the owner's proceed instruction; preserve raw BLOCK score as historical scanner evidence.

## UI/UX Pro Max: 52 scanner findings

- `scripts/tests/test_catalog_refresh.py:26`, `test_core.py:256`, `test_design_system_stack.py:34` (AST4): executable subprocess calls in tests use argument lists to launch Python. Normal local search does not run those tests.
- Twenty-four E1 matches in `data/stacks/flutter.csv` are documentation URLs, not transmission code.
- `data/ux-guidelines.csv:25,35,36,84,114`, `data/stacks/nextjs.csv:21,38,51`, `data/react-performance.csv:29` and `data/stacks/react-native.csv:52` contain guidance and bad-practice examples (system theme, confirmation, environment variables, unsafe HTML, permission assumptions). These rows do not execute their examples. Retrieval must read the do/don't columns in context.
- `references/pro-rules.md:47` warns against reusing opacity without checking the background. `data/stacks/avalonia.csv:49`, `nuxt-ui.csv:69`, `javafx.csv:9` are platform guidance, not a host-control request.
- `scripts/design_system.py:387` and `scripts/reasoning_contract.py:84` (P6) are ordinary Python returns of design rules. `scripts/tests/test_core.py:294` checks no-overwrite behavior.
- `data/products.csv:112` describes password-manager keychain UI. MIT license text and missing permissions metadata are non-executable matches.

Actual capability: read packaged local data and, when requested with persistence flags, write design-system files under the selected project. Python runtime has no external package dependencies. Only SKILL.md search-path guidance is adapted; executable source is unchanged.

## Chrome DevTools MCP: corrected dependency and capability assessment

The scanner reported 166 findings, dominated by 100 license-text matches and 30 semver range warnings on build-time dependencies. The npm distribution has no runtime dependency installation list; code is bundled.

- SC4 at `package.json:95` inferred vulnerable Zod 4.4.3 from `^4.4.3`. The actual bundle embeds 4.6.5 at `build/src/third_party/index.js:6396`.
- Current [CVE Program record](https://github.com/CVEProject/cvelistV5/blob/main/cves/2023/54xxx/CVE-2023-54404.json) and [API](https://cveawg.mitre.org/api/cve/CVE-2023-54404) both mark CVE-2023-54404 REJECTED on October 28. The CNA explains that memory growth is proportional to input already parsed, requires absent request-size limits, and is expected validator behavior. Earlier HIGH/8.2 advisory mirrors are stale for current CVE status. The prior active-vulnerability claim is withdrawn.
- Ordinary oversized-input risk remains: `tools/input.js:524` accepts an elements array. Tool schemas are passed to SDK validation at `index.js:400`, over stdio (`bin/chrome-devtools-mcp-main.js:74`). Do not send unbounded/huge tool arguments. No public network listener or webpage-to-stdio exploit was established.
- PE3 matches at `config/ConfigParser.js:27`, `config/ServerConfig.js:74,111,220` and `third_party/cli.js:2698,2708,6756` are `process.env` handling, not reads of credential files. `utils/url.js:197,199` uses `/etc/passwd` in a comment explaining file-URL detection.
- `bin/check-latest-version.js:14` does invoke npm configuration and query its registry for update information; the installation disables this via `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS=1`.
- `daemon/daemon.js:50` rejects world-writable PID directories, the opposite of weakening permissions. Yargs `skipValidation` matches relate to CLI help/version parsing, not browser sandbox controls.
- Four YARA matches in cookie issue-description Markdown are explanatory browser text. `tools/input.js:517` asks the agent to batch form fills; it does not supersede authorization. Extra packaged debugging skills are not installed globally.

Official [GitHub releases](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases) and npm's current dist-tags identify 1.12.0 as latest. No alternate maintained safe release was established; none is required solely for this rejected CVE. Use the inspected official tarball, not an unreviewed source build.

The MCP runs with the local user's privileges and can inspect pages/network, execute page JavaScript and write screenshots/downloads. These are the requested tool's intended capabilities. Acceptance is scoped to a new isolated headless browser profile, telemetry/CrUX/update checks disabled, no connection to personal sessions, no automatic hook/extension installation, and benign local verification first.

## Prepared files versus approved vendoring

Before acceptance, the skill directories were untracked candidate copies in an isolated checkout, at proposed final paths. They were not committed, published, globally linked or loaded as active skills. The earlier wording “complete packages” described file completeness, not accepted intake. This documented review and the subsequent owner's proceed instruction are the acceptance record; installation and publishing still require observed verification results. No merge is authorized.
