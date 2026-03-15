---
name: power-automate
description: >
  Genius-level Power Automate expertise covering cloud flows, desktop flows (RPA), expressions, triggers,
  connectors, error handling, approvals, business process flows, and enterprise automation patterns.
  Use this skill whenever the user mentions Power Automate, flows, cloud flows, desktop flows, RPA,
  expressions, triggers, actions, connectors, approvals, business process flows, process mining,
  flow expressions, dynamic content, Apply to Each, Do Until, Condition, HTTP connector, custom connectors,
  child flows, solution flows, or any workflow automation in the Microsoft ecosystem. Also trigger for
  questions about flow performance, throttling limits, retry policies, pagination, concurrency control,
  or flow error handling. Even casual mentions of "automating" or "workflow" in a Power Platform context
  should trigger this skill.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: microsoft
  adjacent-skills: power-apps, sharepoint, microsoft-dataverse
  last-reviewed: "2026-03-15"
  review-trigger: "Power Automate major feature release, new connector tiers, expression language breaking change"
---

# Power Automate — Savant-Level Skill

## Philosophy

Power Automate mastery = **expressions over dynamic content**, **error handling by default** (not afterthought), **child flows for reuse**, and **solution-aware from the start**. The difference between amateur and expert flows is error handling and maintainability.

---

## 1. Flow Types & When to Use

| Type | Trigger | Best For |
|---|---|---|
| **Automated cloud flow** | Event (email, item created, HTTP) | React to events |
| **Instant cloud flow** | Button/PowerApps/HTTP request | On-demand actions |
| **Scheduled cloud flow** | Recurrence/timer | Periodic jobs |
| **Desktop flow** | Called from cloud flow or manual | Legacy app automation (RPA) |
| **Business process flow** | Entity-driven stages | Guided multi-stage processes |

---

## 2. Expression Language Mastery

### Data Type Functions
```
// String
concat('Hello ', triggerBody()?['name'])
substring('Hello World', 0, 5)                    // 'Hello'
replace('2024-01-15', '-', '/')                    // '2024/01/15'
toLower(triggerBody()?['Email'])
split('a;b;c', ';')                                // ['a','b','c']
trim(body('Get_item')?['Title'])
if(empty(variables('myVar')), 'default', variables('myVar'))

// Null-safe navigation — THE #1 pattern
triggerBody()?['field']?['nested']                 // Returns null if missing (no error)
coalesce(triggerBody()?['name'], 'Unknown')        // First non-null value

// Number
int('42')                                           // String to int
float('3.14')
add(1, 2)                                           // 3
mul(variables('price'), variables('qty'))
div(variables('total'), variables('count'))
mod(variables('index'), 2)                          // Even/odd check

// Date/Time
utcNow()
convertTimeZone(utcNow(), 'UTC', 'Central Standard Time')
formatDateTime(utcNow(), 'yyyy-MM-dd')
addDays(utcNow(), 7)
addHours(triggerBody()?['StartTime'], 2)
ticks(utcNow())                                     // For duration math
dateDifference('2024-01-01', '2024-12-31')          // Returns duration

// Collection/Array
length(body('Get_items')?['value'])
first(body('Get_items')?['value'])
last(body('Get_items')?['value'])
union(variables('list1'), variables('list2'))        // Merge arrays (distinct)
intersection(variables('list1'), variables('list2')) // Common elements
contains(variables('myArray'), 'searchItem')
join(variables('nameList'), ', ')                    // Array to string
```

### JSON & Object Manipulation
```
// Create JSON object
json(concat('{"name":"', variables('name'), '","age":', variables('age'), '}'))

// Better: Use compose action to build objects, then reference with outputs()

// Parse JSON — always use after HTTP calls
// Schema tip: Paste sample payload in "Generate from sample"

// Access nested properties
body('Parse_JSON')?['data']?['records']?[0]?['id']

// XPath for XML
xpath(xml(body('HTTP')), '//Customer/Name/text()')
```

### Critical Expression Patterns
```
// Conditional with null safety
if(
    equals(triggerBody()?['Status'], 'Approved'),
    'Process payment',
    'Send to review'
)

// Multi-condition (nested if or switch-like with coalesce)
if(equals(variables('tier'), 'Gold'), 100,
    if(equals(variables('tier'), 'Silver'), 50, 25)
)

// Dynamic property access
triggerBody()?[variables('columnName')]             // Column name from variable

// Batch array filtering (select + filter)
// Use Filter Array action, then reference:
@body('Filter_array')
```

---

## 3. Error Handling — Non-Negotiable

### Scope + Configure Run After
```
Architecture:
┌─ Scope: "Try" ────────────┐
│   Action 1                 │
│   Action 2                 │
│   Action 3                 │
└────────────────────────────┘
           │
           ▼
┌─ Scope: "Catch" ──────────┐  ← Configure Run After: "has failed", "has timed out"
│   Compose: Error Details    │
│   Send Error Email          │
│   Terminate (Failed)        │
└────────────────────────────┘
           │
           ▼
┌─ Scope: "Finally" ────────┐  ← Configure Run After: all four states
│   Update Status Log         │
│   Release Lock              │
└────────────────────────────┘
```

