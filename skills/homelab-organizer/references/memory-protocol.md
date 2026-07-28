# Memory Protocol — when to update what

This file is loaded after Phase E approval, before final reporting. Its job: keep the homelab's two memory layers (auto-memory, project memory) consistent without writing noise.

## Two layers, two purposes

| Layer | Path | Purpose | Update frequency |
|---|---|---|---|
| Auto-memory | `/root/.claude/projects/-root/memory/` | Cross-session Claude knowledge | Only on structural findings |
| Project memory | `/root/homelab/docs/memory/` | Homelab-local persistent notes | Every audit |

## Auto-memory updates

Update only on **structural** findings. A "structural" finding is one that changes future Claude's mental model of the homelab. Routine quarantines do NOT qualify.

**Update auto-memory when:**

- Audit detects a new container that has no doc and no entry in `project_homelab.md`. Append a one-liner to that file describing the container.
- A `pattern_rule` graduates from proposal to approved (3 consistent approvals → user signed off). Append one line: `homelab-organizer learned to <action> files matching <pattern> (confirmed YYYY-MM-DD)`.
- Audit detects a major reorg (e.g., migrating /root/scratch/* to /root/homelab/scripts/scratch/). Append one line to `MEMORY.md` index pointing to the `ORGANIZATION_LOG.md` entry.
- A container is decommissioned (was in `container_baselines` but `pct list` no longer shows it). Update `project_homelab.md` to note the decommission.

**Never write to auto-memory:**

- Per-audit summary counts
- Routine quarantines (mtime+90d+no-refs is the boring case)
- Watchlist entries
- Broken-link reports

## Project memory updates

Always update these files on a successful audit:

### `MEMORY_INDEX.md`

Append one line per audit, after existing entries:
```markdown
- [Audit YYYY-MM-DD](AUDIT-YYYY-MM-DD.md) — N quarantined, M broken links, K drift items
```

### `ORGANIZATION_LOG.md`

Append-only structural log. Each quarantine action gets one line:
```markdown
YYYY-MM-DDTHH:MM:SSZ  QUARANTINE  <original_path>  →  <archive_path>  (reason: <reason>, audit: AUDIT-YYYY-MM-DD)
```

Each restore action gets one line:
```markdown
YYYY-MM-DDTHH:MM:SSZ  RESTORE     <archive_path>  →  <original_path>  (manual)
```

Each major reorg gets one line:
```markdown
YYYY-MM-DDTHH:MM:SSZ  REORG       <description>  (audit: AUDIT-YYYY-MM-DD)
```

### `LESSONS_LEARNED.md`

Update only when an audit catches something the skill should have prevented:
- A broken link that mattered (was hit by a runbook or active script)
- A drift item that caused a real incident
- A pattern that fooled the safety rules

Each lesson:
```markdown
## YYYY-MM-DD — <one-line lesson>

What happened: <one paragraph>
Skill change required: <one paragraph or "none — informational">
```

## Update sequence (must be in this order)

After Phase E action approvals are processed:

1. Append entries to `ORGANIZATION_LOG.md` (one per action)
2. Append entry to `MEMORY_INDEX.md` (one per audit)
3. If lesson learned: append to `LESSONS_LEARNED.md`
4. Update `state.yaml` (`audit_history`, `container_baselines`, learned rules)
5. Auto-memory updates (only if structural)

Steps 1-5 are the full sequence.

## Idempotency

If an audit is re-run on the same day:
- `MEMORY_INDEX.md` — check for existing entry with same date; if exists, update it instead of appending
- `ORGANIZATION_LOG.md` — append new entries (each action has unique timestamp)

## What gets committed

After memory updates, the orchestrator does:
```bash
cd /root/homelab
git add docs/memory/MEMORY_INDEX.md docs/memory/ORGANIZATION_LOG.md docs/organizer/state.yaml docs/organizer/AUDIT-*.md .archive/*/MANIFEST.md
git commit -m "chore(organizer): audit YYYY-MM-DD — N quarantined, M links fixed"
```

This is the only commit per audit. Memory updates and the audit report ship together.
