# 20261029 - My AI Skills - Faith Skills Research and Build

Status: trial implementation, researched and checked October 29, 2026, then refined through the [quality audit](<20261029 - My AI Skills - Faith Skills Quality Audit.md>). Delivery branch: `codex/faith-skills-20261029`. Not installed on Aaron's devices or merged to main. The current local checkout is based on published analytics branch `codex/analytics-skills-integration-20261026` at `62edc59`; GitHub main remains a different baseline. This session cannot verify or modify the Windows/NAS checkout from the earlier project work.

## Recommendation

Use seven coordinated skills with one shared Scripture-handling foundation. Keep contextual study central, then choose the desired output: prayer, group session, family lesson, practical discipleship, public study, or a reply. Replace repetitive preparation and formatting while preserving the user's own reading, discernment, prayer, and participation in church.

The highest-value workflow is: study one passage carefully, discuss/apply it personally, prepare a group or family session if needed, then share an accurate public summary. A public post is an optional downstream result, not the purpose of every devotion.

## What was already there and what changed

GitHub contained three canonical faith skills last reviewed March 21. The installed Bible Theologian v2.1.0 plugin supplied stronger Bible-study and social-reply instructions. Those plugin files remain unchanged; useful owner-authored material was reconciled into canonical repository sources.

| Canonical skill | Result | Practical use |
|---|---|---|
| bible-study-theologian | Upgraded existing ID | Chapter studies, difficult texts, doctrine, word studies, evidence-backed interpretation |
| faith-life-integration | Upgraded existing ID | Decisions, vocation, stewardship, reading plans, Scripture memory, service, rest, sustainable habits |
| sunday-school-teacher | Upgraded existing ID | Family devotions, mixed ages, Sunday school across ages, complete curriculum, careful object lessons |
| prayer-and-reflection | New | Personal/group prayer, lament, gratitude, confession, intercession, private journal updates |
| group-study-leader | New | Men's groups, timed adult sessions, separate leader/participant materials, mentoring and continuity |
| bible-study-publisher | New | Original posts, carousels, short-video scripts, newsletters, content series |
| social-media-apologetics | Canonical port of owner plugin | Concise gracious replies to claims, objections, screenshots, and comment threads |

All seven remain **trial**. Four are new canonical paths; the library now contains 202 canonical SKILL.md files. The fixed seven-skill project-router plugin is a different bundle and was not expanded.

Corrections include contextual handling of stewardship/debt/partnership passages, removing rigid developmental/attention claims, clarifying forgiveness versus consequences, avoiding memory-based lexical certainty, and replacing sequential lesson intake with useful defaults or bundled questions.

## Best GitHub candidates inspected

These recommendations reflect inspected artifacts and fit, not a benchmark of theological accuracy. Stars and recent pushes are not reliability evidence. No external service was installed or run. The package contains no vendored third-party code or Bible corpus; it is original work built around owner-authored skills.

