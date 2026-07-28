---
name: obsidian-project-organizer
description: |
  Expert organizational system for keeping Obsidian vault AND every code/project repository in perfect, maintainable order. Enforces folder naming conventions, file structure standards, README/CLAUDE.md presence, dead file detection, and runs organization audits on demand. Use this skill for any organizational task: "organize this project", "clean up this folder", "what's the structure here", "enforce naming conventions", "audit my vault organization", "my files are a mess", "create folder structure", "how should I organize this repo", "project hygiene check". Also auto-triggers before starting any new project to establish structure upfront.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: obsidian-vault-architect, life-os-designer, portable-ai-instructions
  source-repo: GRsoldier7/My_AI_Skills
---

# Obsidian & Project Organizer — Expert Skill

## Core Philosophy

**Entropy is the enemy. Structure is the solution.**
Every project, every vault, every folder follows the same organizing law: **a place for everything, everything in its place, and a system for finding both.**

Organizational debt compounds. 10 minutes of structure now saves hours of confusion later.

## The Two Systems

This skill governs two distinct organizational domains:

1. **Obsidian Vault Organization** — PKM structure, note hygiene, folder discipline
2. **Project/Code Repository Organization** — Directory structure, file naming, meta-files, documentation

---

## System 1: Obsidian Vault Organization

### Vault Health Audit (run monthly)

```
AUDIT CHECKLIST:
[ ] 00_Inbox/ has <20 notes (process if more)
[ ] No notes in root vault directory (all filed)
[ ] All areas have active dashboard notes
[ ] No orphaned notes (zero inlinks, zero outlinks)
[ ] All daily notes in correct YYYY/MM/ subfolder
[ ] Templates folder has no stale/unused templates
[ ] Archives folder has notes >6 months inactive
[ ] _meta/Vault Changelog.md updated this month
```

### Obsidian Naming Conventions
```
Folders:    00_Inbox, 01_Work, 07_Projects (numbered prefix for order)
Daily Notes: YYYY-MM-DD (ISO date)
Project Notes: [ProjectName] - [Status].md  e.g. "Client ABC - Active.md"
Templates:  [TemplateName] Template.md
MOCs:       [Area] MOC.md
Dashboards: [Area Name].md (in 000_Master Dashboard/)
```

### File Organization Rules
- **One topic per note** — if a note covers 3 unrelated things, split it
- **Dates in ISO format always** — `2026-03-21`, never "March 21" or "3/21"
- **No spaces in filenames** — use hyphens or underscores (Obsidian handles this)
- **Archive don't delete** — move completed/inactive notes to `09_Archives/`
- **Link before you duplicate** — search vault before creating new note on a topic

### Inbox Processing Protocol (Weekly, 15 min)
```
For each note in 00_Inbox/:
1. Is it a task? → Add to area daily note with full inline fields, delete inbox note
2. Is it reference? → Move to 08_Resources/ with appropriate tags
3. Is it a project? → Move to 07_Projects/, link from area dashboard
4. Is it a fleeting thought? → Either develop into real note or delete
5. Is it nothing? → Delete without guilt
```

---

## System 2: Project/Code Repository Organization

### Universal Project Structure
Every project repository (code, automation, analysis) follows this skeleton:

```
ProjectName/
├── .claude/
│   ├── commands/          ← Project-specific slash commands/skills
│   └── settings.json      ← Project-level Claude Code settings
├── docs/
│   ├── specs/             ← Design specs (brainstorming output)
│   └── adr/               ← Architecture Decision Records
├── src/                   ← Source code (or app/, lib/)
├── tests/                 ← Test files mirroring src/ structure
├── scripts/               ← Utility scripts (not prod code)
├── data/                  ← Sample data, fixtures (never prod data)
├── .env.example           ← Template for env vars (never .env itself)
├── CLAUDE.md              ← Claude Code project instructions
├── README.md              ← Human-readable project overview
└── requirements.txt       ← (or package.json, pyproject.toml, etc.)
```

### File Naming Conventions (Code Projects)
```
Python files:     snake_case.py
TypeScript files: camelCase.ts or PascalCase.tsx (components)
SQL files:        YYYYMMDD_description.sql (migrations)
Config files:     kebab-case.yaml / kebab-case.json
Test files:       test_[module_name].py / [module].test.ts
Scripts:          [verb]-[noun].sh (e.g., setup-database.sh)
Docs:             YYYY-MM-DD-topic-name.md
```

### Project Hygiene Rules
1. **No files in root except config** — source code goes in `src/`, not root
2. **`.env` always in `.gitignore`** — `.env.example` always committed
3. **`CLAUDE.md` required** — every project gets one before first commit
4. **Dead code = deleted code** — commented-out blocks go, not live in files
5. **`TODO:` comments expire** — if a TODO is >30 days old, it's a task or a decision
6. **Consistent import ordering** — stdlib → third-party → local (enforced by ruff/eslint)

### Project Audit Protocol (run when starting work on any project)

```
QUICK PROJECT AUDIT:
[ ] CLAUDE.md exists and is current?
[ ] README.md describes what the project actually does today?
[ ] .env.example matches all actual env vars in use?
[ ] No credentials, tokens, or secrets in any committed file?
[ ] src/ structure logical — can a new dev navigate it in 2 minutes?
[ ] Tests directory mirrors src/ directory structure?
[ ] docs/specs/ has at least one design doc for major features?
[ ] No orphaned files (created, committed, never referenced)?
[ ] Naming conventions consistent throughout?
[ ] .gitignore covers: .env, __pycache__, node_modules, .DS_Store, *.log?
```

### CLAUDE.md Template (every new project)
```markdown
# [Project Name]

## What This Is
[1-2 sentences — what does this project do?]

## Tech Stack
- Language: Python 3.12+ / TypeScript / etc.
- Database: PostgreSQL
- Key dependencies: [list]

## Project Structure
[Brief folder map]

## How to Run
[Commands to get it running locally]

## Key Conventions
- [Any project-specific rules Claude should know]
- [Naming conventions specific to this project]
- [What NOT to touch without asking]

## Current Status
[Active development / Maintenance / Archived]
```

---

## Organization Audit Workflow

When asked to organize or audit any system:

1. **Map current state** — list all files/folders without judgment
2. **Identify violations** — which naming/structure rules are broken?
3. **Identify orphans** — what exists but is referenced nowhere?
4. **Identify gaps** — what's missing (CLAUDE.md? tests/? .env.example?)?
5. **Propose changes** — specific moves, renames, creates, deletes
6. **Execute with confirmation** — get user approval before destructive ops
7. **Update changelog** — log what changed and why

## Quality Gates
- [ ] Every project has CLAUDE.md, README.md, .env.example
- [ ] Vault Inbox processed — fewer than 20 unprocessed notes
- [ ] No credentials or .env files committed to any repo
- [ ] File naming conventions consistent — no mixed conventions in same project
- [ ] Dead code and orphaned files removed
- [ ] All TODOs either converted to tasks or resolved
- [ ] Project directory structure maps to the universal skeleton above
