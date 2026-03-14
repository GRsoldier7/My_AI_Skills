---
name: power-platform-admin
description: >
  Genius-level Power Platform administration expertise covering environment management, DLP policies,
  tenant settings, capacity management, CoE Starter Kit, ALM, monitoring, and governance at scale.
  Use this skill whenever the user mentions Power Platform admin, environment management, DLP policies,
  data loss prevention, tenant settings, capacity, CoE (Center of Excellence), Starter Kit, managed
  environments, Power Platform pipelines, solution management, ALM, licensing, or governance of the
  Power Platform. Also trigger for questions about maker onboarding, environment strategy, connector
  policies, analytics at the tenant level, or Power Platform security. Even casual mentions of "governance"
  or "admin" in a Power Platform context should trigger this skill.
---

# Power Platform Admin — Savant-Level Skill

## Philosophy

Platform administration mastery = **enable makers safely** (not block them), **DLP as guardrails** (not walls), **environments as boundaries** (not afterthoughts), and **CoE Starter Kit as your eyes** (deploy it immediately).

---

## 1. Environment Strategy

### Recommended Topology
```
Tenant
  ├─ Default Environment (restrict heavily)
  │     - Every user has access by default
  │     - DLP: Strictest policy (block premium connectors)
  │     - Use: Personal productivity only
  │
  ├─ Developer Environments (per-maker or shared)
  │     - Sandbox, auto-reset every 30 days (optional)
  │     - DLP: Standard business policy
  │     - Use: Learning, prototyping, experimentation
  │
  ├─ Project Environments (per-project lifecycle)
  │     ├─ Project-A-Dev (Dataverse, unmanaged solutions)
  │     ├─ Project-A-Test (managed solution import)
  │     └─ Project-A-Prod (managed, locked down)
  │
  └─ Shared Service Environments
        - Integration Hub (shared connectors, child flows)
        - Reference Data (master data, shared Dataverse tables)
```

### Environment Types
| Type | Dataverse | Reset | Backup | Use |
|---|---|---|---|---|
| Production | Yes | No auto-reset | Full backup/restore | Live workloads |
| Sandbox | Yes | Can reset | Full backup/restore | Dev/Test |
| Developer | Yes (2GB) | Optional auto-reset | Limited | Personal dev |
| Trial | Yes | 30-day expiry | None | Evaluation |
| Default | Yes (3GB shared) | No | Limited | Default maker space |

### Managed Environments (Premium)
```
Enable for production environments:
  ✅ Sharing limits: Restrict app sharing to security groups
  ✅ Solution checker enforcement: Block import of solutions with errors
  ✅ Maker welcome content: Custom onboarding message
  ✅ Weekly digest: Admin email with environment activity summary
  ✅ Data policies: More granular connector controls
  ✅ IP firewall: Restrict Dataverse access by IP range (coming)
  ✅ Customer Managed Keys (CMK): Encrypt with your own key
```

---

## 2. DLP (Data Loss Prevention) Policies

### Policy Architecture
```
DLP Policy = Connector Classification + Scope

Three connector groups:
  1. Business: Connectors that can talk to each other
  2. Non-Business: Connectors that can talk to each other (but NOT business)
  3. Blocked: Cannot be used at all

Key insight: A flow/app can only use connectors from ONE group.
If an app needs SharePoint (Business) and Twitter (Non-Business) → BLOCKED.
```

### Recommended DLP Templates
```
Policy 1: "Default Restrictive" (scope: Default environment)
  Business: SharePoint, Office 365, Outlook, OneDrive, Approvals, Teams
  Non-Business: Everything else
  Blocked: HTTP, Custom connectors, SQL Server

Policy 2: "Standard Business" (scope: project environments)
  Business: SharePoint, Dataverse, Office 365, Outlook, Teams,
            SQL Server, Azure SQL, OneDrive, Approvals, PDF
  Non-Business: Social connectors, consumer services
  Blocked: HTTP (without APIM), unvetted custom connectors

Policy 3: "Integration Tier" (scope: integration hub env only)
  Business: All standard + HTTP, Custom Connectors, Azure services
  Non-Business: Consumer/social only
  Blocked: None (trust boundary is the environment itself)
```

### Connector Action Control (Granular DLP)
```
// Block specific actions within a connector
SharePoint connector:
  ✅ Allow: Get items, Create item, Update item
  ❌ Block: Delete item, Grant access, Create site

// Endpoint filtering
HTTP connector:
  ✅ Allow: https://api.yourcompany.com/*
  ❌ Block: All other endpoints
```

---

## 3. ALM & Solution Management

### Pipeline Architecture
```
Power Platform Pipelines (built-in):
  Dev Environment → [Export managed] → Test → [Validate] → Prod

Setup:
  1. Create "Pipeline Host" environment
  2. Install Pipeline application
  3. Define stages (Dev, Test, Prod) linked to environments
  4. Assign deployment permissions per stage
  5. Makers deploy from within their environment

// OR use Azure DevOps / GitHub Actions:
trigger:
  branches: [main]
steps:
  - task: PowerPlatformToolInstaller@2
  - task: PowerPlatformExportSolution@2
    inputs:
      environment: $(DEV_URL)
      solutionName: MyApp
      solutionOutputFile: $(Build.ArtifactStagingDirectory)/MyApp_managed.zip
      managed: true
  - task: PowerPlatformImportSolution@2
    inputs:
      environment: $(PROD_URL)
      solutionFile: $(Build.ArtifactStagingDirectory)/MyApp_managed.zip
```

