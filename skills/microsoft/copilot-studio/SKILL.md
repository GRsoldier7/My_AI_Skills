---
name: copilot-studio
description: >
  Genius-level Copilot Studio (formerly Power Virtual Agents) expertise covering bot design, topics,
  generative AI orchestration, plugin actions, adaptive cards, multi-channel deployment, authentication,
  analytics, and enterprise patterns. Use this skill whenever the user mentions Copilot Studio,
  Power Virtual Agents, PVA, chatbots, conversational AI, topics, trigger phrases, entities, slot filling,
  generative answers, generative actions, plugin actions, bot authentication, Teams bots, webchat,
  multi-channel bots, adaptive cards in bots, or any conversational AI development in the Microsoft
  ecosystem. Also trigger for questions about bot analytics, escalation to live agents, knowledge sources,
  custom GPTs in Copilot Studio, or Microsoft 365 Copilot extensibility.
---

# Copilot Studio — Savant-Level Skill

## Philosophy

Copilot Studio mastery = **generative AI + deterministic topics** as a hybrid (not one or the other), **proper entity extraction for slot filling**, **graceful escalation paths**, and **analytics-driven iteration**. The best bots feel conversational but have guardrails.

---

## 1. Architecture Decision: Classic Topics vs Generative AI

### Hybrid Approach (Best Practice)
```
User utterance
  ├─ Trigger phrase matches a Topic? → Deterministic topic flow
  │     (structured, predictable, business-critical paths)
  ├─ No topic match + Knowledge sources configured? → Generative Answers
  │     (grounded in your uploaded docs/websites/SharePoint)
  └─ Fallback → Escalation or "I don't understand" + suggestions
```

### When to Use Each
| Approach | Use For |
|---|---|
| **Classic Topics** | Order status, password reset, approvals, any process with defined steps |
| **Generative Answers** | FAQ, policy lookup, product info, anything with a knowledge base |
| **Generative Actions (Plugins)** | Dynamic data retrieval, creating records, triggering workflows |
| **Custom GPT Instructions** | Persona, tone, guardrails, response formatting |

---

## 2. Topic Design Patterns

### Anatomy of a Well-Designed Topic
```
Topic: "Request Time Off"
  Trigger phrases (8-12 varied examples):
    - "I want to request time off"
    - "How do I submit PTO"
    - "I need vacation days"
    - "Take a day off"
    - "Submit leave request"
    - "PTO request"
    - "Book holiday"
    - "I want to take next Friday off"

  Flow:
    1. Ask: Leave type? [Entity: Choice - Vacation/Sick/Personal]
    2. Ask: Start date? [Entity: Date and time]
    3. Ask: End date? [Entity: Date and time]
    4. Condition: EndDate >= StartDate?
       ├─ No → "End date must be after start date." → Loop back
       └─ Yes → Continue
    5. Confirm: "You're requesting {LeaveType} from {StartDate} to {EndDate}. Submit?"
       ├─ Yes → Call Power Automate flow (create leave request)
       │         → "Your request has been submitted. Reference: {RefID}"
       └─ No → "What would you like to change?" → Branch
    6. Post-action: "Anything else I can help with?"
```

### Entity Extraction & Slot Filling
```
Built-in entities:
  - Age, Boolean, City, Color, Continent, Country, Currency
  - Date and time, Duration, Email, Event, Money, Number
  - Ordinal, Organization, Percentage, Person name, Phone
  - Point of interest, Speed, State, Street address, Temperature, URL

Custom entities:
  - Closed list: {"Active", "Inactive", "Suspended"} with synonyms
  - Regex: Order ID pattern → ^ORD-\d{6}$
  - Smart match: Fuzzy matching on entity values

Slot filling:
  // If user says "I want to book vacation from March 1 to March 5"
  // Bot extracts: LeaveType=Vacation, StartDate=March 1, EndDate=March 5
  // Skips those questions, asks only for missing slots
```

