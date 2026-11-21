# Aaron's AI Skill Library

Choose a skill for the work in front of you. This repository holds the reusable instructions, references and templates. Each project or client supplies its own private context.

## First use

From a checkout with Python 3.10 or newer, run the following. Use `py -3` on Windows or `python3` on macOS and Linux if your shell uses that command.

```sh
python scripts/skill-picks.py list
python scripts/skill-picks.py inspect faith-personal
python scripts/skill-picks.py export faith-personal --platform chatgpt --output ./faith-study-pack
```

Open the new pack's README for the receiving tool and try one real task. The export writes to a new local folder. For work BI in an approved chat, choose `work-bi`. For separate client engagements, export `consulting` into each client's own project. [Quick Start and example prompts](docs/20261121%20-%20My%20AI%20Skills%20-%20Quick%20Start.md)

| I want to… | Start here |
| --- | --- |
| Study Scripture, pray, teach a group or draft a public post | Select `faith-personal`, `faith-teaching`, or `faith-publishing`. [Faith skill evidence](docs/20261121%20-%20My%20AI%20Skills%20-%20Faith%20Skill%20Evidence.md) |
| Work on analytics, consulting, a website, a bid, household planning or research | Run `python scripts/skill-picks.py list` and inspect the relevant set. [Skill sets](platform-configs/skill-sets/) |
| Start, resume or rescope a project | Use the [project router](skills/aarons-latest/project-router/SKILL.md). It hands the workflow to a single owner. |
| Find a specialist by domain or by agent | Browse the [generated catalog](registry/skills.json) or the [five agent indexes](agents/README.md). |
| Set up Claude Code or Codex on a device | Preview the existing installer and check package ownership in the [device guide](platform-configs/skill-sets/README.md). |
| Prepare instructions for a new project | Preview with `python scripts/project-guidance.py deploy --target . --platforms codex,claude`. Review any existing project rules before adopting a template. |

## How the catalog works

A canonical skill lives at the path recorded in the registry. Claude project helpers under its project configuration have a separate scope and are outside the catalog totals. Use its `SKILL.md` as the entry point and open references when relevant. Reuse that path across sets. The nine Grok Bot-only skills stay with their host. The registry records status, provenance and scope. “Portable” describes the source package. Specific account access, connectors and behavior require a trial on the receiving tool. [Registry guide](registry/README.md) · [Compatibility paths](MOVED.md)

Keep the global install set small. A study, a bid and an analytics report each get different instructions. Keep unpublished study notes, work records, household data and client overlays in the appropriate private project. Automation flows can call reviewed skills when their permissions and outputs have been tested. Keep the source or an export in version control.

## Maintain or extend the library

```sh
python scripts/check-library.py
```

The check exercises registry integrity, export behavior, project guidance and routing packages, and prints the full-library lint summary. When changing curation, run `python scripts/generate-skill-registry.py --registry` first. For external additions, record the license and source revision, compare against existing skills, and demonstrate a recurring task before promoting the addition. [Contribution guide](CONTRIBUTING.md) · [Polish plan](docs/20261121%20-%20My%20AI%20Skills%20-%20Library%20Polish%20Plan.md) · [Verification report](docs/20261121%20-%20My%20AI%20Skills%20-%20Verification%20Report.md)
