---
name: m365-integration
description: >
  Genius-level Microsoft 365 integration expertise covering Microsoft Graph API, Teams development,
  Outlook/Exchange integration, OneDrive API, Entra ID (Azure AD), authentication patterns (MSAL),
  and cross-platform orchestration. Use this skill whenever the user mentions Microsoft Graph,
  Graph API, Teams development, Teams tabs, Teams bots, Teams message extensions, MSAL, Azure AD,
  Entra ID, OAuth2, app registration, service principals, managed identity, OneDrive API, Outlook API,
  Exchange Online, Microsoft 365 admin, or any integration across the Microsoft 365 ecosystem.
  Also trigger for questions about SSO, token management, delegated vs application permissions,
  or building apps that span multiple M365 services.
---

# Microsoft 365 Integration — Savant-Level Skill

## Philosophy

M365 integration mastery = **Graph API as the single unified endpoint**, **MSAL for all auth** (never raw OAuth), **least-privilege permissions**, and **webhooks + change notifications for reactive patterns** (not polling).

---

## 1. Microsoft Graph API

### Core Endpoints
```
Users:      GET /v1.0/users/{id}
Groups:     GET /v1.0/groups/{id}/members
Mail:       GET /v1.0/me/messages?$filter=isRead eq false&$top=10
Calendar:   GET /v1.0/me/events?$filter=start/dateTime ge '{date}'
Files:      GET /v1.0/me/drive/root/children
SharePoint: GET /v1.0/sites/{hostname}:/{path}:/lists
Teams:      GET /v1.0/teams/{id}/channels
Planner:    GET /v1.0/planner/plans/{id}/tasks
```

### Common Patterns
```
// Pagination
GET /v1.0/users?$top=100
→ Response includes @odata.nextLink if more pages
→ Follow @odata.nextLink until null

// Batch requests (up to 20 per batch)
POST /$batch
{
  "requests": [
    {"id": "1", "method": "GET", "url": "/me/messages?$top=5"},
    {"id": "2", "method": "GET", "url": "/me/events?$top=5"},
    {"id": "3", "method": "GET", "url": "/me/drive/recent"}
  ]
}

// Delta queries (incremental sync)
GET /v1.0/users/delta?$select=displayName,mail
→ Returns @odata.deltaLink
→ Next call: GET {deltaLink} → only changed records

// Change notifications (webhooks)
POST /v1.0/subscriptions
{
  "changeType": "created,updated",
  "notificationUrl": "https://yourapp.com/webhook",
  "resource": "/me/messages",
  "expirationDateTime": "2024-01-15T00:00:00Z",
  "clientState": "secretValue"
}
```

### OData Query Parameters
```
$select=displayName,mail          // Specific columns (always use!)
$filter=department eq 'IT'        // Server-side filter
$orderby=displayName asc          // Sort
$top=50                           // Page size
$skip=100                         // Offset (not for all endpoints)
$count=true                       // Include total count
$expand=manager($select=displayName)  // Include related
$search="displayName:John"        // Full-text search
```

---

## 2. Authentication (MSAL)

### App Registration
```
Azure Portal → Entra ID → App registrations → New
  - Name: "My Integration App"
  - Supported account types: Single tenant (most common)
  - Redirect URI: Web → https://yourapp.com/auth/callback
  
After creation:
  1. Note: Application (client) ID, Directory (tenant) ID
  2. Certificates & secrets → New client secret (or certificate for prod)
  3. API permissions → Add:
     - Delegated: User.Read, Mail.Read, Calendars.Read
     - Application: Mail.ReadBasic.All (for daemon/service apps)
  4. Admin consent: Required for Application permissions
```

### Permission Types
```
Delegated (user context):
  - User signs in, app acts on their behalf
  - Scoped to what user can already access
  - Example: Read the signed-in user's mail

Application (daemon/service):
  - App acts as itself (no user)
  - Can access any user's data (if permitted)
  - Example: Read ALL users' mail in the org
  - Requires admin consent

// Principle: Always prefer Delegated over Application
// Application permissions = broad access, higher risk
```

### MSAL Code Patterns
```javascript
// Browser (MSAL.js)
import { PublicClientApplication } from "@azure/msal-browser";

const msalConfig = {
  auth: {
    clientId: "your-client-id",
    authority: "https://login.microsoftonline.com/{tenantId}",
    redirectUri: "https://yourapp.com"
  }
};

const pca = new PublicClientApplication(msalConfig);
const loginRequest = { scopes: ["User.Read", "Mail.Read"] };

// Interactive login
const response = await pca.loginPopup(loginRequest);

// Silent token acquisition (cached)
const tokenResponse = await pca.acquireTokenSilent({
  scopes: ["User.Read"],
  account: pca.getAllAccounts()[0]
});

// Use token
fetch("https://graph.microsoft.com/v1.0/me", {
  headers: { Authorization: `Bearer ${tokenResponse.accessToken}` }
});
```

