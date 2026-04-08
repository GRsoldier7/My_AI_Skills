---
name: obsidian-automation-architect
description: |
  Design and build automations that connect Obsidian to external systems using n8n, webhooks, Python scripts, and API integrations. Specializes in: n8n workflow design for Obsidian, webhook triggers from Obsidian to external services, automated daily note creation, task sync between Obsidian and external tools, file-based data ingestion into vault, and scheduled vault operations. Use when you want to automate something in or around Obsidian, connect Obsidian to another tool, schedule vault operations, or build pipelines that write to/read from the vault programmatically. Trigger phrases: "automate obsidian", "n8n obsidian", "connect obsidian to", "obsidian webhook", "auto-generate note", "sync tasks", "obsidian api", "write to vault automatically", "obsidian pipeline", "schedule vault operation".
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: product
  adjacent-skills: obsidian-vault-architect, ai-business-optimizer, biohacking-data-pipeline
  source-repo: GRsoldier7/My_AI_Skills
---

# Obsidian Automation Architect — Expert Skill

## Integration Architecture Overview

```
External World
     │
     ▼
[Trigger Layer]  — n8n schedules, webhooks, API events, file watchers
     │
     ▼
[Transform Layer] — Python scripts, n8n nodes, data normalization
     │
     ▼
[Vault Layer]    — Markdown files, frontmatter, inline fields
     │
     ▼
[Query Layer]    — Dataview reads, dashboard renders, Claude reads via MCP
```

## Obsidian File Interface

All automations write standard Obsidian markdown. The vault is just a folder of `.md` files — no special API required.

### Standard Note Format for Automated Notes
```markdown
---
created: {{ISO_TIMESTAMP}}
source: {{automation-name}}
area: {{area}}
type: {{note-type}}
---

# {{Title}}

{{content}}
```

### Task Injection Format
```
- [ ] {{task_description}} [area:: {{area}}] [priority:: {{priority}}] [due:: {{YYYY-MM-DD}}]
```

## n8n Workflow Patterns

### Pattern 1: Daily Note Auto-Creation (Schedule Trigger)
```
Cron (6am daily)
→ Read template file (filesystem node)
→ Replace {{date}} placeholders
→ Check if today's note exists (filesystem: file exists)
→ Write file only if not exists (filesystem: create file)
→ Path: Homelab/daily/{{YYYY}}/{{MM}}/{{YYYY-MM-DD}}.md
```

### Pattern 2: Email → Inbox Note (Gmail Trigger)
```
Gmail Trigger (starred emails)
→ Extract subject + body + sender
→ Format as Obsidian note (set node)
→ Write to Homelab/00_Inbox/{{timestamp}}-{{subject-slug}}.md
→ Send confirmation (Gmail: send)
```

### Pattern 3: Consulting Time Log (Webhook)
```
Webhook POST /log-time
Body: {client, hours, description, date}
→ Validate payload
→ Append to Homelab/02_Consulting/{{client}}/Time-Log.md
→ Update monthly summary note
→ Return 200 OK
```

### Pattern 4: Health Data Ingestion (Scheduled)
```
Cron (daily at 11pm)
→ Call health API (Oura/Garmin/etc.)
→ Extract sleep, HRV, steps
→ Format as Dataview-compatible frontmatter
→ Write/update Homelab/06_Health/Daily/{{date}}.md
→ Append to weekly summary
```

### Pattern 5: Task Sync — Todoist → Obsidian (Webhook)
```
Todoist webhook (task completed)
→ Filter by project label
→ Mark corresponding Obsidian task as complete
→ Append completion date
OR
Todoist webhook (task created)
→ Add task to correct Obsidian area daily note
```

## Python Vault Scripts

### Write Note to Vault
```python
from pathlib import Path
from datetime import datetime

VAULT_PATH = Path("C:/Users/Admin/Desktop/Desktop Folders/Obsidian/Homelab")

def write_vault_note(
    folder: str,
    filename: str,
    content: str,
    frontmatter: dict | None = None
) -> Path:
    note_path = VAULT_PATH / folder / filename
    note_path.parent.mkdir(parents=True, exist_ok=True)

    fm_lines = ["---"]
    if frontmatter:
        for k, v in frontmatter.items():
            fm_lines.append(f"{k}: {v}")
    fm_lines += ["---", ""]

    full_content = "\n".join(fm_lines) + content
    note_path.write_text(full_content, encoding="utf-8")
    return note_path

def append_task_to_daily(
    task: str,
    area: str,
    priority: str = "B",
    due: str | None = None
) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")

    daily_path = VAULT_PATH / "daily" / year / month / f"{today}.md"
    due_str = f" [due:: {due}]" if due else ""
    task_line = f"- [ ] {task} [area:: {area}] [priority:: {priority}]{due_str}\n"

    with open(daily_path, "a", encoding="utf-8") as f:
        f.write(task_line)
```

### Scan Vault for Overdue Tasks (Cron Job)
```python
import re
from pathlib import Path
from datetime import date

def find_overdue_tasks(vault_path: Path) -> list[dict]:
    overdue = []
    task_pattern = re.compile(
        r"- \[ \] (.+?) \[area:: (\w+)\].*?\[due:: (\d{4}-\d{2}-\d{2})\]"
    )
    for md_file in vault_path.rglob("*.md"):
        for line in md_file.read_text(encoding="utf-8").splitlines():
            match = task_pattern.search(line)
            if match:
                task_text, area, due_str = match.groups()
                due_date = date.fromisoformat(due_str)
                if due_date < date.today():
                    overdue.append({
                        "task": task_text,
                        "area": area,
                        "due": due_str,
                        "file": str(md_file)
                    })
    return overdue
```

## MCP Obsidian Integration

Install `mcp-obsidian` to give Claude direct vault access:
```json
// Claude Code settings.json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian"],
      "env": {
        "VAULT_PATH": "C:/Users/Admin/Desktop/Desktop Folders/Obsidian/Homelab"
      }
    }
  }
}
```

This enables Claude to: read notes, search vault content, write new notes, update existing notes — all from conversation.

## Anti-Patterns

1. **Writing Directly to Open Notes** — n8n/scripts should never write to a note currently open in Obsidian. Use append-only patterns or write to new files.
2. **Non-Idempotent Automation** — Running a daily note creation script twice should not create duplicates. Always check file existence first.
3. **Hardcoded Vault Paths in Scripts** — Use env vars: `OBSIDIAN_VAULT_PATH`. Vault location changes break everything.
4. **Writing Without Backup** — Before any bulk vault operation, ensure Remotely-Save has synced in the last hour.

## Quality Gates
- [ ] All automation writes use idempotency check (file exists? skip)
- [ ] Vault path stored in env var, not hardcoded
- [ ] n8n workflows have error handling and notification on failure
- [ ] All automated notes follow standard frontmatter format
- [ ] Task injection uses the canonical inline field format
- [ ] MCP Obsidian installed for direct Claude-vault interaction
