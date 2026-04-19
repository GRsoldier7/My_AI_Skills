---
name: notebooklm
description: |
  Complete programmatic access to Google NotebookLM via the notebooklm-py CLI.
  Creates notebooks, adds sources (URLs, YouTube, PDFs, audio, video, images, text),
  generates all artifact types (podcast, video, quiz, flashcards, slide deck, infographic,
  mind map, report), downloads results, and supports web research and chat.

  CORE USE: Automated working-memory backup system — backs up short-term memory, long-term
  memory, lessons learned, and error logs to a dedicated NotebookLM notebook. Triggers
  automatically at session end (Stop hook) and when context window reaches 60%.

  EXPLICIT TRIGGER on: "/notebooklm", "/backup-memory", "create a podcast about",
  "audio overview", "generate a quiz from", "summarize these URLs", "NotebookLM",
  "add to notebooklm", "flashcards for studying", "turn this into a podcast",
  "create flashcards", "generate a slide deck", "make an infographic", "create a mind map",
  "install notebooklm", "briefing doc", "study guide from", "deep dive podcast",
  "backup memory", "save working memory", "context is getting full", "60% context".

compatibility: Requires notebooklm-py CLI installed at ~/.notebooklm-venv; Google account
  authenticated via nlm_login.py; Python 3.10+
metadata:
  author: aaron-deyoung
  version: "4.0"
  domain-category: core
  adjacent-skills: knowledge-management, data-storytelling, session-optimizer
  last-reviewed: "2026-04-19"
  review-trigger: "notebooklm-py version bump, auth flow changes, new artifact type, memory workflow updates"
allowed-tools: Bash
---

## Composability Contract
- Input expects: topic, URLs, files, research query, OR memory backup trigger
- Output produces: notebooks, sources, generated artifacts (audio, quiz, slides, etc.), memory backups
- Hands off to: knowledge-management (vault organization), data-storytelling (artifact framing)
- Receives from: any skill needing content → audio/visual/study material, or session end hooks

---

## Venv Activation Helper

All commands use this prefix (macOS/Linux):
```bash
NLM="source $HOME/.notebooklm-venv/bin/activate && notebooklm"
```

---

## Working Memory Backup System

### ⚠️ PER-PROJECT NOTEBOOK RULE
Every Claude Code project gets **its own dedicated NotebookLM notebook**.
Never mix projects into a single notebook. Each notebook is the single source
of truth for that project's working memory.

**Naming convention (always follow exactly):**
```
[Project Name] — Working Memory | Aaron DeYoung
```

**Examples:**
- `Gmail Inbox Automation — Working Memory | Aaron DeYoung`
- `n8n Workflow Builder — Working Memory | Aaron DeYoung`
- `Foundation AddOn — Working Memory | Aaron DeYoung`
- `Biohacking Dashboard — Working Memory | Aaron DeYoung`

**Notebook ID storage:**
```bash
# Project-level: $PROJECT_DIR/.claude/nlm-notebook-ids.env
NLM_PROJECT_NOTEBOOK_ID="<uuid>"

# Global fallback: ~/.claude/nlm-notebook-ids.env
NLM_WORKING_MEMORY_NOTEBOOK_ID="283d88be-..."   # cross-project / meta only
```

**Known project notebooks:**
| Project | Notebook ID | Name |
|---------|-------------|------|
| Gmail | `bf0a62ee-060e-4f67-945d-97d8c6615669` | Gmail Inbox Automation — Working Memory \| Aaron DeYoung |
| Global/Meta | `283d88be-c73d-4b3f-bb22-4af6f7437dd9` | AI Working Memory — Claude Projects |

**Creating a notebook for a new project:**
```bash
source ~/.notebooklm-venv/bin/activate
notebooklm create "[Project Name] — Working Memory | Aaron DeYoung"
# Then save the returned UUID to $PROJECT_DIR/.claude/nlm-notebook-ids.env
echo 'NLM_PROJECT_NOTEBOOK_ID="<uuid>"' > .claude/nlm-notebook-ids.env
```

### Memory Tiers + Source Naming Convention

**Every source title MUST follow this exact format:**
```
YYYY-MM-DD - [Project Name] — [Type]: [Topic]
```

**Types — use these exact labels:**
| Type | When to use | Frequency |
|------|-------------|-----------|
| `Working Memory (Short Term)` | Current session context, in-flight state, conversation notes | Every Stop |
| `Working Memory (Long Term)` | Persistent `memory/*.md` files, architecture docs | Every Stop |
| `Lesson Learned` | Something discovered that changes future behavior | Every Stop |
| `Problem Faced` | Errors, failures, blockers (even unsolved ones) | Every Stop |
| `Problem Overcome` | A solved problem — include the fix | Every Stop |
| `Session Summary` | End-of-session accomplishments and decisions | Every Stop |
| `Reference` | Stable configs, filter maps, system-state snapshots | On change |