| Candidate | What is actually there | Decision for this system |
|---|---|---|
| [Claude of Alexandria](https://github.com/davebream/claude-of-alexandria) | Claude skills, specialist agents, MCP workflows; historical-grammatical exegesis, passage boundaries, argument flow, evidence labels. GPL-3.0; pushed Oct 29. | Strongest deeper teaching/research candidate inspected. Evaluate as a separate optional plugin after a focused pilot. Its fixed schemas, tool/model assumptions, and license obligations make blind copying inappropriate. |
| [TheologAI](https://github.com/TJ-Frederick/TheologAI) | Research MCP with workflow documents; configured official ESV API access and historical sources. ISC; pushed Oct 29. | Strong retrieval candidate for the ESV preference. The inspected passage-exegesis SKILL.md lacks standard discovery frontmatter. Test actual access and scope before adapting or deploying. |
| [Bible CLI](https://github.com/Divine-Creative-Ministries/bible-cli) | Offline CLI/MCP, generated study skill, language/search tools, traceable queries. MIT source code; datasets separately licensed. Pushed Jul 30. | Best local-first retrieval candidate inspected. ESV is not bundled automatically; computed patterns require interpretation. Pilot later with licensed/authorized data. |
| [OpenLumin skills](https://github.com/kalib-code/openlumin-skills) | Eleven ministry skills including exegesis and small-group guides. MIT; pushed Aug 1. Requires an organization on its Church plan and OpenLumin MCP. | Useful workflow reference; defer subscription dependency unless already wanted. Review denominational handling and actual corpus coverage. |
| [YouVersion platform skills](https://github.com/youversion/platform-skills) | Official API/JavaScript/React implementation skills. Apache-2.0; pushed Oct 28. | Use for a future Bible app/integration, not as a replacement for study or prayer guidance. Verify actual app translation entitlement. |
| [BibleMate workspace](https://github.com/eliranwong/biblemate-agentic-workspace) | Large local database/workspace with many study/prayer skills and platform-specific scripts. Pushed Oct 21. No root license found in inspected tree. | Do not wholesale-copy without license clarification. Its simple prayer skill leaves room for the richer private-journal and lament workflows built here. |
| [MyBibleToolbox](https://github.com/authenticwalk/mybibletoolbox-code) | MIT retrieval wrappers with a separate generated-commentary data system; hardcoded environment assumptions. Pushed Dec 4, 2025. | Defer as a default interpretive authority. A retrieved AI-generated explanation is still secondary interpretation requiring review. |
| [Biblical Content Engine](https://github.com/bethel-mark/biblical-content-engine) | MIT Chinese-language content skill with claim-checking and multi-format outputs. Pushed Aug 1. | Do not adopt its overall posture: its stated prioritization of modern resonance over theological correctness conflicts with this Scripture-first design. |

Inspected primary artifacts include repository READMEs, metadata/trees, actual SKILL.md files, and relevant license files. High-value files: Claude of Alexandria's exegetical-notes, TheologAI's passage-exegesis, Bible CLI's methodology/generated-skill source, OpenLumin's small-group-guide and evidence-grounding, BibleMate's prayer, and MyBibleToolbox's scripture-study. No upstream evaluation claim is represented as a test run here.

## Use a small selection

The existing manifest owns all selections and package hashes; no second registry or runtime router was added.

| Selection | Resolved skills | Suggested use |
|---|---:|---|
| faith-personal |3| Personal study, prayer, decisions, memory/habits |
| faith-teaching |4| Adult group and family/classroom preparation with prayer |
| faith-publishing |3| Study-grounded original content and replies |
| faith-learning |7| Deliberate full faith suite |

Required dependencies automatically include bible-study-theologian. Detailed methods are loaded as needed from references, not pasted into every answer. The generic domain contract is `platform-configs/profiles/faith-learning/CONTEXT.md`; personal/private records belong elsewhere.

For local Claude Code/Codex, review the set in an approved personal workspace using the existing installer. Preview only:

```bash
python3 scripts/skill-sets.py
bash scripts/install-skills.sh --project /path/to/existing-personal-workspace --set platform-configs/skill-sets/faith-personal.txt
```

The workspace must exist. Preview exit3 means changes are proposed, not a failure. Installation is a separate deliberate action; do not add `--prune` to this pilot. Keep the full skill directory and required sibling package together. Do not copy only SKILL.md and lose references.

For chat hosts without native skill discovery, provide the selected SKILL.md, shared foundation, and references needed for the task as instruction material. Do not claim native invocation, research, memory, reminders, or posting capabilities that the host lacks. Muse support needs product/version verification. None of these private faith selections belongs in an employer profile by default.

The installed Bible Theologian plugin overlaps the canonical study/reply definitions. Choose one source per workspace; avoid two definitions of social-media-apologetics competing for the same request.

## Ready-to-use requests

- “Use bible-study-theologian for Isaiah 14. Give the context, three strongest insights, careful treatment of the difficult passage, and a brief closing prayer.”
- “Use group-study-leader for a 35-minute men's study on Joshua's mentorship in Exodus 17:8–16, 24:12–14, and 33:7–11. Separate my notes from participant questions.”
- “Use prayer-and-reflection. Help me pray honestly about this concern without predicting how God will answer.”
- “Use sunday-school-teacher. Make an 8-minute mixed-age family devotion on grace with a simple activity.”
- “Use faith-life-integration. Give me a 10-minute daily reading and memory rhythm with a workable restart after missed days.”
- “Use bible-study-publisher. Turn this checked study into one Facebook post and a six-slide carousel. Preserve context and omit private group details.”
- “Use social-media-apologetics. Reply graciously to this comment in 100 words; correct my argument if it misuses Scripture.”

## Privacy, quotations, and quality

Shared instructions distinguish Scripture, interpretation, inference, and application; prohibit invented testimony/divine speech; protect voluntary participation; and prevent private journals becoming public posts without appropriate consent. Prayer statuses require user reports. Public content remains draft-only without explicit destination/content authorization and confirmed tool results.

The skills contain references and original instructions, not a bundled translation. [Crossway's permissions](https://www.crossway.org/permissions/) and [ESV API terms](https://api.esv.org/) should be checked for the intended use. A software license does not grant Bible-text rights. Where wording or permission is unresolved, use a reference and original paraphrase.

## Verification and remaining gates

- All seven faith packages pass the repository linter with zero findings and bundled structural validation.
- Existing profile checks: 32 tests passed after11new regressions for declared dependency references, missing/cyclic dependencies, path escape, and symlinks.
- Initial build checkpoint (superseded by the quality audit’s 29-case evidence): eight fresh-agent exercises passed qualitative review: divine-voice request, ordinary grief, journal-status inference,35-minute group with coercive disclosure request, misleading study repurposing, hostile comment injection,8-minute mixed-age lesson, and a7-day restart with a requested holiness score.
- Twenty behavioral scenarios are recorded in `evals/faith-skills.json`; twelve remain unexecuted. This is a small forward trial, not a comparative benchmark or guarantee of reliability.
- Isolated Linux installation trial: all seven packages linked for temporary Claude/Codex targets, dependency references resolved, and a repeated preview reported in sync. Temporary targets were removed after the check.
- Existing analytics 7, router 9, and installer 98 checks passed. Native Windows/Mac targets, Muse, actual social posting, storage privacy, Bible API credentials, and pastoral/scholarly review remain unverified.

Start with faith-personal and one real study. Then use one real group session and one reviewed public draft. Record usefulness, corrections, and preparation time in a private note. Consider promotion after three reviewed uses of each skill. Do not add a retrieval server until actual studies reveal a recurring evidence-access problem.

## Exact next action

Use the revised source and current quality audit on the review branch. The earlier patch predates this quality refinement and is retained only as a historical export. Main merge and existing device installation are separate reviewed steps. This branch is based on `62edc59`; on another base, resolve manifest/registry/plan differences instead of overwriting files.