### Solution Best Practices
```
Solution architecture:
  ├─ Base Solution (shared components)
  │     - Shared tables, security roles, connection references
  │     - Rarely changes, versioned independently
  ├─ Feature Solutions (per workstream)
  │     - Apps, flows, specific customizations
  │     - Reference base solution components
  └─ Patch Solutions (hotfixes)
        - Small changes between major versions
        - Clone → Patch → Export → Import

Versioning: Major.Minor.Build.Patch
  - Major: Breaking changes
  - Minor: New features
  - Build: Auto-increment on export
  - Patch: Hotfix
```

---

## 4. CoE Starter Kit

### Components
```
Core Module (deploy first):
  - Environment inventory
  - App/Flow inventory
  - Maker inventory
  - Connector usage analytics
  - Automated cleanup of orphaned resources

Governance Module:
  - Compliance flows (require business justification for apps)
  - App/Flow archival process
  - DLP policy violation detection
  - Maker onboarding automation

Nurture Module:
  - Training material catalog
  - Maker community management
  - App of the month showcase
  - Innovation challenge framework

Theming Module:
  - Branded component library for canvas apps
  - Standard header/footer components
```

### Key CoE Dashboards to Monitor
```
1. Environments dashboard: Count, type, capacity, growth trend
2. Apps dashboard: Total apps, active users, orphaned apps
3. Flows dashboard: Success/failure rates, connector usage
4. Makers dashboard: Active makers, new makers, maker growth
5. DLP dashboard: Policy violations, blocked attempts
6. Capacity dashboard: Dataverse storage, API consumption
```

---

## 5. Licensing & Capacity

### License Types (Simplified)
```
Power Apps:
  - Per User: $20/mo → Unlimited apps (premium connectors)
  - Per App: $5/mo/app → 1 app per user (premium connectors)
  - Included with M365: Standard connectors only (SharePoint, O365)
  - Pay-as-you-go: Azure subscription metered

Power Automate:
  - Per User: $15/mo → Unlimited cloud flows
  - Per Flow: $100/mo/flow → Unlimited users (5 minimum flows)
  - Per User with attended RPA: $40/mo
  - Included with M365: Standard connectors, limited triggers

Copilot Studio:
  - Tenant license: $200/mo → 25,000 messages
  - Per-message overage available
  - Included sessions in some E3/E5 scenarios

Key gotcha: Premium connectors (Dataverse, HTTP, SQL, Custom)
  require premium licenses — M365 inclusion won't cover them.
```

### Capacity Management
```
Dataverse storage:
  - Database: 10 GB base + 50MB per Premium license
  - File: 20 GB base + 2GB per Premium license
  - Log: 2 GB base + additional with add-ons
  
Monitor:
  Admin center → Resources → Capacity
  ├─ Per-environment breakdown
  ├─ Growth trends
  └─ Alerts at 80%, 90%, 95%

API request limits:
  - Per user per 24h: 40,000 (premium) / 6,000 (standard)
  - Per flow per 24h: 250,000 (licensed) / 10,000 (M365)
  - Power Platform Request add-on: 50,000/day ($50/mo)
```

---

## 6. Security & Compliance

### Tenant-Level Settings
```
Power Platform Admin Center → Settings:
  ✅ Tenant isolation: Block cross-tenant connections
  ✅ Managed environments: Enable for production
  ✅ AI Builder: Control AI feature availability
  ✅ Canvas app insights: Route to Application Insights
  ✅ Environment creation: Restrict to admins only
  ✅ Developer environment creation: Allow (controlled by DLP)
```

### Security Model Layers
```
Layer 1: Azure AD / Entra ID
  - Conditional Access: MFA for admin portals
  - PIM: Just-in-time admin access
  
Layer 2: Power Platform DLP
  - Connector classification
  - Environment-scoped policies
  
Layer 3: Dataverse Security
  - Business units, security roles
  - Row-level security, column-level security
  - Teams-based access
  
Layer 4: App-Level
  - App sharing (who can run)
  - Connection sharing (what data they reach)
  - RLS in Power BI
```

### Audit & Compliance
```
// Activity logging
Unified Audit Log (Purview Compliance):
  - App launches, flow runs, environment changes
  - Connector usage, solution imports
  - Admin actions

// Power Automate Management Connector (automate governance)
Trigger: When a new flow is created
  → Check: Is it in a managed environment?
  → Check: Does it use blocked connectors?
  → Action: Notify admin / auto-disable / request justification

// PowerShell admin module
Get-AdminPowerApp -EnvironmentName $env | Where-Object {
    $_.Internal.properties.connectionReferences | 
    ForEach-Object { $_.PSObject.Properties.Value.connectionName -eq "shared_sql" }
}
```

---

## 7. Monitoring & Alerting

### Admin Analytics Setup
```
1. Enable tenant-level analytics (Admin center → Analytics)
2. Deploy CoE Starter Kit dashboards
3. Configure alerts:
   - Environment capacity > 80%
   - Flow failure rate > 10%
   - New premium connector usage detected
   - App shared with > 50 users (review for licensing)
   - Orphaned resources (owner left org)
4. Application Insights integration for canvas apps:
   Set(varAppInsights, 
       {instrumentationKey: LookUp(EnvironmentVars, Name="AIKey").Value});
```

### Health Check Cadence
```
Daily:   Flow failure dashboard, capacity alerts
Weekly:  New apps/flows created, DLP violations, maker activity
Monthly: License utilization, environment sprawl, security review
Quarterly: Full governance review, CoE metrics presentation to leadership
```
