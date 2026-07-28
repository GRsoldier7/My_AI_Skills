# Audit Procedure — Full Audit Phase A-E

This file is loaded only when running a full audit (`/homelab-organizer` with no flag, or with one of `--containers`, `--files`, `--links`).

## Pre-flight

Before any phase:

1. Verify `/root/homelab/docs/organizer/` exists. If not, create it.
2. Load `state.yaml`. If missing, copy from `state.example.yaml`. Mark `first_run: true` in memory.
3. Load `references/safety-rules.md`. The hard-skip floor + default list are now active.
4. Set `AUDIT_DATE=$(date +%Y-%m-%d)`. Set `AUDIT_DIR=/root/homelab/docs/organizer/AUDIT-$AUDIT_DATE`.
5. `mkdir -p "$AUDIT_DIR"`. Subsequent intermediate JSONs write here.

## Phase A — Container audit

Run `scripts/inventory-containers.sh > "$AUDIT_DIR/containers.json"`.

The script does:
1. `pct list` and `qm list` → CT/VM inventory
2. For each container in `state.yaml: container_baselines`, capture current state:
   - `pct config <id>` → resources (RAM, swap, disk allocation)
   - `pct status <id>` → running/stopped, uptime
   - Single bundled `pct exec <id> -- bash -c '<bundled probe>'` returning JSON:
     - `uptime`, `last_login`, `df_root_pct`, `log_files_24h`, `services_up`, `pkgs_outdated`, `key_files_present`
3. Compare result to `state.yaml: container_baselines.<id>` → emit deltas
4. Drift detection:
   - Container exists in `pct list` but no doc in `/root/homelab/lxc/` or `/root/homelab/containers/` → `undocumented_container`
   - Doc exists but no container with matching ID/hostname → `orphaned_doc`
   - Naming/tag mismatch (doc says CT 207, but reality has different name) → `naming_mismatch`

Output `containers.json` schema:
```json
{
  "audit_date": "2026-05-09",
  "containers": [
    {
      "id": "203",
      "type": "lxc",
      "status": "running",
      "current": {"rss_mb": 412, "disk_gb": 2.1, "services_up": ["postgres"], "pkgs_outdated": 4},
      "baseline_delta": {"disk_gb_delta": "+0.3", "new_services": [], "removed_services": []},
      "drift": []
    }
  ],
  "drift_summary": {
    "undocumented": [],
    "orphaned_docs": [],
    "naming_mismatches": []
  }
}
```

## Phase B — File audit

Run `scripts/scan-files.sh > "$AUDIT_DIR/files.json"`.

The script does:

