# Vault map and routing (verified 2026-11-08)

Source of truth for where things live in bucket `obsidian-vault` (Activepieces
connection "Obsidian Minio Self Hosted", externalId `2XVIv9EVizvNEHgye0QBb`).
Every path below was seen in a live listing on 2026-11-08 unless marked
**unverified** or **ghost**. "Ghost" means the folder appears in a
`listFoldersSeparately` listing but a flat listing of the prefix returns zero
keys (MinIO shows folders whose objects only have delete markers). Re-list
before relying on a ghost.

## Top-level folders

| Folder | Role | Write? |
|---|---|---|
| `000_Master Dashboard/` | Dataview dashboards and hubs: `Mission Control.md`, `North Star.md`, `Needle Movers.md`, per-area dashboards, `Agent Review.md` | No (read for context only) |
| `00_Inbox/` | Single capture inlet: `YYYY-MM-DD.md`, created by the first write of that day. Also automation-owned files (see never-write) | Append to today's dated file only |
| `10_Active Projects/` | Project hubs. Live: `Active Business/` (Echelon Seven GovCon Hub, Opportunity Log), `Active Personal/` (`!!! MASTER TASK LIST.md`, MY_MENTOR notes, `A.I. & Vibe Coding & Prompting/` with AI, Agents, Prompts, YouTube2Sheets subfolders, `Task Archive.md`). `Active Consulting/` exists and is empty. `Power Platform/` and top-level `A.I. & Vibe Coding & Prompting/` are ghosts | Yes |
| `20_Domains (Life and Work)/` | Life-domain notes. Live: `Personal/` (dated article captures), `Personal/Homelab/` (service directory note), `Personal/Business Ideas & Projects/`. `Career/` (employer and consulting subfolders per ADR-002) and `2026 Goals/` are ghosts; their content is under `_Archive/` | Yes |
| `30_Knowledge Library/` | Ghost tree: `AI & Automation/`, `Bible Studies & Notes/`, `Biohacking/`, `Skills & Development/`, `Topics/` all list zero keys | Open decision, see below |
| `_Archive/30_Knowledge Library/` | The real knowledge notes today (19 keys verified in `Bible Studies & Notes/` alone: Genealogy of Jesus, Prayers, Archeology, False Gods). Same five subfolders as above. `_Archive/20_Domains (Life and Work)/` holds the archived Career and Personal notes; `_Archive/05_Templates/` holds Templater templates | Read; write only after Aaron decides |
| `30_Reviews/` | Hermes-generated digests, last written July 2026 | No |
| `40_Timeline_Weekly/` | `Daily/` (auto-created blank notes, janitor deletes them), `Weekly/`, `Weekly_Review.md` (Dataview hub) | No |
| `98_Agents/` | Agent operations: `README.md` (rules), `System-Design.md` (capture, absorb, retrieve design), `Muse.md`, `Hermes.md`, `Shared-vs-Private.md`, `Log/YYYY-MM.md`, `Templates/New-VA.md`, audit notes | Append to `Log/` only |
| `99_System/` | Automation state, logs, backups, archive of retired brain dumps, `Pipeline Health.md`, `health.md` | No |
| Legacy, empty or test | `! TO DO/`, `01_Projects/`, `02_Learning/`, `03_Resources/`, `04_Personal/`, `05_Templates/` (empty), `05_Work/`, `06_Archive/`, `06_Templates/`, `07_Archive/`, `09_Archives/`, `10_Projects/`, `20_Areas/`, `30_Resources/`, `AI_Inbox/`, `Daily/`, `Homelab/` (empty), `Scripts/`, `_smoke_test/`, `rs-test-folder-*/` (Remotely Save probes). Contents **unverified**, not listed individually | Never |

## Routing table: this kind of insight goes here

| Domain / insight | Folder and note pattern | Lane |
|---|---|---|
| Echelon Seven, GovCon, SAM, VetCert, offers, buyers | `10_Active Projects/Active Business/Echelon Seven - GovCon Hub.md` (status, positioning, plan); opportunities in `Echelon Seven - Opportunity Log.md`; new hubs as `Echelon Seven - <Topic>.md` | shared |
| Consulting clients and training engagements | `10_Active Projects/Active Consulting/<Client> - <Topic>.md` (folder exists, empty) | shared |
| AI, agents, prompting, Claude Code, Hermes, MY_MENTOR, skills | `10_Active Projects/Active Personal/A.I. & Vibe Coding & Prompting/<Area>/<Title>.md`; dated references as `10_Active Projects/Active Personal/YYYYMMDD - <Project> - <Topic>.md` | shared |
| Power Platform, Power BI, day-job work | `10_Active Projects/Power Platform/` (ghost) or `20_Domains (Life and Work)/Career/<employer>/` (ghost, ADR-002). **Unverified**: list first; if both empty, create in `10_Active Projects/Power Platform/` and tell Aaron | shared |
| Homelab, Proxmox, Tailscale, services, YouTube-to-NotebookLM pipeline infra | `20_Domains (Life and Work)/Personal/Homelab/YYYYMMDD - Homelab - <Topic>.md` | shared |
| Business ideas not yet a project | `20_Domains (Life and Work)/Personal/Business Ideas & Projects/<Title>.md` | shared |
| Goals, quarterly rocks | `000_Master Dashboard/North Star.md` and `Needle Movers.md` are Aaron's; propose changes in the report, do not edit | shared |
| Faith, Bible study, theology, apologetics, prayer | `_Archive/30_Knowledge Library/Bible Studies & Notes/<Series>/<Claim>.md` today; live `30_Knowledge Library/Bible Studies & Notes/` is the ADR-002 target. See open decision | shared |
| Biohacking knowledge (general) | `30_Knowledge Library/Biohacking/` (ADR-002 target, ghost) or its `_Archive/` twin. See open decision | shared |
| Personal labs, biomarkers, peptides, medical | Same folder as above | private |
| Family, home, school, schedules | `20_Domains (Life and Work)/Personal/Family/` and `Personal/Home/` per ADR-002, **unverified** live (archived copies exist). List first | private |
| Tax, money, invoices, contracts | No verified folder. Use `20_Domains (Life and Work)/Personal/<Topic>.md` and tell Aaron a Money folder is missing | private |
| Job search, career moves | `20_Domains (Life and Work)/Career/` is a ghost; same handling as Power Platform | private |
| Raw idea or fact with no home yet | Append a timestamped bullet to `00_Inbox/YYYY-MM-DD.md` (today, Central time). The nightly janitor and weekly review absorb it | per content |
| Action or commitment | `10_Active Projects/Active Personal/!!! MASTER TASK LIST.md`, canonical task line, under the fitting section | per content |
| What an agent did in the vault | `98_Agents/Log/YYYY-MM.md`, one appended entry | shared |

