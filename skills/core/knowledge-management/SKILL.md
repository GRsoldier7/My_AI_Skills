---
name: knowledge-management
description: |
  Personal knowledge management architect. Use when organizing information, designing
  documentation systems, building reference architectures, or structuring project knowledge
  across multiple systems and repositories.

  EXPLICIT TRIGGER on: "organize", "document", "knowledge base", "notes", "second brain",
  "information architecture", "project documentation", "how do I find", "where is",
  "reference system", "PKM", "personal knowledge management", "Obsidian", "note-taking",
  "documentation strategy", "information retrieval", "PARA", "Zettelkasten", "wiki",
  "decision log", "meeting notes", "project post-mortem", "knowledge capture",
  "I keep losing track of", "where did I put", "how to organize my".

  Also trigger when the user describes difficulty finding, organizing, or maintaining
  information across their projects and systems.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: portable-ai-instructions, polychronos-team, skill-amplifier, session-optimizer
  last-reviewed: "2026-03-21"
  review-trigger: "User reports information retrieval failures, new tool adoption, system reorganization"
  capability-assumptions:
    - "Works with any note system — Obsidian, Notion, plain markdown, Google Docs"
    - "File system access helpful for organizing local projects"
    - "Obsidian MCP server available for direct vault interaction"
  fallback-patterns:
    - "If no file access: provide framework as text guidance for user to implement"
    - "If no specific tool chosen: default to plain markdown — most portable format"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: organizational challenge, documentation need, or information retrieval question
- Output produces: folder structure, documentation template, workflow design, or retrieval strategy
- Can chain from: any skill (capture knowledge generated during skill execution)
- Can chain into: portable-ai-instructions (knowledge → CLAUDE.md), session-optimizer (knowledge persistence)
- Orchestrator notes: recommend plain markdown as default format for maximum portability

---

## PKM Architecture — PARA Method Adapted

Organize everything into four categories:

### Projects (Active, with a deadline)
Things you're actively working on that have a defined endpoint.
- Sunday_School_Transformation — curriculum redesign
- Client engagement: [Company] automation buildout
- Biohacking data platform MVP
- Each project gets: README.md, decision-log.md, and relevant working files

### Areas (Ongoing responsibilities, no deadline)
Domains you maintain continuously with no finish line.
- Docker Home Server — infrastructure, maintenance, monitoring
- Master_Skills — skill library curation and optimization
- AI Consulting Practice — pipeline, client relationships, marketing
- Faith & Ministry — teaching prep, study notes, church involvement
- Health/Biohacking — protocols, tracking, research

### Resources (Reference material)
Information you reference but don't actively work on.
- Technology references (API docs, framework guides, stack notes)
- Business templates (proposals, SOWs, invoice templates)
- Research collections (articles, papers, bookmarks by topic)

### Archive (Completed or inactive)
Finished projects and deprecated resources. Searchable but not in your daily view.

### Mapping Your Systems to PARA
```
Master_Skills repo           → Resource (reference library)
Sunday_School_Transformation → Project (active, has deliverables)
Docker Automation configs    → Area (ongoing maintenance)
Client project repos         → Project (active) → Archive (when complete)
Obsidian vault               → Hub for Areas + Resources
Claude Code memory           → Area-specific context persistence
```

---

## Folder Structure Template

```
~/Knowledge/
├── 10-Projects/              # Active projects with deadlines
│   ├── 2026-Q1-ClientName/
│   │   ├── README.md         # Project overview, goals, status
│   │   ├── decision-log.md   # All key decisions with reasoning
│   │   ├── deliverables/
│   │   └── notes/
│   └── ...
├── 20-Areas/                 # Ongoing responsibilities
│   ├── consulting/
│   ├── docker-infrastructure/
│   ├── faith-ministry/
│   └── health-biohacking/
├── 30-Resources/             # Reference material by topic
│   ├── tech/
│   ├── business/
│   └── research/
└── 40-Archive/               # Completed projects, old references
    └── 2025/
```

Use numbered prefixes (10, 20, 30, 40) to enforce sort order in any file browser.

---

## Documentation Standards

### Decision Log Format
```markdown
## [Date] — [Decision Title]

**Context:** What situation prompted this decision?
**Decision:** What was decided?
**Reasoning:** Why this option over alternatives?
**Alternatives considered:** What else was on the table?
**Consequences:** What follows from this decision?
**Review date:** When should this be reconsidered? (optional)
```