1. Walk tracked roots (depth-bounded; respect `.gitignore` patterns when present)
2. Apply hard-skip floor (drop entries entirely — they don't even appear in output)
3. For each survivor, compute:
   - `mtime_days` (days since last modification)
   - `inbound_refs` (count of files mentioning this file's basename or relative path)
   - `in_use_signals` (list of which in-use signal patterns matched, per `safety-rules.md` §"In-use signals")
   - `is_dated_artifact` (filename contains `YYYY-MM-DD` and that date is past)
   - `content_hash` (sha256 first 8 chars, for dedup)
4. Categorize:
   - `mtime_days > 90 AND inbound_refs == 0 AND in_use_signals == []` → `SAFE_QUARANTINE`
   - `mtime_days > 90 AND (inbound_refs > 0 OR in_use_signals != [])` → `WATCHLIST`
   - `mtime_days > 90 AND is_dated_artifact AND inbound_refs == 0` → `DATED_HISTORICAL` (subtype of SAFE_QUARANTINE)
   - any pair sharing `content_hash` → `DUPLICATE` (one keeps, others go to QUARANTINE candidates)

Output `files.json` schema:
```json
{
  "audit_date": "2026-05-09",
  "totals": {"scanned": 8421, "skipped_floor": 1203, "candidates": 47},
  "categorized": {
    "SAFE_QUARANTINE": [{"path": "...", "mtime_days": 120, "size": 1024, "hash": "abc12345", "reason": "mtime+90 no_refs"}],
    "WATCHLIST": [{"path": "...", "mtime_days": 95, "in_use_signals": ["mentioned_in_runbook"], "reason": "in-use signal blocks action"}],
    "DATED_HISTORICAL": [],
    "DUPLICATE": [{"path": "...", "duplicate_of": "...", "hash": "abc12345"}]
  }
}
```

## Phase C — Link integrity

Run `scripts/check-links.sh > "$AUDIT_DIR/links.json"`.

The script does:
1. Markdown link checker — for every `.md` in tracked roots, extract `[text](path)` patterns. For each path that's relative and not a URL, check existence.
2. Symlink checker — `find <tracked roots> -type l ! -exec test -e {} \;` → list dangling symlinks.
3. Shell source checker — for every `.sh`, grep for `source <path>` and `. <path>`. Verify each.
4. Python import checker (project-internal only) — for every `.py`, parse `from X import` and `import X`. If `X` looks project-local (not stdlib, not installed package), verify the corresponding file exists.

Output `links.json`:
```json
{
  "audit_date": "2026-05-09",
  "broken_md_links": [{"in_file": "...", "line": 42, "target": "...", "reason": "target_missing"}],
  "dangling_symlinks": [{"path": "...", "points_to": "..."}],
  "broken_sources": [{"in_file": "...", "line": 17, "target": "..."}],
  "broken_imports": [{"in_file": "...", "line": 3, "module": "..."}]
}
```

## Phase D — Generate REPORT.md

Read `containers.json`, `files.json`, `links.json` + `state.yaml`. Render against `templates/REPORT.md`.

Sections in order:

1. **Header** — date, run flags, time elapsed
2. **Summary counts** — at-a-glance numbers (stale found, broken links, drift items, watchlist size)
3. **Trend** — pull last 12 entries from `state.yaml: audit_history`. Show whether stale-file count is accelerating, holding, or shrinking. One-paragraph diagnosis.
4. **Container drift** — every entry from `containers.json: drift_summary`. Per-container: delta from baseline, services added/removed, disk growth.
5. **Stale files (proposed action)** — `SAFE_QUARANTINE` + `DATED_HISTORICAL` + `DUPLICATE`. Each row: path, mtime, hash, reason, **proposed quarantine path**, **restore command**.
6. **Watchlist** — `WATCHLIST` entries. No proposed action. Listed for transparency.
7. **Broken links** — by category (md, symlinks, sources, imports). Each: file:line, target, suggested fix (when obvious).
8. **What I deliberately did NOT touch and why** — counts of hard-skip applications by reason. The negative space.
9. **Pattern-rule proposals** — if `state.yaml: decision_log` shows 3+ consistent approvals on a glob, propose graduating to `pattern_rule`.
10. **Auto-restored allow-list entries** — files the user `mv`'d back from `.archive/`. These are auto-added to `allow_list` with a comment.
11. **Approval gate** — explicit list of categories awaiting y/n.

Write to `/root/homelab/docs/organizer/AUDIT-YYYY-MM-DD.md`.

## Phase E — Approval gate

Stop after Phase D. Present summary to user via `AskUserQuestion`:

```
Audit complete. Proposed actions:
  - Quarantine N files (SAFE_QUARANTINE)
  - Quarantine M dated artifacts (DATED_HISTORICAL)
  - Quarantine K duplicates (keeping the canonical)
  - Fix L broken links (suggested fixes available)

Approve all / approve per category / approve per item / decline
```

For each approved bucket:
- Run `scripts/quarantine.sh --bucket <name> --audit-dir "$AUDIT_DIR"`
- Append entries to `/root/homelab/.archive/$AUDIT_DATE/MANIFEST.md`
- Update `state.yaml: decision_log`
- Append to `/root/homelab/docs/memory/ORGANIZATION_LOG.md`

After all approvals processed:
- Append `audit_history` entry to `state.yaml` (counts, status)
- Append one-line entry to `/root/homelab/docs/memory/MEMORY_INDEX.md` linking to the AUDIT report

Final report to user:
```
Quarantined: N files → /root/homelab/.archive/YYYY-MM-DD/
Manifest: /root/homelab/.archive/YYYY-MM-DD/MANIFEST.md
state.yaml updated: <fields>
Memory updated: ORGANIZATION_LOG.md, MEMORY_INDEX.md
```

Stop. Do not run another audit immediately.
