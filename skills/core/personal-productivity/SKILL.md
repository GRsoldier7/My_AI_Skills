---
name: personal-productivity
description: |
  Personal productivity architect for high-output professionals juggling multiple domains.
  Use when managing time, designing routines, prioritizing work, setting goals, building
  systems for focus and execution, or feeling overwhelmed by competing priorities.

  EXPLICIT TRIGGER on: "productivity", "time management", "GTD", "routine", "morning routine",
  "daily schedule", "time blocking", "focus", "deep work", "prioritize", "overwhelmed",
  "too many things", "how to organize my day", "weekly review", "goal setting", "OKRs",
  "Eisenhower matrix", "Pomodoro", "energy management", "work-life balance", "burnout",
  "batch processing", "context switching", "habit", "system for getting things done",
  "planning my week", "planning my day", "todo system", "task management".

  Also trigger when the user describes feeling stretched across too many projects or
  struggling with execution despite having clear goals.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: knowledge-management, session-optimizer, entrepreneurial-os, faith-life-integration
  last-reviewed: "2026-03-21"
  review-trigger: "User reports system isn't working, new productivity research, role change"
  capability-assumptions:
    - "Text-based guidance — works with any task manager or calendar"
    - "No external tool integration required"
  fallback-patterns:
    - "If user has no system: start with simplest viable system, not the most complete"
    - "If user is overwhelmed: triage first, systematize later"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: productivity challenge, scheduling need, or system design request
- Output produces: time architecture, priority framework, routine design, or triage plan
- Can chain from: entrepreneurial-os (business goals → daily execution)
- Can chain into: knowledge-management (organize outputs), faith-life-integration (stewardship lens)
- Orchestrator notes: always assess current pain point before prescribing a system

---

## Priority Framework

### The Eisenhower Matrix — Applied
| | Urgent | Not Urgent |
|---|--------|------------|
| **Important** | DO NOW: client deliverable due today, production outage | SCHEDULE: strategic planning, skill building, health, relationships |
| **Not Important** | DELEGATE/TIMEBOX: most emails, Slack, "quick questions" | ELIMINATE: social media scrolling, unnecessary meetings, busywork |

**The trap:** Most people live in Urgent-Important and Urgent-Not-Important, neglecting
Not-Urgent-Important (the quadrant that builds your future). Schedule Q2 work like
appointments — it won't happen otherwise.

### Energy-Based Scheduling
Not all hours are equal. Map your work to your energy:
- **Peak energy (usually morning):** Deep work — coding, writing, strategy, creative thinking
- **Moderate energy (mid-day):** Collaborative work — meetings, client calls, code reviews
- **Low energy (late afternoon):** Administrative — email, invoicing, organizing, routine tasks

Protect your peak hours ruthlessly. A 2-hour deep work block at peak energy produces more
than 4 hours of fragmented work at low energy.

---

## Time Architecture

### The Ideal Week Template
Design your week before it happens:
```
Monday:    Planning + deep work (set the week's direction)
Tuesday:   Client/collaboration day (meetings, calls, reviews)
Wednesday: Deep work day (protect this — no meetings if possible)
Thursday:  Client/collaboration + admin catch-up
Friday:    Review + learning + project wrap-up
Weekend:   Rest, faith, family (guard this boundary)
```

Adapt this to your reality — the point isn't the specific layout but the intentional allocation.

### Daily Structure
```
[30 min]  Morning routine: review today's plan, top 3 priorities
[2-4 hr]  Deep work block 1 (most important task, no interruptions)
[30 min]  Break + email/Slack triage
[1-2 hr]  Meetings / collaborative work
[30 min]  Lunch (actual break, not desk lunch)
[2-3 hr]  Deep work block 2 or meetings
[30 min]  Daily shutdown: capture loose ends, plan tomorrow's top 3
```