```python
# Python (MSAL)
from msal import ConfidentialClientApplication

app = ConfidentialClientApplication(
    client_id="your-client-id",
    authority="https://login.microsoftonline.com/{tenantId}",
    client_credential="your-client-secret"
)

# Application (daemon) flow
result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
token = result["access_token"]

# Delegated (with user credentials — device code flow)
flow = app.initiate_device_flow(scopes=["User.Read"])
print(flow["message"])  # User visits URL and enters code
result = app.acquire_token_by_device_flow(flow)
```

```powershell
# PowerShell
Connect-MgGraph -Scopes "User.Read.All","Group.Read.All"
# or with certificate:
Connect-MgGraph -ClientId $clientId -TenantId $tenantId -CertificateThumbprint $thumbprint

Get-MgUser -Filter "department eq 'Engineering'" -Select displayName,mail
```

---

## 3. Teams Development

### Teams App Types
```
Tabs:
  - Personal tab: Single-user view (iframe to your web app)
  - Channel tab: Shared in channel (configurable)
  - SSO: Use Teams JS SDK for silent token acquisition

Bots:
  - Conversational: Built with Bot Framework or Copilot Studio
  - Messaging extensions: Search/action in compose box
  - Proactive messaging: Bot initiates conversation

Webhooks:
  - Incoming: POST URL to send messages to Teams channel
  - Outgoing: Teams sends messages to your endpoint

Connectors:
  - Office 365 Connectors: Cards in channel (being deprecated)
  - Use Workflows (Power Automate) instead
```

### Incoming Webhook (Simplest Integration)
```
// Create: Teams channel → Manage channel → Connectors → Incoming Webhook
// Use the webhook URL to send adaptive cards

POST {webhookUrl}
{
  "type": "message",
  "attachments": [{
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": {
      "type": "AdaptiveCard",
      "version": "1.4",
      "body": [
        {"type": "TextBlock", "text": "Build Failed!", "weight": "Bolder", "color": "Attention"},
        {"type": "TextBlock", "text": "Pipeline: main-ci | Duration: 4m 32s"}
      ],
      "actions": [
        {"type": "Action.OpenUrl", "title": "View Logs", "url": "https://..."}
      ]
    }
  }]
}
```

### Proactive Bot Messaging
```javascript
// Store conversation reference when bot is first installed
adapter.onTurnError = async (context, error) => { /* handle */ };

// Later, send proactive message
await adapter.continueConversationAsync(
  botAppId,
  storedConversationReference,
  async (turnContext) => {
    await turnContext.sendActivity("Your report is ready!");
  }
);
```

---

## 4. Cross-Service Orchestration Patterns

### Event-Driven Architecture
```
Pattern: SharePoint → Graph webhook → Azure Function → Teams notification

1. Subscribe to SharePoint changes:
   POST /v1.0/subscriptions
   { "resource": "sites/{id}/lists/{id}/items", "changeType": "updated" }

2. Azure Function receives notification:
   - Validate subscription
   - Query changed items via Graph
   - Determine notification recipients

3. Send Teams message:
   POST /v1.0/teams/{id}/channels/{id}/messages
   { "body": { "content": "Document updated: <a href='...'>Report.docx</a>" } }
```

### Data Sync Pattern
```
Pattern: External CRM → Dataverse → Power BI + Teams

1. Scheduled Power Automate flow:
   - HTTP GET from external CRM API
   - Upsert into Dataverse (alternate key matching)
   - Log sync results

2. Dataverse change triggers:
   - Power Automate: On record update → Notify Teams channel
   - Power BI: DirectQuery/Import from Dataverse → Dashboard refresh

3. Error handling:
   - Failed syncs → Teams alert to admin channel
   - Conflict resolution → Last-write-wins with audit trail
```

---

## 5. Security Best Practices

```
Authentication:
  ✅ Use MSAL libraries (never raw HTTP to token endpoint)
  ✅ Certificate auth for production (not client secrets)
  ✅ Managed Identity for Azure-hosted apps (no secrets at all)
  ✅ Token caching with MSAL (it handles refresh automatically)
  ❌ Never store tokens in localStorage
  ❌ Never expose client secrets in client-side code

Permissions:
  ✅ Request minimum scopes needed
  ✅ Use incremental consent (request scopes as needed)
  ✅ Prefer delegated over application permissions
  ✅ Use app-only for daemon scenarios, never for user-facing apps
  ❌ Never request Directory.ReadWrite.All "just in case"
  
API Security:
  ✅ Validate tokens on your backend (issuer, audience, signature)
  ✅ Use $select to minimize data exposure
  ✅ Rate limit your calls (Graph throttles at 429)
  ✅ Handle 429 with Retry-After header
```
