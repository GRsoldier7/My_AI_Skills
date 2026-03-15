# Canonical SKILL.md Template

This is the master template for every skill produced by the skill-builder meta-skill.
All 9 sections are required. Omission requires written justification in the skill itself.
SKILL.md body must stay ≤500 lines. Heavy content goes in references/ with relative links.

---

```markdown
---
name: <kebab-case-name>
description: |
  <ENGINEERED FOR PRECISION — see description engineering guide below>
  Functional: what the skill does.
  Activation: when to use it.
  Triggers: specific phrases that should activate it.
  Implicit: what users say when they need this but don't know the name.
  Max 1024 characters.
compatibility: <only include if required — e.g., "Requires network access to GitHub API">
metadata:
  author: <author-slug>
  version: "1.0"
  domain-category: <core|strategy|product|engineering|microsoft|custom>
  adjacent-skills: <comma-separated skill slugs>
  last-reviewed: "<YYYY-MM-DD>"
  review-trigger: "<specific condition that should trigger a review>"
allowed-tools: <only if required — space-delimited>
---

## Purpose and Scope

One paragraph: what this skill does. What it does NOT do. When to use it vs. the adjacent
alternative. The activation boundary should be sharp enough that a user can decide in 5 seconds
whether to use this skill or a different one.

---

## Section 1 — Core Knowledge

The 20% that delivers 80% of value. Compressed, high-signal, non-obvious.
This is what a practitioner needs before anything else. Not definitions. Not overviews.
The first things an expert would say to a competent practitioner who needs to get this right.

### Key Principles
<3–7 actionable principles. Each should encode judgment, not just describe a concept.>

### Decision Framework
<When to use what. Structured decision logic with named conditions and named choices.>

---

## Section 2 — Advanced Patterns

What experts get right that practitioners with 1–2 years of experience get wrong.
Non-obvious. Experience-encoded. The things that books don't teach.

### Pattern 1: <name>
<Concrete explanation with a realistic example.>

### Pattern 2: <name>
<Concrete explanation with a realistic example.>

### Pattern 3: <name>
<For large domains, move additional patterns to references/advanced-patterns.md>

---

## Section 3 — Standard Workflow

Step-by-step for the most common case. Be specific. Include decision points.
Not pseudocode — actual guidance for the model to follow.

1. <First action>
2. <Second action — include what to check before proceeding>
3. <Third action>
...

---

## Section 4 — Edge Cases

Specific conditions that break the standard workflow. Name the condition. Name the mitigation.
"Handle exceptions appropriately" is not an edge case.

**Edge Case 1: <named condition>**
<Why it breaks the standard workflow + specific mitigation>

**Edge Case 2: <named condition>**
<Why it breaks the standard workflow + specific mitigation>

**Edge Case 3: <named condition>**
<Why it breaks the standard workflow + specific mitigation>

---

## Section 5 — Anti-Patterns

What NOT to do. Why it's tempting. Why it fails. What to do instead.
These encode the most valuable lessons in the skill — hard-won experience.

**Anti-Pattern 1: <name>**
Temptation: <why smart people do this>
Failure: <what goes wrong, specifically>
Instead: <the correct approach>

**Anti-Pattern 2: <name>**
Temptation: <why smart people do this>
Failure: <what goes wrong, specifically>
Instead: <the correct approach>

**Anti-Pattern 3: <name>**
Temptation: <why smart people do this>
Failure: <what goes wrong, specifically>
Instead: <the correct approach>

---

## Section 6 — Quality Gates

How to know this skill produced good output. Specific. Testable. Binary where possible.
"Good output" is not a quality gate. A quality gate has a clear pass/fail condition.

- [ ] <Gate 1: specific testable condition>
- [ ] <Gate 2: specific testable condition>
- [ ] <Gate 3: specific testable condition>
- [ ] <Gate 4: specific testable condition>

---

## Section 7 — Failure Modes and Fallbacks

Named failure states with detection signals and specific recovery paths.
Generic "things may go wrong" is not a failure mode.

**Failure 1: <named failure state>**
Detection: <specific signal that indicates this failure>
Fallback: <specific recovery action>

**Failure 2: <named failure state>**
Detection: <specific signal that indicates this failure>
Fallback: <specific recovery action>

---

## Section 8 — Composability

Which skills this one hands off to and when. Which skills hand off to this one.
This treats the library as a network and prevents orphan skills.

**Hands off to:**
- `<skill-slug>` — <specific condition that triggers the handoff>
- `<skill-slug>` — <specific condition that triggers the handoff>

**Receives from:**
- `<skill-slug>` — <specific condition where that skill sends work here>

---

## Section 9 — Improvement Candidates

2–3 things that would make this skill better but were excluded for scope or length reasons.
This is the improvement backlog. Review it at the next review cycle.

- <Improvement 1>
- <Improvement 2>
- <Improvement 3>
```

---

## Description Field Engineering Guide

The description is the most important field. It is the entire discovery surface.

### Structure
```
Functional clause: "[Skill name] does X, Y, and Z."
Activation clause: "Use when [specific conditions]."
Trigger phrases: "Trigger phrases: [phrase 1], [phrase 2], [phrase 3], ..."
Implicit patterns: "Also activates when user [says/asks/mentions] [implicit pattern]."
```

### Length
Target 200–600 characters for most skills. Max 1024.
Shorter is better if precision is maintained.

### Testing the Description
Before finalizing, test against:

**Should fire (representative use cases — all 10 should fire):**
1. The most common explicit invocation
2. The second most common explicit invocation
3–7. Varied phrasings of the core use case
8–9. Implicit phrasings (user doesn't know the skill name)
10. An adjacent-but-different case that should NOT fire (if it fires, description is too broad)

**Should NOT fire (adjacent queries — none of these should fire):**
1. A query that belongs to the closest adjacent skill
2. A query that is superficially similar but about a different domain
3. A query that is completely unrelated
4–5. Edge cases that should go to the adjacent skill named in composability

---

## Frontmatter Completeness Checklist

- [ ] `name`: kebab-case, matches directory name, ≤64 chars
- [ ] `description`: ≥200 chars, ≤1024 chars, passes 10/10 should-fire test
- [ ] `metadata.author`: populated
- [ ] `metadata.version`: semantic version string (e.g., "1.0")
- [ ] `metadata.domain-category`: one of the valid categories
- [ ] `metadata.adjacent-skills`: comma-separated slugs or "none"
- [ ] `metadata.last-reviewed`: ISO date YYYY-MM-DD
- [ ] `metadata.review-trigger`: specific condition (not generic)
- [ ] `compatibility`: omit unless required
- [ ] `allowed-tools`: omit unless required

---

## Section Completeness Checklist

- [ ] Purpose and Scope: sharp activation boundary, states what it does NOT cover
- [ ] Section 1 Core Knowledge: 3–7 principles, decision framework present
- [ ] Section 2 Advanced Patterns: ≥3 patterns, genuinely non-obvious
- [ ] Section 3 Standard Workflow: numbered steps, decision points named
- [ ] Section 4 Edge Cases: ≥3 named conditions with specific mitigations
- [ ] Section 5 Anti-Patterns: ≥3 anti-patterns with temptation + failure + instead
- [ ] Section 6 Quality Gates: ≥4 testable binary conditions
- [ ] Section 7 Failure Modes: ≥2 named failures with detection + fallback
- [ ] Section 8 Composability: hands-off-to AND receives-from both populated
- [ ] Section 9 Improvement Candidates: 2–3 backlog items
- [ ] Total body length: ≤500 lines
