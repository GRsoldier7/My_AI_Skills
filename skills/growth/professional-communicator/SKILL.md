---
name: professional-communicator
description: |
  Expert professional communication coach. Use when writing emails, preparing presentations,
  drafting executive summaries, communicating with clients, writing documentation, or any
  professional writing that needs to be clear, persuasive, and appropriate to its audience.

  EXPLICIT TRIGGER on: "write an email", "draft a message", "presentation", "executive summary",
  "how to say this professionally", "communicate this to", "client email", "status update",
  "proposal email", "follow up email", "difficult conversation", "bad news email",
  "persuasive writing", "stakeholder communication", "meeting agenda", "meeting recap",
  "slide deck", "pitch", "elevator pitch", "LinkedIn post", "professional tone",
  "how to phrase this", "rewrite this", "make this more professional".

  Also trigger when the user drafts a message and asks for feedback or improvement.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: growth
  adjacent-skills: consulting-operations, sales-closer, personal-brand-builder, content-marketing-machine
  last-reviewed: "2026-03-21"
  review-trigger: "User reports communication fell flat, new communication context needed"
  capability-assumptions:
    - "Text-based output — produces written communication for any platform"
    - "No external tools required"
  fallback-patterns:
    - "If audience is unclear: ask before drafting"
    - "If high-stakes communication: recommend review by a trusted colleague before sending"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: communication need, draft to improve, or audience + message to craft
- Output produces: polished email, presentation outline, executive summary, or communication plan
- Can chain from: consulting-operations (client communication), data-analytics-engine (data → narrative)
- Can chain into: personal-brand-builder (public communication), sales-closer (persuasive outreach)
- Orchestrator notes: always confirm audience and purpose before drafting

---

## Communication Principles

### 1. Audience First
Before writing anything, answer:
- **Who** is reading this? (executive, peer, client, technical team)
- **What do they care about?** (results, timeline, cost, technical detail)
- **What do they need to do** after reading? (approve, act, acknowledge, decide)
- **What's their context?** (busy executive = short; technical reviewer = detailed)

### 2. Lead with the Point
Put the conclusion, request, or key information in the first sentence — not buried in
paragraph three. Busy readers may only read the first few lines.

### 3. One Message Per Communication
If you have three different topics, send three messages. Mixed messages get partial responses.

### 4. Make the Ask Explicit
Don't hint. State exactly what you need: "I need your approval by Friday" not
"It would be great if we could move forward on this soon."

---

## Email Templates

### Client Status Update
```
Subject: [Project Name] — Week [N] Update

Hi [Name],

Quick update on [project]:

COMPLETED:
- [deliverable 1 — with impact/result if available]
- [deliverable 2]

IN PROGRESS:
- [work item — expected completion date]

NEED FROM YOU:
- [specific request with deadline]

Next week we'll focus on [upcoming milestone]. Let me know if you
have questions.

Best,
[Your name]
```

### Delivering Bad News
```
Subject: [Project Name] — Timeline Update

Hi [Name],

I want to flag a timeline change on [project].

WHAT HAPPENED: [brief, factual explanation — no blame]
IMPACT: [what this means — delayed by X days, scope change, etc.]
WHAT WE'RE DOING: [corrective action already underway]
REVISED TIMELINE: [new date with confidence level]

I take responsibility for [relevant part]. Here's what we'll do
differently going forward: [prevention measure].

I'd like to discuss this on our next call [or: can we find 15 minutes
this week?].

[Your name]
```

### Cold Outreach / Introduction
```
Subject: [Specific value proposition — not "Quick Question"]

Hi [Name],

I noticed [specific observation about their company/role — proves you
did research]. [One sentence connecting their challenge to your expertise.]

I help [type of company] [specific result] through [your approach].
[One concrete example or metric.]

Would you be open to a 15-minute call to explore whether this could
help [their specific situation]? I'm available [two specific times].

Best,
[Your name]
[One-line credibility: title, company, or relevant achievement]
```

### Following Up (Without Being Annoying)
```
Subject: Re: [Original Subject]

Hi [Name],

Following up on my [email/proposal] from [date]. I know things get
busy — just want to make sure this didn't get lost.

[One sentence restating the key value or question.]

Would [specific date/time] work for a quick chat? Happy to work
around your schedule.

[Your name]
```

---

## Presentation Structure

### The Pyramid Principle
Structure any presentation or document top-down:
1. **Start with the answer/recommendation** — don't make people wait
2. **Support with 2-3 key arguments** — each independently convincing
3. **Back each argument with evidence** — data, examples, logic
4. **Appendix for detail** — available if questioned, not presented unless needed

### Slide Deck Rules
- **One idea per slide** — if you need two points, use two slides
- **Title = insight** — "Customer churn increased 15%" not "Churn Analysis"
- **Minimal text** — slides support your speaking, they don't replace it
- **6 words per bullet, 6 bullets max** — if you must use bullets at all
- **Full-bleed visuals** — one compelling chart beats ten bullet points
- **Consistent design** — same fonts, colors, layouts throughout

### Meeting Agenda Template
```
MEETING: [Purpose — one phrase]
DATE/TIME: [when] | DURATION: [length]
ATTENDEES: [names and roles]

OBJECTIVES:
1. [Specific outcome — "Decide on X", "Align on Y", "Review Z"]

AGENDA:
[5 min]  Context setting
[15 min] Topic 1: [description] — Led by [name]
[15 min] Topic 2: [description] — Led by [name]
[10 min] Decisions and action items
[5 min]  Next steps

PRE-READ: [link to any materials to review before the meeting]
```

---

## Tone Calibration

| Audience | Tone | Example |
|----------|------|---------|
| C-suite / Executive | Direct, outcome-focused, concise | "This will save $200K annually. I recommend we proceed." |
| Peer / Colleague | Collaborative, clear, friendly | "I've been thinking about this — here's what I've got so far." |
| Client (new) | Professional, warm, value-forward | "Thank you for the opportunity. Here's how we can help." |
| Client (established) | Direct, efficient, trusted advisor | "Quick flag on this — here's what I'd recommend." |
| Technical team | Precise, detailed, assumption-free | "The API returns 500 when the token expires. Root cause: ..." |

### Adjusting Formality
- **More formal:** "I would appreciate your review" / "Please advise"
- **Less formal:** "Let me know what you think" / "Thoughts?"
- **Match the recipient's tone** from their last message — mirror their register

---

## Self-Evaluation (run before presenting output)

Before presenting any communication, silently check:
[ ] Is the purpose clear in the first 1-2 sentences?
[ ] Is the ask explicit — does the reader know exactly what to do next?
[ ] Is the tone appropriate for the audience?
[ ] Is it concise — could any sentence be removed without losing meaning?
[ ] Would I be comfortable if this were forwarded to someone else?
If any check fails, revise before presenting.
