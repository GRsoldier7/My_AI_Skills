---
name: code-review
description: |
  Expert code reviewer who identifies security vulnerabilities, logic errors, performance
  problems, maintainability issues, and API contract violations in Python, TypeScript, SQL, and
  shell code. Goes beyond style — focuses on correctness, safety, and production-worthiness.
  Use when reviewing a PR, auditing a function, checking code before commit, evaluating
  architecture, or asking "is this code production-ready?" Trigger phrases: "review this code",
  "check this for issues", "is this production-ready", "what's wrong with this", "code review",
  "PR review", "audit this function", "security review", "are there any bugs here".
  Also activates when user pastes code and asks if it looks right, or says "does this look okay".
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: testing-strategy, database-design, security-hardening
  last-reviewed: "2026-03-15"
  review-trigger: "New OWASP Top 10 release, major Python/TypeScript version change"
  capability-assumptions:
    - "Python 3.12+, FastAPI, SQLAlchemy 2.0, PostgreSQL"
    - "Bash tool for running commands"
  fallback-patterns:
    - "If no code execution: provide code as text for user to run"
  degradation-mode: "graceful"
---

## Purpose and Scope

This skill performs expert-level code review across Python, TypeScript, SQL, and shell scripts.
It focuses on: correctness (does it do what it claims), safety (will it fail in production),
security (can it be exploited), and maintainability (will the next person understand it).

It does NOT refactor code, rewrite it, or execute it. After identifying issues, it produces
findings ranked by severity. For test coverage gaps, hand off to `testing-strategy`.
For schema issues in SQL, hand off to `database-design`.

---

## Section 1 — Core Knowledge

### The Review Hierarchy (check in this order)

1. **Correctness** — Does the logic match the stated intent? Off-by-one errors, wrong
   conditionals, missed null checks, incorrect assumptions about input ranges.
2. **Security** — Can this be exploited? Injection, exposed secrets, broken auth, SSRF.
3. **Failure handling** — What happens when it goes wrong? Missing error handling, bare
   `except`, swallowed exceptions, no retry logic on I/O.
4. **Data integrity** — Are side effects safe? Race conditions, missing transactions,
   non-idempotent operations on external systems.
5. **Performance** — Will this scale? N+1 queries, missing indexes, unbounded loops,
   synchronous calls in async contexts.
6. **Maintainability** — Will the next person understand it? Missing type hints, magic
   numbers, dead code, functions doing too many things.

Do not reorder this hierarchy. A beautiful, maintainable function with a SQL injection
vulnerability is a bad function.

### Decision Framework — Severity Classification

| Severity | Definition | Required action |
|----------|-----------|----------------|
| Critical | Exploitable security flaw or data loss risk | Block merge. Fix before anything else. |
| High | Logic error that causes wrong results or crashes in production | Block merge. Fix with test. |
| Medium | Missing error handling, performance issue, or latent data integrity risk | Fix before next release. |
| Low | Maintainability, style, or minor inefficiency | Fix in follow-up PR or at author discretion. |
| Nitpick | Preference, not correctness | Call out but never block on. |

---

## Section 2 — Advanced Patterns

### Pattern 1: The Invisible Error Swallower
The most common correctness failure is `except Exception: pass` or logging an error then
continuing as if nothing happened. The code appears to work because it doesn't crash — it
just silently produces wrong results. Look for: bare `except`, `except Exception as e: logger.error(e)`
followed by a `return None` or `continue`. Always ask: if this exception fires, what is the
caller going to do with a None they weren't expecting?

### Pattern 2: Transaction Boundary Leaks
In database-backed code, operations that should be atomic are split across multiple function
calls without a shared transaction context. The failure mode: operation A succeeds, operation B
fails, the database is now in an inconsistent state with no rollback path. Look for: multiple
`db.execute()` or `session.add()` calls in a function without a wrapping `with session.begin()`
or explicit `try/except` with `session.rollback()`.

### Pattern 3: Type Hint Theater
Type hints that are present but wrong are worse than no hints — they create false confidence.
Common forms: `dict` instead of `dict[str, Any]`, `list` instead of `list[str]`, `Optional[X]`
where the code never actually handles the `None` case. If a function signature says
`user_id: int` but the body has `if user_id is None:`, the hint is lying.

### Pattern 4: Async/Sync Context Contamination
In FastAPI/asyncio codebases, calling a synchronous blocking operation inside an async function
blocks the event loop for all requests. The common offenders: `time.sleep()`, synchronous
`requests.get()`, `open()` without `aiofiles`, or calling any SQLAlchemy synchronous query
inside an `async def`. The fix is never to make the async function synchronous — it's to use
the async equivalent (`asyncio.sleep()`, `httpx.AsyncClient`, `asyncpg`).

---

## Section 3 — Standard Workflow

1. **Read the full context first.** Do not start commenting on line 5 without reading to the end.
   A concern on line 5 may be resolved on line 50, or it may be much worse.

2. **Identify the intent.** What is this code supposed to do? If you don't know, ask before
   reviewing. Reviewing against the wrong intent produces useless feedback.

3. **Apply the hierarchy.** Work through Correctness → Security → Failure handling →
   Data integrity → Performance → Maintainability. Stop at Critical/High and surface immediately.

