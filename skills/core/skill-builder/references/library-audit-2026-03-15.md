# Skill Library Audit Report
**Date:** 2026-03-15
**Auditor:** skill-builder v1.0
**Method:** 10-dimension rubric, full library scan

Minimum passing score: ≥4.0 on all dimensions, ≥3.5 average.

---

## Executive Summary

Of 17 existing skills, **0 pass all 10 dimensions at ≥4**. All skills have strong domain depth
and good description precision (the most critical dimensions). The universal failure is missing
infrastructure: no metadata blocks, no anti-patterns sections, no failure modes, no composability
graph, no quality gates, no progressive disclosure compliance for several skills. These are
structural gaps that require additions, not rewrites. The content is high quality; the architecture
is pre-standard.

**Priority classification:**
- 🔴 Critical: D10 (Auditability) — ALL skills fail (no metadata blocks exist)
- 🔴 Critical: D6 (Composability) — ALL skills fail (no adjacent-skills graph)
- 🟡 High: D4 (Anti-patterns) — partial coverage in most skills
- 🟡 High: D7 (Failure modes) — missing in most skills
- 🟡 High: D6 (Quality gates) — missing in most skills
- 🟢 Good: D1 (Description precision), D2 (Domain depth), D9 (Future-proofing)

---

## Per-Skill Scorecards

### 1. polychronos-team

```
D1  Description Precision:      [5/5] — Excellent. Precise activation phrases, clear scope.
D2  Domain Depth:                [5/5] — 13 specialist agents, BLAST protocol, tier classification.
D3  Signal Density:              [4/5] — High signal. Minor overlap between agent descriptions.
D4  Anti-Pattern Coverage:       [2/5] — No anti-patterns section. Several implicit warnings exist.
D5  Edge Case Handling:          [3/5] — Task tiers address some cases but no named edge conditions.
D6  Composability:               [2/5] — References other skills conceptually, no adjacent-skills graph.
D7  Failure Mode Documentation:  [2/5] — No named failure states. Quality gates exist but no fallbacks.
D8  Progressive Disclosure:      [4/5] — References files exist. Body is within limits.
D9  Future-Proofing:             [4/5] — Methodology-focused, not version-specific.
D10 Auditability:                [1/5] — No metadata block (version, last-reviewed, review-trigger).
Average: 3.2 | FAIL
```

**Priority fixes:** Add metadata block (D10). Add anti-patterns section (D4). Add failure modes (D7).

---

### 2. prompt-amplifier

```
D1  Description Precision:      [5/5] — Very precise. Multiple trigger phrases and implicit patterns.
D2  Domain Depth:                [5/5] — 6 amplification layers, cross-model optimization, examples.
D3  Signal Density:              [4/5] — Dense and specific.
D4  Anti-Pattern Coverage:       [2/5] — "When NOT to amplify" section exists but lacks anti-patterns.
D5  Edge Case Handling:          [3/5] — "When NOT to amplify" covers some edges.
D6  Composability:               [2/5] — No adjacent-skills graph.
D7  Failure Mode Documentation:  [1/5] — Not present.
D8  Progressive Disclosure:      [5/5] — Well-structured, within limits.
D9  Future-Proofing:             [5/5] — Principle-based, not tool-specific.
D10 Auditability:                [1/5] — No metadata block.
Average: 3.3 | FAIL
```

**Priority fixes:** Metadata block (D10). Failure modes section (D7). Rename "When NOT to amplify"
to Anti-patterns, add 2 more specific anti-patterns (D4).

---

### 3. portable-ai-instructions

```
D1  Description Precision:      [5/5] — Precise. Lists all output file types as triggers.
D2  Domain Depth:                [5/5] — Covers CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules formats.
D3  Signal Density:              [4/5] — Good. Some template content could be moved to references/.
D4  Anti-Pattern Coverage:       [2/5] — None.
D5  Edge Case Handling:          [2/5] — Doesn't address: what to do when a platform isn't supported.
D6  Composability:               [2/5] — No adjacent-skills graph.
D7  Failure Mode Documentation:  [1/5] — Not present.
D8  Progressive Disclosure:      [4/5] — Long template content is inline; could move to references/.
D9  Future-Proofing:             [3/5] — Lists specific platforms that will change as ecosystem evolves.
D10 Auditability:                [1/5] — No metadata block.
Average: 2.9 | FAIL
```

