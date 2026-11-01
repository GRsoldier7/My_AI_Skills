---
name: alm
description: "Aaron's single lifecycle driver for existing project work: drives the plan of record to production, lean and surgical, one verified slice per cycle. Grounds in fresh evidence, detects the ALM phase (entry/stop/operate/review-in/debug/plan/rescope/build/verify/release/close), dispatches the best-fit specialist, actions pending Fable findings under the 93% bar, runs §5 verification before anything is called done, and closes every response with §9.2. Carries the 'continue to production, no over-architecture' directive and the /using-superpowers + /project-router behavior built in. Use ONLY on /alm; it owns the loop and never nests another controller."
argument-hint: "[optional: focus or task id | phase override: plan|build|debug|verify|review|release|close | status | budget: 'N slices' or 'until <task>']"
disable-model-invocation: true
metadata:
  version: "1.1.0"
  owner: "Aaron DeYoung"
  last-reviewed: "2026-10-26"
  domain-category: aarons-latest
  adjacent-skills: resume-grounded, recommendations, wrapitup
  review-trigger: "CLAUDE.md §4/§5/§8/§9 change, or any routed skill is renamed/removed"
---

# /alm — one owner, one verified slice per cycle, until done

ALM = application lifecycle management (never asset-liability). Invoked with: `$ARGUMENTS`
(empty = continue toward production). CLAUDE.md governs; this file cites its gates, never restates.

## Outcome

Continue forward, grounded and focused, iterating over the plan of record to full optimization and
production: one verified slice per cycle through the best-fit specialist, cycling until a stop
condition holds — leaving state the next `/alm` resumes cold.

## Standing directive — `/alm` alone carries it

`/using-superpowers` (§2 best-fit check) and `/project-router` (§2 route table) are built in: typed
with `/alm` they add nothing and are not invoked.

- **Production** = the plan's own done-when, including any release gate it names; none → ask once in
  §9.2, keep working, never invent a bar.
- **Lean, surgical:** the smallest diff that passes the exit gate, only the slice's paths, the
  surrounding idiom. No new layer, abstraction, config, flag, dependency or file unless the task
  fails without it; no drive-by refactors.
- **No fluff:** no comments restating code, no speculative options, no prose nobody needs; extend an
  existing record before creating one; deleting beats adding.
- **Future-proof = cheap to change later, never built for later:** standard maintained options,
  stable interfaces, no values that rot.
- **Optimize only a measured gap** — a red gate, a profiled cost, a plan target; never taste.

## Ownership — why this is one skill, not four

- **`/alm` is the only execution owner while it runs.** Never invoke `continuing-alm-work`,
  `workbetter`, `project-router`, `ce-work` or `lfg`: their loops are merged here, and invoking one
  nests a second controller. "Continue the project" mid-run means `/alm` continues.
- **`resume-grounded` runs once, at entry, only on a pasted handoff/continuity block** (CLAUDE.md §2).
  Its Lock's **Next action** is cycle 1; its "begin work in the same turn" is satisfied by `/alm` —
  write `**Proceeding:** /alm cycle 1 — <action>`. Never re-invoke it mid-run.
- **Specialists get one bounded slice** with the closed brief in
  [module-brief.md](${CLAUDE_SKILL_DIR}/references/module-brief.md) and return ownership at their exit
  gate. A specialist's "next, invoke X" is advice to `/alm`, never a transfer of the loop.
- **After any compaction**, unless this file's full text is visible after the summary, Read
  `~/.claude/skills/alm/SKILL.md` before the next cycle — re-attachment keeps only recent skills.

## Cycle — then continue or stop

One cycle = **ground → route (first match) → one slice through its exit gate → record → trailer.**
Then start the next cycle without asking, unless a stop condition holds:

- the plan is at production (row 10) · every remaining task Blocked · the only ready path needs
  approval · the §8 stop · the `$ARGUMENTS` budget (`2 slices`, `until T7`) is spent · `status` was
  asked;
- a cycle added no new evidence → change approach once; a second empty cycle stops and names the
  failed assumption. Never repeat an identical action hoping for a different result.

## 1. Ground — every cycle, one batched read

Authority, highest first: **Aaron's latest direction → plan of record / accepted spec →
`git status --short`, `git diff --stat`, `git log --oneline -5` → fresh gate output (tests, build,
CI, health) → tracker → old handoffs and memory (hints, never authority).**