**Examples:**
- `2026-04-19 - Gmail — Working Memory (Long Term): Inbox System Architecture`
- `2026-04-19 - Gmail — Session Summary: Built 120 Filters + Backfilled 3100 Emails`
- `2026-04-19 - Gmail — Lesson Learned: Gmail Filter API Only Allows 1 User Label`
- `2026-04-19 - Gmail — Problem Faced: batch_modify Throttles at ~50 IDs`
- `2026-04-19 - Gmail — Problem Overcome: Sequential Retry Clears Concurrency Errors`
- `2026-04-19 - n8n — Working Memory (Short Term): Article Processor Debug State`
- `2026-04-19 - Global — Reference: NotebookLM Per-Project Notebook Registry`

### 60% Context Trigger
The Stop hook fires after EVERY Claude response. This is the 60% proxy — the backup runs
before context is lost to compaction. The `nlm-backup.sh` script uses file timestamps to
only upload CHANGED files (deduplication via SHA256 hash tracking).

---

## CLI Operator Mode

1. **Preflight:** auth check, venv activation, context selection.
2. **Ingest:** add sources with stable titles + wait for READY.
3. **Generate:** one artifact at a time with explicit instructions.
4. **Verify:** wait for completion, download, size-check output.
5. **Persist memory:** append concise outcomes to project memory file.

---

## NotebookLM Memory Lifecycle

### 1. Capture
- Topic, objective, audience, and success criteria.
- Source list (URLs/files) and trust-level notes.

### 2. Distill
- Artifact outputs (podcast, slides, quiz) with one-line usefulness summary.
- Key claims needing citation or follow-up verification.

### 3. Store
- Save compact session summary in `.ai-memory/` or linked run log.
- Keep only durable facts/decisions, not raw transcript dumps.

### 4. Rehydrate
- Before next run, read prior memory and reuse notebook where continuity helps.
- If context diverged, create new notebook and link to previous one.

---

## Core Principles

1. **Auth is fragile** — Google cookies expire 7–30 days. Always `notebooklm auth check` first.
2. **Context required** — Every command except `list`/`create` needs `notebooklm use <id>`.
3. **Sources must be READY** — Wait with `source wait <id>` before generating.
4. **Generation is async** — Prefer `--wait` flag for blocking inline completion. For non-blocking, use `artifact wait <id>`. Audio 10–20 min, video 15–45 min.
5. **No parallel generation** — Google rate-limits per notebook. Sequential only.
6. **Deduplication** — Hash-check files before upload. Never re-upload unchanged content.
7. **Graceful degradation** — If auth fails, write backup to local file; alert user.

---

## Environment Setup

### Install (one-time)
```bash
python3 -m venv ~/.notebooklm-venv
source ~/.notebooklm-venv/bin/activate
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
| Backup memory | `~/.claude/scripts/nlm-backup.sh` |

---

## Standard Workflows

### Working Memory Backup (automated)
```bash
~/.claude/scripts/nlm-backup.sh [project_dir]
# Runs automatically via Stop hook. Backs up all memory tiers.
```

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
| Backup hook fails | Auth expired at session end | Write fallback to `~/.claude/nlm-backup-pending/` |

---

## Anti-Patterns

1. **Running `notebooklm login` directly** — requires interactive input. Use nlm_login.py.
2. **Generating before sources are READY** — silently produces incomplete output.
3. **Parallel generations** — both fail with 429. Always sequential.
4. **Re-uploading unchanged files** — wastes quota. Always hash-check first.
5. **Embedding full storage_state.json in Co-work** — wastes ~1,700 tokens. Strip to 3 domains.
6. **Asking user to run commands** — skill must be fully automated. User only signs in to Google.
7. **Ignoring graceful degradation** — if backup fails, always log error + write local fallback.

---

## Quality Gates

- [ ] Auth check passes with SID cookie before any workflow
- [ ] Notebook context set before source/generate commands
- [ ] All sources confirmed READY before generating
- [ ] Artifact confirmed COMPLETED before downloading
- [ ] Download file exists and is non-zero bytes
- [ ] Operator state tracked (notebook_id, source_ids, artifact_ids, output paths)
- [ ] Memory lifecycle completed (capture → distill → store → rehydrate)
- [ ] Hash deduplication prevents re-uploading unchanged files
- [ ] Graceful degradation: local fallback written if NLM unavailable
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
- [ ] Local fallback configured?
