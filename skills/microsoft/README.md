# Aaron's Microsoft Ecosystem Skill Library

Savant-level Claude skills for the full Microsoft Power Platform and M365 stack.

## Skills Included

| Skill | File | Scope |
|---|---|---|
| **Power BI** | `power-bi/SKILL.md` | DAX, Power Query (M), data modeling, star schema, performance, RLS, deployment, semantic models |
| **Power Apps** | `power-apps/SKILL.md` | Canvas Apps, Model-Driven Apps, Power Fx, delegation, components, offline, custom connectors, ALM |
| **Power Automate** | `power-automate/SKILL.md` | Cloud flows, desktop flows (RPA), expressions, error handling, approvals, HTTP, child flows, batch processing |
| **SharePoint** | `sharepoint/SKILL.md` | Site architecture, lists, document mgmt, search (KQL), permissions, PnP PowerShell, SPFx, migration |
| **Copilot Studio** | `copilot-studio/SKILL.md` | Bot design, topics, generative AI, plugin actions, adaptive cards, multi-channel, authentication, analytics |
| **Power Platform Admin** | `power-platform-admin/SKILL.md` | Environments, DLP, CoE Starter Kit, ALM pipelines, licensing, capacity, governance, monitoring |
| **Microsoft Dataverse** | `microsoft-dataverse/SKILL.md` | Table design, relationships, business rules, security model, Web API, FetchXML, plugins, integration |
| **M365 Integration** | `m365-integration/SKILL.md` | Microsoft Graph API, MSAL auth, Teams development, cross-service orchestration, webhooks |

## Reference Files

- `power-bi/references/dax-patterns-advanced.md` — Basket analysis, ABC, parent-child hierarchies, headcount snapshots, what-if
- `power-bi/references/power-query-patterns.md` — Connection patterns, transformations, custom functions, API pagination

## Usage

### Claude Code
Skills are registered as slash commands via the registration script:
```bash
# Register all Microsoft skills
./scripts/register-commands.sh --category microsoft

# Register into a specific project
./scripts/register-commands.sh --project /path/to/project --category microsoft
```

Then use `/power-bi`, `/power-apps`, etc. in any Claude Code conversation.

### Other Platforms
Copy the relevant SKILL.md content into your conversation or include in your platform's instruction file.

## Design Principles

1. **Comprehensively concise** — Maximum signal, minimum fluff
2. **Decision frameworks first** — When to use what, before how
3. **Anti-patterns included** — Know what NOT to do
4. **Production patterns** — Enterprise-grade, not tutorial-level
5. **Cross-referenced** — Skills link to each other where relevant
