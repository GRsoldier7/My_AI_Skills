---
name: skill-builder
description: |
  Genius-level meta-skill for designing, building, auditing, and improving other Agent Skills.
  Activates when the user wants to create a new skill, improve an existing SKILL.md, identify
  gaps in a skill library, audit a skill for quality, or produce a batch of skills for a domain.
  Trigger phrases: "build a skill", "create a skill for", "improve this skill", "audit this skill",
  "what skills are missing", "skill for X domain", "write a SKILL.md", "skill library gap".
  Uses a 5-module pipeline: Domain Intelligence → Capability Decomposition → Skill Architecture
  → Quality Evaluation (10-dimension rubric) → Continuous Improvement Protocol. Every skill
  produced meets the Agent Skills open standard and passes a minimum quality bar before output.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: prompt-amplifier, portable-ai-instructions, polychronos-team
  last-reviewed: "2026-03-15"
  review-trigger: "Agent Skills spec update, new Claude major version, 3+ user-reported quality failures"
  capability-assumptions:
    - "No external tools required beyond standard Claude Code tools"
  fallback-patterns:
    - "If tools unavailable: provide text-based guidance"
  degradation-mode: "graceful"
---

## Purpose and Scope

This skill builds other Skills. It is a structured creation, auditing, and improvement system for
the Agent Skills format. It does NOT write application code, answer domain questions directly, or
perform the work of the skills it produces. It does one thing: produce exceptional SKILL.md files.

Use this skill when you need to:
- Create a new skill for any domain from scratch
- Audit an existing SKILL.md against a quality rubric and get specific improvement recommendations
- Identify the highest-value gaps in the current skill library
- Produce a coordinated batch of skills for a new domain category
- Upgrade a skill when its domain evolves or the platform changes

Do NOT use when you just want to activate a skill and use it — load that skill directly instead.

---

## The 5-Module Pipeline

Every skill creation runs all five modules in sequence. Auditing runs Module 4 only.
Upgrading runs Modules 1, 3, and 4. Gap analysis runs a lightweight version of Module 1 across
the full library.

```
Module 1: Domain Intelligence Brief
       ↓
Module 2: Capability Decomposition Map
       ↓
Module 3: Skill Architecture (write the SKILL.md)
       ↓
Module 4: Quality Evaluation (10-dimension rubric)
       ↓
Module 5: Continuous Improvement Protocol
```

---

## Module 1 — Domain Intelligence Brief

Before writing a single line, answer all six questions. Do not skip or approximate.

**Question 1 — Expert delta:**
What do world-class practitioners in this domain know that merely competent ones don't?
List 3–5 specific things. If you cannot name them concretely, you are not ready to write the skill.

**Question 2 — Top failure modes:**
What are the top 3 ways this domain destroys results when handled naively?
Name them specifically. "Poor planning" is not an answer. "Using INNER JOIN on a table with NULL
foreign keys eliminates valid rows silently" is an answer.

**Question 3 — Domain vocabulary:**
What are the 5–10 terms, frameworks, or mental models specific to this domain that a skilled
practitioner uses fluently? These should appear naturally in the skill's content.

**Question 4 — Anti-pattern inventory:**
What approaches look correct but produce subtly wrong results? List at least 3.
These are the most valuable thing in any skill — they encode hard-won experience.

**Question 5 — Activation boundary:**
When should this skill NOT be used? What adjacent skill handles those cases instead?
If you cannot name a clear boundary, the skill's scope is too broad.

**Question 6 — Composability surface:**
What other skills does this one naturally hand off to? What skills hand off to this one?
Name them by slug (e.g., `database-design`, `security-hardening`).

Output: A Domain Intelligence Brief (written out inline before proceeding to Module 2).

---

## Module 2 — Capability Decomposition Map

Decompose the domain into three layers. Be specific. Avoid vague abstractions.

**Layer 1 — Core (the 20% that delivers 80% of value):**
The foundational knowledge that must be in every invocation of this skill.
Limit to 5–7 items. Each item should be actionable, not descriptive.

**Layer 2 — Advanced (what experts get right that others get wrong):**
The nuanced, non-obvious, experience-encoded knowledge.
This is what separates a good skill from an exceptional one.
Limit to 5–7 items.

**Layer 3 — Edge cases and constraints:**
Specific conditions that break the standard approach.
Named conditions, not generic warnings. Each edge case should have a named mitigation.

