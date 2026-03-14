---
name: sharepoint
description: >
  Genius-level SharePoint expertise covering SharePoint Online, site architecture, lists, libraries,
  document management, SPFx, search, permissions, governance, migration, and integration patterns.
  Use this skill whenever the user mentions SharePoint, SP Online, SPO, SharePoint lists, document libraries,
  site collections, hub sites, SPFx (SharePoint Framework), content types, site columns, managed metadata,
  term store, SharePoint search, KQL, permissions, sharing, site templates, PnP PowerShell, CSOM,
  REST API, Graph API for SharePoint, migration, or any content/document management in the Microsoft 365
  ecosystem. Also trigger for questions about information architecture, retention policies, sensitivity
  labels, compliance, Teams-connected sites, or SharePoint Embedded. Even casual mentions of
  "document management", "intranet", or "team site" in a Microsoft context should trigger this skill.
---

# SharePoint — Savant-Level Skill

## Philosophy

SharePoint mastery = **information architecture first** (before building anything), **hub sites for governance** (not site collection hierarchy), **metadata over folders** (always), and **Graph API as the future** (PnP PowerShell for admin, Graph for apps).

---

## 1. Information Architecture

### Site Topology (Modern)
```
Hub Site (Intranet)
  ├─ Hub Site (HR)
  │   ├─ Communication Site: HR Policies
  │   ├─ Communication Site: Benefits Portal
  │   └─ Team Site: HR Operations (Teams-connected)
  ├─ Hub Site (Engineering)
  │   ├─ Team Site: Project Alpha (Teams-connected)
  │   ├─ Team Site: Project Beta (Teams-connected)
  │   └─ Communication Site: Engineering Standards
  └─ Communication Site: Company News
```

### Site Type Decision
| Type | Purpose | Teams Integration |
|---|---|---|
| **Communication Site** | Broad audience, publishing, news | No (not recommended) |
| **Team Site** | Collaboration, project work | Yes (auto-provisions) |
| **Hub Site** | Navigation, search scope, governance roll-up | Associates other sites |

### Metadata vs Folders
```
❌ Folder structure:
  Documents/
    2024/
      Q1/
        Finance/
          report.docx

✅ Metadata approach:
  Documents/report.docx
    Year: 2024
    Quarter: Q1
    Department: Finance
    DocType: Report

Benefits:
  - Views: Filter by any combination (folders can't do this)
  - Search: Metadata is searchable and refinable
  - Reuse: Same doc can "belong" to multiple categories
  - Automation: Power Automate can filter/route by metadata
  - Retention: Policies apply by metadata, not location
```

### Content Types & Site Columns
```
Site Column: "Department" (Managed Metadata, Term Store: "Departments")
Site Column: "DocType" (Choice: Policy, Procedure, Report, Template)
Site Column: "ReviewDate" (Date)

Content Type: "Controlled Document"
  Inherits from: Document
  Columns: Department, DocType, ReviewDate, ApprovalStatus
  Workflow: Requires approval before publish
  Retention: 7 years after ReviewDate

Content Type: "Project Deliverable"
  Inherits from: Document
  Columns: ProjectID, Phase, DeliverableType
```

---

## 2. Lists — Advanced Patterns

### List Design Best Practices
- **5,000 item threshold**: Not a limit — it's an index threshold. Add indexes on filtered/sorted columns.
- **Index strategy**: Add indexes on columns used in views, filters, sort, group-by
- **Calculated columns**: Compute at write-time (good for search/filter); can't reference other lists
- **JSON column formatting**: Rich display without SPFx

### Column Formatting (JSON)
```json
// Status badge with color
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": {
    "padding": "4px 8px",
    "border-radius": "16px",
    "background-color": "=if(@currentField == 'Active', '#dff6dd', if(@currentField == 'Pending', '#fff4ce', '#fde7e9'))",
    "color": "=if(@currentField == 'Active', '#107c10', if(@currentField == 'Pending', '#7f6000', '#a80000'))"
  },
  "txtContent": "@currentField"
}

// Progress bar
{
  "elmType": "div",
  "children": [
    {
      "elmType": "div",
      "style": {
        "width": "=toString(@currentField) + '%'",
        "background-color": "=if(@currentField >= 75, '#107c10', if(@currentField >= 50, '#ffaa44', '#d13438'))",
        "height": "8px",
        "border-radius": "4px"
      }
    }
  ]
}

// Clickable link to person's profile
{
  "elmType": "a",
  "txtContent": "[$AssignedTo.title]",
  "attributes": {
    "href": "='/_layouts/15/me.aspx?u=' + [$AssignedTo.email]",
    "target": "_blank"
  }
}
```

