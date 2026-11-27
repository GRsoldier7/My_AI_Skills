---
name: apex-mode
description: |
  Maximum-stack execution mode. Bundles + sequences the full best-of-the-best skill
  chain (prompt-amplifier → master-orchestrator → relevant domain skills →
  parallel-execution-strategist → anti-hallucination HARD-gate → session-optimizer),
  AND propagates the same discipline into every spawned Agent/subagent via the
  Subagent Envelope pattern. Triggers automatically on phrases: "apex mode",
  "max mode", "best of the best", "use the best skills", "use top skills", "give
  me your best", "spare no effort", "maximum output", "supercharge", "use all
  relevant skills". Persists across turns within the session via /tmp/apex-mode-active
  sentinel file (created by skills-kickoff hook on trigger). Disengages on phrases
  "exit apex", "stop apex", "normal mode". Designed to be the single
  highest-priority skill — overrides per-turn router-precedence pile-up and forces
  full-stack execution including in subagent contexts.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: master-orchestrator, prompt-amplifier, polychronos-team, parallel-execution-strategist, anti-hallucination, session-optimizer, karpathy-guidelines
  last-reviewed: "2026-05-29"
  review-trigger: "Skill stack expansion, new always-on meta-skills added to library, subagent dispatch contract changes"
  trigger-priority: highest
  capability-assumptions:
    - "Requires Skill tool to chain meta-skill invocations"
    - "Requires Agent tool for subagent dispatch with envelope prepending"
    - "Requires /tmp writable for sentinel-file persistence across hook firings"
  fallback-patterns:
    - "If Skill tool unavailable: inline the discipline as plain instructions to the model"
    - "If /tmp not writable: trigger per-turn via phrase match only (no persistence)"
  degradation-mode: "graceful"
---

## Purpose

Apex Mode is the *maximum-output execution discipline*. When active, EVERY active
work stream — the main thread AND every spawned subagent — runs the full
best-of-the-best skill stack, not selectively. Use this when stakes are high,
when the user explicitly demands top performance, or when failure cost dwarfs
the cost of running the full chain.

It is intentionally NOT the default mode — running the full chain on every
trivial reply would burn tokens with no benefit. Apex Mode is the "switch this
on when it matters" gear.

## When apex mode auto-activates

The `skills-kickoff.sh` UserPromptSubmit hook detects these phrase classes and
flips apex mode on for the session:

- Direct invocation: "apex mode", "max mode", "supercharge", "full power"
- Quality demand: "best of the best", "use the best skills", "use top skills",
  "give me your best", "spare no effort", "maximum output", "use all relevant skills"
- Stakes signal: "this matters", "production-critical", "high stakes",
  "can't fail", "no mistakes"

When detected, the hook touches `/tmp/apex-mode-active` so the mode persists
across subsequent turns in the session until explicitly disengaged.

## How apex mode disengages

User says any of: "exit apex", "stop apex", "normal mode", "disable apex".
The hook removes the sentinel file. Mode reverts to default per-turn skill
selection.

## The Apex Stack — execution order every turn while active

1. **prompt-amplifier** (silent) — rewrite the incoming prompt for maximum
   clarity and signal density before routing.
2. **master-orchestrator** — select the domain skill chain. Apex Mode does NOT
   replace it; it WRAPS it.
3. **Domain skills** triggered by content:
   - `karpathy-guidelines` — any code write/modify/refactor/deploy
   - `app-security-architect` — auth, input handling, secrets, file uploads,
     external API integration, database access
   - `superpowers:systematic-debugging` — any bug, error, unexpected behavior
   - `superpowers:brainstorming` — any new feature, component, or behavior change
   - `superpowers:test-driven-development` — implementing a feature or bug fix
4. **parallel-execution-strategist** — engage when 2+ independent operations
   are identified. Spawn parallel `Agent` calls when total wall-clock matters.
5. **polychronos-team** — engage only when master-orchestrator decides the task
   is T2+ multi-specialist (apex mode does NOT double-engage).
6. **anti-hallucination** — escalated from "always-on" to **HARD gate**. Before
   any factual claim ships:
   - Every `file_path:line_number` citation verified via Read or Grep
   - Every function/flag/API name verified to exist in current code
   - Every claim about file contents re-grounded against the live file
   - Surface confidence as TIER 1 (verified just now) / TIER 2 (probable from
     fresh memory) / TIER 3 (unverified — caller beware)