### Time Blocking Rules
- **Block time for your priorities first**, then let reactive work fill the gaps
- **Batch similar tasks:** all emails at 10am and 3pm, all admin on Thursday afternoon
- **Buffer blocks:** leave 30-60 min unscheduled per day for overflow
- **Context-switch tax:** every switch costs 15-25 minutes of re-focus. Minimize switches.

---

## Task Management System

### The Minimum Viable System
You need exactly three lists:
1. **Today** — 3-5 tasks you will complete today (not 15)
2. **This Week** — everything committed for this week
3. **Backlog** — everything else, reviewed weekly

### Weekly Review (30-45 minutes, same time each week)
1. **Capture:** Empty your head — everything floating in your mind → backlog
2. **Review:** Go through each active project — what's the next action?
3. **Decide:** Pick your top priorities for next week
4. **Schedule:** Block time for the priorities
5. **Reflect:** What worked this week? What didn't? One adjustment for next week.

### The "Top 3" Rule
Each day has exactly 3 most important tasks. If you complete these 3 things and nothing
else, the day was a success. Everything else is bonus. This prevents the feeling of "I did
a lot but accomplished nothing."

---

## Focus and Deep Work

### Protecting Deep Work
- Close Slack, email, and notifications during deep work blocks
- Use a physical or digital "do not disturb" signal
- Start deep work with a clear intention: "In this block, I will [specific deliverable]"
- Set a timer — knowing the end time helps sustain focus

### Managing Interruptions
- **Urgent and important:** handle immediately, then return to deep work
- **Urgent but not important:** capture it, handle in your next admin block
- **Not urgent:** say "I'll get to that by [time]" and log it
- Train your environment: people adapt to your boundaries if you're consistent

### The 2-Minute Rule
If a task takes less than 2 minutes, do it immediately. Don't add it to a list —
the overhead of tracking it exceeds the time to do it.

---

## Multi-Domain Management

For someone managing consulting, faith/ministry, health, technical projects, and family:

### Domain Days vs Domain Blocks
- **Domain days:** dedicate entire days to one domain (Monday = consulting, Wednesday = product)
- **Domain blocks:** dedicate 2-3 hour blocks within a day to different domains
- Domain days reduce context-switching but aren't always realistic
- Domain blocks work better when you have daily obligations in multiple domains

### The Weekly Compass
At your weekly review, check each life domain:
- **Work/Consulting:** What's the most important deliverable this week?
- **Faith/Ministry:** Am I preparing for Sunday school? Personal study time scheduled?
- **Health:** Are my protocols on track? Workout scheduled?
- **Family/Relationships:** Quality time planned?
- **Business Building:** What moves the needle on my own ventures this week?
- **Learning/Growth:** What am I learning or building skill-wise?

If any domain has been neglected for 2+ weeks, it needs attention this week.

---

## Burnout Prevention

### Warning Signs
- Dreading work you used to enjoy
- Difficulty concentrating even on interesting tasks
- Irritability, cynicism, or emotional exhaustion
- Physical symptoms: poor sleep, headaches, constant fatigue
- Neglecting relationships, health, or faith

### Prevention Protocol
- **Sabbath rest:** one day per week with no work (non-negotiable — this is both biblical wisdom and productivity science)
- **Recovery rituals:** daily shutdown routine, weekend boundaries, quarterly breaks
- **Say no:** every yes is a no to something else. Protect your capacity.
- **Audit your commitments:** quarterly, review everything you've said yes to. Cut 20%.

---

## Self-Evaluation (run before presenting output)

Before presenting, silently check:
[ ] Am I prescribing a system that matches the user's current capacity, not an ideal?
[ ] Is the first step small and actionable (not "redesign your entire life")?
[ ] Have I addressed the specific pain point, not just given generic productivity advice?
[ ] Does the system account for multiple life domains, not just work?
[ ] Have I recommended rest and boundaries, not just optimization?
If any check fails, revise before presenting.
