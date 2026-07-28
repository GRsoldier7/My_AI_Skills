---
name: notebooklm
description: |
  Human-artifact generation via Google NotebookLM, on explicit request ONLY — NotebookLM is
  NOT a memory backend, NOT a recall source, and has NO automatic triggers.

  Memory-of-record is the Hermes internal stack (pgvector on pg-prime + Graphiti graph) plus
  operator file memory. Never call this reflexively at session end or on context fill.

  Capabilities: creates notebooks, adds sources (URLs, YouTube, PDFs, audio, video, images,
  text), generates all artifact types (podcast, video, quiz, flashcards, slide deck,
  infographic, mind map, report), downloads results, and supports web research and chat.

  EXPLICIT TRIGGER on: "/notebooklm", "create a podcast about",
  "audio overview", "generate a quiz from", "summarize these URLs", "NotebookLM",
  "add to notebooklm", "flashcards for studying", "turn this into a podcast",
  "create flashcards", "generate a slide deck", "make an infographic", "create a mind map",
  "install notebooklm", "briefing doc", "study guide from", "deep dive podcast".

compatibility: Requires notebooklm-py CLI installed at ~/.notebooklm-venv; Google account
  authenticated via nlm_login.py; Python 3.10+
metadata:
  author: aaron-deyoung
  version: "4.0"
  domain-category: core
  adjacent-skills: knowledge-management, data-storytelling, session-optimizer
  last-reviewed: "2026-07-28"
  review-trigger: "notebooklm-py version bump, auth flow changes, new artifact type"
allowed-tools: Bash
---

## Composability Contract
- Input expects: topic, URLs, files, research query
- Output produces: notebooks, sources, generated artifacts (audio, quiz, slides, etc.)
- Hands off to: knowledge-management (vault organization), data-storytelling (artifact framing)
- Receives from: an explicit user request for a human artifact — never a hook, schedule, or session-end trigger

---

## Venv Activation Helper

All commands use this prefix (macOS/Linux):
```bash
NLM="source $HOME/.notebooklm-venv/bin/activate && notebooklm"
```

---

## NotebookLM is not memory

Memory-of-record is the internal Hermes stack — Postgres/pgvector `memory_vectors`
on pg-prime (CT 252), the Graphiti graph on graph-prime (CT 253), Redis L0 — plus
operator file memory under `/root/.claude/projects/-root/memory/` indexed by
`MEMORY.md`. Session state, lessons learned and problems solved go THERE.

This skill produces human artifacts — podcasts, briefings, decks, quizzes, study
guides — and only when Aaron asks for one. It is never a backup target, never a
recall source, and has no automatic triggers: no Stop hook, no session-end push,
no context-fill threshold.

Retired 2026-07-28, along with the per-project "Working Memory" notebook scheme,
the six `Every Stop` memory tiers, and the nightly bundle cron. A notebook that is
written on a schedule becomes a second source of truth that silently drifts from
the first — and the drift is invisible until you trust the wrong copy.

**Source titles** for artifact material follow: `YYYY-MM-DD - [Project] — [Topic]`.

---

## CLI Operator Mode

1. **Preflight:** auth check, venv activation, context selection.
2. **Ingest:** add sources with stable titles + wait for READY.
3. **Generate:** one artifact at a time with explicit instructions.
4. **Verify:** wait for completion, download, size-check output.
5. **Persist memory:** append concise outcomes to project memory file.

---

## Artifact Workflow

### 1. Capture
- Topic, objective, audience, and success criteria.
- Source list (URLs/files) and trust-level notes.

### 2. Distill
- Artifact outputs (podcast, slides, quiz) with one-line usefulness summary.
- Key claims needing citation or follow-up verification.

### 3. Report the outcome
- Tell the user what was produced and where it was downloaded. Reporting is this
  skill's last step — it holds `allowed-tools: Bash` and deliberately writes no
  memory of its own.
- If the outcome is worth keeping, `wrapup` persists it to operator file memory.
  Nothing is ever written back into the notebook.

---

## Core Principles

1. **Auth is fragile** — Google cookies expire 7–30 days. Always `notebooklm auth check` first.
2. **Context required** — Every command except `list`/`create` needs `notebooklm use <id>`.
3. **Sources must be READY** — Wait with `source wait <id>` before generating.
4. **Generation is async** — Prefer `--wait` flag for blocking inline completion. For non-blocking, use `artifact wait <id>`. Audio 10–20 min, video 15–45 min.
5. **No parallel generation** — Google rate-limits per notebook. Sequential only.
6. **Platform paths differ** — Linux/macOS use `bin/activate`; Windows uses `Scripts/activate` and the `PYTHONIOENCODING=utf-8 PYTHONUTF8=1` prefix.
7. **Deduplication** — Hash-check files before upload. Never re-upload unchanged content.
8. **Fail loudly** — If auth fails, report it and stop. There is nothing to fall back to: no artifact was generated, and no memory depends on this running.

---

## Environment Setup

**Linux / macOS (primary):**
```bash
source "$HOME/.notebooklm-venv/bin/activate" && notebooklm <command>
```

**Windows only** — also requires the encoding prefix:
```bash
source "$HOME/.notebooklm-venv/Scripts/activate" && PYTHONIOENCODING=utf-8 PYTHONUTF8=1 notebooklm <command>
```