### Conversation Flow Patterns
```
// Disambiguation
"Did you mean:
  1. Check order status
  2. Return an order
  3. Cancel an order"
→ Use "Question" node with Choice entity

// Confirmation loop
Ask → Validate → If invalid, explain error → Re-ask (max 3 attempts)
→ After 3 failures, escalate to agent

// Context carryover
Set variable: Topic.CustomerName = Activity.From.Name
// Use across nodes: "Thanks {Topic.CustomerName}, I found your order."

// Progressive disclosure
"I found 3 results. Want to see:"
  1. A summary
  2. Full details
  3. Download as PDF
```

---

## 3. Generative AI Configuration

### Knowledge Sources
```
Supported sources:
  - SharePoint sites (auto-indexes)
  - Public websites (crawled)
  - Uploaded documents (PDF, Word, txt)
  - Dataverse tables
  - Custom data via connectors

Configuration:
  Settings → Generative AI → Knowledge sources
  ├─ Add SharePoint site URLs
  ├─ Upload documents
  ├─ Content moderation: High/Medium/Low
  └─ Citation format: Inline/Footnote
```

### Generative Actions (Plugin Architecture)
```
Plugin = Connector + Action + Description

Flow:
  User: "What's the status of Project Alpha?"
  Bot: [Generative orchestrator decides which plugin to invoke]
    → Plugin: "Dataverse - Get Project"
    → Input: ProjectName = "Alpha"
    → Output: Status, Budget, Timeline
  Bot: "Project Alpha is currently in Phase 2, on budget at $450K, with 3 weeks remaining."

Creating a plugin action:
  1. Topics → Add Plugin Action
  2. Select connector (Dataverse, SharePoint, Custom, Power Automate flow)
  3. Define input/output schema with descriptions
  4. Add description: "Use this action when user asks about project status, timeline, or budget"
  5. Test with varied utterances
```

### System Instructions (Custom GPT Behavior)
```
Settings → Generative AI → System instructions:

"You are an IT Help Desk assistant for Contoso Corp. Follow these rules:
1. Always be professional and empathetic
2. For password resets, always verify the employee ID first
3. Never share internal system URLs or admin credentials
4. If you don't know the answer, say so and offer to create a ticket
5. For hardware requests, always ask about the user's department for approval routing
6. End every interaction by asking if there's anything else
7. Maximum response length: 3 sentences for simple queries, 5 for complex"
```

---

## 4. Adaptive Cards in Bots

### Rich Response Patterns
```json
// Order status card
{
  "type": "AdaptiveCard",
  "version": "1.5",
  "body": [
    {
      "type": "ColumnSet",
      "columns": [
        {
          "type": "Column", "width": "auto",
          "items": [{"type": "Image", "url": "{ProductImage}", "size": "Medium"}]
        },
        {
          "type": "Column", "width": "stretch",
          "items": [
            {"type": "TextBlock", "text": "Order #{OrderID}", "weight": "Bolder", "size": "Medium"},
            {"type": "TextBlock", "text": "Status: {Status}", "color": "Good"},
            {"type": "TextBlock", "text": "Estimated delivery: {DeliveryDate}", "isSubtle": true}
          ]
        }
      ]
    }
  ],
  "actions": [
    {"type": "Action.OpenUrl", "title": "Track Package", "url": "{TrackingURL}"},
    {"type": "Action.Submit", "title": "Report Issue", "data": {"action": "reportIssue", "orderId": "{OrderID}"}}
  ]
}

// Input form card (collect structured data)
{
  "type": "AdaptiveCard", "version": "1.5",
  "body": [
    {"type": "TextBlock", "text": "Submit IT Ticket", "weight": "Bolder"},
    {"type": "Input.ChoiceSet", "id": "category", "label": "Category",
      "choices": [
        {"title": "Hardware", "value": "hw"},
        {"title": "Software", "value": "sw"},
        {"title": "Network", "value": "net"}
      ]},
    {"type": "Input.Text", "id": "description", "label": "Description", "isMultiline": true},
    {"type": "Input.ChoiceSet", "id": "priority", "label": "Priority", "style": "compact",
      "choices": [
        {"title": "Low", "value": "low"},
        {"title": "Medium", "value": "med"},
        {"title": "High", "value": "high"}
      ]}
  ],
  "actions": [
    {"type": "Action.Submit", "title": "Submit Ticket"}
  ]
}
```