**Priority fixes:** Metadata block (D10). Anti-patterns + failure modes (D4, D7). Move platform
templates to references/ to improve D9.

---

### 4. ai-agentic-specialist

```
D1  Description Precision:      [5/5] — Excellent. Many trigger phrases, clear activation scope.
D2  Domain Depth:                [5/5] — LLM landscape, agentic architectures, cost optimization, ROI.
D3  Signal Density:              [4/5] — High signal. Some sections could be tightened.
D4  Anti-Pattern Coverage:       [2/5] — No dedicated section. Implicit in "always search web" guidance.
D5  Edge Case Handling:          [3/5] — Addresses bootstrapper context but limited edge cases.
D6  Composability:               [2/5] — No adjacent-skills graph.
D7  Failure Mode Documentation:  [1/5] — Not present.
D8  Progressive Disclosure:      [4/5] — Good structure.
D9  Future-Proofing:             [4/5] — Explicitly instructs to search for current info.
D10 Auditability:                [1/5] — No metadata block.
Average: 3.1 | FAIL
```

**Priority fixes:** Metadata block (D10). Anti-patterns section (D4). Failure modes (D7).

---

### 5. business-genius

```
D1  Description Precision:      [5/5] — Very precise with implicit activation patterns.
D2  Domain Depth:                [5/5] — Three Pillars framework, opportunity scoring, AI moats.
D3  Signal Density:              [4/5] — High density. Some frameworks have slight repetition.
D4  Anti-Pattern Coverage:       [2/5] — No dedicated section. Some implicit warnings.
D5  Edge Case Handling:          [3/5] — Solo founder constraints addressed. Limited.
D6  Composability:               [2/5] — No adjacent-skills graph.
D7  Failure Mode Documentation:  [1/5] — Not present.
D8  Progressive Disclosure:      [4/5] — Good structure.
D9  Future-Proofing:             [4/5] — Framework-based, not trend-specific.
D10 Auditability:                [1/5] — No metadata block.
Average: 3.1 | FAIL
```

---

### 6. market-intelligence

```
D1  Description Precision:      [5/5] — Precise. Covers explicit + implicit activation.
D2  Domain Depth:                [4/5] — TAM/SAM/SOM, competitor mapping, opportunity scoring.
D3  Signal Density:              [4/5] — Good.
D4  Anti-Pattern Coverage:       [2/5] — No dedicated section.
D5  Edge Case Handling:          [3/5] — Mentions founder-market fit but limited edge cases.
D6  Composability:               [2/5] — No adjacent-skills graph.
D7  Failure Mode Documentation:  [1/5] — Not present.
D8  Progressive Disclosure:      [4/5] — Good.
D9  Future-Proofing:             [4/5] — Framework-based.
D10 Auditability:                [1/5] — No metadata block.
Average: 3.0 | FAIL
```

---

### 7. biohacking-data-pipeline

```
D1  Description Precision:      [5/5] — Precise. Lists specific data types and trigger conditions.
D2  Domain Depth:                [5/5] — EVTLVL pipeline, 4 data domains, API catalog, temporal versioning.
D3  Signal Density:              [4/5] — High. Some principles could be tightened.
D4  Anti-Pattern Coverage:       [3/5] — Implicit warnings throughout but no dedicated section.
D5  Edge Case Handling:          [3/5] — Rate limiting, idempotency mentioned but not as named edges.
D6  Composability:               [2/5] — No adjacent-skills graph.
D7  Failure Mode Documentation:  [2/5] — Partial. Error handling mentioned but no named failure states.
D8  Progressive Disclosure:      [4/5] — API catalog in references/. Good.
D9  Future-Proofing:             [4/5] — API catalog isolated in references/ (good pattern).
D10 Auditability:                [1/5] — No metadata block.
Average: 3.3 | FAIL
```

---

### 8. brand-website-strategy

```
D1  Description Precision:      [5/5] — Strong. Covers explicit + implicit triggers.
D2  Domain Depth:                [5/5] — Positioning, visual identity, conversion, SEO. Specific hex codes.
D3  Signal Density:              [4/5] — High.
D4  Anti-Pattern Coverage:       [2/5] — No dedicated section.
D5  Edge Case Handling:          [2/5] — Single-brand vs two-brand decision addressed. Limited.
D6  Composability:               [2/5] — No adjacent-skills graph.
D7  Failure Mode Documentation:  [1/5] — Not present.
D8  Progressive Disclosure:      [4/5] — Good length.
D9  Future-Proofing:             [3/5] — Lists specific tools (Vercel, Next.js) in body. Should move.
D10 Auditability:                [1/5] — No metadata block.
Average: 2.9 | FAIL
```

