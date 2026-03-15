# Domain Intelligence Brief Template

Complete this template before writing any SKILL.md content.
Do not begin Module 3 (Skill Architecture) until all 6 questions are answered with specific,
non-generic answers. Generic answers indicate insufficient domain knowledge — not a skill that
should be built yet.

---

## Specificity Test

Before finalizing each answer, apply this test:
> Could this answer appear in a beginner tutorial or a Wikipedia article?

If yes: the answer is not specific enough. Go deeper.
If no: proceed.

---

## Domain Intelligence Brief

**Skill being designed:** `<skill-name>`
**Date:** `<YYYY-MM-DD>`
**Author:** `<name>`

---

### Q1 — Expert Delta

> What do world-class practitioners in this domain know that merely competent ones don't?
> List 3–5 things. Be concrete and specific.

Answer:
1. <specific insight — passes specificity test>
2. <specific insight — passes specificity test>
3. <specific insight — passes specificity test>
4. (optional)
5. (optional)

**Specificity check passed:** [ ] Yes — proceed | [ ] No — go deeper

---

### Q2 — Top Failure Modes

> What are the top 3 ways this domain destroys results when handled naively?
> Name them specifically. "Poor planning" is not an answer. A named failure mode is.

Answer:
1. <named failure mode — specific technical or process failure>
2. <named failure mode — specific technical or process failure>
3. <named failure mode — specific technical or process failure>

**Specificity check passed:** [ ] Yes — proceed | [ ] No — go deeper

---

### Q3 — Domain Vocabulary

> What are the 5–10 terms, frameworks, or mental models specific to this domain that a
> skilled practitioner uses fluently?
> These should appear naturally in the skill's content.

Answer:
- <term/concept>: <one-line definition or description>
- <term/concept>: <one-line definition or description>
- <term/concept>: <one-line definition or description>
- <term/concept>: <one-line definition or description>
- <term/concept>: <one-line definition or description>
(add more as needed)

---

### Q4 — Anti-Pattern Inventory

> What approaches look correct but produce subtly wrong results?
> List at least 3. Each should be something smart people do before they know better.

Answer:
1. <anti-pattern name>: <why it's tempting> / <what actually happens>
2. <anti-pattern name>: <why it's tempting> / <what actually happens>
3. <anti-pattern name>: <why it's tempting> / <what actually happens>
(add more as needed)

**Are these genuinely non-obvious?** [ ] Yes — proceed | [ ] No — they're too obvious, find better ones

---

### Q5 — Activation Boundary

> When should this skill NOT be used?
> What adjacent skill handles those cases instead?
> If you cannot name a clear boundary, the skill's scope is too broad.

This skill does NOT handle:
- <case 1> — handled by `<adjacent-skill-slug>`
- <case 2> — handled by `<adjacent-skill-slug>`
- <case 3> — handled by `<adjacent-skill-slug>`

**Is the boundary sharp?** [ ] Yes — proceed | [ ] No — narrow the scope

---

### Q6 — Composability Surface

> What other skills does this one naturally hand off to?
> What skills hand off to this one?
> Name them by slug.

Hands off to:
- `<skill-slug>` when: <specific condition>
- `<skill-slug>` when: <specific condition>

Receives from:
- `<skill-slug>` when: <specific condition>

---

## Brief Completion Checklist

- [ ] All 6 questions answered
- [ ] All answers pass the specificity test
- [ ] Q2 anti-patterns are genuinely non-obvious
- [ ] Q5 boundary is sharp enough to decide in 5 seconds
- [ ] Q6 composability names actual skills in the library (or "TBD — to be built")

---

## Module 2 Transition

Once the brief is complete, use it to populate the Capability Map:

**Layer 1 — Core (from Q1 + Q2):**
What goes into every invocation. Distill Q1 expert delta + Q2 failure modes into 5–7 actionable
items. These become Section 1 of the SKILL.md.

**Layer 2 — Advanced (from Q1 + Q4):**
The nuanced, experience-encoded knowledge from Q1 + anti-patterns from Q4.
These become Section 2 and Section 5 of the SKILL.md.

**Layer 3 — Edge cases and constraints (from Q2 + Q5):**
Named conditions from Q2 failure modes + Q5 boundary cases.
These become Section 4 and Section 7 of the SKILL.md.
