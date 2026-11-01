# 20261101 - My AI Skills - Design Intake Review

## Outcome

Reviewed and installed all four requested projects globally on the owner's Mac
following the owner's proceed authorization. A persistent local checkout supplies
the three skill packages. MCP uses the exact inspected official npm artifact.
No merge has occurred. See the Installation Results for verification and the
Approval Scope for source-level findings; raw scanner scores below are retained
as historical results, not unresolved current findings.

| Component | Pin/version | Intake outcome | Next action |
| --- | --- | --- | --- |
| Impeccable | `e89e3ada3e875a89ac2c5d33d11e65ebef6fe285`, 4.8.0 | 50/100, NOTIFY; 29 findings | Accepted after source review and owner proceed approval |
| Taste Skill | `12af471f627f866411b4bd785b19646d3672784c`, 2.1.5 | 76/100, BLOCK; 63 findings | Accepted false-positive disposition after owner proceed approval |
| UI/UX Pro Max | `3a13158ff1f32156cbe144108de48eda2ecaed9a`, CLI 2.5.0 | 50/100, NOTIFY; 52 findings | Accepted after source review and owner proceed approval |
| Chrome DevTools MCP | source `8d009e854f8aa55b1ec31628e836d4d4731b8ec8`; npm 1.12.0 | 100/100, BLOCK band; 166 findings | Accepted reviewed dispositions; primary CVE is rejected |

The existing `/root/bin/skill-scan` wrapper on the configured agent host uses
SkillSpector 2.2.3: scores <=20 ALLOW, 21–50 NOTIFY, >50 BLOCK. Skill directories
were scanned explicitly, with static analysis and no LLM. Detailed JSON reports
were retained outside the repository. Scanner risk scores are heuristics, not a
probability of compromise. No permissions, scanner flags or thresholds were
weakened to obtain a passing result.

The first transfer included macOS extended metadata; the detailed scans used a
fresh metadata-free transfer. Final verification also restored Impeccable's Windows
launcher to its original Git-blob line endings and rescanned that package. The
final candidate contains 178 files, of which only UI/UX Pro Max's SKILL.md is
deliberately adapted. Per-file original and installed hashes are recorded in
`platform-configs/skill-sets/design-sources.json`.

## Review of the skill findings

**Impeccable:** two flagged POST requests target `http://localhost:<PORT>` for its
live preview result/claim protocol. Several findings match Apache license text,
design identity/state terminology, and instructions warning against changes made
without approval. The screenshot bundle uses character conversion. Optional
hooks alter project-local configuration; this integration does not enable them.
The launcher can download its pinned engine from GitHub releases and verifies it
against the packaged checksum manifest. These are real capabilities to accept,
even though the scanner's broad labels do not establish malicious behavior.

**Taste:** the two HIGH findings are `--no-check` in the image-search helper's
documentation. Code at `scripts/assets.mjs:145` sets whether to check that remote
images load; it does not disable TLS verification or sandboxing. Other matches
include external Fontshare/image-provider URLs, keychain/keyring illustrations,
the phrase "curl of a breaking teal wave", and a described looping animation.
Its browser helper uses a new temporary profile and removes its own profile on
exit. Image search sends query text to public providers and downloads assets;
private material must not be placed in those queries. These findings justify a
documented exception request, not silently treating the BLOCK as ALLOW.

**UI/UX Pro Max:** findings include subprocess calls in upstream tests, reference
URLs in CSV rows, bad-practice examples in do/don't guidance, license text and
ordinary Python `return rule`/`return rules` statements. Its local search reads
packaged data and may persist a requested design system to the project. The
plugin-only path in SKILL.md was adapted for a portable user-scope installation;
all Python, CSV, JSON and reference files retain their upstream bytes. No Python
dependencies need global installation.

Recommendation: accept the three reviewed skill candidates with explicit intake
authorization. This is a bounded source review, not a security certification.

## Chrome DevTools MCP: corrected dependency assessment

**Correction:** the primary CVE record marks CVE-2023-54404 REJECTED as of
2026-10-28T21:17:22.423Z. The earlier statement that this was an active dependency
vulnerability was incorrect. The scanner's raw result remains unchanged for audit.

