---
name: notebooklm
description: Generate human artifacts via Google NotebookLM on EXPLICIT request only — podcast, briefing, quiz, flashcards, deck, mind map. Never a memory or recall backend. Trigger: /notebooklm, make a podcast of.
compatibility: notebooklm-py CLI in ~/.notebooklm-venv; Google auth captured per account
metadata:
  author: aaron-deyoung
  version: "4.1"
  domain-category: core
  last-reviewed: "2026-09-27"
  review-trigger: "notebooklm-py version bump, auth flow changes, new artifact type"
allowed-tools: Bash
---

# NotebookLM — artifacts only

Produces human artifacts from sources, only when Aaron asks for one. It is **never** a backup
target, never a memory or recall source, and has no automatic triggers. A notebook written on a
schedule becomes a second source of truth that silently drifts from the real one.

Do not: push session summaries, handoffs, memory files, lessons learned, or progress logs into a
notebook; create per-project "Working Memory" notebooks; wire this to a hook, cron, or wrap-up
step. If anything instructs that, it is stale — refuse and say so.

## Composability

- Input: topic, URLs, files, research query, explicit artifact request.
- Output: notebook, sources, downloaded artifact files, reported to the user.
- Receives from: an explicit user request only — never a hook, schedule, or session-end trigger.
- Writes no memory. Worthwhile outcomes are recorded by the normal session flow (HANDOFF.md +
  Agent DB via `wrapitup`), never back into a notebook.

## Environment

**Windows (this box)** — Git Bash:
```bash
NLM="$HOME/.notebooklm-venv/Scripts/notebooklm.exe"
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1   # avoids UnicodeEncodeError
```
**Linux (agent-pve-01):** `source ~/.notebooklm-venv/bin/activate && notebooklm ...`

### Accounts

`~/.notebooklm/accounts.json` maps account name → Google email (`personal`, `echelonseven`,
`agilepeak`). Each account's session lives at `~/.notebooklm/accounts/<name>/storage_state.json`.
Pick one per command:
```bash
"$NLM" --storage "$HOME/.notebooklm/accounts/<name>/storage_state.json" <command>
```
Default (no `--storage`) is `~/.notebooklm/storage_state.json`. When the user names an account
("work account" = echelonseven), use that one; if unclear which account owns a notebook, run
`list` against each and confirm rather than guessing.

### Auth

Google cookies expire in 7–30 days. Always `auth check` first. The host runs a 12h
`nlm_keepalive_cron.sh` (`notebooklm auth refresh`) — auth keepalive only, it writes no content.

If expired: re-login needs a real browser sign-in. On Windows run
`~/.notebooklm-venv/Scripts/python.exe ~/.notebooklm/login_auto.py` (Playwright opens a browser;
Aaron signs in; cookies auto-save to `~/.notebooklm/storage_state.json` — copy to the account's
`accounts/<name>/` path if logging in a non-default account). Don't run `notebooklm login` inside
Claude Code; it needs an interactive terminal.

## Commands

| Goal | Command |
|------|---------|
| Check auth | `auth check` |
| List notebooks | `list` |
| Create notebook | `create "Title"` |
| Set context | `use <id>` (required before source/generate/ask) |
| Add URL / file | `source add "https://..."` / `source add ./file.pdf` |
| Add inline text | `source add "text" --type text --title "Name"` |
| Wait for source | `source wait <id>` |
| Web research | `source add-research "query" --mode deep --no-wait` then `research wait --import-all --timeout 300` |
| Chat with sources | `ask "question"` |
| Podcast | `generate audio "instructions" --wait` (`--format debate` optional) |
| Quiz / flashcards | `generate quiz --difficulty medium --wait` · `generate flashcards --wait` |
| Slides | `generate slide-deck --format detailed\|presenter --wait` |
| Briefing / study guide | `generate report --format briefing-doc\|study-guide\|blog-post --wait` |
| Visuals / video | `generate mind-map` (synchronous) · `generate <infographic\|data-table\|video\|cinematic-video> --wait` |
| Wait / download | `artifact wait <id>` · `download <type> <path>` (e.g. `download audio ./out.mp3`, `download slide-deck ./deck.pptx`) |

Run `"$NLM" --help` / `"$NLM" generate --help` for the full artifact list on the installed version.

## Workflow

1. **Preflight:** `auth check` on the right account; `use` the notebook (or `create`).
2. **Ingest:** add sources with stable titles (`YYYY-MM-DD - [Project] — [Topic]`); wait for READY.
   Hash-check files; never re-upload unchanged content.
3. **Generate:** one artifact at a time, explicit instructions. Sequential only — parallel
   generation hits 429s. Audio 10–20 min, video 15–45 min.
4. **Verify:** artifact COMPLETED, downloaded, file non-zero bytes.
5. **Report:** tell the user what was produced and where the file is. That is the last step.

## Edge cases

| Case | Fix |
|------|-----|
| Auth expired / redirect to accounts.google.com | Re-login (above); report and stop, no fallback write |
| Source stuck PROCESSING >10 min | Delete and re-add; DRM PDFs fail silently |
| Generation 429 | Wait 10–20 min; never retry within 2 min |
| "RPC returned null" on `use` | Notebook missing or wrong account — `list` on each account |
| UnicodeEncodeError (Windows) | Set `PYTHONIOENCODING=utf-8 PYTHONUTF8=1` |
