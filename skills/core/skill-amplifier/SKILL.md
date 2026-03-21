---
name: skill-amplifier
description: |
  Genius-level SKILL.md transformer that takes any existing skill and rewrites it to its absolute
  peak performance. Use this whenever you want to maximize, optimize, future-proof, amplify,
  supercharge, or upgrade any skill file. Trigger on: "optimize this skill", "make this skill
  better", "amplify this skill", "maximize this skill", "upgrade my skill", "improve SKILL.md",
  "make this run better", "future-proof this skill", "how can I make this skill more powerful",
  "this skill isn't triggering right", "skill performance", "rewrite this skill for maximum
  output". Also trigger when the user pastes a SKILL.md and asks "what do you think?" or
  "can we improve this?" or "is this good?". Works in three modes: on-demand (single skill),
  pre-commit (verify before pushing), and batch (entire library audit + rewrite).
  DO NOT use for creating a brand-new skill from scratch — use skill-builder for that.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: skill-builder, prompt-amplifier, polychronos-team
  last-reviewed: "2026-03-21"
  review-trigger: "New Claude major version, new prompt engineering research, user reports a skill underperforming"
  capability-assumptions:
    - "Requires file read/write access for batch and pre-commit modes"
    - "Bash tool needed for scanning skills directory in batch mode"
  fallback-patterns:
    - "If no file access: user pastes SKILL.md content, output rewritten version as text"
    - "If no Bash: process skills one at a time instead of batch scanning"
  degradation-mode: "graceful"
---

## Purpose

This skill transforms any existing SKILL.md into its maximum performance version. It does not
create skills from scratch (use `skill-builder` for that). It takes what exists and elevates it
across eight amplification dimensions that go beyond any quality rubric — producing a rewritten,
production-hardened, future-proofed, composable skill ready to perform at frontier level.

The output is always a complete, drop-in replacement SKILL.md — not a list of suggestions.

---

## Operating Modes — Dynamic, All Three Always Available

The skill-amplifier detects which mode is needed from context and executes it fully and
automatically. Do not ask the user to choose a mode — infer it and proceed.

**Mode 1 — On-Demand (single skill, deepest optimization):**
Triggered when: user names a skill, pastes a SKILL.md, points to a file path, or says
"amplify [skill name]" / "maximize this skill" / "optimize [skill]".
Action: Run ALL eight amplification passes in full. Rewrite every section that scores below
4.5. Output the complete production-ready SKILL.md replacement.
This is the highest-fidelity mode — spare no effort. Every pass runs at full depth.

**Mode 2 — Pre-Commit (verification gate, automatic on push/commit):**
Triggered when: user mentions committing, pushing, or finalizing a skill before sending to
GitHub. Also trigger proactively when a new SKILL.md is written in this session.
Action: Run rapid triage across all eight dimensions. Score each 1-5. For any dimension
scoring below 4, output the corrected section only. Report:
"Pre-commit check: [N] of 8 dimensions needed work. Updated sections: [list]. File is now
production-ready."
This mode runs fast — it is a gate, not a full rewrite. Only fix what fails.

**Mode 3 — Batch (full library, comprehensive upgrade):**
Triggered when: user asks to amplify/optimize/upgrade multiple skills or "the whole library"
or "all my skills" or "run this on everything".
Action:
1. Scan all SKILL.md files in the skills/ directory tree
2. Score each skill across all eight dimensions (triage pass — fast)
3. Output a prioritized upgrade table (see references/amplification-patterns.md §4)
4. Automatically rewrite ALL skills scoring below 3.5 (High priority) in full
5. Rewrite ALL skills scoring 3.5-4.0 (Medium priority) for the failing passes only
6. Output a summary: "[N] skills fully rewritten, [N] partially updated, [N] optimal"
7. Write all rewritten SKILL.md files back to their original paths
Do not ask permission to proceed — run the full batch and report when done.

