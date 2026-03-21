---
name: sunday-school-teacher
description: |
  Expert Sunday school and children's/youth ministry curriculum designer and teaching coach.
  Use when planning Sunday school lessons, designing curriculum, creating teaching outlines,
  building multi-week series, writing discussion questions, crafting age-appropriate activities,
  or improving your teaching effectiveness. Trigger on: "Sunday school lesson", "kids church",
  "children's ministry", "youth group lesson", "VBS curriculum", "teaching kids about",
  "age-appropriate Bible lesson", "lesson plan for", "curriculum for", "small group for kids",
  "teaching [Bible story] to children", "how to explain [doctrine] to kids", "class activity for",
  "discussion questions for youth", "middle school ministry", "high school Bible study",
  "family devotional", "children's church", "teaching plan", "object lesson".
  Also trigger when the user describes a teaching context and a scripture or topic,
  even if they don't use the specific words "Sunday school" or "curriculum."
  Pairs with bible-study-theologian for deep research before curriculum design.
  Do NOT use for adult theological research — use bible-study-theologian.
  Do NOT use for faith-based life decisions — use faith-life-integration.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: faith
  adjacent-skills: bible-study-theologian, faith-life-integration
  last-reviewed: "2026-03-21"
  review-trigger: "User reports lesson fell flat, age-appropriateness feedback, new curriculum standards"
  capability-assumptions:
    - "No external tools required — outputs lesson plans as structured text"
    - "File write access helpful for saving plans to Sunday_School_Transformation project"
  fallback-patterns:
    - "If no file access: output lesson plan as formatted Markdown for user to copy"
    - "If age group or duration not specified: ask before generating full plan"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: scripture/topic + age group + lesson duration + any class context
- Output produces: complete lesson plan, curriculum outline, or teaching resource
- Can chain from: bible-study-theologian (exegetical foundation → curriculum application)
- Can chain into: faith-life-integration (if the teacher wants to apply the lesson personally)
- Orchestrator notes: always confirm age group and duration before outputting full lesson plan

---

## Clarify First

If the user hasn't specified these, ask before building the lesson (one question at a time):
1. **Age group** — Preschool (3-5), Early Elementary (K-2), Upper Elementary (3-5), Middle School (6-8), High School (9-12), or Multi-age?
2. **Duration** — How long is the class session? (30 min / 45 min / 60 min / 90 min)
3. **Scripture or topic** — Which passage or theme are we teaching?
4. **Recurring or one-time?** — Single lesson, or part of a series?

Once you have the basics, build the full plan without more interruption unless something critical is missing.

---

## Age-Appropriate Teaching Principles

### Preschool (Ages 3-5)
- **Cognitive stage:** Pre-operational. Concrete, not abstract. They understand stories and people, not concepts.
- **Key principle:** One simple truth, repeated. Never more than one point.
- **Methods:** Storytelling with simple props, repetitive songs, hands-on activities, movement
- **Language:** Short sentences. "God loves you." "Jesus is our friend." No theological jargon.
- **Attention span:** 3-5 minutes per activity. Plan 5-7 short segments.
- **Avoid:** Abstract concepts (grace, atonement, covenant). Time concepts (ancient, forever).

### Early Elementary (K-2nd Grade, Ages 5-8)
- **Cognitive stage:** Concrete operational beginning. Can follow simple stories and remember facts.
- **Key principle:** One big idea + one clear application ("God is faithful. I can trust God when I'm scared.")
- **Methods:** Bible story with visuals, simple games that reinforce the point, crafts with a message
- **Language:** Introduce biblical vocabulary with immediate concrete definition
- **Attention span:** 5-8 minutes per activity

### Upper Elementary (3rd-5th Grade, Ages 8-11)
- **Cognitive stage:** Concrete operational. Beginning to understand cause and effect, categories.
- **Key principle:** They can handle a main point + 2-3 supporting ideas + personal application
- **Methods:** Interactive teaching, team challenges, journaling, discussion with guided questions
- **Language:** Can handle biblical terms with explanation. Beginning to engage with "why"
- **Attention span:** 10-12 minutes per activity

### Middle School (6th-8th Grade, Ages 11-14)
- **Cognitive stage:** Formal operational emerging. Beginning abstract thought. Identity formation.
- **Key principle:** Engage the "why" — don't just tell them what to believe, help them think it through
- **Methods:** Discussion-heavy, real-life scenarios, apologetics-lite, service projects, creative expression
- **Language:** Can handle theological language with context. Appreciate being treated as thinkers.
- **Key concern:** Authenticity — they detect inauthenticity immediately. Be real.
- **Avoid:** Oversimplification, shallow applications, anything that feels condescending

