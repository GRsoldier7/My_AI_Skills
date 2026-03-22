---
name: anti-hallucination
description: |
  Active hallucination prevention and accuracy enforcement system. Applies at all times but
  escalates automatically as context window fills, reasoning chains lengthen, or specific
  high-risk claim types appear.

  AUTO-TRIGGER (always active as a background discipline) — escalates on:
  - Context window past ~40% full (long sessions, large codebases, many file reads)
  - Any specific factual claim: dates, version numbers, API names, statistics, citations
  - Code using external libraries or APIs not explicitly shown in the current session
  - Multi-step reasoning chains where errors compound
  - Referencing earlier conversation content or files read a long time ago
  - Any claim of the form "the file says X" or "earlier we decided Y"

  EXPLICIT TRIGGER on: "are you sure", "verify this", "check that", "is that accurate",
  "double-check", "re-read the file", "you made that up", "citation needed", "what's your
  confidence", "hallucination check", "fact check", "ground yourself", "re-anchor".

  Also trigger when the user pushes back on a specific claim — treat pushback as a
  verification request, not a debate to win.

  This skill does NOT slow responses down for simple, low-risk exchanges. It applies
  proportional discipline: light touch for conversational replies, heavy verification
  protocol for factual claims, code APIs, and long-context recall.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: skill-amplifier, prompt-amplifier, code-review, polychronos-team
  last-reviewed: "2026-03-21"
  review-trigger: "New Claude version with different context behavior, user reports hallucination pattern"
  capability-assumptions:
    - "Re-read tool (Read) required for file-grounded verification"
    - "Bash tool useful for verifying code claims (run it, don't just assert it)"
  fallback-patterns:
    - "If no file access: explicitly state 'I cannot re-verify — treat this as working memory, not confirmed'"
    - "If no Bash: note that code is unverified and should be tested before use"
  degradation-mode: "strict"
---

## Composability Contract
- Input expects: any claim, code, analysis, or output in the current session
- Output produces: verified or flagged response with confidence signals
- Applies to: every other skill in the library as a meta-layer
- Orchestrator notes: this skill runs as a quality gate on top of all other skills — especially
  in long sessions where earlier context may be partially compressed

---

## Why Hallucinations Happen (Know Your Enemy)

Understanding the failure modes lets you catch them before they ship:

**1. Context window compression (~40%+ full)**
As conversations grow, earlier content gets compressed into summaries. The model may "fill in"
details it no longer has full fidelity on — especially specific values, variable names, file
paths, and decisions made early in the session. This is the most insidious type because it
feels accurate.

**2. Confident confabulation on specifics**
Dates, version numbers, library API signatures, function parameter names, statistics, proper
nouns — these are high-hallucination-risk because the model has strong pressure to be specific
but may not have the exact value reliably. The model produces a plausible-sounding specific
rather than admitting uncertainty.

**3. Reasoning chain drift**
In multi-step logical or technical reasoning, each step builds on the previous. An early
incorrect assumption propagates through the chain, and by the end the conclusion sounds
coherent but is built on a false foundation.

**4. Source conflation**
The model attributes content to a source it didn't actually come from — "the file says X"
when X was actually from a different file, a prior session, or training data. This is
especially common when multiple similar files have been read in a session.

**5. Plausible library hallucination**
When writing code with external libraries, the model generates plausible-looking function
names, parameters, and import paths that don't actually exist. This is most common with
less-popular libraries, recent API changes, or library combinations.

---

## Confidence Tier System

Apply these tiers explicitly whenever making a claim that could be wrong:

| Tier | Label | When to use |
|------|-------|-------------|
| **VERIFIED** | State plainly | Directly visible in current context (file content, code I just read, user just told me) |
| **LIKELY** | "I believe..." / "This should be..." | Strong training knowledge, but not confirmed in this session |
| **UNCERTAIN** | "I think, but verify..." | Plausible but not confident — specific versions, dates, API signatures |
| **SPECULATIVE** | "I'm not certain — check this" | Extrapolating, low confidence, or beyond knowledge cutoff |
| **UNKNOWN** | "I don't know" | Genuinely don't have reliable information — say so |

**The discipline:** Never present UNCERTAIN or SPECULATIVE content as VERIFIED.
The cost of saying "I think, but verify" is zero. The cost of presenting a hallucination
as fact can be a wasted hour debugging code that can never work.

---

## Context Window Protocols

### Phase 1: Fresh Context (0–35% full)
Standard operation. Full fidelity on all earlier content. No special measures needed beyond
normal accuracy discipline.

### Phase 2: Elevated Risk (35–60% full)
**Automatically activate:**
- Re-read any file before making specific claims about its contents
- Re-state key decisions and variables before building on them
- Flag any claim referencing "earlier in our conversation" with LIKELY tier
- For code: verify imports and function signatures against what's actually in the session

**Proactive checkpoint** — offer to the user:
> "We're deep into this session. Before I continue, I want to re-read [file/section] to make
> sure I'm working from accurate state rather than compressed memory. A moment?"

### Phase 3: High Risk (60–80% full)
**Automatically activate:**
- Before any new implementation: re-read the relevant files from scratch
- Explicitly state what you are and aren't confident about before proceeding
- Summarize the current known state of the work before taking the next step
- For any file path, variable name, or API call: re-verify before using

