# Skill Quality Rubric — 10-Dimension Scoring System

Use this rubric to evaluate any SKILL.md before finalizing it. Score each dimension 1–5.
Minimum passing score: ≥4 on all dimensions, ≥3.5 average.
Dimensions scoring <4 require specific revision before the skill is finalized.

---

## Scoring Scale

| Score | Meaning |
|-------|---------|
| 5 | Exceptional — sets the standard, no improvement needed |
| 4 | Passing — meets production requirements, minor polish possible |
| 3 | Marginal — present but insufficient; specific revision required |
| 2 | Weak — exists in name only; needs substantial rework |
| 1 | Missing or broken — not present or actively harmful |

---

## Dimension 1 — Description Precision

**What it measures:** Whether the `description` field activates the skill on the right queries
and does not activate it on the wrong ones.

**Why it matters:** Skill selection is pure LLM reasoning against the description field.
A weak description means the skill is either invisible or fires indiscriminately.

| Score | Criteria |
|-------|---------|
| 5 | Fires on 10/10 representative queries; no misfires on 5 adjacent queries; includes trigger phrases and implicit patterns; under 1024 chars |
| 4 | Fires on 9/10 representative queries; 0–1 misfire; includes functional + activation language |
| 3 | Fires on 7–8/10; 2–3 misfires OR description is too generic; trigger phrases vague |
| 2 | Fires on <7/10; description is a single vague sentence OR over-broad |
| 1 | Description missing, empty, or "Helps with X" pattern |

**Revision trigger:** Any misfire on adjacent queries OR <8/10 on representative queries.
**Revision instruction:** List the 10 test queries, show which fail, rewrite the description to
fix failures without losing correct activations.

---

## Dimension 2 — Domain Depth

**What it measures:** Whether the skill encodes expert-level knowledge, not tutorial-level content.

**Why it matters:** Skills are used by practitioners who already know the basics. The value
is in what they don't know — the nuanced judgment, the non-obvious patterns, the things that
take years to learn.

| Score | Criteria |
|-------|---------|
| 5 | Content that only domain experts produce; non-obvious decision rules; named failure modes from real experience |
| 4 | Clearly above tutorial level; at least one advanced section; content a junior dev would not produce |
| 3 | Mix of obvious and advanced content; could be mistaken for a good tutorial |
| 2 | Predominantly tutorial-level; "here is what X is" rather than "here is how to judge when X is right" |
| 1 | Trivially google-able; nothing that requires domain expertise |

**Revision trigger:** Content a beginner tutorial would cover.
**Revision instruction:** Return to Module 1, Question 1. Name 3 specific things experts know
that novices don't. Rewrite the skill to foreground those 3 things.

---

## Dimension 3 — Signal Density

**What it measures:** The ratio of useful information to total words. No padding.

**Why it matters:** Context window is finite. Every token of padding is a token stolen from
the model's ability to reason about the actual task.

| Score | Criteria |
|-------|---------|
| 5 | Every sentence contains non-obvious information; zero filler; would lose value if shortened |
| 4 | Mostly high-signal; 1–2 sentences that could be trimmed; no significant padding |
| 3 | Noticeable filler; vague platitudes present (e.g., "it is important to consider"); 10–20% trimmable |
| 2 | Heavy padding; repetitive; states the obvious; >20% trimmable without information loss |
| 1 | Predominantly vague; mostly platitudes and general advice anyone would give |

**Revision trigger:** Any sentence that could appear in a generic overview article.
**Revision instruction:** Remove every sentence that could be true of any similar skill. What
remains must be specific to this domain.

---

## Dimension 4 — Anti-Pattern Coverage

**What it measures:** Whether the skill documents the top failure modes of the domain explicitly,
with explanation of why each is tempting and why it fails.

**Why it matters:** Anti-patterns encode hard-won experience. They prevent the model from
reproducing the most common mistakes. A skill without anti-patterns is a tutorial, not expertise.

| Score | Criteria |
|-------|---------|
| 5 | ≥4 named anti-patterns; each is genuinely tempting; each explains why it fails with specific consequences |
| 4 | ≥3 named anti-patterns; all are genuinely non-obvious; explanations are specific |
| 3 | ≥2 anti-patterns but they are obvious (things no expert would do) OR explanations are vague |
| 2 | 1 anti-pattern OR anti-patterns that are trivial/obvious |
| 1 | No anti-patterns section |

**Revision trigger:** Anti-patterns that are obvious OR fewer than 3.
**Revision instruction:** Return to Module 1, Question 4. Ask: what do smart, experienced people
do before they know better? Those are the real anti-patterns.

---

## Dimension 5 — Edge Case Handling

**What it measures:** Whether the skill addresses non-standard conditions by name with specific
mitigations, not just "handle exceptions appropriately."

**Why it matters:** The happy path is easy. Edge cases are where skills fail in production.
A skill that only handles the standard case is only half a skill.

| Score | Criteria |
|-------|---------|
| 5 | ≥4 named edge cases with specific mitigations; each condition is realistically encountered |
| 4 | ≥3 named edge cases with specific mitigations |
| 3 | Edge cases mentioned but without specific mitigations OR cases are trivial |
| 2 | Single edge case OR edge cases only implied, not named |
| 1 | No edge case section; only the happy path |

**Revision trigger:** Fewer than 3 named edge cases with mitigations.
**Revision instruction:** For the domain in question, ask: what are the 3 most common inputs that
break the standard workflow? Name each condition specifically and write a mitigation.

---

## Dimension 6 — Composability

**What it measures:** Whether the skill knows which adjacent skills it relates to and when to
hand off to them. Treats the library as a network, not isolated files.

