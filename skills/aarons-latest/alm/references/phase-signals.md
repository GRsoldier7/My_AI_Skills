# Phase signals and exit gates

Read when the route-table match in SKILL.md is not obvious. **Evidence means tool output from this
session.** A handoff, memory, plan checkbox or agent report is a *hint* that tells you what to check,
never the check itself.

**Tie-break:** two rows match → the lower number wins (safety first). None matches cleanly → row 11
(direct) or the narrowest read-only reconstruction, and name the gap in one line.

---

## 0 · entry → `resume-grounded`
- **Signals:** a handoff, continuity block or `🧭 GROUNDED HANDOFF` pasted with `/alm`, or the last
  such block in the conversation when `/alm` starts.
- **Not an entry signal:** a handoff found on disk. SKILL.md §1 reads it at entry, pasted block or
  not; it never invokes `resume-grounded`, whose trigger is a pasted block. When a block is pasted,
  the later of block and file (higher `SUPERSEDING UPDATE` number, none = 0, else later date) is the
  Lock's briefing, quoted in the `resume-grounded` Skill call's args; the conflict is named in the
  Lock. Same-date index rows resolve first, by SKILL.md §1's tie rule.
- **Exit gate:** Continuity Lock emitted; plan-of-record link resolves (`test -f` or an opened URL);
  `**Proceeding:** /alm cycle 1 — <Lock's Next action>`.

## 1 · stop → `wrapitup` (CLAUDE.md §8)
- **Signals:** any §8 trigger, including a tool call denied with `[CONTEXT GATE`.
- **Rule:** never retry or route around a denial. `wrapitup` runs here without Aaron's word: CLAUDE.md
  §8 prescribes it and carves `Skill(wrapitup)` out of the deny, and CLAUDE.md outranks its
  explicit-only trigger. Its other checks (`git diff`, `git log`, gate runs, plan update) come back
  denied → tag them ASSUMED, name the deferred writes, never retry.
- **Exit gate:** §9.1 handoff emitted plus §8's compact / fresh-thread / continue question; then wait.

## 2 · operate → `engineering:incident-response`
- **Signals:** a failed unit (`systemctl --failed`), a red health check, a 5xx spike, a down
  container, or Aaron reporting an outage.
- **False signal:** a failing *test* — that is row 4.
- **Exit gate:** contained and the cause noted with evidence. No feature work while it is live.
  Containment that touches production still needs Aaron's approval unless he already gave it.

## 3 · review-in → `recommendations` (93% bar)
- **Signals:** a Fable/Codex verdict table, a review file, a findings register or audit with rows
  not yet dispositioned; "follow Fable recs", "action these".
- **False signal:** findings already dispositioned with evidence and built. That is row 8 or 7.
- **Rules:** pass the source to `recommendations`, never a paraphrase. No new review is launched for
  them; under-bar rows get the one second opinion that skill requires.
- **Exit gate:** every row ADOPT / REJECT / MODIFY with evidence; adopted changes built and verified.
  `recommendations` runs its own independent §5 verifier, so that pass stands for row 8 — do not
  re-verify those rows.

## 4 · debug → `systematic-debugging` (+ `test-driven-development` for the fix)
- **Signals:** a failing test, build, type check, lint gate, CI job or runtime error in fresh output
  that blocks the next ready task.
- **Pre-existing vs new:** compare against the base revision's gate result (CI history, or a run in a
  separate worktree). Never `git stash` a user's work to get a clean baseline.
- **False signal:** a red gate unrelated to the next task. Record it, route around it, keep going.
- **Exit gate:** root cause named with evidence; failing check green; no new failures vs the baseline.

## 5 · plan → `writing-plans` or `projectplan-builder`
- **Signals:** no plan of record covers this scope, and the work is MAJOR (CLAUDE.md §4: ≥3 files or
  ≥100 lines, infra/auth/schema/CI/install, a new script/service/feature, a merge to main).