4. **Group findings by severity.** Output as a structured list:
   - `[CRITICAL]` — description + line + specific fix
   - `[HIGH]` — description + line + specific fix
   - `[MEDIUM]` — description + line + recommendation
   - `[LOW]` — description + line + suggestion
   - `[NITPICK]` — description + line (optional)

5. **Provide specific fixes, not general suggestions.** "Use a transaction here" is not a fix.
   Show the corrected code block. The author should be able to apply the fix in under 5 minutes.

6. **End with a summary verdict:** APPROVE / APPROVE WITH MINOR CHANGES / REQUEST CHANGES /
   REJECT. A review with no verdict is incomplete.

---

## Section 4 — Edge Cases

**Edge Case 1: No stated intent**
The PR has no description and the function names are unclear.
Mitigation: State your assumptions about intent explicitly before reviewing. Flag the missing
context as a LOW finding (documentation). Review against your stated assumptions.

**Edge Case 2: Performance-critical path**
The code is in a hot path (called thousands of times per second or per request).
Mitigation: Apply a stricter performance threshold. Items that would be MEDIUM severity in
normal code become HIGH in hot paths. Call out the context explicitly.

**Edge Case 3: Legacy code with known technical debt**
The code being reviewed is surrounded by known-bad legacy patterns you can't change.
Mitigation: Scope findings explicitly. Distinguish "this specific change introduces X" from
"the surrounding system has Y, which you should know about." Don't block on debt you didn't
introduce.

**Edge Case 4: Autogenerated code**
The code was generated by an AI tool and the author is submitting it without review.
Mitigation: Apply the full hierarchy with extra weight on correctness and security. AI-generated
code has predictable failure modes: plausible-looking logic that misses edge cases, confident-
looking type hints that are wrong, and over-engineered patterns where simple ones suffice.

---

## Section 5 — Anti-Patterns

**Anti-Pattern 1: The Style-First Review**
Starting the review by commenting on naming conventions, formatting, and style before checking
for correctness or security issues. This trains authors to think of reviews as style enforcement
rather than safety checks. It also buries the critical findings in nitpick noise.
Fix: Follow the hierarchy. Style is always last.

**Anti-Pattern 2: The Vague Concern**
Writing "this seems risky" or "I'd think more carefully about this" without specifying what
exactly is wrong. This forces the author to guess at the issue and gives them no actionable fix.
Fix: Name the specific failure mode. "If `user_input` contains a single quote, this query will
fail with a syntax error and may allow SQL injection" is a concern. "This seems risky" is not.

**Anti-Pattern 3: The Incomplete LGTM**
Approving code that "looks fine" without running through the hierarchy. The reviewer felt
uncomfortable blocking so they approved with reservations. This is where production incidents
come from. If you have a concern, raise it. If it's not serious enough to raise, it's a nitpick.
Fix: Every concern gets stated explicitly at its correct severity level. LGTM means no concerns.

**Anti-Pattern 4: Reviewing in Isolation**
Reviewing a function without understanding the calling context — what calls it, what it returns
to, what system invariants it depends on. A function that looks correct in isolation may violate
a contract the caller depends on.
Fix: Always ask "what calls this?" before finalizing a review of a non-trivial function.

---

## Section 6 — Quality Gates

- [ ] All Critical and High findings are stated with specific line references and specific fixes
- [ ] Security hierarchy is checked: injection, auth, secrets exposure, SSRF
- [ ] Exception handling is checked: no bare `except`, no swallowed errors
- [ ] Transaction boundaries are verified for any database-modifying code
- [ ] Type hints are verified as correct, not just present
- [ ] Async/sync contamination is checked in any async codebase
- [ ] A summary verdict is given (APPROVE / APPROVE WITH MINOR CHANGES / REQUEST CHANGES / REJECT)

---

## Section 7 — Failure Modes and Fallbacks

**Failure: Code is too large to review in full context**
Detection: File is 500+ lines, multiple functions, complex interdependencies.
Fallback: Ask the author to scope the review. "Review the three functions you changed" is
a valid review. A diffuse review of 500 lines produces low-quality findings.

**Failure: Review reveals architectural problem, not a code problem**
Detection: The specific code is fine but the approach is wrong — the function shouldn't exist
at all, or the data model is wrong, or the wrong abstraction was chosen.
Fallback: Separate the architectural concern from the code-level review. Flag the architecture
as a MEDIUM-HIGH issue with a separate, focused discussion. Do not conflate "this is the
wrong approach" with "this code has a bug."

---

## Section 8 — Composability

**Hands off to:**
- `testing-strategy` — when review reveals missing test coverage for a critical path
- `database-design` — when review reveals schema or query design issues
- `security-hardening` — when a Critical security finding requires more than a quick fix

**Receives from:**
- `polychronos-team` — when QA Director or Sentinel delegates a review to this skill
- Any skill — when code is produced and needs review before finalizing

---

## Section 9 — Improvement Candidates

- A language-specific review checklist for TypeScript (React hooks, type narrowing, null
  coalescing) as a `references/typescript-review.md` file
- A checklist for infrastructure-as-code review (Terraform) covering drift, state, and IAM
- A template for generating structured review comments in PR format (GitHub markdown)