**Why it matters:** No skill covers all of a domain. Skills that don't know their boundaries
trap users in the skill when they need a different one.

| Score | Criteria |
|-------|---------|
| 5 | Names ≥2 skills it hands off to with clear handoff conditions; names ≥1 skill that hands off to it; adjacent-skills metadata populated |
| 4 | Names ≥2 adjacent skills with handoff conditions; adjacent-skills metadata populated |
| 3 | Names adjacent skills but without clear handoff conditions OR adjacent-skills metadata missing |
| 2 | Mentions adjacent domain but doesn't name the specific skill |
| 1 | No composability section; adjacent-skills metadata missing |

**Revision trigger:** Missing adjacent-skills metadata OR no named handoff conditions.
**Revision instruction:** Name the 2–3 skills that are most related. For each, write one sentence
describing the condition that triggers a handoff.

---

## Dimension 7 — Failure Mode Documentation

**What it measures:** Whether the skill names specific failure states with specific fallbacks,
not generic warnings.

**Why it matters:** Models operating in complex domains will encounter failures. A skill that
says "things may go wrong" gives the model nothing to work with. A skill that says "if the
foreign key constraint fails with DETAIL: key is not present in table X, check the ingestion
order" gives the model a recovery path.

| Score | Criteria |
|-------|---------|
| 5 | ≥3 named failure states; each has a specific detection signal and a specific fallback; realistic conditions |
| 4 | ≥2 named failure states with specific detection and fallback |
| 3 | Failure states mentioned but detection signals vague OR fallbacks generic |
| 2 | Single failure state OR failure modes section is "things can go wrong" |
| 1 | No failure modes section |

**Revision trigger:** Generic failure descriptions OR fewer than 2 named failure states.
**Revision instruction:** For this domain, ask: what are the 3 most common ways an invocation of
this skill goes wrong? Name each specifically and write what signal indicates it and what to do.

---

## Dimension 8 — Progressive Disclosure Compliance

**What it measures:** Whether the skill respects the three-tier loading model. SKILL.md body
≤500 lines. Heavy reference material in `references/` files. Metadata minimal and complete.

**Why it matters:** Skills carry 1,500+ tokens of overhead per activation. A bloated SKILL.md
degrades context budget for everything else in the session. Progressive disclosure exists
specifically to avoid this.

| Score | Criteria |
|-------|---------|
| 5 | SKILL.md body <400 lines; all heavy content in references/; references linked correctly |
| 4 | SKILL.md body ≤500 lines; appropriate use of references/ for detailed content |
| 3 | SKILL.md body 500–600 lines; references/ used but some content should be moved |
| 2 | SKILL.md body 600–800 lines; references/ not used despite heavy content |
| 1 | SKILL.md body >800 lines OR no progressive disclosure structure at all |

**Revision trigger:** Over 500 lines in SKILL.md body.
**Revision instruction:** Identify the 2–3 heaviest sections. Move them to `references/` files.
Replace with a 1–3 sentence summary and a relative link: `See [references/X.md](references/X.md)`.

---

## Dimension 9 — Future-Proofing

**What it measures:** Whether the skill body is free of brittle version-specific dependencies
that will decay as tools and platforms evolve.

**Why it matters:** Skills are meant to last. Version-specific syntax in the body means the
skill requires updates every time a library updates. Isolate volatility.

| Score | Criteria |
|-------|---------|
| 5 | Body contains only principles and patterns; no version numbers; specifics isolated in references/ |
| 4 | 1–2 version-specific mentions acceptable if clearly marked as "as of version X" |
| 3 | 3–5 version-specific mentions in the body that will decay |
| 2 | Significant version-specific content woven through the body |
| 1 | Skill is built around a specific version, API endpoint, or configuration that will change |

**Revision trigger:** Any version number or deprecated API endpoint in the body.
**Revision instruction:** Move all version-specific content to `references/` with a header
documenting what version it applies to. Body should state the principle; references state the
specific implementation.

---

## Dimension 10 — Auditability

**What it measures:** Whether the skill carries complete metadata for tracking, versioning,
and maintenance.

**Why it matters:** A library of 50+ skills without provenance, versioning, or review schedules
is unmanageable. Metadata is not bureaucracy — it is the minimum infrastructure for sustainability.

| Score | Criteria |
|-------|---------|
| 5 | All metadata fields populated; review-trigger is specific; adjacent-skills populated; improvement candidates documented |
| 4 | Required metadata fields populated; review-trigger present and specific |
| 3 | Most metadata populated but review-trigger is generic OR adjacent-skills missing |
| 2 | Minimal metadata — version and last-reviewed only |
| 1 | No metadata block OR metadata block is empty |

**Revision trigger:** Missing review-trigger OR generic review-trigger.
**Revision instruction:** Name the specific conditions that would make this skill need updating.
"API changes" is not specific. "Anthropic deprecates the current skill description field format"
is specific.

---

## Rubric Scorecard Template

Copy this into the skill review output:

```
Skill: <name>
Date: <YYYY-MM-DD>
Reviewer: <name>

D1  Description Precision:      [ /5] —
D2  Domain Depth:                [ /5] —
D3  Signal Density:              [ /5] —
D4  Anti-Pattern Coverage:       [ /5] —
D5  Edge Case Handling:          [ /5] —
D6  Composability:               [ /5] —
D7  Failure Mode Documentation:  [ /5] —
D8  Progressive Disclosure:      [ /5] —
D9  Future-Proofing:             [ /5] —
D10 Auditability:                [ /5] —

Average: [ /5]
Pass/Fail: [ ]

Dimensions requiring revision:
- D[N]: <specific revision instruction>
```