### View Formatting
```json
// Tile/card layout for list items
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/tile-formatting.schema.json",
  "height": 200,
  "width": 300,
  "hideSelection": false,
  "formatter": {
    "elmType": "div",
    "style": {
      "display": "flex",
      "flex-direction": "column",
      "padding": "16px",
      "border-radius": "8px",
      "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
    },
    "children": [
      {"elmType": "div", "txtContent": "[$Title]", "style": {"font-weight": "600", "font-size": "16px"}},
      {"elmType": "div", "txtContent": "[$Status]", "style": {"margin-top": "8px"}},
      {"elmType": "div", "txtContent": "=toLocaleDateString([$DueDate])", "style": {"margin-top": "auto", "color": "#666"}}
    ]
  }
}
```

---

## 3. Document Management

### Document Sets
- Group related documents as a single unit with shared metadata
- Enable on library → Content Types → Add "Document Set"
- Use for: RFP packages, contract bundles, project deliverables

### Version History Strategy
| Scenario | Major Versions | Minor (Draft) Versions | Content Approval |
|---|---|---|---|
| Team collaboration | Unlimited (trim to 50) | Off | No |
| Controlled documents | Unlimited | 10 drafts | Yes |
| Records management | Unlimited (no delete) | Off | Yes |

### Retention & Compliance
```
Retention Policy (Microsoft Purview):
  - Apply to: SharePoint sites / specific libraries
  - Retain for: 7 years after last modified
  - Action after: Delete automatically / Review
  - Scope: By sensitivity label, content type, or KQL query

Retention Label:
  - "Financial Record" → Retain 7 years, then dispose
  - "Legal Hold" → Retain indefinitely
  - Auto-apply: KQL query matching "contract" AND "signed"

Record Declaration:
  - Mark as record → Immutable (no edit/delete)
  - Regulatory record → Even admins can't delete
```

---

## 4. Search (KQL)

### KQL Query Patterns
```
// Basic
contentclass:STS_ListItem_DocumentLibrary Title:budget

// Managed properties
RefinableString00:"Project Alpha" RefinableDate00>2024-01-01

// File types
FileExtension:pdf OR FileExtension:docx

// Path scoping
Path:"https://contoso.sharepoint.com/sites/HR"

// People
Author:"Jane Smith" OR ModifiedBy:"Jane Smith"

// Date ranges
LastModifiedTime>2024-01-01 AND LastModifiedTime<2024-06-30

// Wildcards (prefix only)
Title:budg*

// Exclusions
-ContentType:"Folder" -FileExtension:aspx

// Complex
(Title:quarterly OR Title:annual) AND FileExtension:pptx AND Path:"*/Finance/*"

// Promoted results / query rules
// Admin → Search → Manage query rules → Add promoted results for key terms
```

### Search Schema
- **Crawled properties**: Auto-discovered (ows_fieldname)
- **Managed properties**: Mapped from crawled, queryable/refinable/sortable
- **Custom mapping**: Site Column → Crawled property → Managed property (RefinableStringXX)

---

## 5. Permissions Architecture

### Permission Inheritance Model
```
Tenant
  └─ Site Collection (unique permissions)
      └─ Site (inherits or unique)
          └─ Library (inherits or unique)
              └─ Folder (inherits or unique)    ← AVOID
                  └─ Item (inherits or unique)  ← AVOID

Golden rule: Break inheritance at SITE level, almost never below.
```

### Permission Levels
| Level | Access | Use Case |
|---|---|---|
| Full Control | Everything | Site owners |
| Design | Add/customize pages | Intranet editors |
| Edit | Add/edit/delete items | Team members |
| Contribute | Add/edit items (no delete lists) | External contributors |
| Read | View only | Broad audience |
| View Only | View in browser (no download) | Restricted content |

### Sharing Best Practices
- Use **M365 Groups** (not individual permissions)
- **Sensitivity labels** control external sharing at site level
- **Site-level sharing settings** override item-level
- Audit sharing with: `Get-SPOSite | Select SharingCapability`

---

## 6. PnP PowerShell & Automation

### Common Admin Tasks
```powershell
# Connect
Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/HR" -Interactive

# Bulk create sites from CSV
Import-Csv sites.csv | ForEach-Object {
    New-PnPSite -Type CommunicationSite `
        -Title $_.Title -Url $_.Url -Description $_.Description
    Add-PnPHubSiteAssociation -Site $_.Url -HubSite $_.HubUrl
}