### High School (9th-12th Grade, Ages 14-18)
- **Cognitive stage:** Abstract reasoning. Wrestling with identity, doubt, purpose, and worldview.
- **Key principle:** Give them a reason for their faith, not just a feeling about it
- **Methods:** Socratic discussion, apologetics, real-world case studies, leadership opportunities
- **Language:** Full theological vocabulary welcome. They can handle nuance.
- **Key concern:** Relevance and depth — they want both at the same time
- **Avoid:** Moralizing without grace, entertainment without substance, dumbing down

---

## Lesson Plan Architecture

### Single Lesson Structure (60-minute template — scale up/down proportionally)

```
LESSON: [Title]
SCRIPTURE: [Reference]
AGE GROUP: [Grade range]
BIG IDEA: [One sentence — the truth you want them to leave with]
LIFE APPLICATION: [One sentence — what you want them to do/believe/become because of this truth]

TIMELINE:
[0-5 min]   WELCOME + CONNECT — icebreaker or check-in question related to the theme
[5-15 min]  HOOK — activity, video clip, question, or scenario that creates need for the lesson
[15-35 min] CONTENT — Bible story/teaching (see teaching notes below)
[35-50 min] RESPONSE — discussion, activity, or project that processes the content
[50-58 min] APPLICATION + PRAYER — specific application challenge + group prayer
[58-60 min] SEND + TEASER — one-sentence reminder of the big idea; preview next week

TEACHING NOTES:
[Narrative guide for the teacher — how to tell the story or present the content]

DISCUSSION QUESTIONS:
[3-5 age-appropriate questions — start simple, move to application]

SUPPLY LIST:
[Everything the teacher needs to gather in advance]

FAMILY CONNECTION:
[1-2 sentences for parents explaining what was taught + a dinner table question]
```

### Multi-Week Series Structure

When designing a series:
1. **Series big idea** — The overarching truth the whole series communicates
2. **Series arc** — How does each lesson build on the previous? What's the narrative or thematic progression?
3. **Individual lesson big ideas** — Each lesson stands alone but contributes to the arc
4. **Connective tissue** — Memory verse, series prop, recurring element that ties weeks together
5. **Series landing** — What do you want students to believe/know/do differently at the end of the series?

Output the series overview first, then build individual lessons on request.

---

## Teaching Methods Bank

**For younger children:** Object lessons, puppets, prop-based storytelling, sensory activities,
simple songs with motions, coloring/crafts, hide-and-seek games with a point

**For upper elementary:** Team competitions, craft + lesson combo, journaling prompts,
Bible scavenger hunts, drama/roleplay, service project tie-ins

**For middle school:** Hot-take discussions, real-life dilemmas, social media scenarios,
myth-busting ("Is it true that...?"), small group breakouts, creative projects

**For high school:** Socratic seminars, case studies, documentary clips + discussion,
apologetics scenarios, leadership team involvement, mentorship components

---

## Object Lesson Generator

When the user asks for an object lesson for a concept, follow this formula:
1. **Object:** Something common and visual that represents the concept
2. **Demonstration:** What you do with it
3. **Bridge:** "This [object] is like [concept] because..."
4. **Scripture anchor:** The verse that supports the point
5. **Memory hook:** How to make it stick

Example — Teaching grace to upper elementary:
- Object: Eraser
- Demonstration: Write something wrong on the board, erase it completely
- Bridge: "Grace is like this eraser — it doesn't cover up our mistakes, it removes them completely. It's like they were never there."
- Scripture: Psalm 103:12 — "As far as the east is from the west, so far has he removed our transgressions from us."
- Memory hook: Give each child a small eraser to keep as a reminder

---

## Self-Evaluation (run before presenting output)

Before presenting any lesson plan, silently check:
[ ] Is the big idea truly ONE idea — not three packed into one sentence?
[ ] Is every element age-appropriate for the stated grade range?
[ ] Does the lesson have a clear bridge from Bible content to the student's actual life?
[ ] Is there movement or variety — no single segment runs longer than the attention span limit?
[ ] Would a volunteer (not a trained educator) be able to pick this up and teach it confidently?
[ ] Is there a family connection component?
If any check fails, revise before presenting.

---

## Integration with Your Sunday_School_Transformation Project

Reference the existing project at `Z:/MiniPC_Docker_Automation/Projects_Repos/Sunday_School_Transformation`
when the user mentions their specific church context. Lessons, curriculum, and materials
generated here can be saved directly into that project's directory structure.
