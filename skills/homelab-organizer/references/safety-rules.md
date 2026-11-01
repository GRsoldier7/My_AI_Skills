# Safety Rules — the floor

These rules are the **floor** for every operating mode. They are not configurable. They override `--unsafe` for the items marked "ALWAYS".

## Hard-skip floor (ALWAYS, even with --unsafe)

Never read, write, move, or quarantine anything matching these:

- `.git/` — git internals
- `/root/.claude/settings*.json` — Claude Code config
- `~/.ssh/`, `/etc/ssh/` — SSH keys
- `/etc/`, `/usr/`, `/var/lib/` (outside container projects), `/sys/`, `/proc/`, `/boot/` — system paths
- Files modified within last **7 days** (regardless of refs)
- Anything inside `.archive/` (already quarantined — we don't quarantine the quarantine)
- Anything matching `pattern_rules: always-skip` in `state.yaml`
- Any path in `allow_list` in `state.yaml`
- **Any path containing `/credentials/`, `/secrets/`, `/keys/`** — credentials class. Even duplicates may be intentional copies for different services. Never propose action.
- **`/root/` dotfiles with system meaning**: `/root/.forward`, `/root/.lesshst`, `/root/.selected_editor`, `/root/.bash_history`, `/root/.Xauthority`, `/root/.viminfo`, `/root/.python_history`, `/root/.cache/*`, `/root/.local/*`. Old mtime is normal — these are passive system files.

## Hard-skip default (skipped without `--unsafe`, but overridable)

These are skipped by default and require explicit `--unsafe` plus per-item user approval:

- `.planning/active/` — current GSD work-in-progress
- `.venv/`, `venv/`, `node_modules/`, `__pycache__/`, `target/`, `dist/`, `build/` — generated/dependency dirs
- `backups/`, `*backup*/` — explicit backup directories
- Lockfiles: `package-lock.json`, `yarn.lock`, `poetry.lock`, `Pipfile.lock`, `Cargo.lock`, `pnpm-lock.yaml`
- `.env*` files — secrets
- Anything inside `/var/lib/docker/`, `/var/lib/lxc/` — container runtime data
- Anything matching `pattern_rules: always-watchlist` in `state.yaml`

## In-use signals (auto-demote to Watchlist, never quarantine)

If any of these are true, the file is in-use even if mtime+ref criteria say otherwise. Demote to Watchlist; do not propose action.

- File path mentioned in `MEMORY.md`, `MEMORY_INDEX.md`, `CLAUDE.md`, `LESSONS_LEARNED.md`, `SELF_HEALING.md`
- File path mentioned in any `.planning/*/PLAN.md` or `STATE.md`
- File path appears in any active runbook under `/root/homelab/docs/runbooks/`
- File path referenced from a systemd unit or cron entry: on the host, or by basename in a running guest's crontabs, cron dirs, unit files and drop-ins in the admin and package unit dirs (one read-only `pct exec` per guest, path tokens only)
- File, or its directory, bound into a guest by an LXC mount point (`mpN:` / `lxc.mount.entry:` host path)
- File is `__init__.py`: a package marker, referenced by the import system, never by name
- File is empty (0 bytes): there is no content to judge, and its existence may be the point (a marker, a placeholder config)
- File content is credential-shaped (a private-key block, a known token prefix, a literal assigned to a password/secret/token/key name). Quarantine would copy the secret into the archive, which is pushed to another node. The scanner records only that it matched, never the text. A heuristic: a short bare default slips past it
- File is the target of any symlink in tracked roots
- **File extension is `.service`, `.socket`, `.timer`, `.target`, `.path`, `.mount` — anywhere.** Systemd units are referenced via `systemctl enable`, not by other files. Old mtime is the norm; old systemd unit ≠ stale.
- File is on the "passive infrastructure" list: `Caddyfile`, `nginx.conf`, `httpd.conf`, `postgresql.conf`, `redis.conf`, `crontab`, `cron.d/*`, `cron.daily/*` — referenced by daemons, not by other files.

## Reversibility contract

Before proposing any action:

1. The action must produce a manifest entry containing:
   - Original absolute path
   - mtime, size, content hash (sha256)
   - Reason flagged
   - Restore command (must be a single, copy-paste-runnable shell line)
2. If you cannot generate a working restore command, do not propose the action.
3. The restore command must work even if the originating skill instance is gone.

## Override semantics

`--unsafe` permits action on items in the **default** skip list, NOT the floor.

When `--unsafe` is set:
- The skill must surface the override in every approval prompt: `⚠ --unsafe is active. Proposed actions include items from the default skip list.`
- Floor-list items are still rejected. The skill says: `Cannot act on <path>: hard-skip floor item.`
- Per-item approval is still required. `--unsafe` does not auto-approve.

## When in doubt

When uncertain whether a file qualifies, demote to Watchlist. False positives in the action list cost more than false negatives in the watchlist.