Authoritative evidence:
- [CVE Program API](https://cveawg.mitre.org/api/cve/CVE-2023-54404)
- [CVE Program source record](https://github.com/CVEProject/cvelistV5/blob/main/cves/2023/54xxx/CVE-2023-54404.json)

The CNA rejected the report because memory growth is proportional to input already
allocated by JSON.parse, requires absent application request-size limits, and is
expected validator behavior rather than a defect in Zod. GitHub's advisory and
OSV still displayed the older HIGH/8.2 assessment when checked; the current primary
record takes precedence. Do not describe the historical rating as an active CVE.

The artifact facts remain true: npm 1.12.0 bundles Zod 4.6.5 at
`build/src/third_party/index.js:6396`; source HEAD's lockfile resolves 4.6.7. The
historical upstream change moves size checks ahead of element validation only for
explicitly bounded collections; it does not establish that unbounded input is safe.

Relevant exposure is the client's JSON tool arguments, not an automatically public
HTTP endpoint. The normal entrypoint uses StdioServerTransport at
`build/src/bin/chrome-devtools-mcp-main.js:74`. For example, `fill_form` declares an
unbounded elements array at `build/src/tools/input.js:524`; input schemas are
registered with the SDK at `build/src/index.js:400`. An excessively large invalid
tool request could exhaust resources. No attack was executed and no webpage-to-stdio
exploit path was established. The official security policy treats the calling agent
as responsible for validating tool arguments.

Official npm dist-tags and GitHub releases still identify 1.12.0 as latest. No
supported patched alternate release was established. A new version is not required
to address a rejected CVE. Keep the exact inspected 1.12.0 pin as the candidate;
do not substitute a source build or downgrade on speculation.

Disposition: accepted following source review and owner proceed authorization.
Isolated local-page smoke tests subsequently passed before reporting operational. Browser automation can read page/network data,
execute page JavaScript and write requested screenshots/downloads. Use a throwaway
profile, no personal session attachment, usage statistics/CrUX/update checks disabled,
and ordinary small tool inputs. Global registration is now installed in both hosts with these settings.

## Validation and installation boundaries

- All three manifests, full file inventories, licenses, full commit pins and
  local Markdown references verify against their recorded upstream Git blobs.
- Design-only linter: 3 skills, 0 findings.
- Design-only validator: 16 passing checks, 0 failures, 2 warnings. The warnings
  concern upstream multiline description parsing and Taste's long SKILL.md;
  upstream content was not rewritten to hide them.
- Existing installer regression tests: 98 passed, 0 failed.
- Existing Project Router packaging/installer suite: 9 tests passed.
- Installer applied six links: three each to `~/.claude/skills` and
  `~/.agents/skills`, with no name collisions. Subsequent dry run reports In sync.
- Whole-library validator: 4 failures in both baseline and candidate (187 to 189 warnings).
  Whole-library linter: 7 failures and 76 warnings in both baseline and candidate.
  No new failures; the two additional warnings are the documented upstream style warnings.
- Runtime search, checksum-pinned engine startup, screenshots, fresh host discovery
  and MCP initialization/interaction have now been verified; see Installation Results.

## Publishing approval

`CLAUDE.md` says: "Always ask before: Git commits, PRs, merges, or pushes."
The owner subsequently approved proceeding after notice of the pending review.
That authorization covers commit/push/draft PR for this scoped integration. It
does not authorize merging. The other analytics-integration work remains separate.

## Candidate location clarification

The three packages are untracked review candidates copied into their proposed
`skills/design/` destinations inside an isolated checkout before intake completed.
They were not committed, pushed, globally linked, loaded as skills, or accepted into
the canonical repository history. Calling them "vendored" would imply acceptance
that has not happened; "prepared candidates" is the accurate status. The installer
can see their intended paths, but only its dry run was used. Taste was subsequently accepted after documented false-positive review and the
owner’s proceed authorization; raw scanner output remains unchanged.

For exact grouped findings and practical approval scope, see the accompanying
`20261101 - My AI Skills - Design Approval Scope.md`.
