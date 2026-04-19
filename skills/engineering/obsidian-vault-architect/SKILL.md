---
name: obsidian-vault-architect
description: |
  Expert Obsidian PKM architect who designs, audits, and evolves Obsidian vaults for life management systems. Specializes in: folder structure design (PARA/GTD hybrid), Dataview query architecture, Templater template engineering, plugin configuration (Tasks, QuickAdd, Calendar, Remotely-Save), cross-area task visibility, and vault-to-automation bridges (n8n/webhook). Use when designing vault structure, writing Dataview queries, creating templates, diagnosing broken queries, planning a new life area, building dashboards, or connecting Obsidian to external automations. Trigger phrases: "obsidian structure", "dataview query", "templater", "vault design", "obsidian dashboard", "quickadd", "obsidian template", "obsidian automation", "connect obsidian to", "fix my dataview", "obsidian plugin setup".
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: product
  adjacent-skills: life-os-designer, obsidian-automation-architect, obsidian-project-organizer, database-design
  source-repo: GRsoldier7/My_AI_Skills
---

# Obsidian Vault Architect — Expert Skill

## Vault Architecture Principles

**Principle 1: Capture is sacred, organization is optional at capture time.**
Inbox first. Process later. Never let friction block capture.

**Principle 2: Structure serves queries, not aesthetics.**
Every folder and tag choice should answer: "What Dataview query does this enable?"

**Principle 3: Templates are the operating system.**
A good template makes the right behavior automatic. A bad one makes it bureaucratic.

**Principle 4: One task format, always.**
`- [ ] Task description [area:: x] [priority:: A] [due:: YYYY-MM-DD]` — never deviate, never extend without updating all queries.

## Canonical Vault Structure (Aaron's Life OS)

```
Homelab/
├── 00_Inbox/              ← Uncategorized capture zone (process weekly)
├── 000_Master Dashboard/  ← Mission Control + per-area dashboards
├── 01_Work/               ← Parallon BAM role notes + tasks
├── 02_Consulting/         ← Client engagements, proposals, deliverables
├── 03_Business/           ← Startup ventures, product ideas, revenue tracking
├── 04_Personal/           ← Life admin, family, goals, finance
├── 05_Faith/              ← Spiritual practice, prayer, reflection
├── 06_Health/             ← Biohacking, supplements, biomarkers, workouts
├── 07_Projects/           ← Cross-area projects with own notes
├── 08_Resources/          ← Reference material, research, guides
├── 09_Archives/           ← Completed projects and old notes
├── 05_Templates/          ← All Templater templates
└── _meta/                 ← Vault changelog, plugin config notes
```

## Dataview Query Patterns

### Task Dashboard — Overdue (all areas)
```dataview
TASK
WHERE !completed AND due < date(today)
SORT due ASC
```

### Task Dashboard — Today by Area
```dataview
TASK
WHERE !completed AND due = date(today) AND area = "consulting"
SORT priority ASC
```

### Project Status Board
```dataview
TABLE project-status, area, due, priority
FROM "07_Projects"
WHERE project-status != "archived"
SORT due ASC
```

### Weekly Completed Tasks (for Weekly Review auto-population)
```dataview
TASK
WHERE completed AND completion >= date(today) - dur(7 days)
SORT completion DESC
```

### Cross-area Overdue with Context
```dataview
TASK
WHERE !completed AND due < date(today)
GROUP BY area
SORT due ASC
```

## Templater Patterns

### Dynamic Daily Note
```javascript
// Auto-pull today's priorities from overdue + due today
<%*
const today = tp.date.now("YYYY-MM-DD");
tR += `date:: ${today}\n`;
tR += `energy_level:: \n`;
tR += `focus_theme:: \n`;
%>
```

### Quick Project Scaffold
```javascript
<%*
const projectName = await tp.system.prompt("Project name?");
const area = await tp.system.suggester(
  ["work","consulting","business","personal","faith","health"],
  ["work","consulting","business","personal","faith","health"]
);
tR += `project:: ${projectName}\narea:: ${area}\nproject-status:: active\n`;
%>
```

## Plugin Configuration Recommendations

### Tasks Plugin
- Global filter: `#task` (optional — inline fields preferred)
- Due date format: `YYYY-MM-DD`
- Global task filter: none (use inline fields)

### QuickAdd
- **Capture Task** macro → appends to today's Daily Note with full inline field format
- **New Project** macro → runs Project Scaffold template in `07_Projects/`
- **Inbox Note** macro → creates timestamped note in `00_Inbox/`

### Remotely Save
- Sync target: your preferred cloud (OneDrive/S3/Dropbox)
- Schedule: on-close + every 30 minutes
- Conflict resolution: newer-wins

## Anti-Patterns

1. **Nested tags instead of inline fields** — `#work/consulting/active` is unqueryable in Dataview. Use `[area:: consulting]` instead.
2. **One giant MOC** — Map of Content files that become 200+ link dumps. Each MOC should have <20 links with descriptive context.
3. **Templates that require editing** — If you have to delete placeholder text every time, the template is friction, not flow.
4. **Orphaned notes** — Notes not linked to any dashboard or MOC become vaultrot. Monthly: `FROM "" WHERE length(file.inlinks) = 0`.

## Quality Gates
- [ ] Every life area has a dedicated dashboard with working Dataview queries
- [ ] `00_Inbox/` exists and is processed weekly
- [ ] Task format consistent: `[area::] [priority::] [due::]` on all tasks
- [ ] Weekly Review template auto-populates from vault data (not typed from memory)
- [ ] All templates use Templater dynamic fields, not static placeholders
- [ ] Vault structure maps 1:1 to actual life areas being tracked