---

### 9. cloud-migration-playbook

```
D1  Description Precision:      [5/5] — Strong. Lists GCP services as triggers.
D2  Domain Depth:                [5/5] — 5 migration phases, cost estimates, security hardening.
D3  Signal Density:              [4/5] — High.
D4  Anti-Pattern Coverage:       [3/5] — Some implicit warnings about over-provisioning, etc.
D5  Edge Case Handling:          [3/5] — Cost estimation addressed. Migration phases cover edges.
D6  Composability:               [2/5] — No adjacent-skills graph.
D7  Failure Mode Documentation:  [2/5] — Partial. Rollback strategy absent.
D8  Progressive Disclosure:      [4/5] — Good. Cost optimization in references/.
D9  Future-Proofing:             [3/5] — GCP service names in body. Will change.
D10 Auditability:                [1/5] — No metadata block.
Average: 3.2 | FAIL
```

---

### 10–17. Microsoft Skills (8 skills: power-bi, power-apps, power-automate, sharepoint, copilot-studio, power-platform-admin, microsoft-dataverse, m365-integration)

All 8 Microsoft skills follow the same structural pattern. Scores are representative:

```
D1  Description Precision:      [5/5] — All have excellent, detailed descriptions with many triggers.
D2  Domain Depth:                [5/5] — All are savant-level. Deep, non-obvious content.
D3  Signal Density:              [4/5] — High signal across all 8.
D4  Anti-Pattern Coverage:       [3/5] — Partial in most (implicit warnings). power-bi is best.
D5  Edge Case Handling:          [3/5] — Good coverage in power-bi and power-automate. Weaker elsewhere.
D6  Composability:               [2/5] — None have adjacent-skills graph.
D7  Failure Mode Documentation:  [2/5] — Partial in power-automate (error handling). Missing in others.
D8  Progressive Disclosure:      [3/5] — Several skills approach or exceed 500 lines.
D9  Future-Proofing:             [3/5] — Microsoft platform/API versions in body of several skills.
D10 Auditability:                [1/5] — No metadata blocks in any.
Average: 3.1 | ALL FAIL
```

**power-bi is the strongest Microsoft skill.** The `references/` pattern for DAX patterns and
Power Query is exactly correct and should be replicated across all Microsoft skills.

---

## Top 5 Cross-Cutting Improvements (Highest ROI)

### Fix 1: Add metadata blocks to all 17 skills [D10 — Critical]
Every skill needs:
```yaml
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: <category>
  adjacent-skills: <slugs>
  last-reviewed: "2026-03-15"
  review-trigger: "<specific condition>"
```

### Fix 2: Add composability section to all 17 skills [D6 — Critical]
Template:
```
## Composability

**Hands off to:**
- `<skill>` — when <condition>

**Receives from:**
- `<skill>` — when <condition>
```

### Fix 3: Add anti-patterns sections to 15 skills [D4 — High]
The 2 skills with partial coverage (biohacking-data-pipeline, cloud-migration-playbook) need
their implicit warnings formalized. The remaining 15 need 3+ named anti-patterns added.

### Fix 4: Add failure modes sections to 15 skills [D7 — High]
Template:
```
## Failure Modes and Fallbacks

**Failure: <named state>**
Detection: <signal>
Fallback: <action>
```

### Fix 5: Push version-specific content to references/ [D9 — Medium]
Skills with specific tool versions or platform-specific configurations in the body:
- brand-website-strategy (Next.js, Vercel)
- cloud-migration-playbook (GCP service names — acceptable as principles but need dates)
- Microsoft skills (platform API versions)

---

## Implementation Plan

**Immediate (this session):** Apply Fix 1 (metadata) and Fix 2 (composability) to the 9 core +
strategy + product skills. Build the 3 new engineering skills as reference implementations.

**Next session:** Apply Fixes 3, 4, 5 to the 9 core/strategy/product skills.

**Subsequent session:** Apply all fixes to the 8 Microsoft skills (largest volume).
