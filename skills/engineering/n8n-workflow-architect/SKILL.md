---
name: n8n-workflow-architect
description: |
  Expert n8n workflow designer and automation architect. Use whenever building, debugging,
  optimizing, or planning n8n workflows, automation pipelines, webhook integrations, or
  scheduled data processing. AUTO-TRIGGER on any automation, workflow, webhook, ETL, or
  integration architecture discussion.

  EXPLICIT TRIGGER on: "n8n", "workflow", "automation", "webhook", "trigger", "schedule",
  "cron job", "API orchestration", "data pipeline", "ETL", "integration", "node",
  "error handling in n8n", "retry logic", "sub-workflow", "n8n credential", "HTTP request node",
  "Code node", "batch processing", "event-driven", "notification pipeline", "sync data",
  "n8n Docker", "workflow design", "automate this".

  Also trigger when the user describes a process that should be automated, even without
  mentioning n8n — assess whether n8n is the right tool and recommend accordingly.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: ai-agentic-specialist, power-automate, cloud-migration-playbook, app-security-architect
  last-reviewed: "2026-03-21"
  review-trigger: "New n8n major version, new node types, user reports workflow pattern failure"
  capability-assumptions:
    - "n8n self-hosted in Docker on home server (192.168.1.240)"
    - "HTTP Request node, Code node (JS), PostgreSQL node available"
    - "No external tools required — outputs workflow architecture as text"
  fallback-patterns:
    - "If no n8n access: suggest Power Automate or direct Python script alternative"
    - "If cloud-only: note that n8n Cloud differs from self-hosted in credential management"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: automation requirement, integration need, or workflow to debug/optimize
- Output produces: workflow architecture, node configuration guide, or troubleshooting plan
- Can chain from: ai-agentic-specialist (agent design → automation layer)
- Can chain into: app-security-architect (secure the webhook/credentials), cloud-migration-playbook (deploy)
- Orchestrator notes: recommend sub-workflows for any design exceeding 15 nodes

---

## Workflow Architecture Principles

### 1. Start with the Trigger
Every workflow begins with exactly one trigger. Choose deliberately:
- **Webhook** — external system pushes data to you (real-time)
- **Schedule/Cron** — time-based execution (polling, batch jobs, reports)
- **Event trigger** — n8n-native events (error trigger, workflow trigger from another workflow)
- **App trigger** — platform-specific (email received, Slack message, form submission)

### 2. Design for Idempotency
Running the same workflow twice with the same input should produce the same result without
side effects. This means:
- Use upserts instead of inserts where possible
- Check for existing records before creating new ones
- Include deduplication keys in webhook payloads

### 3. Keep Workflows Modular
- No workflow should exceed 15-20 nodes — split into sub-workflows
- Use the Execute Workflow node to chain workflows
- Each workflow has one clear purpose (Single Responsibility)
- Pass data between workflows via input parameters, not global state

### 4. Error Handling at Every Critical Node
- Wrap risky nodes (HTTP requests, database writes) in try/catch
- Use the Error Trigger workflow as a global safety net
- Always have a notification path for failures

### 5. Never Hardcode Credentials or URLs
- Use n8n's built-in credential system for all API keys
- Use environment variables for base URLs and configuration
- In Docker: pass env vars via docker-compose.yml or .env file

---

## Node Selection Guide

| Need | Node | Key Pattern |
|------|------|-------------|
| Call external API | HTTP Request | Set auth headers, handle pagination with loop |
| Transform data | Code (JS) | `items.map()` for batch transforms, return `[{json: {...}}]` |
| Conditional logic | IF / Switch | IF for binary, Switch for multi-branch |
| Set/rename fields | Set | Map fields, add computed values, remove sensitive data |
| Combine data streams | Merge | Append (concat), Combine (join on key), Multiplex (cross-product) |
| Wait for event | Wait | Webhook resume, timer delay, or external signal |
| Store/query data | PostgreSQL | Use parameterized queries — never string interpolation |
| Send notifications | Slack / Email | Final nodes in success/error paths |
| Handle errors globally | Error Trigger | Separate workflow that catches all failures |
| Call another workflow | Execute Workflow | Pass input data, receive output |

### HTTP Request Patterns
```
Authentication: Use predefined credentials (OAuth2, API Key header, Bearer token)
Pagination: Loop with IF node checking `hasMore` or `nextPage` field
Rate limiting: Add Wait node (1-2 sec) between paginated calls
Retry: Enable retry on fail (3 attempts, exponential backoff)
```

### Code Node Patterns
```javascript
// Transform items — always return array of {json: {...}} objects
return items.map(item => ({
  json: {
    ...item.json,
    fullName: `${item.json.firstName} ${item.json.lastName}`,
    processedAt: new Date().toISOString()
  }
}));
```

---

## Common Workflow Patterns

### Pattern 1: Webhook → Process → Store → Notify
```
Webhook → Code (validate/transform) → PostgreSQL (upsert) → Slack (confirm)
                                     ↘ Error Trigger → Slack (alert)
```
Use for: incoming data from external systems, form submissions, third-party callbacks.

