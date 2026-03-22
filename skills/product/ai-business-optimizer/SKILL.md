---
name: ai-business-optimizer
description: >
  Genius-level AI-native business operations covering AI audit methodology, process
  identification for automation, tool stack selection, agentic workflow design, ROI
  measurement, and building a business that runs on AI as its operating system. Use this
  skill whenever the user wants to automate their business processes with AI, build an
  AI-first operations stack, reduce manual work through LLM-powered automation, design
  agentic workflows, evaluate AI tools for ROI, or run their business more efficiently
  using AI as a force multiplier. Also trigger for AI integration into existing workflows,
  prompt engineering for business automation, AI tool stack comparison, building internal
  AI tools, or any request to "make my business run on AI."
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: product
  adjacent-skills: ai-agentic-specialist, entrepreneurial-os, micro-saas-builder, cloud-migration-playbook
  last-reviewed: "2026-03-15"
  review-trigger: "Major LLM capability release, new agentic framework reaches production-readiness, AI tool pricing shift, new automation platform emerges — review tool stack section every 3-6 months"
  capability-assumptions:
    - "Python/FastAPI/GCP stack available"
    - "Docker for containerization"
  fallback-patterns:
    - "If stack differs: ask user to confirm their stack before generating code"
  degradation-mode: "graceful"
---

# AI Business Optimizer — Savant-Level Skill

## Philosophy

