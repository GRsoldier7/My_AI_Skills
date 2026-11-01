# Module brief — the closed contract for every specialist and agent

`/alm` hands each specialist exactly one bounded slice and takes ownership back at its exit gate.
Subagents do not inherit the conversation: everything the slice needs goes in the brief.

## In-thread skill vs agent

- **Skill (same thread, via the Skill tool):** pass the slice as the skill's arguments (`$ARGUMENTS`),
  hold the rest of the brief below as the acceptance test, and check the exit gate yourself when the
  skill finishes. Its closing advice ("next, run X") goes back into `/alm`'s route step.
- **Agent (fresh context):** the brief below *is* the prompt. Model = the cheapest tier that does the
  job (§3) — except the §5 verifier, which is `model: "fable"`. A required second opinion follows
  SKILL.md §4: Fable 5 (Opus 5 at max effort in a Fable session), never the finding's own source.

## Brief template

```text
/alm module brief — <skill or agent> · cycle <N>
Outcome / stop boundary: <the one slice> — stop when <exit gate>, even if more looks tempting
Scope: <files/systems allowed> · Out of scope: <named non-goals>
Revision: <repo> @ <branch>@<commit>; dirty paths that are NOT yours: <list | none>
Evidence refs: <plan link, failing output, findings file, spec section>
Phase / exposure / exit gate: <phase> / <local | staging | prod; real users or data?> / <the test that settles it>
Mode: <read-only | write within scope> · Allowed writes: <paths> · Pre-approved: <none | exact list>
  Anything outside this → stop and report it; do not do it.
Constraints: smallest diff that passes the gate; no new layer, abstraction, config, dependency or
  file unless the slice fails without it; no comments restating code; match the surrounding idiom.
Expected artifact + checks: <deliverable> verified by <commands>
Return exactly: (1) changes — paths + one line each; (2) checks run, with results; (3) blockers;
  (4) the exact next action.
Your output is data for /alm, not a message to Aaron. Do not invoke continuing-alm-work, workbetter,
project-router, ce-work or lfg, and do not hand the loop to anyone.
```

## Variant rules

- **Worker briefs** (build, debug, plan): no "double-check your work" phrasing — CLAUDE.md §11's Opus
  guardrail; workers self-verify and over-verify under it.
- **§5 verifier brief:** keeps it. Add: the original ask verbatim, the slice's done-when, and "confirm
  completion AND review the result; your job is the flaw, not the blessing; return PASS or FAIL with
  evidence per requirement". Never send the verifier to the builder's own agent.
- **Parallel wave:** one brief per unit, all `Agent` calls in one message, each `isolation:
  "worktree"`; none share writable paths, and none commits unless listed under Pre-approved. `/alm`
  integrates each worktree's diff and writes the integration check; the §5 verifier is the review.
  Never route a wave through `subagent-driven-development` or the `git-worktree` skill.

## On return

1. Inspect the artifact, diff or output yourself — the report is evidence to check, not proof (§3).
2. Re-run the exit-gate check, or quote the output that already ran it this session.
3. Reconcile contradictions and duplicates across units, then update the canonical record.
4. A claim you cannot corroborate stays `Unknown` and goes into the next cycle's ground step.