### Pattern 2: Scheduled Data Sync
```
Schedule (every 6h) → HTTP Request (fetch API) → Code (transform) →
  IF (new records?) → PostgreSQL (upsert) → Slack (summary)
                    → No-op (nothing new)
```
Use for: pulling data from APIs that don't support webhooks.

### Pattern 3: Multi-Step API Orchestration
```
Trigger → HTTP (Step 1) → Code (extract ID) → HTTP (Step 2, using ID) →
  Code (merge results) → PostgreSQL (store) → Slack (complete)
Each HTTP node: retry on fail enabled, error output connected to error handler
```

### Pattern 4: File Processing Pipeline
```
Webhook (file upload) → Code (validate type/size) →
  IF (valid?) → HTTP (send to processing API) → Wait (webhook resume) →
    Code (parse result) → PostgreSQL (store metadata) → Slack (done)
  → Slack (rejected: invalid file)
```

### Pattern 5: Fan-Out / Fan-In
```
Trigger → SplitInBatches (chunk large dataset) →
  HTTP Request (process each batch) → Merge (collect results) →
  Code (aggregate) → PostgreSQL (store summary)
```

---

## Integration with Your Stack

### n8n → FastAPI
- Webhook node in n8n calls your FastAPI endpoint
- Or: FastAPI calls n8n webhook to trigger a workflow
- Auth: use shared API key in header (stored in n8n credentials + FastAPI settings)
- Pattern: FastAPI handles complex business logic, n8n handles orchestration/scheduling

### n8n → PostgreSQL
- Use the PostgreSQL node directly for simple queries
- For complex operations: call your FastAPI endpoint which handles the database logic
- Always use parameterized queries in PostgreSQL node — never build SQL strings in Code node

### n8n → GCP
- Cloud Run: HTTP Request node with service account token auth
- Cloud Storage: HTTP Request to GCS JSON API (or use dedicated GCS node if available)
- BigQuery: HTTP Request to BigQuery REST API with OAuth2 credential
- Pub/Sub: Webhook trigger receives Pub/Sub push messages

### n8n → Docker
- Use HTTP Request to Docker API socket (if exposed) for container management
- Or: SSH node to execute docker commands on host
- Pattern: n8n monitors → detects issue → restarts container → notifies

### n8n → Power Platform
- Dataverse: HTTP Request with Azure AD OAuth2 to Dataverse Web API
- Power Automate: n8n webhook triggers PA flow, or PA calls n8n webhook
- Bidirectional: use n8n for heavy data processing, PA for Microsoft ecosystem actions

---

## Error Handling & Monitoring

### Global Error Handler Pattern
Create a dedicated workflow with an Error Trigger node:
```
Error Trigger → Code (format error details: workflow name, node, message, timestamp) →
  Slack (post to #n8n-errors channel) → PostgreSQL (log to error_log table)
```

### Node-Level Error Handling
- Enable "Continue on Fail" only when you explicitly handle the error downstream
- Use the error output (red connector) to route failures to notification/logging
- Add retry settings on HTTP Request nodes: 3 retries, 1000ms initial interval, exponential

### Dead Letter Queue Pattern
For critical workflows where data loss is unacceptable:
```
Main workflow fails → Error Trigger → PostgreSQL (store failed payload in dead_letter table) →
  Schedule (hourly) → Query dead_letter → Retry processing → IF (success?) → Remove from table
```

### Monitoring Checklist
- Set up execution logging in n8n settings (keep 30 days)
- Create a daily summary workflow: count executions, errors, avg duration
- Alert thresholds: >5 failures/hour, execution time >2x normal, queue depth growing

---

## Security

- **Credentials:** Use n8n's built-in credential store — encrypted at rest. Never pass secrets
  through workflow data fields or Code nodes.
- **Webhook auth:** Always protect webhooks with at least header-based authentication.
  For production: use HMAC signature verification in a Code node.
- **Network:** Self-hosted n8n should not be exposed to public internet without reverse proxy
  (Traefik, Nginx) with TLS. Use Cloudflare Tunnel or Tailscale for remote access.
- **Docker env vars:** Pass sensitive config via Docker secrets or `.env` file (in `.gitignore`).
  Never bake secrets into docker-compose.yml.
- **Least privilege:** Each n8n credential should have minimum required permissions.
  Read-only where possible, scoped API keys over admin keys.

---

## Self-Evaluation (run before presenting workflow design)

Before presenting any workflow design, silently check:
[ ] Does every workflow start with exactly one trigger?
[ ] Is the workflow under 15-20 nodes? If not, should it be split into sub-workflows?
[ ] Does every HTTP Request and database node have error handling?
[ ] Are credentials managed through n8n's credential system, not hardcoded?
[ ] Is the design idempotent — can it run twice safely?
[ ] Is there a notification path for both success and failure?
If any check fails, revise before presenting.

---

## Read references/ for:
- Extended pagination patterns for common APIs
- Docker Compose template for n8n with PostgreSQL and Redis
- n8n backup and migration procedures
- Advanced sub-workflow communication patterns
