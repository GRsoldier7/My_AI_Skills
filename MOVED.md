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

## 2026-11-27: Business folder

General business skills moved into `skills/business/<domain>/`: 29 skills. Each keeps its domain (`seo`, `growth`, `strategy`, `govcon`, `legal-financial`), so core sets, caps and agent indexes are unchanged. `ai-business-optimizer` moved from `product` to `strategy`.

Aaron, 2026-11-27: "If they are general skills, not specific to the actual Business, keep them in a Business folder (SEO, website building and design, any other business specialty...)". Skills specific to E7 or TempleProtocol were not moved; they wait for a separate private repository.

Every old path is a relative compatibility symlink to its new path, under the same 90-day window and device steps as above. Links in `skills/grok-bot-team/` that pointed at a moved skill now point straight at its new path. The installer resolves skills by folder name (now searching one level deeper), so `./scripts/install-skills.sh --apply <skill-dir-name>` relinks a device.

| Destination | Count | Skills |
| --- | --- | --- |
| `skills/business/govcon` | 3 | cmmc-nist-800-171-readiness, govcon-bid-no-bid-screening, govcon-proposal-compliance-matrix |
| `skills/business/growth` | 12 | claims-guardrail-check, community-builder, competitor-value-prop-scan, content-marketing-machine, copywriting-conversion, growth-hacking-engine, marketing-strategist, personal-brand-builder, professional-communicator, retention-loop-design, sales-closer, social-media-architect |
| `skills/business/legal-financial` | 1 | startup-tax-strategist |
| `skills/business/seo` | 7 | ai-search-visibility, local-seo-audit, local-seo-team-project, schema-markup-jsonld, seo-agentic, seo-content-brief-aeo, technical-seo-baseline |
| `skills/business/strategy` | 6 | ai-business-optimizer, business-plan-architect, consulting-operations, entrepreneurial-os, financial-model-architect, go-to-market-engine |

| Old path | New path |
| --- | --- |
| `skills/seo/ai-search-visibility` | `skills/business/seo/ai-search-visibility` |
| `skills/seo/local-seo-audit` | `skills/business/seo/local-seo-audit` |
| `skills/seo/local-seo-team-project` | `skills/business/seo/local-seo-team-project` |
| `skills/seo/schema-markup-jsonld` | `skills/business/seo/schema-markup-jsonld` |
| `skills/seo/seo-agentic` | `skills/business/seo/seo-agentic` |
| `skills/seo/seo-content-brief-aeo` | `skills/business/seo/seo-content-brief-aeo` |
| `skills/seo/technical-seo-baseline` | `skills/business/seo/technical-seo-baseline` |
| `skills/growth/claims-guardrail-check` | `skills/business/growth/claims-guardrail-check` |
| `skills/growth/community-builder` | `skills/business/growth/community-builder` |
| `skills/growth/competitor-value-prop-scan` | `skills/business/growth/competitor-value-prop-scan` |
| `skills/growth/content-marketing-machine` | `skills/business/growth/content-marketing-machine` |
| `skills/growth/copywriting-conversion` | `skills/business/growth/copywriting-conversion` |
| `skills/growth/growth-hacking-engine` | `skills/business/growth/growth-hacking-engine` |
| `skills/growth/marketing-strategist` | `skills/business/growth/marketing-strategist` |
| `skills/growth/personal-brand-builder` | `skills/business/growth/personal-brand-builder` |
| `skills/growth/professional-communicator` | `skills/business/growth/professional-communicator` |
| `skills/growth/retention-loop-design` | `skills/business/growth/retention-loop-design` |
| `skills/growth/sales-closer` | `skills/business/growth/sales-closer` |
| `skills/growth/social-media-architect` | `skills/business/growth/social-media-architect` |
| `skills/strategy/business-plan-architect` | `skills/business/strategy/business-plan-architect` |
| `skills/strategy/consulting-operations` | `skills/business/strategy/consulting-operations` |
| `skills/strategy/entrepreneurial-os` | `skills/business/strategy/entrepreneurial-os` |
| `skills/strategy/financial-model-architect` | `skills/business/strategy/financial-model-architect` |
| `skills/strategy/go-to-market-engine` | `skills/business/strategy/go-to-market-engine` |
| `skills/product/ai-business-optimizer` | `skills/business/strategy/ai-business-optimizer` |
| `skills/govcon/cmmc-nist-800-171-readiness` | `skills/business/govcon/cmmc-nist-800-171-readiness` |
| `skills/govcon/govcon-bid-no-bid-screening` | `skills/business/govcon/govcon-bid-no-bid-screening` |
| `skills/govcon/govcon-proposal-compliance-matrix` | `skills/business/govcon/govcon-proposal-compliance-matrix` |
| `skills/legal-financial/startup-tax-strategist` | `skills/business/legal-financial/startup-tax-strategist` |
