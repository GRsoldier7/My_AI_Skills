# Moved

31 skills and the old folder README moved out of `skills/grok-bot-team/`. Nine went to the fenced folder `agents/grok-bot/skills/`. The other 22 went into domain folders under `skills/`. `skills/grok-bot-team/` now holds only compatibility symlinks.

Every old path is a relative symlink to its new path. Device symlinks and links into `skills/grok-bot-team/...` keep resolving. The full map is `registry/moved.json` (32 paths: 31 skills and the old folder README).

## Fix your device

On each device:

1. `git pull`
2. `./scripts/install-skills.sh` (dry run)
3. `./scripts/install-skills.sh --apply <skill-dir-name>` for any moved skill you had installed.

The installer resolves skills by folder name, so it links the new path. Windows clones with `core.symlinks=false` see the compatibility links as small text files. Skills still install by name.

## Compatibility window

Compatibility symlinks stay at least 90 days (until 2027-02-16). They are removed only in a separate pull request that Aaron approves, after each device re-runs its installer.

## Destinations

| Destination | Count | Skills |
| --- | --- | --- |
| `agents/grok-bot/skills` | 9 | api-first-heavy-work, bot-team-review, chief-of-staff-intake-routing, evidence-before-claims, govcon-sources-sought-response, kaizen-evolution, outcome-effect-closeout, skill-and-prompt-evals, skill-scout |
| `skills/seo` | 6 | ai-search-visibility, local-seo-audit, local-seo-team-project, schema-markup-jsonld, seo-content-brief-aeo, technical-seo-baseline |
| `skills/govcon` | 3 | cmmc-nist-800-171-readiness, govcon-bid-no-bid-screening, govcon-proposal-compliance-matrix |
| `skills/homelab-ops` | 3 | alerting-observability-design, homelab-decision-record, homelab-runbook-generator |
| `skills/core` | 5 | agent-run-forensics, bot-prompt-tuning, bot-usage-cost-optimizer, output-quality-no-slop, weekly-open-loops-review |
| `skills/strategy` | 3 | consulting-tiered-proposal-sow, discovery-call-prep, lead-research-brief |
| `skills/legal-financial` | 1 | renewals-and-alerts-tracker |
| `skills/engineering` | 1 | obsidian-second-brain-wiki |