# Apply site template (PnP provisioning)
Invoke-PnPSiteTemplate -Path "template.xml"

# Bulk metadata update
Get-PnPListItem -List "Documents" -PageSize 500 | ForEach-Object {
    Set-PnPListItem -List "Documents" -Identity $_.Id -Values @{
        "Department" = "Engineering"
    }
}

# Export site structure
Get-PnPSiteTemplate -Out "template.xml" -IncludeAllPages `
    -Handlers Lists,Fields,ContentTypes,Navigation

# Permissions report
Get-PnPList | ForEach-Object {
    Get-PnPListItem -List $_.Title -PageSize 100 | Where-Object {
        $_.HasUniqueRoleAssignments
    } | Select-Object Id, @{N="Title";E={$_.FieldValues.Title}}
}
```

### Graph API for SharePoint
```
// List items
GET /sites/{site-id}/lists/{list-id}/items?$expand=fields

// Create item
POST /sites/{site-id}/lists/{list-id}/items
{
  "fields": {
    "Title": "New Item",
    "Department": "Engineering"
  }
}

// Upload file
PUT /sites/{site-id}/drive/items/{parent-id}:/{filename}:/content
Content-Type: application/octet-stream
<file binary>

// Search
POST /search/query
{
  "requests": [{
    "entityTypes": ["driveItem"],
    "query": {"queryString": "budget 2024"},
    "from": 0, "size": 25
  }]
}
```

---

## 7. SPFx (SharePoint Framework)

### When to Use SPFx
- Custom web parts beyond OOTB capabilities
- Extensions (header/footer, field customizers, command sets)
- Integration with external APIs requiring client-side code
- Custom Teams tabs backed by SharePoint

### Project Setup
```bash
# Generator
npm install -g @microsoft/generator-sharepoint
yo @microsoft/sharepoint

# Key choices:
#   Component: WebPart | Extension
#   Framework: React | No framework
#   Permissions: Isolated (service-scoped) | Standard
```

### Architecture Patterns
```
// Service layer for data access
export class DataService {
  constructor(private context: WebPartContext) {}

  async getItems(): Promise<IItem[]> {
    const client = await this.context.msGraphClientFactory.getClient('3');
    const response = await client.api('/sites/{id}/lists/{id}/items')
      .expand('fields').get();
    return response.value.map(mapToItem);
  }
}

// PnPjs integration (preferred over raw REST)
import { spfi, SPFx } from "@pnp/sp";
import "@pnp/sp/lists";
import "@pnp/sp/items";

const sp = spfi().using(SPFx(this.context));
const items = await sp.web.lists.getByTitle("Tasks").items
  .select("Title", "Status", "DueDate")
  .filter("Status eq 'Active'")
  .top(100)();
```

---

## 8. Migration Patterns

### Migration Decision Tree
```
Source → Tool → Target:
  File shares → SharePoint Migration Tool (SPMT) or Migration Manager → SPO
  On-prem SP → SPMT / Sharegate / AvePoint → SPO
  Google Drive → Migration Manager → SPO/OneDrive
  Box/Dropbox → Mover (Microsoft) → SPO/OneDrive
  
Pre-migration:
  1. Inventory: File count, size, path lengths (>400 char = problem)
  2. Cleanup: Delete ROT (redundant, obsolete, trivial)
  3. Permissions mapping: AD groups → M365 groups
  4. URL mapping: Old paths → new site/library structure
  5. Content type planning: What metadata to add during migration
  
Post-migration:
  1. Validation: Row counts, spot-check permissions
  2. Redirect: URL redirect from old → new
  3. Training: User adoption (SharePoint ≠ file share)
  4. Monitoring: Search coverage, broken links, permission escalations
```

---

## 9. Integration with Power Platform

### SharePoint + Power Automate
```
Trigger: "When an item is created or modified"
  - Use trigger conditions to filter (reduce flow runs):
    @equals(triggerBody()?['Status']?['Value'], 'Submitted')
  - Handles: Approval workflows, notifications, data sync, document generation

Common pattern: Document approval
  1. User uploads to library
  2. Flow triggers on new item
  3. Start approval (Teams adaptive card)
  4. On approve: Set metadata "Approved", move to final library
  5. On reject: Notify author, set "Rejected"
```

### SharePoint + Power Apps
```
// Custom form for SharePoint list
SharePoint list → Customize forms → Opens Power Apps
// Replace default list forms with canvas app for:
  - Conditional logic (show/hide fields by role)
  - Multi-step wizard forms
  - Cross-list lookups
  - Rich validation beyond column validation
  - Signature capture, barcode scanning
```