- **Pick:** `projectplan-builder` when no delivery baseline exists (phases, roadmap);
  `writing-plans` when a spec exists and needs an implementation plan.
- **`writing-plans` output:** replace its `REQUIRED SUB-SKILL: …subagent-driven-development…` header
  with `Execute with /alm`; save per §11 and the project's docs index, not `docs/superpowers/plans/`.
- **False signal:** small, obvious work — act directly; planning it is ceremony.
- **Exit gate:** plan file named `YYYYMMDD - Plan - <description>.md`, placed per the project's docs
  index, index row added, linked. Fable pre-execution review **offered** in §9.2, not run.

## 6 · rescope → `projectplan-rescope`
- **Signals:** fresh evidence makes a locked plan item impossible, unsafe or obsolete (a failed
  spike, a changed API, a measured limit), or Aaron changes direction.
- **False signal:** a task finishing, or a cleaner-looking alternative. Neither is evidence.
- **Exit gate:** revised plan with task IDs preserved; the triggering artifact cited; Aaron's
  decision recorded (a scope change needs his decision, so it goes to §9.2).

## 7 · build → `test-driven-development` / a direct `Agent` wave
- **Signals:** a valid plan, a next task with prerequisites met, and no red gate blocking it.
- **Parallel wave only when** ≥2 tasks have independent inputs and outputs and touch disjoint files,
  or are isolated in worktrees. Otherwise run them sequentially.
- **Wave = direct `Agent` calls in one message**, each `isolation: "worktree"` and briefed with
  module-brief.md (no commit unless pre-approved); in-thread isolation is `EnterWorktree` /
  `ExitWorktree`. Not `subagent-driven-development` (its Red Flags forbid parallel implementers, and
  it auto-runs reviewers and commits) and not the `git-worktree` skill (its required
  `worktree-manager.sh` is not installed). Row 8's §5 verifier is the review.
- **Non-code slices** (docs, config, data) skip TDD; their check is the narrowest meaningful one
  (render, parse, dry-run, count).
- **Exit gate:** slice built; its tests and the relevant suite green; diff limited to the slice.

## 8 · verify → §5 verifier
- **Signals:** a built slice with no independent verification yet, or Aaron asks "is it done?".
- **How:** a fresh Agent, `model: "fable"`, given the original ask, the slice's done-when, the diff
  or paths, and the brief "confirm completion AND review; find the flaw, do not bless". Run project
  gates in parallel.
- **Exit gate:** verifier PASS plus gate output quoted. FAIL → the slice returns to `In progress`.

## 9 · release → `engineering:deploy-checklist`
- **Signals:** a verified slice AND Aaron named the operation (commit / push / deploy / merge).
- **False signal:** "ship it" — CLAUDE.md §4 makes it a MAJOR marker, not an operation. Ask in §9.2
  which operation he means and perform none until he names one.
- **Rules:** quote his authorization; never widen it ("commit" is not "push"). A MAJOR push → T3
  duck **offered** in §9.2. No deploy target → just the authorized git operation.
  The project's own ship skill, when its instructions route shipping there, replaces
  `engineering:deploy-checklist` (SKILL.md §2 best-fit check).
- **Exit gate:** operation done; post-release check (CI run, health endpoint, `git log origin/<b>`).

## 10 · close → `wrapitup`
- **Signals:** the plan's done-when holds, Aaron says wrap, or the topic changed (§7 thread-restart).
- **Rule:** run `wrapitup` only when Aaron says wrap (its trigger is explicit-only;
  row 1's §8 stop is the one exception). Objective met,
  or a §7 thread-restart, without his word → emit §9.1 and **offer** `wrapitup` (and a fresh thread)
  in §9.2.
- **Exit gate:** §9.1 handoff, memory mirrored (file layer + Hermes). Stop — no manufactured work.

## 11 · none → direct
- **Signals:** a one-off question, a single-file obvious edit, nothing multi-step.
- **Exit gate:** answer given; §9.2 closes. No cycle trailer, no loop.
