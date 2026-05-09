# Homelab Audit — {{AUDIT_DATE}}

**Run flags:** {{FLAGS}}
**Elapsed:** {{ELAPSED}}
**Scanned:** {{SCANNED_TOTAL}} files across {{SCANNED_ROOTS}} roots

---

## Summary

| Category | Count |
|---|---|
| Stale files (proposed quarantine) | {{COUNT_SAFE_QUARANTINE}} |
| Dated historical artifacts | {{COUNT_DATED}} |
| Duplicates | {{COUNT_DUPLICATE}} |
| Watchlist (in-use, no action) | {{COUNT_WATCHLIST}} |
| Broken markdown links | {{COUNT_BROKEN_MD}} |
| Dangling symlinks | {{COUNT_DANGLING}} |
| Broken script sources | {{COUNT_BROKEN_SOURCES}} |
| Container drift items | {{COUNT_DRIFT}} |

---

## Trend (last 12 audits)

{{TREND_PARAGRAPH}}

| Date | Stale found | Broken links | Drift | Approved actions |
|---|---|---|---|---|
{{TREND_TABLE}}

**Diagnosis:** {{TREND_DIAGNOSIS}}

---

## Container Drift

{{CONTAINER_DRIFT_SECTION}}

---

## Stale files — proposed actions

> Each row below is a proposed action. The `restore` command will undo the action if approved.

{{STALE_FILES_TABLE}}

---

## Dated historical artifacts

{{DATED_TABLE}}

---

## Duplicates

> Canonical (kept) vs duplicate (proposed quarantine).

{{DUPLICATES_TABLE}}

---

## Watchlist (no action proposed — radar only)

{{WATCHLIST_TABLE}}

---

## Broken links

### Markdown
{{BROKEN_MD_LIST}}

### Symlinks
{{DANGLING_SYMLINKS_LIST}}

### Shell sources
{{BROKEN_SOURCES_LIST}}

---

## What I deliberately did NOT touch and why

| Reason | Count | Examples |
|---|---|---|
| Hard-skip floor (system paths) | {{COUNT_SKIP_SYSTEM}} | {{EXAMPLES_SKIP_SYSTEM}} |
| Modified ≤7 days ago | {{COUNT_SKIP_RECENT}} | {{EXAMPLES_SKIP_RECENT}} |
| Inside .git/ | {{COUNT_SKIP_GIT}} | — |
| Inside .planning/active/ | {{COUNT_SKIP_PLANNING}} | {{EXAMPLES_SKIP_PLANNING}} |
| Build artifacts (node_modules/.venv/etc) | {{COUNT_SKIP_BUILD}} | — |
| In allow_list | {{COUNT_SKIP_ALLOWLIST}} | {{EXAMPLES_SKIP_ALLOWLIST}} |
| Has in-use signal | {{COUNT_SKIP_INUSE}} | (these went to Watchlist) |

---

## Pattern-rule proposals

> Recurring patterns the skill has seen approved 3+ times. With your sign-off they graduate to `pattern_rules` and trigger automatically next time.

{{PATTERN_PROPOSALS}}

---

## Auto-restored allow-list entries

> Files you `mv`'d back from `.archive/`. These are now auto-added to `allow_list`.

{{AUTO_RESTORED}}

---

## Approval gate

Categories awaiting approval:

- [ ] Quarantine {{COUNT_SAFE_QUARANTINE}} stale files (SAFE_QUARANTINE)
- [ ] Quarantine {{COUNT_DATED}} dated historical artifacts
- [ ] Quarantine {{COUNT_DUPLICATE}} duplicates (canonical retained)
- [ ] Apply {{COUNT_BROKEN_MD}} suggested fixes for broken markdown links

**Reply with:**
- `approve all` — process all categories
- `approve <category-name>` — process specific bucket
- `decline` — skip this audit's actions, keep Watchlist + report on file
- `per-item` — walk through proposals individually

After approval: `quarantine.sh` runs, `state.yaml` updates, memory layers refresh, NotebookLM sources push.
