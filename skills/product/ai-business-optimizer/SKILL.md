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
  review-trigger: "Claude/GPT major capability update, new agentic framework release, AI tool pricing shift, new automation platform breakthrough"
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

## 2. The 2025 AI Tool Stack

### Recommended Stack by Function
```
Thinking & Strategy:
  Claude Opus 4.6 (claude.ai/claude.ai Teams)
    → Deep reasoning, long documents, strategic analysis
  Perplexity Pro
    → Real-time research with citations
  NotebookLM (Google, free)
    → Deep research on uploaded documents (books, papers, transcripts)

Coding & Building:
  Claude Code (this system)
    → Full-stack development, architecture, debugging
  Cursor IDE
    → IDE-integrated coding with context-aware suggestions
  v0 (Vercel)
    → UI prototyping from natural language

Content & Writing:
  Claude (claude.ai) for long-form drafts and editing
  Copy.ai or Jasper for structured content workflows
  Descript for audio/video content (AI transcription + editing)
  Opus Clip for short-form video repurposing

Automation & Orchestration:
  Make (formerly Integromat)
    → Visual workflow automation; better than Zapier for complex flows
  n8n (self-hosted option)
    → Open-source, runs on your infrastructure
  Clay
    → Data enrichment + personalized outreach at scale

Research & Intelligence:
  Perplexity Pro (real-time)
  Claude Projects (persistent context)
  Exa.ai (semantic web search API)

Voice & Meeting:
  Otter.ai or Fireflies.ai
    → Meeting transcription + summary + action items
  ElevenLabs
    → Voice synthesis for content/demos
```

### AI Stack Budget Tiers
```
Bootstrapper ($50-100/month):
  Claude.ai Pro ($20/mo)
  Perplexity Pro ($20/mo)
  Make (starter $10/mo)
  Total: ~$50/mo
  ROI: 20-30 hours/week recovered if used systematically

Growth Stage ($200-500/month):
  All bootstrapper tools +
  Claude Code (session-based) or Cursor Pro ($20/mo)
  Clay (starter $149/mo)
  Descript (creator $24/mo)
  Total: ~$250/mo
  ROI: 40-60 hours/week recovered; 3x content output

Scale ($500-2K/month):
  All growth tools +
  Claude Teams or API access
  n8n (self-hosted for complex automations)
  Custom agentic workflows via Claude API
  Total: ~$800-1,500/mo
  ROI: Entire departments automated; new leverage impossible without AI
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

### Building an Agentic Workflow (Claude API)
```python
# Pattern: Multi-step agent with tools
from anthropic import Anthropic

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
        "name": "write_to_notion",
        "description": "Write structured content to Notion database",
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
            Save the briefing to Notion."""
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
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
Monthly AI ROI report:

Tool/Workflow        | Monthly Cost | Hours Saved | Hourly Rate | Annual Value | ROI
─────────────────────────────────────────────────────────────────────────────────────
Claude Pro           | $20          | 25h         | $150        | $45,000      | 2,250x
Perplexity Pro       | $20          | 5h          | $150        | $9,000       | 450x
Make (automation)    | $30          | 15h         | $150        | $27,000      | 900x
Clay (outreach)      | $149         | 8h          | $150        | $14,400      | 97x
─────────────────────────────────────────────────────────────────────────────────────
Total                | $219/mo      | 53h         |             | $95,400      | 436x

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