Areas for `[area:: ]`: `faith`, `family`, `business` (Echelon Seven),
`consulting` (client work), `work` (day job), `health`, `home`,
`personal`. Lowercase; Dataview matching is case-sensitive.

## Never write

`000_Master Dashboard/*`, `99_System/*`, `30_Reviews/*`,
`40_Timeline_Weekly/*`, `00_Inbox/articles-to-process.md`,
`00_Inbox/quick-capture.md`, `00_Inbox/review-queue.md`,
`00_Inbox/daily-summary.md`, `00_Inbox/muse-handshake.md`,
`00_Inbox/brain-dumps/*`, `00_Inbox/processed/*`, anything under `.obsidian/`,
`_Archive/*` (until the decision below), and all legacy folders.

Never read or quote a note whose title suggests credentials or connection
config (MCP server setups, API keys, auth). If a read returns a secret anyway,
stop, do not repeat it, and tell Aaron the note path so he can rotate and remove it.

## Naming and templates

- Filenames: ASCII only, no em dash, `.md`. Hubs: `<Entity> - <Topic>.md`.
  Dated references: `YYYYMMDD - <Project or Area> - <Topic>.md`. Atomic notes:
  the title is a claim ("Subcontract first, prime later"), not a topic.
- Store with `contentType: text/markdown`. Plain markdown bodies, wikilinks
  for relationships, no tag taxonomy.
- Agents create `status: seed`. Only Aaron promotes to `evergreen`.

Note frontmatter (from `98_Agents/System-Design.md` and `Shared-vs-Private.md`):

```
---
type: note | project | decision | person | task
status: seed | growing | evergreen
created: 2026-11-08
updated: 2026-11-08
source: 00_Inbox/2026-11-08 or the conversation, repo path, or URL it came from
lane: shared | private
---

# Title as a claim

Body, 50-300 words. What is true, why, evidence, what is open.

## Links
- [[Related hub]]
- [[Second related note]]
```

Canonical task line (every dashboard depends on it):

```
- [ ] Task description [area:: business] [priority:: A] [due:: 2026-11-21]
```

Priority: `A` needle-mover, `B` important, `C` nice-to-have.

Agent log entry, appended to `98_Agents/Log/YYYY-MM.md` (exact format):

```
## 2026-11-08 14:00 CT - Claude Code - Short topic [capture]

- Date: 2026-11-08 14:00 CT (2026-11-08T20:00Z)
- Agent: Claude Code
- Topic: short topic
- What: one or two lines
- Outcome: what is true now, verified by read-back
- Links: vault paths, one per line
- Next: what is open and who owns it
```

Topic tags: `[audit]`, `[delete]`, `[decision]`, `[handoff]`, `[fix]`,
`[capture]`. Append at the end only; correct a past entry with a new entry.

## Automation already running (do not duplicate)

- **Vault Janitor v1** (Activepieces flow `rl6Al4NNJlsbfVtrd1pzE`, daily 02:00
  America/Chicago, enabled): lists `00_Inbox/` and `40_Timeline_Weekly/Daily/`,
  reads each file, and deletes a file only when its name is `YYYY-MM-DD.md`,
  it is template-only after stripping frontmatter, headings and known
  boilerplate, and it is older than 48 hours. Nothing else is touched.
- **n8n** (left alone by Aaron's decision 2026-11-07): Daily Note Creator v2
  writes a blank daily note at 06:00 CT; a five-minute capture poller processes
  `00_Inbox/` automation files. Brain-dump capture stalled 2026-10-29 and the
  eight brain-dump files were retired to `99_System/archive/brain-dumps/`.
- Remotely Save (Obsidian plugin) syncs the desktop vault to the bucket.

## Open decisions for Aaron (state them when relevant, do not resolve)

1. Knowledge Library home: the live `30_Knowledge Library/` tree is a ghost
   and the notes sit in `_Archive/30_Knowledge Library/` (104 notes moved
   2026-06-27, reported as not synced to the Mac). New faith, biohacking and
   skills notes need one canonical folder.
2. Capture inlet shape: daily `00_Inbox/YYYY-MM-DD.md` (in use since
   2026-11-07) versus a rolling file; `System-Design.md` is still "proposed".
3. Missing folders for money/tax and job search.
4. `00_Inbox/quick-capture.md` links to `99_System/VAULT-CONTRACT`, which does
   not exist in the listing.