Output: A Capability Map with three populated layers before proceeding to Module 3.

---

## Module 3 — Skill Architecture

Write the SKILL.md using the canonical template. See
[references/skill-template.md](references/skill-template.md) for the full template.

**Hard constraints during writing:**

- SKILL.md body must be ≤500 lines. Move heavy reference material to `references/` files.
- Every line must earn its place. Cut anything that could be removed without loss.
- The description field is the most important field. See the description engineering rules below.
- Sections are not optional. All 9 canonical sections must be present. Omission requires
  written justification.
- Anti-patterns section must contain ≥3 named anti-patterns with explanation of why each is
  tempting and why it fails.
- Failure modes section must name specific failure states (not generic ones) with fallback guidance.
- Quality gates must be testable. "Good output" is not a quality gate. "The schema has no
  nullable foreign keys unless explicitly justified" is a quality gate.

**Description field engineering rules:**

The description is the entire discovery surface. Skills are selected by pure LLM reasoning
against this field. Engineer it for precision:

1. State what the skill does (functional description)
2. State when to use it (activation conditions)
3. Include 5–8 specific trigger phrases that should activate it
4. Include implicit trigger patterns (what users say when they need this but don't know the name)
5. Stay under 1024 characters
6. Test it: would this description fire on the 10 most common use cases? Would it misfire
   on 5 adjacent-but-different queries?

---

## Module 4 — Quality Evaluation (The 10-Dimension Rubric)

Score every dimension 1–5. A skill must score ≥4 on all dimensions and ≥3.5 average before
finalizing. Dimensions scoring <4 go back to the relevant module for specific revision.

See [references/quality-rubric.md](references/quality-rubric.md) for full scoring criteria.

**Quick reference — the 10 dimensions:**

| # | Dimension | What Fails at <4 |
|---|-----------|-----------------|
| 1 | Description precision | Misfires on wrong queries OR misses right ones |
| 2 | Domain depth | Tutorial-level content, novice examples |
| 3 | Signal density | Padding, vague platitudes, obvious statements |
| 4 | Anti-pattern coverage | Missing the top failure modes of the domain |
| 5 | Edge case handling | Only the happy path, no named boundary conditions |
| 6 | Composability | Doesn't know adjacent skills or when to hand off |
| 7 | Failure mode documentation | Generic "things may go wrong" instead of named failures |
| 8 | Progressive disclosure compliance | Over 500 lines OR heavy content not pushed to references/ |
| 9 | Future-proofing | Brittle version-specific syntax in the body (not references/) |
| 10 | Auditability | Missing metadata fields, no review trigger, no version |

**Scoring process:**
Score each dimension. Write one sentence of justification per dimension. For any dimension <4,
write specific revision instructions before proceeding. Do not finalize until all dimensions ≥4.

---

## Module 5 — Continuous Improvement Protocol

Every finalized skill must include:

**In metadata:**
- `version: "1.0"` (or current version)
- `last-reviewed: "YYYY-MM-DD"`
- `review-trigger: "<specific condition>"` — be precise. "API deprecation" is not precise.
  "GitHub Actions caching API v3 deprecation" is precise.

**At the end of the skill body:**
A brief "Improvement candidates" note listing 2–3 things that would make this skill better
but were excluded for scope/length reasons. This is the improvement backlog.

**In evals/evals.json:**
Add at least one test case with a prompt that should activate the skill and expected output
characteristics. See the existing evals.json for format.

---

## Operating Modes

### Creation Mode (default)
Run all 5 modules. Produce: Domain Intelligence Brief, Capability Map, finalized SKILL.md,
rubric scorecard, and improvement protocol notes. Ask at most 3 clarifying questions upfront.

### Audit Mode
Triggered by: "audit this skill", "score this skill", "review this SKILL.md"
Run Module 4 only on the provided skill. Output: dimensional scorecard with specific revision
instructions for every dimension scoring <4. Do not rewrite the skill unless asked.

### Upgrade Mode
Triggered by: "update this skill", "this skill is outdated", review-trigger condition fires
Re-run Modules 1, 3, and 4. Produce a diff-style description of what changed and why.
Bump the version number (minor if additions, major if restructure).

### Library Gap Analysis Mode
Triggered by: "what skills are missing", "what should I build next", "gaps in my library"
Analyze the full skill library. Score each domain against: coverage depth, usage frequency,
leverage value. Output a prioritized list of skills to build, with rationale for each.

### Batch Mode
Triggered by: "build skills for [category]", "create a full set of [domain] skills"
Run all 5 modules per skill. Ensure skills in the batch reference each other correctly in
their `adjacent-skills` fields. Output all skills in sequence with a coverage map at the end.

---

## Anti-Patterns

**1. The Description Placeholder**
Writing `description: Helps with X tasks.` — This will either never activate or activate on
everything. The description is the skill's entire discoverability surface. A vague description
means the skill is invisible. Spend as much time on the description as on any other section.

**2. The Tutorial Trap**
Writing content at the level of a beginner tutorial — what a function does, what a pattern is
named — instead of encoding expert judgment. Skills are for practitioners who know the basics.
The value is in the things that books don't teach: the edge cases, the failure modes, the
anti-patterns, the decision rules that take years to learn.

**3. The Mega-Prompt**
Trying to put everything into one 800-line SKILL.md. Progressive disclosure exists for a reason:
1,500+ tokens of overhead per activation. A monolithic skill bloats the context, degrades
performance on everything else in the session, and is harder to maintain. Use `references/` files.

**4. The False Anti-Pattern**
Writing anti-patterns that aren't actually tempting — things no one would actually do. The best
anti-patterns document exactly what smart people do before they know better. "Don't use SELECT *"
is obvious. "Using a UUID primary key without a covering index on your foreign-key table causes
silent full scans on every join" is an anti-pattern worth documenting.

**5. The Orphan Skill**
Building a skill with no `adjacent-skills` metadata and no composability section. Skills that
don't know what to hand off to trap users in the skill when they've reached the edge of its
domain. Always name the skill that handles what this one doesn't.

**6. The Set-and-Forget**
Publishing a skill with no `review-trigger` and no improvement notes. The Agent Skills ecosystem
evolves rapidly. A skill with no maintenance plan is technical debt. Every skill needs a specific
condition that triggers a review.

---

## Quality Gates (for the meta-skill's own outputs)

- All 5 modules produce written output before the SKILL.md is finalized
- The Domain Intelligence Brief answers all 6 questions with specific, non-generic answers
- The description field passes the 10 "should fire" / 5 "should not fire" test
- All 10 rubric dimensions score ≥4
- The SKILL.md body is ≤500 lines
- The metadata block is complete: all required fields populated
- At least one eval test case is added to evals.json

---

## Failure Modes and Fallbacks

**Failure: Domain is too broad ("build a Python skill")**
Mitigation: Narrow it using Module 2's three-layer decomposition. "Python" is a language, not a
domain. Ask: what specific workflow, pattern, or decision is this skill encoding? Split into
focused skills (e.g., `python-async-patterns`, `python-testing-patterns`) rather than building
one unfocused skill.

**Failure: Domain Intelligence Brief produces generic answers**
Mitigation: Each answer must pass the specificity test — could this answer appear in a beginner
tutorial? If yes, it's not specific enough. Force concrete examples, named failure modes, and
specific terminology before continuing.

**Failure: Rubric score repeatedly fails one dimension**
Mitigation: The dimension that keeps failing is the one the creator is avoiding. Name it
explicitly. If anti-patterns keep scoring <4, the domain hasn't been interrogated deeply enough
for real failure modes. Return to Module 1, Question 4.

**Failure: Output skill is over 500 lines**
Mitigation: Identify the 3 heaviest sections. Move them to `references/` files with clear
relative links. The SKILL.md body should be the operational guide; references hold the details.

---

## Composability

**Hands off to:**
- `prompt-amplifier` — when refining the description field for maximum activation precision
- `portable-ai-instructions` — when the skill needs platform-specific adaptation
- `polychronos-team` — when building a batch of 5+ skills that require coordinated architecture

**Receives from:**
- `polychronos-team` — when a multi-phase project identifies a domain gap that needs a new skill
- Any skill — when invoked in Audit Mode to evaluate an existing SKILL.md

---

## Improvement Candidates

- A formal description field testing harness (automated query-to-activation testing against
  the live skill selection mechanism)
- A `catalog-generate.sh` script that reads all metadata fields and rebuilds catalog.json
  automatically after any skill creation
- A dimension-9 (future-proofing) scanner that flags version-specific strings in SKILL.md bodies
