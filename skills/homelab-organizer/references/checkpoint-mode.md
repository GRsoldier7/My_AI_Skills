# Checkpoint Mode — the 5-check fast path

Used when another skill creates or moves files in a tracked root. Cost target: <5 seconds, ≤50 tokens output. Read-only and non-blocking.

## Invocation context

Triggered when the calling skill (gsd-execute-phase, gsd-new-project, gsd-add-phase, frontend-design, mcp-server-builder) finishes a write/move and the new path falls under a tracked root:

- `/root/homelab/`
- `/opt/echelon/Biohacking_Optimization/`
- `/root/.claude/sessions/`, `/root/.claude/todos/`, `/root/.claude/file-history/`
- `/root/My_AI_Skills/`
- `/root/` top-level scratch (depth-1 only)

## The 5 checks

Run all five against the new file. Each is a yes/no with a clear flag string if no.

### 1. Expected location for type

Is this file type living where files of its type belong? Inferred from existing folder conventions:

- `*.md` runbooks → `docs/runbooks/`
- `*.sh` scripts → `scripts/` or `tools/`
- `*.py` scripts → `scripts/` or `tools/`
- `*.tf` Terraform → `infra/` or `terraform/`
- `*.yaml`/`*.yml` configs → `infra/`, `configs/`, or alongside the thing they configure

Flag: `unexpected location for type — expected near <expected_dir>, got <actual_dir>`

### 2. Naming convention for folder

Does the new filename match the convention of its sibling files?

- All siblings UPPERCASE? → flag if camelCase or kebab-case
- All siblings kebab-case? → flag if snake_case
- Sibling pattern includes `YYYY-MM-DD-`? → flag if date-prefix is missing or wrong format

Flag: `naming mismatch — siblings use <pattern>, new file uses <new>`

### 3. Duplication check

Compute `sha256sum` of the new file. If any other file in the same tracked root has matching hash → flag.

For markdown specifically, also do a fuzzy check: first 200 bytes match → flag as near-duplicate.

Flag: `duplicate of <path>` or `near-duplicate of <path>`

### 4. Stale-folder landing

Is the parent directory in the current `state.yaml` `pattern_rules` as `always-watchlist` or `auto-quarantine`? If so, the new file inherits the same status flag — alerting the user that their new file landed in a folder already on the radar.

Flag: `landed in flagged folder <parent> (rule: <rule_action>)`

### 5. New top-level dir

Is this the first file inside a brand-new top-level directory in a tracked root? (e.g., `/root/homelab/<new-dir>/`)

Flag: `new top-level dir created: <path>`

## Output protocol

If all 5 checks pass:
```
✓ ok
```

If any flag(s):
```
⚠ flag: <comma-separated reasons> — added to watchlist
```

Append the flag to `/root/homelab/docs/organizer/watchlist.md` with one line:
```
YYYY-MM-DDTHH:MM:SS  <new_file_path>  <flag_reasons>
```

## Hard rules in checkpoint mode

- NEVER propose an action
- NEVER load `references/audit-procedure.md` (that's full-audit territory)
- NEVER touch state.yaml `audit_history` (that's full-audit territory)
- NEVER call any of the `scripts/*.sh` (those are full-audit only)
- DO append to `watchlist.md` (cheap, append-only)
- DO output ≤1 line of text

## When to escalate

If the new file looks dangerous (lands inside `/etc/`, has world-writable perms, contains what looks like a secret key) → checkpoint exits with `⚠ escalate: <reason>` and tells the user to run `/homelab-organizer --files` for full investigation. Don't try to act on it in checkpoint mode.