- Batch independent reads in one message; on later cycles re-read only what may have changed.
- **At entry, read the newest handoff on disk, pasted block or not** — before `resume-grounded`, so
  its Lock starts from the newest update. Sources: `~/.claude/handoffs/README.md` rows matching this
  project; a project-root `HANDOFF.md`; the handoff MEMORY.md points to. **Match** = the repo/project
  basename ignoring case and `_`/`-`/space (`Temple_Protocol` = `TempleProtocol`), the plan of
  record's name, a project or handoff name in `$ARGUMENTS` (never a phase, task id or budget), or a
  handoff MEMORY.md names. The index is **not** reliably ordered: take the latest `YYYYMMDD`/`YYYY-MM-DD`
  among ALL matching rows, confirmed by filename prefix in `ls ~/.claude/handoffs/`. **Date tie** →
  read each tied file's head: the highest `SUPERSEDING UPDATE` number wins (none = 0); still tied → the
  one naming the others as superseded or as its plan of record — in the file, or in its index cell
  ("Supersedes the row below"); still tied → newest mtime (`/bin/ls -t` — bare `ls` is `eza --icons`,
  whose `-t` exits 3), the tie named in the Lock. When the tier-1/2 winner is not the mtime-newest
  file, read both heads and name the disagreement in the Lock. Read the winner in full, top update
  first. Pasted block vs file: the later (higher UPDATE number, none = 0, else later date) is the
  briefing, quoted as the Skill args for `resume-grounded`; the Lock names the conflict. Aaron's
  directions quoted there carry forward as intent until he says otherwise; its state claims are hints
  to re-verify. No match, or a tie that survives all three → name the candidates in one line; never
  guess.
- Statuses, exactly: `Verified complete` · `In progress` · `Blocked` · `Not started` · `Superseded` ·
  `Unknown`. **Not run means not passed.** Assess components separately when their maturity differs.
- Narrative vs fresh evidence: evidence wins on technical status, Aaron wins on intent. Name the
  conflict; never pick the convenient version.
- Canonical record: the one Aaron named → the one project instructions or the plan name → the
  existing tracker/handoff convention → `Checkpoint: conversation-only`. Never create a competing
  plan, state or handoff file. Update it after every verified slice when writes are allowed.

## 2. Route — first match wins; safety rows first

Evidence = fresh tool output this session, never narrative. Per-phase signals, false signals and exit
gates: [phase-signals.md](${CLAUDE_SKILL_DIR}/references/phase-signals.md) — read it when the match
is not obvious.

| # | Signal (evidence) | Phase | Route | Exit gate |
|---|---|---|---|---|
| 0 | Handoff/continuity block pasted, or last in chat, at entry | entry | `resume-grounded` | Lock emitted; plan link resolves |
| 1 | Any §8 stop trigger (incl. a `[CONTEXT GATE` denial) | stop | `wrapitup`, per §8 | handoff emitted; wait |
| 2 | Production/service down, live incident | operate | `engineering:incident-response` | contained; no feature work until then |
| 3 | Unactioned Fable/Codex findings in context or a named file | review-in | `recommendations` (93% bar) | every row ADOPT/REJECT/MODIFY with evidence; adopted code built; its own §5 pass stands for row 8 |
| 4 | A red gate in fresh output blocks the next task | debug | `systematic-debugging`, fix via `test-driven-development` | root cause named; gate green; no new failures |
| 5 | No plan of record, and the work is MAJOR (§4) | plan | `writing-plans` (from a spec) or `projectplan-builder` (first baseline) | plan named, placed, indexed per §11; executor line names `/alm`; Fable pre-exec review **offered** |
| 6 | Fresh evidence or Aaron's direction invalidates a locked plan item | rescope | `projectplan-rescope` | revised plan, IDs preserved; Aaron's decision recorded |
| 7 | Plan valid, next task ready | build | `test-driven-development` for code; ≥2 independent tasks → one wave of direct `Agent` calls in one message, each `isolation: "worktree"`, briefed per module-brief.md (no commit unless pre-approved); row 8 is the review | slice built; tests green; ownership back to `/alm` |
| 8 | Slice built but unverified, or Aaron asks to verify | verify | §5 verifier (below) + project gates | evidence lines; nothing called done before |
| 9 | Verified, and Aaron named commit/push/deploy/merge. "Ship it" names none — it marks the work MAJOR (§4): ask in §9.2 which operation | release | `engineering:deploy-checklist` when a deploy exists | authorization quoted; MAJOR push → T3 duck **offered** |
| 10 | Objective met, a §7 thread-restart, or Aaron says wrap | close | `wrapitup` only on Aaron's word; otherwise §9.1, and **offer** `wrapitup` in §9.2 | §9.1 block; memory mirrored |
| 11 | One-off question or no multi-step need | none | direct answer, no loop | §9.2 only |