---

## 5. Multi-Channel Deployment

### Channel Configuration
```
Channels:
  ├─ Microsoft Teams (primary for enterprise)
  │     - Auto-deployed via Teams admin center
  │     - Supports adaptive cards, SSO, file sharing
  │     - Deep links: teams://chat?userPrincipalName=bot@contoso.com
  │
  ├─ Web Chat (customer-facing)
  │     - Embed: <iframe src="https://web.powerva.microsoft.com/...">
  │     - Custom canvas: Use Direct Line token + Bot Framework WebChat SDK
  │     - Branding: Custom CSS, avatar, welcome message
  │
  ├─ Facebook, Slack, Twilio (SMS) — via Bot Framework channels
  │
  └─ Custom App — Direct Line API
        POST /v3/directline/conversations
        Authorization: Bearer {DirectLineSecret}
```

### Channel-Specific Adaptation
```
// Detect channel in topic
If System.Activity.ChannelId = "msteams"
  → Rich adaptive cards, SSO, file attachments
If System.Activity.ChannelId = "webchat"
  → Simpler cards, link-based auth, no file upload
If System.Activity.ChannelId = "directline"
  → JSON responses for custom rendering
```

---

## 6. Authentication

### SSO for Teams
```
Settings → Security → Authentication
  - Select: "Authenticate with Microsoft"
  - Scope: User.Read (minimum)
  - Teams SSO: Enabled (automatic, no login prompt)

In topics:
  System.User.DisplayName → User's name
  System.User.Email → User's email
  System.User.Id → AAD Object ID

// Use for personalization:
"Hi {System.User.DisplayName}, I can see you're in the {Department} team."
```

### Manual Auth (OAuth2)
```
For external systems:
  1. Register app in Azure AD / external IdP
  2. Add authentication node in topic
  3. On success: Use token in HTTP actions
  4. On failure: "Please try again or contact support"
```

---

## 7. Analytics & Optimization

### Key Metrics
```
Built-in analytics:
  - Resolution rate: % of sessions with "resolved" outcome
  - Escalation rate: % transferred to human agent
  - Abandon rate: % where user left mid-conversation
  - CSAT: Post-conversation satisfaction survey
  - Topic triggering: Which topics fire most, accuracy

Dashboard → Identify:
  1. High-volume topics → Optimize these first
  2. Low-resolution topics → Fix flow or add training phrases
  3. Frequent escalations → Add topic or expand knowledge
  4. Unmatched utterances → Create new topics or add to existing
```

### Continuous Improvement Loop
```
Weekly:
  1. Review unmatched utterances → Add trigger phrases or new topics
  2. Check escalation transcripts → Identify automatable patterns
  3. Review generative answer quality → Add/update knowledge sources
  
Monthly:
  4. Analyze CSAT trends → Correlate with topic changes
  5. Test new generative actions → A/B test vs classic topics
  6. Review security logs → Check for prompt injection attempts
```

---

## 8. Enterprise Patterns

### Escalation to Live Agent
```
// Omnichannel for Customer Service integration
Topic: Escalation
  1. "I'm connecting you with a human agent."
  2. Collect context: {Summary of conversation so far}
  3. Transfer to Agent node:
     - Queue: Based on topic/department
     - Context variables: CustomerName, IssueType, ConversationSummary
     - Wait message: "You're in queue. Estimated wait: {QueueTime}"
```

### Multi-Language
```
Settings → Languages → Add languages
  - Primary: English
  - Secondary: Spanish, French, German

Content localization:
  - Each topic can have language-specific responses
  - Generative answers: Separate knowledge sources per language
  - Entity recognition: Language-aware built-in entities
```

### Governance
```
Solution-aware development:
  - Build bots in Dev environment
  - Export as managed solution
  - Import to Test → Prod
  - Environment variables for:
    - API endpoints
    - Knowledge source URLs
    - Escalation queue IDs

Security:
  - DLP policies: Block sensitive connector use
  - Conversation logging: Enable for compliance
  - Content moderation: Configure sensitivity thresholds
```