### Capturing Error Details
```
// Inside Catch scope — get error from Try scope
result('Try_Scope')                           // Full result array
// Filter to failed actions:
outputs('Specific_Action_Name')?['statusCode']
outputs('Specific_Action_Name')?['body']?['error']?['message']

// Generic error capture with Compose:
{
  "flowName": workflow()?['tags']?['flowDisplayName'],
  "runId": workflow()?['run']?['name'],
  "timestamp": utcNow(),
  "error": result('Try_Scope')
}
```

### Retry Policies
```
// Set on individual actions (HTTP, connectors):
{
    "retryPolicy": {
        "type": "exponential",    // or "fixed", "none"
        "count": 4,
        "interval": "PT10S",       // ISO 8601 duration
        "minimumInterval": "PT5S",
        "maximumInterval": "PT1H"
    }
}
```

---

## 4. Performance & Throttling

### Concurrency Control
- **Apply to Each**: Default = sequential. Enable concurrency (up to 50) for independent items.
- **Trigger concurrency**: Controls parallel flow runs. Default = 25.
- **Degree of parallelism**: Set explicitly; don't rely on defaults.

### Throttling Limits (Key Numbers)
| Resource | Limit |
|---|---|
| Actions per flow run | 100,000 |
| Flow runs per 5 min (per flow) | 100,000 |
| API calls per connection per 24h | 6,000 (standard) / 12,000 (premium) |
| HTTP request size | 100 MB |
| Apply to Each items | 100,000 |
| Expression nesting depth | 8 levels |

### Pagination
```
// Enable on "List items" actions for >256 (SharePoint) or >5000 items
// Settings → Pagination → On → Threshold: 10000

// For custom pagination (HTTP):
Do Until: empty(body('HTTP')?['@odata.nextLink'])
    HTTP GET: variables('nextLink')
    Append to array: union(variables('allResults'), body('HTTP')?['value'])
    Set variable: body('HTTP')?['@odata.nextLink']
```

---

## 5. Enterprise Patterns

### Child Flows (Reusable Sub-Flows)
```
Parent Flow:
  ├─ Run a Child Flow: "Process Invoice"
  │     Input: { invoiceId: ..., amount: ... }
  │     Output: { status: "approved", approver: "..." }
  └─ Use output: body('Run_a_Child_Flow')?['status']

Child Flow:
  Trigger: "When a flow is invoked from another flow" (solution-aware only)
  Input parameters defined in trigger
  "Respond to a Power App or flow" action at end for outputs
```

### Approval Patterns
```
// Basic approval
Start and wait for an approval → Approve/Reject
If outcome = 'Approve' → proceed
If outcome = 'Reject' → notify requestor

// Sequential approval chain
ForEach approver in ApproverList:
    Start and wait for approval
    If Reject → break, notify all

// Parallel approval (First to respond)
Start and wait for an approval (Everyone must approve = No)

// Parallel approval (All must approve)
Start and wait for an approval (Everyone must approve = Yes)

// Custom approval with Adaptive Cards
Post adaptive card and wait for a response (Teams)
// Gives rich UI with dropdown, text input, date picker in approval
```

### HTTP Connector Patterns
```
// REST API with OAuth
HTTP Action:
  Method: POST
  URI: https://api.service.com/endpoint
  Headers:
    Authorization: Bearer @{body('Get_Token')?['access_token']}
    Content-Type: application/json
  Body: @{variables('requestBody')}

// Graph API call
HTTP:
  Method: GET
  URI: https://graph.microsoft.com/v1.0/me/messages?$top=10
  Authentication: Active Directory OAuth
  Tenant: @{variables('tenantId')}
  Client ID: @{variables('clientId')}
  Secret: @{variables('clientSecret')}
  Resource: https://graph.microsoft.com
```

### Batch Processing Pattern
```
// Process large datasets without timeout
1. Scheduled trigger
2. Get items (with pagination)
3. Initialize counter = 0
4. Do Until counter >= length(items) OR counter >= 5000
   ├─ Compose: slice of items[counter..counter+50]
   ├─ Apply to Each (concurrent: 20)
   │   └─ Process item
   ├─ Increment counter by 50
   └─ Delay: 1 second (rate limit buffer)
5. If more items remain: HTTP trigger self (continuation)
```

---

## 6. Desktop Flows (RPA)

### When to Use
- Legacy apps with no API (mainframe, thick client, old web apps)
- File system operations (network drives, local folders)
- Desktop app automation (Excel macros, SAP GUI, AS400)

### Key Patterns
```
// Web automation
Launch browser → Navigate → Wait for element → Extract data → Close

// Excel automation
Launch Excel → Open workbook → Read range → Process → Write range → Save → Close

// UI automation (any Windows app)
Launch app → Focus window → Send keys → Click element → Scrape data

// Error handling in desktop flows
On Block Error:
    Retry: 3 times, interval 5 seconds
    On Retry Failure: Continue / Throw
```