Side rules, any phase: document created/renamed → §11 name + index row, same change · ground-truth
fact changed while the corpus disagrees → `supersede-state` · change to CLAUDE.md or its hook →
`amend-protocol`, never in place.

**Best-fit check, once per slice** (the `/using-superpowers` rule): before dispatching, scan the
installed skills. The project's own skill routing (its CLAUDE.md/AGENTS.md) and project-local skills
beat the table's default, never with a controller from Ownership's never-invoke list. A repo that
routes every ship through its own skill uses that skill at row 9. Process skills (debug, plan, TDD)
before implementation skills; a poor fit is dropped, never forced.

**Overrides:** a phase in `$ARGUMENTS` (`review` = row 3, `verify` = row 8, the rest by name) jumps to
its row only after rows 0–2 are clear and the row's prerequisite holds (`build` needs a plan for MAJOR
work); otherwise route to the prerequisite and say why in one line. `status` = ground, then §9.1,
zero writes.

## 3. Execute one slice

Prerequisites confirmed → artifact produced → verified at the exit gate → integrated → record updated.

- Pick the highest-leverage ready task: unblocks dependents, shortens the critical path, or retires
  the largest risk. Ship the smallest verifiable slice; keep one primary task active.
- Parallel only across genuinely independent units with their own outputs; write collisions get
  worktrees, never surrendered parallelism; `/alm` owns integration and the cross-check.
- Every agent or specialist result is evidence to inspect, not completion (§3): re-check its
  load-bearing claim before integrating it.
- Park optional improvements in the existing backlog. Separate pre-existing failures from new ones
  with evidence. Never manufacture cleanup.

## 4. Fable and review rules (§4/§5 cited, not restated)

- **Findings already in context** — a verdict table, a review file, "follow Fable recs" — are a
  recommendation set → `recommendations`. Never re-review them; never silently adopt or drop one.
- **Runs without asking:** the §5 verifier on every slice before it is called done — a *fresh* Agent,
  `model: "fable"`, never the builder, brief = confirm completion AND review. Plus the one second
  opinion §4's bar requires for an under-bar call — never from the finding's own source; still split
  → §9.2.
- **Offered only, in §9.2:** Fable pre-execution review of a MAJOR plan, a T3 duck on a MAJOR push,
  `code-review` / `security-review` / `ce-review`. Reviews run on request (§4 rule 1).
- Reviewers: Fable 5 or Codex only, and Codex is paused. Opus 5 at max effort only as the single
  second opinion inside a Fable session. Never Ollama or Sonnet. None reachable → report **SKIPPED**.

## 5. Boundaries

- **Proceed:** routine, reversible, in-scope work in the established workspace.
- **Approval first** — mark the task `Blocked`, keep doing independent safe work: destructive or
  hard-to-reverse changes; production deploy/rollback/restart; schema, migration or bulk-data ops;
  anything sent or published as Aaron; secrets/credentials; scope, architecture, cost or
  security-posture change; resetting or claiming unknown uncommitted work; creating or publishing a
  skill not already requested.
- **Approval request**, once, in §9.2: Action (exact command) / Why now / Risk / Reversibility /
  Alternatives / the one decision / I recommend / If you say nothing (§9.2's schema).
- **Commit, push, deploy, merge only when Aaron named that operation.** "Keep going" authorizes none.
  Never commit, stash or revert to tidy. Dirty tree: inspect status and diff, alter nothing that is
  not this task's.
- Plan-only or read-only runtime: reconstruct state, name the first executable action, write nothing.

## 6. Output

Per completed cycle, exactly four lines:

```
**/alm · cycle N — phase → route:** <phase> → <skill | agent | direct>
**Did:** <changes actually made, paths>
**Evidence:** <command → result, run this session>
**Next:** <exact next action, or the stop condition that ended the loop>
```

- A wrap, `status`, or a MAJOR completion → §9.1 Grounded Handoff (fenced); a close Aaron asked for
  goes through `wrapitup`, otherwise it is offered. Every response ends with §9.2.
- Never emit a Continuity Lock (resume-grounded's, once, at entry), a `RESUME FROM` block (§9.1 covers
  every field), or any third status block.

## 7. Anti-patterns

- Most recently *discussed* ≠ most recently *completed*. A stale handoff never beats red CI.
- Re-reviewing Fable's own findings, or launching a review nobody asked for.
- Calling anything done before the §5 verifier passed; treating an agent report, memory or handoff
  as verification.
- Manufacturing work after the objective is met. Nesting a controller. Three status blocks.
- Widening tool permissions; editing the original skills' repo files to point here.