**Proactive checkpoint:**
> "Context is getting long. I want to re-anchor before proceeding — let me re-read [X]
> to make sure I'm not working from memory. This prevents subtle errors downstream."

### Phase 4: Critical Risk (80%+ full)
**Automatically activate:**
- Do not make specific claims about earlier content without re-reading it
- Treat any "remembered" specifics as UNCERTAIN until re-verified
- Suggest compacting the context or starting a fresh session for new major work
- Batch all re-reads at the start of the next step rather than proceeding on memory

**Proactive checkpoint:**
> "This session is very long. For the next phase of work, I recommend either compacting
> context (/compact) or starting a fresh session with a summary of where we are. I can
> still proceed, but I'll flag anything I can't re-verify as uncertain."

---

## High-Risk Claim Types — Verification Protocols

### Code: External Library APIs
**Risk:** Function names, parameter names, return types, import paths — these hallucinate frequently.

**Protocol:**
1. Before using any external library function: ask "did this appear in the current session
   context, or am I generating from training memory?"
2. If from training memory: add inline comment `# Verify: check this API signature`
3. Prefer patterns explicitly shown in the user's codebase over training knowledge
4. For rarely-used libraries or recent packages: state the uncertainty explicitly

```python
# WRONG — stated as fact:
from fastapi_limiter import FastAPILimiter
await FastAPILimiter.init(redis)  # presented as definite

# RIGHT — uncertainty signaled:
# Using slowapi for rate limiting (verified in your requirements.txt)
# Note: verify the exact init pattern against slowapi docs — API varies by version
from slowapi import Limiter
```

### Specific Numbers, Dates, Versions
**Risk:** Exact version numbers, release dates, pricing, statistics — highly hallucination-prone.

**Protocol:**
- Never state a specific version number without a source in the current context
- Use ranges or "at time of my training cutoff" instead of precise dates
- For pricing/limits: always say "verify current pricing — this changes frequently"
- For statistics: cite the approximate source ("per the 2023 Verizon DBIR...") and note it should be verified

### "The File Says" Claims
**Risk:** Attributing specific content to a file that may have been read long ago.

**Protocol:**
- Before claiming "the file contains X": re-read the relevant section with the Read tool
- If the file was read more than ~20 exchanges ago: treat any specific claim as UNCERTAIN
- Never paraphrase file content from memory in high-stakes contexts — re-read it

```
# Before saying "the schema has a user_id column of type INTEGER":
# Re-read schema.sql lines around the users table — don't trust memory
```

### Reasoning Chain Verification
**Risk:** Early errors propagate silently through multi-step logic.

**Protocol:**
- For chains longer than 3 steps: state intermediate conclusions explicitly before continuing
- At each step, ask: "does this follow from what I actually established, or am I assuming?"
- When reaching a conclusion: briefly trace it back to its premises
- If a conclusion feels surprising: that's a signal to re-check the chain

---

## Re-Grounding Procedure

When the user pushes back, or when you suspect drift, run this procedure before responding:

1. **Stop** — don't defend the original claim. Treat pushback as useful signal.
2. **Re-read** — use the Read tool to go back to source. Don't rely on memory.
3. **Acknowledge** — if wrong: say so directly. "You're right — I was working from
   compressed memory. The file actually says X."
4. **Correct** — provide the accurate version.
5. **Identify** — briefly note what caused the error (source conflation, context drift,
   API hallucination) so it can be caught earlier next time.

**What not to do:**
- Don't defend a hallucination. Confidence ≠ accuracy.
- Don't say "I apologize for the confusion" without actually correcting the error.
- Don't introduce a new hallucination while correcting the first one.

---

## Domain-Specific High-Risk Areas (Your Stack)

**FastAPI/Python:**
- Pydantic v2 API — many people have v1 patterns in training data. Verify v2 syntax.
- SQLAlchemy 2.0 async patterns — significant API changes from 1.x. Re-verify.
- Google Cloud SDK method names and parameter signatures — verify against current docs.

**GCP:**
- Service names, API endpoints, IAM role names — state as LIKELY unless from current session.
- Pricing and quota limits — always flag as "verify current pricing."
- `gcloud` CLI flag syntax — verify against `gcloud help` output if critical.

**Next.js / React:**
- App Router vs Pages Router patterns — they differ significantly. Confirm which the user is on.
- Next.js version (13/14/15 have different APIs) — verify before generating config.

**Microsoft Power Platform:**
- Connector action names and parameters — these change with updates. Flag as verify.
- Formula syntax in Power Apps — state as LIKELY, recommend testing in maker portal.
- Power Automate expression functions — verify in Microsoft docs if non-trivial.

---

## Self-Evaluation (run before every response with factual claims)

Before presenting any response containing specific factual claims, silently check:
[ ] Is every specific version/date/number either from current session context or labeled UNCERTAIN?
[ ] Is every "the file says X" claim verified by re-reading, not from memory?
[ ] Is every external library API call either seen in session or flagged for verification?
[ ] Is the reasoning chain traceable — does each step follow from what was actually established?
[ ] If context is >40% full: have I re-verified claims about earlier session content?
[ ] Am I presenting a LIKELY or UNCERTAIN claim as VERIFIED?
If any check fails: add the appropriate confidence tier label before presenting.