### Desktop + Cloud Integration
```
Cloud Flow (Trigger: scheduled)
  ├─ Get data from Dataverse/SharePoint
  ├─ Run Desktop Flow (attended or unattended)
  │     Machine: registered machine/machine group
  │     Input: data from cloud flow
  │     Output: processed result
  └─ Update Dataverse with results
```

---

## 7. Solution-Aware Development

### Connection References
```
// Never hardcode connections in flows
// Use connection references in solutions:
1. Create connection reference in solution
2. Flow actions auto-use connection reference
3. On import to new environment: map to environment-specific connection
```

### Environment Variables
```
// Use for:
- API endpoints that differ per environment
- Email distribution lists
- Feature flags
- Threshold values

// Reference in expressions:
@{triggerBody()?['custom_envvar_schema_name']}
// Or use the "List rows" action filtered to your env var
```

### ALM Pipeline
```
Dev:  Build in unmanaged solution → Test
        ↓ Export as managed
Test: Import managed → Integration test
        ↓ Export (or use same package)
Prod: Import managed → Smoke test → Monitor
```

---

## 8. Monitoring & Diagnostics

### Flow Analytics
- **Power Automate Analytics** (admin center): Run history, success/failure rates
- **Application Insights integration**: Custom tracking via HTTP actions
  ```
  HTTP POST to App Insights ingestion endpoint:
  {
    "name": "FlowEvent",
    "properties": {
      "flowName": "@{workflow()?['tags']?['flowDisplayName']}",
      "action": "ProcessInvoice",
      "duration": "@{div(sub(ticks(utcNow()), ticks(variables('startTime'))), 10000000)}"
    }
  }
  ```

### Common Failure Patterns & Fixes
| Symptom | Root Cause | Fix |
|---|---|---|
| "Action timed out" | API slow/down | Retry policy + timeout increase |
| "Rate limit exceeded" | Too many API calls | Add delays, reduce concurrency |
| 403 on SharePoint | Permissions | Service account or app-only auth |
| "Expression evaluation failed" | Null reference | Add null-safe `?` operators |
| Apply to Each slow | Sequential processing | Enable concurrency |
| Flow runs but no trigger | Trigger conditions not met | Check trigger conditions/filters |

---

## Anti-Patterns

**Anti-Pattern 1: No Error Handling**
Building flows with no Scope + Configure Run After error handling. A single failed action silently
fails the entire flow with no notification to anyone. Days of failed processing go unnoticed until
a business process breaks.
Fix: Every production flow gets a Try/Catch/Finally scope structure. The Catch scope always sends
a notification (Teams or email) with the flow name, run ID, timestamp, and error details.

**Anti-Pattern 2: Personal Account Connections**
Building flows that connect to SharePoint, Outlook, or Dataverse using the maker's personal credentials.
When that person leaves the organization, every flow they built breaks simultaneously.
Fix: Use service accounts for all production flow connections. Service accounts should have the
minimum permissions needed and should never expire. Document ownership in the flow description.

**Anti-Pattern 3: Monolithic Flows with Hundreds of Actions**
Building one massive flow that handles every edge case, every branch, and every notification in a
single run. When it fails, diagnosing which of 200 actions failed is a nightmare. Editing any
part risks breaking other parts.
Fix: Decompose into child flows. Each child flow is a named, testable unit of work. The parent flow
orchestrates by calling child flows. Child flows can be reused across multiple parent flows.

---

## Quality Gates

- [ ] Every production flow has Try/Catch/Finally scope structure
- [ ] Catch scope sends notification with flow name, run ID, and error details
- [ ] All connections use service accounts, not personal accounts
- [ ] All flows are solution-aware (inside a solution with connection references)
- [ ] Apply to Each concurrency explicitly configured (not left at default sequential)
- [ ] Retry policy configured on all HTTP and external connector actions

---

## Failure Modes and Fallbacks

**Failure: Flow runs reach the 30-day auto-cancel timeout**
Detection: Long-running approval flows (waiting for human input) are cancelled after 30 days with no
resolution.
Fallback: Redesign the approval to send reminders before the timeout. At day 25, send a reminder.
At day 28, escalate to the approver's manager. Consider splitting long-running flows into multiple
flows that restart via a scheduled trigger checking for pending approvals.

**Failure: Connector throttling causes mass flow failures**
Detection: Multiple flows fail simultaneously with "429 Too Many Requests" errors.
Fallback: Implement a queue-based pattern: instead of all flows calling the connector directly,
have them write requests to a SharePoint list or Service Bus queue. A single scheduled flow processes
the queue with explicit rate limiting and delays between calls.

---

## Composability

**Hands off to:**
- `power-apps` — when a flow output needs to be surfaced in an app UI
- `microsoft-dataverse` — when the flow needs to read/write complex Dataverse data

**Receives from:**
- `power-apps` — app button clicks and form submissions trigger instant cloud flows
- `sharepoint` — SharePoint list item events are the most common automation trigger
- `power-platform-admin` — DLP policies constrain which connectors flows can use
