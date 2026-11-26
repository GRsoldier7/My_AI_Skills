# Retired skills

This folder holds skills retired from the library so the files stay in git and are not scanned or counted.

On 2026-11-26 Aaron approved retiring engineering/git-commit-push-pr in the same pull request that added n8n-debugging-official, to stay at the library soft cap of 240.

The retired skill now lives at archive/git-commit-push-pr/ (moved from skills/engineering/git-commit-push-pr/). It is not in registry/curation.json review or deprecated lists, and it is not in scripts/lint-config.json vendored_paths, because those lists require a SKILL.md under a live library path.

Reason it was on the review list: its optional capture path names ce-demo-reel, which this library does not ship. Prefer git-commit and ce-pr-description with supplied evidence.

To restore it, move the folder back under skills/engineering/, put it back on the review or optional list and vendored_paths, and regenerate the registry.