AI-native business mastery = **process-first, tool-second** (understand the workflow before picking a tool), **ROI measurement** (AI spending without measurement is a hobby), **agentic > assistive** (don't chat — automate), and **the flywheel** (each AI implementation frees time to build the next AI implementation — compound leverage is the goal).

---

## 1. The AI Business Audit

### Process Inventory Framework
```
Step 1: Time audit (1 week)
  Track every task you do:
  - Task name
  - Time spent per week
  - Whether it requires judgment (hard to automate) or pattern following (easy)
  - Whether the output is text, data, or decision

Step 2: Classify each task
  Tier A (automate now): Repetitive, pattern-based, text output
    Examples: Drafting emails, summarizing documents, formatting data,
              generating reports, writing code, research synthesis

  Tier B (augment with AI): Requires judgment but AI accelerates
    Examples: Strategy planning, content creation, customer analysis,
              proposal writing, market research, decision analysis

  Tier C (human only): High-stakes, relationship, or novel judgment
    Examples: C-suite relationships, crisis management, novel product decisions,
              ethical trade-offs, complex negotiation

Step 3: ROI prioritization
  Priority = (Time saved/week × hourly rate × 52) / Implementation cost
  Example: 5 hrs/week × $150/hr × 52 = $39,000/year saved
           Implementation: 8 hours at $150/hr = $1,200
           ROI: 32.5x in year 1
```

### Business Function Automation Map
```
Marketing & Content:
  ✅ Blog post drafts → Claude + human edit
  ✅ Social media posts → AI generates; human approves
  ✅ Email newsletter → AI draft from bullet points
  ✅ SEO keyword research → Perplexity + Claude analysis
  ✅ Ad copy variants → AI generates 10; human picks 2
  ROI target: 80% reduction in content creation time

Sales & Business Development:
  ✅ Cold email personalization → Clay + Claude (1-click personalized outreach)
  ✅ CRM notes synthesis → AI summarizes call recording
  ✅ Proposal drafts → AI template + human customization
  ✅ Competitor research → Perplexity + Claude analysis
  ROI target: 3x outreach volume at same person-hours

Operations & Admin:
  ✅ Meeting notes + action items → AI transcript → structured output
  ✅ Document summarization → upload to Claude, get briefing
  ✅ Email triage → AI labels + draft responses for approval
  ✅ Invoice and contract review → AI flags unusual clauses
  ✅ Research synthesis → NotebookLM for uploaded documents
  ROI target: 10 hours/week recovered from administrative work

Product & Engineering:
  ✅ Code generation → Claude Code (this very skill set!)
  ✅ PR reviews → AI first pass; human final
  ✅ Documentation → AI draft from code; human validates
  ✅ Bug triage → AI categorizes and prioritizes
  ROI target: 2-3x output per engineer
```

---

## 2. Current AI Tool Landscape

> **Note:** AI tools, pricing, and capabilities change rapidly. The categories and selection criteria below are durable; specific tool names and prices are representative examples — validate against current offerings before committing. Review this section every 3-6 months.

### Recommended Stack by Function
```
Thinking & Strategy:
  Reasoning-optimized LLM (e.g., frontier model from Anthropic, OpenAI, or Google)
    → Deep reasoning, long documents, strategic analysis
  Real-time research tool with citations (e.g., Perplexity)
    → Up-to-date information retrieval beyond training cutoff
  Document-grounded research tool (e.g., NotebookLM or equivalent)
    → Deep research on uploaded documents (books, papers, transcripts)

Coding & Building:
  AI-native coding CLI or agent (e.g., Claude Code, Codex)
    → Full-stack development, architecture, debugging
  IDE with AI integration (e.g., Cursor, GitHub Copilot)
    → In-editor context-aware suggestions and completions
  UI prototyping tool (e.g., v0, Bolt)
    → Rapid UI from natural language before writing component code

Content & Writing:
  Frontier LLM (e.g., claude.ai) for long-form drafts and editing
  Structured content workflow tool for repeatable content pipelines
  Audio/video transcription + editing tool (e.g., Descript or equivalent)
  Short-form video repurposing tool for multi-platform distribution

Automation & Orchestration:
  Visual workflow automation platform (e.g., Make, Zapier)
    → No-code/low-code trigger-action automation across apps
  Self-hosted open-source automation (e.g., n8n)
    → Runs on your infrastructure; no per-operation pricing
  Data enrichment + personalized outreach platform (e.g., Clay)
    → Lead enrichment + AI-personalized messaging at scale

Research & Intelligence:
  Real-time web search with LLM synthesis
  LLM with persistent project/context management
  Semantic web search API for programmatic research

Voice & Meeting:
  AI transcription + meeting summary tool (e.g., Otter.ai, Fireflies)
    → Meeting notes, action items, searchable transcripts
  Voice synthesis tool for demos and content
```

### AI Stack Budget Tiers
```
// Prices below are representative ranges — validate current pricing before committing.

Bootstrapper (~$50-150/month):
  Frontier LLM subscription tier (~$15-25/mo)
  Real-time research tool (~$15-25/mo)
  Workflow automation starter plan (~$10-20/mo)
  ROI: 20-30 hours/week recovered if used systematically

Growth Stage (~$200-500/month):
  All bootstrapper tools +
  AI coding tool subscription (~$15-25/mo)
  Data enrichment + outreach platform starter tier (~$100-200/mo)
  Content/media production tool (~$20-50/mo)
  ROI: 40-60 hours/week recovered; 3x content output

Scale (~$500-2K/month):
  All growth tools +
  LLM Teams/API access for custom workflows
  Self-hosted automation (infrastructure cost only)
  Custom agentic workflows via LLM API
  ROI: Entire departments automated; leverage impossible without AI
```

---

## 3. Agentic Workflow Design

### When to Use Agentic vs. Assistive
```
Assistive (you are in the loop):
  Use when: Output quality needs human judgment; stakes are high
  Pattern: You → AI → You review → Output
  Examples: Strategic writing, customer communications, complex analysis

Agentic (AI runs the process):
  Use when: Process is repeatable; errors are recoverable; ROI justifies setup
  Pattern: Trigger → AI Agent → Output (human reviews exceptions only)
  Examples: Content repurposing, data processing, lead enrichment, reporting

Fully automated (set and forget):
  Use when: Process is deterministic; errors are minimal risk
  Pattern: Trigger → Process → Output (no human in loop)
  Examples: Data sync, scheduled reports, form routing, monitoring alerts
```

### Building an Agentic Workflow (LLM API — Anthropic SDK Pattern)
```python
# Pattern: Multi-step agent with tools
# Note: Replace MODEL_NAME with current flagship model from your chosen provider.
# For Anthropic, check https://docs.anthropic.com/en/docs/about-claude/models
# for the latest recommended model ID before deploying.
from anthropic import Anthropic

MODEL_NAME = "claude-opus-4-6"  # Replace with current recommended model

client = Anthropic()

# Tool definitions for the agent
tools = [
    {
        "name": "web_search",
        "description": "Search the web for current information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "write_to_storage",
        "description": "Write structured content to your data store",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"},
                "category": {"type": "string"}
            },
            "required": ["title", "content"]
        }
    }
]

# Example: Competitive intelligence agent
def run_competitive_intelligence(competitor_name: str):
    messages = [
        {
            "role": "user",
            "content": f"""Research {competitor_name} and produce a competitive
            intelligence briefing covering: recent news, product updates,
            pricing changes, customer sentiment, and strategic positioning.
            Save the briefing to storage."""
        }
    ]

    while True:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            break

        # Process tool calls and continue the loop
        tool_results = process_tool_calls(response.content)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return response.content
```

### Make.com Workflow Patterns
```
Pattern 1: Content Repurposing Machine
  Trigger: New blog post published (RSS or webhook)
  → HTTP: Fetch full article content
  → Claude API: Generate LinkedIn post (3 variations)
  → Claude API: Generate 5 tweets from the article
  → Claude API: Generate email newsletter section
  → Airtable: Store all variations for review
  → Typefully API: Schedule approved posts
  Time saved: 2-3 hours per article → 10 minutes to review/approve

Pattern 2: Lead Intelligence on Demand
  Trigger: New lead added to CRM (HubSpot webhook)
  → Clay API: Enrich lead (company, LinkedIn, funding stage)
  → Claude API: Generate personalized outreach angle based on enriched data
  → Claude API: Draft personalized cold email
  → CRM: Update lead record with enrichment + draft email
  Time saved: 30 min/lead → 2 min to review

Pattern 3: Weekly Business Intelligence Report
  Trigger: Monday 8 AM (scheduled)
  → Multiple HTTP calls: Gather data from Stripe (revenue), PostHog (product),
    Google Analytics (traffic), Customer.io (email metrics)
  → Claude API: Analyze all data and write executive summary with insights
  → Format: Markdown → PDF or Notion page
  → Notify: Send to email + Slack
  Time saved: 2-3 hours/week → 5 minutes to read the summary
```

---

## 4. ROI Measurement Framework

### AI Investment Tracking
```
Monthly AI ROI report (fill in your actual tool costs — prices change; validate current pricing):

Tool/Workflow           | Monthly Cost | Hours Saved | Hourly Rate | Annual Value | ROI
──────────────────────────────────────────────────────────────────────────────────────
LLM subscription        | $_____       | ____h       | $150        | $_______     | ___x
Research tool           | $_____       | ____h       | $150        | $_______     | ___x
Workflow automation     | $_____       | ____h       | $150        | $_______     | ___x
Outreach/enrichment     | $_____       | ____h       | $150        | $_______     | ___x
──────────────────────────────────────────────────────────────────────────────────────
Total                   | $_____/mo    | ____h       |             | $_______     | ___x

// Illustrative example at $150/hr: A $20/mo tool saving 25h/week = $45,000 annual value = 2,250x ROI.
// Rule: Any tool with ROI < 10x should be replaced or eliminated.
// Any workflow saving >10h/week that isn't automated yet should be.
```

---

## 5. Prompt Engineering for Business Automation

### System Prompt Templates for Common Business Tasks
```
Email Response Automation:
  system: """You are the AI assistant for [Business Name], responding on behalf of [Name].
  Your job is to draft professional, warm email responses.
  Style: [Concise / Detailed]. Tone: [Professional / Casual].
  Always: Acknowledge the sender's point; provide value; clear next step.
  Never: Commit to timelines; share confidential info; be defensive.
  Draft a response to the following email:"""

Competitive Analysis:
  system: """You are a competitive intelligence analyst.
  For the company provided, analyze:
  1. Core value proposition and target market
  2. Pricing model and positioning
  3. Key strengths vs. [Your Company]
  4. Key weaknesses and opportunities for [Your Company]
  5. Recent strategic moves (last 90 days)
  Output: Structured briefing in markdown. Be direct and specific."""

Content Creation:
  system: """You are a content strategist and writer for [Name], a [role].
  Audience: [specific ICP description]
  Voice: [specific tone descriptors]
  Topics: [core content pillars]
  Format for LinkedIn: First 2 lines must be a hook. Short paragraphs.
  No buzzwords. Specific and concrete. End with a question.
  Write the following:"""
```

---

## Anti-Patterns

**Anti-Pattern 1: Tool Accumulation Without System Design**
Signing up for 20 AI tools because they seem useful. No integration between them. Each one requires manual context transfer. The "productivity stack" becomes another source of cognitive load rather than leverage.
Fix: Map your core workflows first. Then ask: which ONE tool would reduce the most manual work in this workflow? Add tools only when a specific workflow bottleneck requires it. Every tool in your stack should have a documented workflow it serves.

**Anti-Pattern 2: Automating Before Standardizing**
Automating a messy, inconsistent process. If the human-executed process produces inconsistent outputs, the automated version will produce consistently bad outputs at high speed.
Fix: Standardize before automating. Run the process manually 10 times with a documented SOP. When the process produces consistent outputs manually, then automate it. The automation will be more reliable and easier to debug.

**Anti-Pattern 3: AI as a Replacement for Thinking**
Using AI to generate strategy, make decisions, and produce content without human review or original thinking. The output sounds good but has no genuine insight or competitive differentiation — because it's the same output any competitor with ChatGPT could produce.
Fix: AI should amplify your thinking, not replace it. The best AI-assisted outputs start with your unique perspective, data, or framework — then use AI to structure, polish, and distribute. Original insight is your moat; AI is the leverage.

---

## Quality Gates

- [ ] AI audit completed: all recurring tasks classified into Tier A/B/C (automate/augment/human)
- [ ] ROI tracking in place: monthly report on hours saved per tool vs. cost
- [ ] Top 3 highest-ROI automations identified and implemented
- [ ] Agentic workflows running for at least 2 repetitive business processes
- [ ] AI tool stack reviewed quarterly: remove tools with ROI < 10x
- [ ] All AI-assisted content reviewed by human before publishing (quality gate on outputs)

---

## Failure Modes and Fallbacks

**Failure: Automated workflow producing low-quality outputs that require more time to fix than doing manually**
Detection: Time spent reviewing and correcting AI outputs exceeds time saved by automation.
Fallback: Negative-ROI automation is usually a prompt engineering problem. Fix: (1) Add explicit output format instructions and examples to system prompts, (2) Narrow the task scope — one specific job per prompt is better than multi-task prompts, (3) Add a "confidence signal" to the output — ask the AI to flag when it's uncertain, (4) Consider if this task should remain in Tier B (augment) not Tier A (automate) — some judgment-heavy tasks shouldn't be fully automated yet.

**Failure: Critical business information locked in AI tools with no backup**
Detection: Changing AI tool requires rebuilding all prompts, workflows, and stored context from scratch.
Fallback: AI tool lock-in is a real operational risk. Mitigation: (1) Keep all system prompts and prompt libraries in version-controlled documents (Notion, GitHub), not just in the tool, (2) Document all Make/n8n workflows with screenshots and descriptions, (3) Keep all data in your own databases, not AI tool storage, (4) Review quarterly: if this tool disappeared, how long would it take to rebuild? > 1 week = unacceptable dependency risk.

---

## Composability

**Hands off to:**
- `ai-agentic-specialist` — deep agentic framework design and bleeding-edge AI tool evaluation
- `cloud-migration-playbook` — self-hosted AI tools (n8n, open-source LLMs) require infrastructure

**Receives from:**
- `entrepreneurial-os` — stage determines which AI investments are worth making now
- `micro-saas-builder` — the AI operations stack powers the solo SaaS business
