# Retired skills

This folder holds skills retired from the library so the files stay in git and are not scanned or counted.

On 2026-11-26 Aaron approved retiring engineering/git-commit-push-pr in the same pull request that added n8n-debugging-official, to stay at the library soft cap of 240.

The retired skill now lives at archive/git-commit-push-pr/ (moved from skills/engineering/git-commit-push-pr/). It is not in registry/curation.json review or deprecated lists, and it is not in scripts/lint-config.json vendored_paths, because those lists require a SKILL.md under a live library path.

Reason it was on the review list: its optional capture path names ce-demo-reel, which this library does not ship. Prefer git-commit and ce-pr-description with supplied evidence.

To restore it, move the folder back under skills/engineering/, put it back on the review or optional list and vendored_paths, and regenerate the registry.

On 2026-11-26 Aaron approved retiring core/polychronos-team in the same pull request that added history-signal-check, to stay at the library soft cap of 240.

The retired skill now lives at archive/polychronos-team/ (moved from skills/core/polychronos-team/). It is not in registry/curation.json review or deprecated lists, because those lists require a SKILL.md under a live library path.

Reason it was on the review list: broad team trigger overlaps parallel-execution-strategist and the existing project router. No agent index listed it.

To restore it, move the folder back under skills/core/, put it back on the review or optional list, and regenerate the registry.

On 2026-11-26 Aaron approved retiring the six skills below in the same pull request that added offer-and-pricing-review, competitor-value-prop-scan, lead-magnet-spec, retention-loop-design, claims-guardrail-check, and case-study-draft, to stay at the library soft cap of 240.

Each retired skill now lives under archive/<name>/ and is not in registry/curation.json review, core, or deprecated lists. Vendored paths for grilling and lfg were removed from scripts/lint-config.json, because those lists require a SKILL.md under a live library path. Nothing was deleted.

| Retired skill | Moved from | Why it was retired |
|---|---|---|
| pricing-strategist | skills/strategy/pricing-strategist/ | High overlap with the new offer-and-pricing-review skill; no history mentions. |
| grilling | skills/aarons-latest/grilling/ | Status review (overlaps grill-me); no history mentions. |
| apex-mode | skills/core/apex-mode/ | Status review (broad maximum-stack trigger); no history mentions. |
| organize-project | skills/core/organize-project/ | Status review (overlaps directory-cleanup and file-organizer); no history mentions. |
| wrapitup | skills/core/wrapitup/ | Status review (likely duplicate of wrapup); no history mentions. |
| lfg | skills/engineering/lfg/ | Status review (overlaps ce-work/ce-plan); no history mentions. |

To restore one, move its folder back under its original live path, put it back on the matching core, optional, or review list (and vendored_paths if it was vendored), and regenerate the registry.
