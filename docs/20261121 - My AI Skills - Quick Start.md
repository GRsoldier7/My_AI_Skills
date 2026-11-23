# 20261121 - My AI Skills - Quick Start

Pick the outcome you need. The same canonical skill can appear in several sets. Carry a single selected set into the project that owns the work.

| Goal | Set | A first request |
| --- | --- | --- |
| Personal study or prayer | `faith-personal` | “Walk me through Psalm 13 in context. Give me one question and a prayer I can make my own tonight.” |
| Prepare a group or Sunday school lesson | `faith-teaching` | “Prepare a 20-minute James 1:19–22 discussion for a mixed-experience group. Give the leader a way to invite quiet members in.” |
| Turn a study into a public draft | `faith-publishing` | “Write a short public post about lament and trust from Psalm 13. Use the passage and leave family stories private. Give me the draft to review.” |
| Validate a BI measure | `work-bi` | “Using these fictional counts, test whether the DAX measure behaves at both detail and total level. Show expected results and assumptions.” |
| Scope client work | `consulting` | “Turn this discovery brief into a proposed scope with deliverables, assumptions, exclusions and open questions.” |
| Improve a business website | `business-web` | “Use the supplied landing-page text and crawl summary to prioritize three SEO fixes. Include an acceptance check per fix.” |
| Screen a public solicitation | `govcon` | “Build a bid/no-bid screen and a compliance matrix from this public excerpt. Cite section numbers and identify missing information.” |
| Manage the week at home | `home` | “I have two evening commitments and one 30-minute planning block. Help me choose what to do, defer or delegate.” |
| Compare tools or methods | `deep-research` | “Compare three ways to meet these requirements. Cite the strongest evidence for the recommendation and explain what would change it.” |

## Use a set

Run commands from the reviewed checkout. On Windows `py -3` may be the Python launcher. On macOS and Linux use `python3` if needed. A fresh export needs an existing parent directory and a new destination name.

```sh
python scripts/skill-picks.py list
python scripts/skill-picks.py list --platform chatgpt
python scripts/skill-picks.py inspect work-bi
python scripts/skill-picks.py export work-bi --platform chatgpt --output ./work-bi-trial
```

Open the exported README and use the reading copy in the intended chat. In an Enterprise workspace configured for instructions only, paste or attach the permitted text and use synthetic BI inputs for the first run. The workflow requires no API or Actions. In Copilot, use approved project context and check the result against a known fixture. For Claude Code or Codex native discovery, review the [existing installer and device guide](../platform-configs/skill-sets/README.md). For Muse or another agent, follow the supported modes listed by the CLI and test a known prompt on that host before relying on automatic selection.

For a faith profile, keep the founding study package and referenced resources together. Keep private prayers in the personal space. Start a public draft in its own context and review Scripture references, attribution, wording and consent before posting. Giving the public author just the passage and approved study takeaway is usually sufficient.

## Keep contexts separate

Use one private repository or project and tool profile per employer, business entity or consulting client. The public set supplies general procedures. A private project supplies its vocabulary, approved tools, access, examples and review date. If a Spec Kit constitution already owns enduring project rules, link to it from the project's context note. A shared skill then works across domains without transferring their facts.

The check for a first trial is concrete. For a BI example, enter two synthetic groups with rates 1/2 and 2/8. A correctly weighted total is 3/10. For a study, verify one interpretation against its surrounding passage and check that the application follows. For a bid, trace a mandatory item back to its solicitation section. Record elapsed minutes and corrections privately. Reuse the skill when it earns its place in the workflow.

## Return to a known version

Each export stands alone at the revision used to create it. Keep an accepted pack while testing an update, export changes into a new folder, and compare the receipts. For repository changes, review the feature branch and revert an accepted commit through a pull request. Existing account configuration stays under that account owner's control.
