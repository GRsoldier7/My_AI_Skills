---
name: notebooklm
description: |
  Complete programmatic access to Google NotebookLM via the notebooklm-py CLI.
  Creates notebooks, adds sources (URLs, YouTube, PDFs, audio, video, images), generates
  all artifact types (podcast, video, quiz, flashcards, slide deck, infographic, mind map,
  report), downloads results, and supports web research and chat.

  EXPLICIT TRIGGER on: "/notebooklm", "create a podcast about", "audio overview", "generate
  a quiz from", "summarize these URLs", "NotebookLM", "add to notebooklm", "flashcards for
  studying", "turn this into a podcast", "create flashcards", "generate a slide deck",
  "make an infographic", "create a mind map", "install notebooklm", "add notebooklm to cowork",
  "briefing doc", "study guide from", "deep dive podcast".

  Also activates on: "create a podcast about X", "I want to study this material", "can you
  summarize these documents into something I can listen to", "make this into audio content".
compatibility: Requires notebooklm-py CLI installed; Google account authenticated; Python 3.10+
metadata:
  author: aaron-deyoung
  version: "2.1"
  domain-category: core
  adjacent-skills: wrapup, knowledge-management, obsidian-automation-architect
  last-reviewed: "2026-04-04"
  review-trigger: "notebooklm-py version bump, Google NotebookLM UI changes that break auth, new artifact type added"
allowed-tools: Bash
---

## Composability Contract
- Input expects: topic, URLs, files, or research query to process
- Output produces: notebooks, sources, generated artifacts (audio, quiz, slides, etc.)
- Hands off to: wrapup (session summaries), knowledge-management (vault organization)
- Receives from: any skill needing to transform content into audio/visual/study material

---

## Core Principles

1. **Auth is fragile** — Google cookies expire 7–30 days. Always `notebooklm auth check` first.
2. **Context required** — Every command except `list`/`create` needs `notebooklm use <id>`.
3. **Sources must be READY** — Wait with `source wait <id>` before generating.
4. **Generation is async** — Audio 10–20 min, video 15–45 min. Use `artifact wait`.
5. **No parallel generation** — Google rate-limits per notebook. Sequential only.
6. **Windows encoding** — Prefix ALL commands with `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`.

---

## Environment Setup

**CRITICAL on Windows:** Every `notebooklm` command MUST be prefixed:
```bash
source "$HOME/.notebooklm-venv/Scripts/activate" && PYTHONIOENCODING=utf-8 PYTHONUTF8=1 notebooklm <command>
```

### First-Time Install
```bash
python3 -m venv ~/.notebooklm-venv
source ~/.notebooklm-venv/Scripts/activate  # or bin/activate on Linux/Mac
pip install "notebooklm-py[browser]" && playwright install chromium
```

### Authentication
Claude writes and runs a Playwright login script automatically — user only signs in to Google:
```python
# nlm_login.py — auto-detects login completion
import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright

STORAGE_DIR = Path.home() / ".notebooklm"
STORAGE_FILE = STORAGE_DIR / "storage_state.json"

async def main():
    STORAGE_DIR.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://notebooklm.google.com/")
        print("Sign in to Google in the Chrome window.")
        try:
            await page.wait_for_selector(
                "mat-sidenav-container, notebook-list, .notebooks-container",
                timeout=300_000)
        except Exception:
            for _ in range(150):
                if "notebooklm.google.com" in page.url and "accounts.google.com" not in page.url:
                    break
                await asyncio.sleep(2)
        await asyncio.sleep(3)
        storage = await context.storage_state()
        STORAGE_FILE.write_text(json.dumps(storage, indent=2))
        print(f"Session saved to {STORAGE_FILE}")
        await browser.close()

asyncio.run(main())
```

**NEVER** use `notebooklm login` directly — it requires interactive terminal input unavailable in Claude Code.

---

## Decision Framework

| Goal | Command |
|------|---------|
| Check auth | `notebooklm auth check` |
| List notebooks | `notebooklm list` |
| Create notebook | `notebooklm create "Title"` |
| Set context | `notebooklm use <id>` |
| Add URL source | `notebooklm source add "https://..."` |
| Add file source | `notebooklm source add ./file.pdf` |
| Add inline text | `notebooklm source add "text content" --type text --title "Name"` |
| Research topic | `notebooklm source add-research "query" --mode deep --no-wait` |
| Chat with sources | `notebooklm ask "question"` |
| Generate podcast | `notebooklm generate audio "instructions"` |
| Generate quiz | `notebooklm generate quiz --difficulty medium` |
| Generate slides | `notebooklm generate slide-deck --format detailed` |
| Download artifact | `notebooklm download audio ./out.mp3` |

---

## Standard Workflows

### Research-to-Podcast
```bash
notebooklm auth check
notebooklm create "Research: [topic]"
notebooklm use <id>
notebooklm source add "https://..."     # for each URL
notebooklm source wait <source_id>      # wait for processing
notebooklm generate audio "Focus on key decisions"
notebooklm artifact wait <artifact_id>
notebooklm download audio ./podcast.mp3
```

### Session Wrapup to AI Brain
```bash
notebooklm auth check
notebooklm use <brain_notebook_id>
notebooklm source add "/path/to/session-summary.md"
```

### Multi-Format from One Notebook
```bash
notebooklm generate audio "Executive summary"    # sequential only
notebooklm artifact wait <id>
notebooklm generate quiz --difficulty hard
notebooklm artifact wait <id>
notebooklm generate slide-deck --format presenter
```

---

## Edge Cases

| Case | Symptom | Fix |
|------|---------|-----|
| Auth expired | SID cookie missing | Re-run nlm_login.py |
| Source stuck PROCESSING | >10 min in processing state | Delete and re-add; DRM PDFs fail silently |
| Generation 429 | Rate limit error | Wait 10–20 min; never retry within 2 min |
| Download fails | Artifact shows completed | Check file extension matches type (audio→.mp3) |
| CLI not found | `command not found` | Activate venv or use full path |
| RPC error on `use` | "RPC returned null" | Notebook may not exist; try `notebooklm list` |
| Source add fails | "Failed to get SOURCE_ID" | Create new notebook with `-n <id>` flag |

---

## Anti-Patterns

1. **Running `notebooklm login` directly** — requires interactive input. Use nlm_login.py.
2. **Missing PYTHONIOENCODING on Windows** — causes UnicodeEncodeError. Always prefix.
3. **Generating before sources are READY** — silently produces incomplete output.
4. **Parallel generations** — both fail with 429. Always sequential.
5. **Embedding full storage_state.json in Co-work** — wastes ~1,700 tokens. Strip to 3 domains.
6. **Asking user to run commands** — skill must be fully automated. User only signs in to Google.

---

## Quality Gates

- [ ] Auth check passes with SID cookie before any workflow
- [ ] Notebook context set before source/generate commands
- [ ] All sources confirmed READY before generating
- [ ] Artifact confirmed COMPLETED before downloading
- [ ] Download file exists and is non-zero bytes
- [ ] Auth flow was fully automated — user only signed in to Google

---

## Self-Evaluation

Before presenting any NotebookLM workflow:
[ ] Did I prefix all commands with PYTHONIOENCODING=utf-8 on Windows?
[ ] Did I check auth before starting?
[ ] Did I set notebook context with `use`?
[ ] Am I waiting for sources before generating?
[ ] Am I generating sequentially, not in parallel?
[ ] Am I handling the case where `use` fails with RPC error?