### Project README Template
```markdown
# [Project Name]

## Purpose
One paragraph: what this project is and why it exists.

## Current Status
Active / On Hold / Complete — last updated [date]

## Quick Start
How to get this running or pick up where you left off.

## Architecture / Key Decisions
Pointer to decision-log.md or inline summary.

## Key Files
- `path/to/important/thing` — what it does
```

### Meeting Notes Template
```markdown
## [Date] — [Meeting Title]

**Attendees:** [names]
**Purpose:** [one line]

### Key Points
- [point 1]
- [point 2]

### Decisions Made
- [decision with owner]

### Action Items
- [ ] [action] — [owner] — [due date]
```

---

## Information Retrieval Strategy

### Naming Conventions for Findability
- Files: `YYYY-MM-DD-descriptive-name.md` for dated content
- Projects: verb or noun phrase that describes the outcome
- Use lowercase-kebab-case for all file and folder names
- Never use spaces in filenames — they break scripts and links

### Tagging vs Folders
- **Folders** for primary categorization (PARA structure)
- **Tags** for cross-cutting concerns that span categories
- Keep tag vocabulary small (20-30 tags max) — too many tags = no tags
- Review and prune tags quarterly

### Cross-Referencing
- Use relative links between documents: `[related decision](../project-x/decision-log.md)`
- In Obsidian: `[[wikilinks]]` for fast cross-referencing
- Create index/MOC (Map of Content) files for large topic areas
- Rule: if you reference something 3+ times, it deserves its own document

### Search-First vs Browse-First
- **Search-first** works when: you know what you're looking for, good naming conventions
- **Browse-first** works when: exploring a topic, discovering connections
- Design your system for search-first (consistent naming) but support browse (good folder structure)

---

## Knowledge Capture Workflows

### Daily Capture
1. **Inbox:** Quick notes, ideas, links go into a daily inbox (one file or folder)
2. **Process:** At end of day or next morning, sort inbox items into PARA locations
3. **File:** Each item gets a proper home or gets discarded
- Rule: inbox zero weekly. Anything sitting in inbox >7 days gets archived or deleted.

### Weekly Review
- What did I learn this week that's worth capturing?
- What decisions did I make that need documenting?
- Are any projects stale and should move to archive?
- Are any documents outdated and need updating?

### Project Knowledge Extraction
At project completion, before archiving:
1. What worked well? (process, tools, approaches)
2. What would I do differently?
3. What non-obvious insights emerged?
4. Capture these in a `post-mortem.md` — this is the highest-value document in any project.

---

## Claude Code Memory Integration

### CLAUDE.md as Project Knowledge
- Each project's `CLAUDE.md` is its machine-readable knowledge summary
- Include: architecture decisions, coding conventions, deployment patterns, gotchas
- Update it when you learn something future sessions need
- Keep it concise — it loads into every session's context window

### Memory Directory (~/.claude/projects/.../memory/)
- For persistent context across sessions within a project
- User preferences, feedback patterns, project-specific decisions
- Organized by topic, not chronology
- Memory supplements CLAUDE.md — use memory for things too specific for CLAUDE.md

### When to Save Where
| What | Where | Why |
|------|-------|-----|
| Project architecture | CLAUDE.md | Needed every session |
| User preferences | Memory (user type) | Persistent across projects |
| Decision with reasoning | decision-log.md in project | Human-readable record |
| Lesson learned | Memory (project type) or post-mortem | Future sessions benefit |
| Reference pointer | Memory (reference type) | Quick lookup across sessions |

---

## Maintenance and Hygiene

### Monthly Knowledge Audit (15 minutes)
- Scan Projects: any completed? → move to Archive
- Scan Areas: any documents outdated? → update or flag
- Scan Resources: any stale references? → verify or remove
- Check inbox: anything lingering? → process or delete

### Archive vs Delete
- **Archive** when: might need it again, has historical value, documents a decision
- **Delete** when: duplicate, truly obsolete, contains no unique information
- When in doubt: archive. Storage is cheap; lost knowledge is expensive.

---

## Self-Evaluation (run before presenting output)

Before presenting, silently check:
[ ] Is the recommended system simple enough to actually maintain?
[ ] Does it work with the user's existing tools, not require a full migration?
[ ] Are naming conventions consistent and searchable?
[ ] Is there a clear capture → process → file workflow?
[ ] Have I avoided over-engineering (too many categories, too many tags)?
If any check fails, revise before presenting.