### First-Time Install
```bash
python3 -m venv ~/.notebooklm-venv
# Linux/macOS:
source ~/.notebooklm-venv/bin/activate
# Windows:
# source ~/.notebooklm-venv/Scripts/activate
pip install "notebooklm-py[browser]" && playwright install chromium
```

### Authentication
```bash
source ~/.notebooklm-venv/bin/activate && python3 ~/.claude/skills/notebooklm/nlm_login.py
```
Claude writes and runs the Playwright login script — user only signs in to Google.
**NEVER** use `notebooklm login` directly — requires interactive terminal unavailable in Claude Code.

---

## Decision Framework

| Goal | Command |
|------|---------|
| Check auth | `notebooklm auth check` |
| List notebooks | `notebooklm list` |
| Create notebook | `notebooklm create "Title"` |
| Set context | `notebooklm use <id>` |
| Add URL source | `notebooklm source add "https://..."` |
| Add file source | `notebooklm source add ./file.md` |
| Add inline text | `notebooklm source add "text" --type text --title "Name"` |
| Research (blocking) | `notebooklm source add-research "query" --mode deep --import-all` |
| Research (non-blocking) | `notebooklm source add-research "query" --mode deep --no-wait` |
| Wait for research | `notebooklm research wait --import-all --timeout 300` |
| Chat with sources | `notebooklm ask "question"` |
| Generate podcast (blocking) | `notebooklm generate audio "instructions" --wait` |
| Generate podcast (debate) | `notebooklm generate audio "instructions" --format debate --wait` |
| Generate quiz | `notebooklm generate quiz --difficulty medium --wait` |
| Generate slides | `notebooklm generate slide-deck --format detailed --wait` |
| Generate briefing doc | `notebooklm generate briefing --wait` |
| Generate FAQ | `notebooklm generate faq --wait` |
| Wait for artifact | `notebooklm artifact wait <id>` |
| Download artifact | `notebooklm download audio ./out.mp3` |

---

## Standard Workflows

### Research-to-Podcast (recommended — blocking, agent-safe)
```bash
notebooklm auth check
notebooklm create "Research: [topic]"
notebooklm use <id>
notebooklm source add "https://..."          # seed source
notebooklm source add-research "topic" --mode deep --no-wait  # start research
notebooklm research wait --import-all --timeout 300           # wait + import
notebooklm generate audio "Focus on key decisions" --wait     # blocking generation
notebooklm download audio ./podcast.mp3
```

### Session Wrapup to AI Brain
```bash
notebooklm auth check
notebooklm use <brain_notebook_id>
notebooklm source add "/path/to/session-summary.md"
```

---

## Edge Cases

| Case | Symptom | Fix |
|------|---------|-----|
| Auth expired | SID cookie missing | Re-run nlm_login.py |
| Source stuck PROCESSING | >10 min in processing | Delete and re-add; DRM PDFs fail silently |
| Generation 429 | Rate limit error | Wait 10–20 min; never retry within 2 min |
| Download fails | Artifact shows completed | Check file extension matches type |
| CLI not found | `command not found` | Activate venv: `source ~/.notebooklm-venv/bin/activate` |
| RPC error on `use` | "RPC returned null" | Notebook may not exist; run `notebooklm list` |
| Source add fails | "Failed to get SOURCE_ID" | Create new notebook with `-n <id>` flag |

---

## Anti-Patterns

1. **Running `notebooklm login` directly** — requires interactive input. Use nlm_login.py.
2. **Missing PYTHONIOENCODING on Windows** — causes UnicodeEncodeError. Always prefix on Windows; not needed on Linux/macOS.
3. **Generating before sources are READY** — silently produces incomplete output.
4. **Parallel generations** — both fail with 429. Always sequential.
5. **Re-uploading unchanged files** — wastes quota. Always hash-check first.
6. **Embedding full storage_state.json in Co-work** — wastes ~1,700 tokens. Strip to 3 domains.
7. **Asking user to run commands** — skill must be fully automated. User only signs in to Google.
8. **Treating a notebook as memory** — no session state, lessons, or working memory goes here. It is an artifact target only; memory-of-record is the Hermes stack plus operator file memory.
9. **Firing without being asked** — no Stop hook, no schedule, no context-fill threshold. If Aaron did not request an artifact, this skill does not run.

---

## Quality Gates

- [ ] Auth check passes with SID cookie before any workflow
- [ ] Notebook context set before source/generate commands
- [ ] All sources confirmed READY before generating
- [ ] Artifact confirmed COMPLETED before downloading
- [ ] Download file exists and is non-zero bytes
- [ ] Operator state tracked (notebook_id, source_ids, artifact_ids, output paths)
- [ ] Artifact downloaded, verified non-zero, and its location reported to the user
- [ ] Hash deduplication prevents re-uploading unchanged files
- [ ] Auth/API failure reported to the user, not silently written somewhere else
- [ ] Auth flow was fully automated — user only signed in to Google

---

## Self-Evaluation

Before any NotebookLM workflow:
- [ ] Auth check passed?
- [ ] Notebook context set with `use`?
- [ ] Waiting for sources before generating?
- [ ] Generating sequentially, not in parallel?
- [ ] Hash-checking before re-upload?
- [ ] RPC error handling in place?
- [ ] Failure path reports and stops (no fallback write)?