**Auto-detection rules:**
- Single file path or skill name mentioned → Mode 1
- Words like "before I push", "pre-commit", "check this skill", "ready to commit" → Mode 2
- Words like "all skills", "whole library", "every skill", "batch", "run on everything" → Mode 3
- New SKILL.md just created in this session → Mode 2 (automatic gate, no prompt needed)

---

## The Eight Amplification Passes

Run all eight in sequence on the target skill. Each pass reads the current state and rewrites
where needed. Do not skip passes because a dimension looks "fine" — every pass finds something.

### Pass 1 — Metacognitive Scaffolding

**What it does:** Rewrites skill instructions so the model reflects on its own outputs before
delivering them. The goal is a skill that catches its own errors without human intervention.

**Patterns to add:**
- Before finalizing output, the skill explicitly checks: "Does this accomplish the user's stated
  goal? Have I missed any constraints they mentioned? Is there a simpler path I haven't considered?"
- Add a "confidence signal" instruction: if the model is uncertain about a key decision, the
  skill instructs it to surface that uncertainty rather than paper over it.
- For multi-step skills: add checkpoint instructions between phases so each phase validates its
  own outputs before handing off to the next.

**Red flags in the original that need fixing:** Skills that end with "output the result" with
no self-check. Skills where the model could plausibly go off-track mid-task with no recovery.

### Pass 2 — Adaptive Context Injection

**What it does:** Rewrites static instructions into dynamic ones that detect the execution
environment and adjust behavior accordingly.

**Patterns to add:**
- Tool availability detection: "If the Bash tool is available, run X. If not, fall back to Y."
- Platform detection: "In Claude Code, use file tools directly. In Claude.ai, output as artifact."
- User expertise detection: "If the user's message is highly technical, skip the explanation
  preamble. If it suggests they're new to this domain, explain key terms before proceeding."
- Scope detection: "If the user's request is narrow (single file, single function), stay
  narrow. If broad (whole system, all skills), proceed in batches with checkpoints."

**Red flags:** Skills with hard-coded platform assumptions. Skills that behave identically
regardless of what tools or context are actually present.

### Pass 3 — Composability Protocol

**What it does:** Adds structured input/output declarations so this skill can be orchestrated
by `polychronos-team` or chained with other skills without ambiguity.

**Pattern to add (append to skill frontmatter or top of body):**
```
## Composability Contract
- Input expects: [what data/files/context this skill needs to operate]
- Output produces: [what this skill returns — file, report, code, decision, etc.]
- Can chain into: [skill names that naturally follow this one]
- Receives from: [skill names that naturally precede this one]
- Orchestrator notes: [any special handling needed when run as a sub-skill]
```

Keep this section concise — 5-8 lines max. Its purpose is machine-readable orchestration hints,
not human documentation.

### Pass 4 — Self-Evaluation Hooks

**What it does:** Embeds a quality gate inside the skill so it validates its own output before
presenting it to the user. This turns every invocation into a mini-review cycle.

**Pattern to add:**
After the main task instructions, add an explicit self-evaluation step:
```
Before presenting your final output, run this internal checklist silently:
[ ] Does the output directly address what the user asked for?
[ ] Have I followed every constraint or format specified in this skill?
[ ] Is the output complete — no placeholders, no "TBD" sections?
[ ] If I were the user receiving this, would I need to ask a follow-up?
If any box is unchecked, fix the output before presenting it.
```

Customize the checklist items to the specific domain of the skill being amplified.

### Pass 5 — Progressive Disclosure Optimization

**What it does:** Restructures what lives in the frontmatter description vs. the SKILL.md body
vs. the references/ directory to minimize token load while maximizing performance.

**Rules:**
- Frontmatter description: ONLY triggering language + one-sentence purpose. 150-300 words max.
  No how-to content in the description — that belongs in the body.
- SKILL.md body: Workflow, instructions, decision rules, patterns. Under 400 lines.
- references/: Domain knowledge, examples, templates, large lookup tables. Loaded on demand.
  Add explicit "Read references/X.md when you need Y" instructions in the body.

**What to move:** Large example tables, domain glossaries, step-by-step reference procedures,
template files. These slow down every invocation even when not needed.