7. **session-optimizer** — proactively compact and offload sub-work to subagents
   once context fill exceeds 40%.

## The Subagent Envelope — MANDATORY while apex active

When apex mode is active, every `Agent` dispatch prompt MUST begin with the
Subagent Envelope so the spawned agent inherits the same discipline. Spawned
agents do NOT see CLAUDE.md or hook output; the envelope is the only mechanism
to propagate apex discipline downstream.

**Envelope template (verbatim, prepend to every Agent prompt while apex active):**

```
SKILL ENVELOPE — apex-mode active (inherited from parent thread).

Before responding, invoke applicable skills via the Skill tool. Pick ONE
router: master-orchestrator (multi-domain) OR best-practice-router (general).
Then chain relevant domain skills:
- karpathy-guidelines for any code change
- app-security-architect for auth/input/secrets/uploads/external APIs
- superpowers:systematic-debugging for any bug or unexpected behavior
- parallel-execution-strategist for 2+ independent sub-tasks
- anti-hallucination as a HARD gate on every factual claim

Cite file_path:line_number for every factual claim. NEVER cite a path,
function name, line number, or API call without verifying it via Read or
Grep in this very session. If you spawn further subagents, prepend this
envelope to their prompts too.

Then perform the task in the next paragraph.
```

The envelope is fixed and copy-pasted as-is. Do not paraphrase. Do not skip.
Do not summarize "I added the envelope" — actually include the literal block.

## Anti-Hallucination — HARD gate while apex active

While apex mode is active, the following rules upgrade from "best practice"
to "blocking":

1. **No file:line citations without verification.** If you have not Read or
   Grep'd the file in this conversation, do not cite a line number. Either
   verify now or label the claim TIER 3 unverified.
2. **No memory-claimed APIs without re-verification.** Memory snapshots decay;
   function names rename, flags rename. Re-verify against the live code before
   recommending.
3. **Subagent findings are TIER 2 maximum** until the main thread verifies
   them. Audit subagents are prone to hallucinating (saw this on 2026-05-29 —
   audit claimed "no cron deployed" when 4 crons were live). Always verify
   subagent claims before acting on them.
4. **Cited counts must be observed.** "X bugs found" requires the list with
   verified file:line for each. Vague counts are TIER 3.
5. **Tense discipline.** "I verified" only after the verification ran in this
   session. "Memory says" for prior-session snapshots.

## Triple-check at session-wrap

Before any "all done" / "ready to ship" / "session complete" summary, run the
pre-end-of-session triple-check protocol per global feedback memory:

1. Identify every factual claim about to ship in the summary
2. Spawn parallel verifiers (Agent / caveman:cavecrew-investigator) to re-check
   each claim against live state
3. Fix any drift found before the summary ships
4. If a downstream decision depended on a now-disproven claim, re-architect that
   decision too

This applies even when work looks complete — the summary is the artifact most
likely to harbor drift after a long session.

## Boundary with other meta-skills

- **master-orchestrator** still routes domain choices — apex wraps, doesn't replace
- **prompt-amplifier** runs silently as step 1, every turn
- **polychronos-team** is engaged BY master-orchestrator when T2+ multi-specialist
- **anti-hallucination** is escalated from advisory to HARD-gate while apex active
- **parallel-execution-strategist** is engaged proactively, not opportunistically
- **caveman compression** continues independently — apex does not change output
  verbosity, only execution discipline

## Examples

**Trigger: "use the best skills for everything you do"**
Hook flips sentinel on. Next turn: invoke prompt-amplifier (silent) →
master-orchestrator → domain stack. Spawn any Agent calls with the envelope.

**Trigger: "this is high stakes, don't miss anything"**
Sentinel on. Anti-hallucination escalates to HARD gate. Every claim verified.

**Disengage: "ok normal mode"**
Sentinel cleared. Next turn returns to per-turn skill selection.

## Failure modes to watch

- Forgetting the envelope on spawned Agents = subagents will hallucinate
  without the same discipline. ALWAYS prepend.
- Treating subagent output as verified — it is TIER 2 until the main thread
  re-checks.
- Letting apex persist when no longer needed — burns tokens. Disengage when
  the high-stakes window closes.