**What to keep in body:** The workflow, the decision logic, the quality gates. The things the
model needs to know BEFORE it starts, not things it looks up along the way.

### Pass 6 — Future-Proofing Annotations

**What it does:** Documents capability assumptions so the skill degrades gracefully when the
environment changes rather than failing silently.

**Add to metadata section:**
```yaml
metadata:
  capability-assumptions:
    - "Requires Bash tool for script execution"
    - "Requires file read/write access"
    - "Optimized for Claude Sonnet 4+ (extended context)"
  fallback-patterns:
    - "If Bash unavailable: output script as artifact for user to run manually"
    - "If file access unavailable: request user paste content directly"
  version-notes: "Reviewed for Claude Sonnet 4.6. Re-review on next major Claude version."
  degradation-mode: "graceful" # or "strict" — graceful means attempt with reduced capability
```

### Pass 7 — Trigger Precision Rewrite

**What it does:** Rewrites the description field to maximize both activation accuracy (fires
when it should) and suppression accuracy (does not fire when it shouldn't).

**Rewrite formula:**
1. State the core purpose in one concrete sentence ("This skill does X")
2. List 5-8 explicit trigger phrases — actual words a user would type, not abstractions
3. Add 2-3 implicit trigger patterns — situations where the user needs this but won't name it
4. Add 1-2 explicit non-trigger statements to suppress misfires ("Do NOT use for Y — use Z instead")
5. Stay under 350 words total

**Test the rewrite mentally:** Run 10 representative queries through the new description.
If any obviously correct query wouldn't trigger it, the description needs work.
If any obviously wrong query would trigger it, add a non-trigger statement.

### Pass 8 — Constitutional Constraints

**What it does:** Adds explicit guardrails so the skill behaves safely even under adversarial
prompting, scope creep, or ambiguous instructions.

**Patterns to add:**
- Scope enforcement: "If the request expands beyond [defined scope], pause and confirm with
  the user before proceeding. Do not assume expanded scope is desired."
- Irreversibility gate: "Before any action that cannot be undone (file deletion, API call,
  commit, send), state what will happen and ask for confirmation."
- Ambiguity resolution: "If a key parameter is missing or ambiguous, ask one clarifying
  question before proceeding. Do not guess at intent for high-stakes decisions."
- Secrets/credentials: "Never log, output, or embed credentials, API keys, or PII even if
  they appear in the input. Redact before processing."

Add only the constraints relevant to the skill's domain — don't paste all four into every skill.

---

## Output Protocol

After running all eight passes:

1. **Present the rewritten SKILL.md** as a complete file, ready to drop in as a replacement.
   Do not present it as a diff or a list of changes — give the full file.

2. **Append a brief amplification report** (8 lines max):
   ```
   Amplification Report:
   Pass 1 (Metacognitive): [what changed]
   Pass 2 (Adaptive): [what changed]
   Pass 3 (Composability): [what changed]
   Pass 4 (Self-Eval): [what changed]
   Pass 5 (Progressive Disclosure): [what changed]
   Pass 6 (Future-Proofing): [what changed]
   Pass 7 (Trigger Precision): [what changed]
   Pass 8 (Constitutional): [what changed]
   ```

3. **For batch mode:** Present the prioritized upgrade report first, then the rewrites.
   Format: skill name | lowest-scoring pass | overall readiness score (1-10).

---

## Quality Bar

A skill leaving this process must meet all of the following:
- Triggering description fires on 9/10 representative queries, misfires on 0/5 adjacent queries
- Self-evaluation hook is domain-specific (not generic)
- Composability contract is present and accurate
- No platform hard-coding without fallback
- Body is under 400 lines (overflow to references/)
- Constitutional constraints are scoped to actual risks in this skill's domain
- Metadata includes capability-assumptions and fallback-patterns

If any criterion is unmet after the eight passes, run the failing pass again before outputting.

---

## Read references/amplification-patterns.md for:
- Extended examples of each pass applied to real skills
- Domain-specific constitutional constraint templates
- Composability chain examples from the Master_Skills library
- Batch mode scoring spreadsheet template
