---
name: testing-strategy
description: |
  Expert testing strategist for Python applications using pytest. Designs test suites that
  catch real bugs without becoming maintenance burdens. Covers: fixture design, parametrize
  patterns, property-based testing with hypothesis, integration vs unit test decisions,
  async testing, database testing patterns, and coverage strategy. Use when writing tests
  for new code, deciding what to test, debugging a flaky test, improving test coverage,
  or asking whether an approach is testable. Trigger phrases: "write tests for this",
  "how should I test this", "test coverage", "pytest fixtures", "hypothesis testing",
  "flaky test", "integration test vs unit test", "how do I test async code", "mock vs real".
  Also activates when user says "I need to test this" or "tests keep breaking".
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: code-review, database-design, biohacking-data-pipeline
  last-reviewed: "2026-03-15"
  review-trigger: "pytest major version change, hypothesis API change, Python 3.x deprecation"
  capability-assumptions:
    - "Python 3.12+, FastAPI, SQLAlchemy 2.0, PostgreSQL"
    - "Bash tool for running commands"
  fallback-patterns:
    - "If no code execution: provide code as text for user to run"
  degradation-mode: "graceful"
---

## Purpose and Scope

This skill designs and writes test suites using pytest, with hypothesis for property-based
testing. It covers strategy (what to test, at what level, with what approach) and implementation
(how to write tests that are fast, reliable, and maintainable).

It does NOT cover performance benchmarking, load testing, or end-to-end browser testing.
For reviewing existing test code for correctness, use `code-review`. For database schema testing
strategies, the `database-design` skill covers constraint testing.

---

## Section 1 — Core Knowledge

### The Test Value Hierarchy

Not all tests are equally valuable. Write in this priority order:

1. **Tests that prevent data corruption** — anything that writes to the database, modifies
   shared state, or sends external requests. The cost of a wrong result here is a production incident.
2. **Tests for critical paths** — the operations users care most about. Login, data ingestion,
   API endpoints that drive the UI.
3. **Tests for edge cases in pure functions** — input validation, transformation logic,
   business rules. These are cheap to write and fast to run.
4. **Tests for integration points** — does the code work with the real database, real API, or
   real file system as expected?
5. **Tests for error paths** — does the code fail correctly? Does it return the right error,
   rollback correctly, log appropriately?

### The Unit/Integration Decision

**Write a unit test when:** The logic is self-contained, the function is pure or mockable,
and the test would run in <10ms. Most business logic qualifies.

**Write an integration test when:** The correctness depends on how components interact,
especially with the database or an external API. Mock-based unit tests for database code
create false confidence — they test that you called the mock correctly, not that your SQL works.

**The rule:** If you're testing code that touches PostgreSQL, use a real test database.
Mocking SQLAlchemy gives you confidence that your code compiles; a real database gives you
confidence that your code works.

### Fixture Hierarchy

```python
# Scope hierarchy: session > module > class > function (default)
# Use session scope for expensive one-time setup (DB connection)
# Use function scope for anything that modifies state
# Never share mutable state between tests

@pytest.fixture(scope="session")
def db_engine():  # Expensive: create once per test run
    ...

@pytest.fixture(scope="function")
def db_session(db_engine):  # Cheap: fresh transaction per test
    ...
```

---

## Section 2 — Advanced Patterns

### Pattern 1: Transaction-Rollback Test Isolation
Instead of creating and deleting test data, wrap each test in a transaction that rolls back
at the end. This is 5–20x faster than teardown-based cleanup and leaves no test artifacts.

```python
@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
```

This pattern requires all test code to use the same session object — pass it explicitly
rather than relying on a global session registry.

### Pattern 2: Hypothesis for Edge Case Discovery
Hypothesis generates inputs you wouldn't think to write. The most valuable use is on
functions that parse, transform, or validate data — exactly the kind that biohacking
pipelines use.

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=100))
def test_supplement_name_normalization_handles_any_string(name: str):
    result = normalize_supplement_name(name)
    assert isinstance(result, str)
    assert len(result) <= 100  # invariant: we never expand the string
```

The key insight: Hypothesis finds the *boundaries* you missed. Run it, let it shrink failures
to minimal examples, and those minimal examples reveal your actual assumptions.

### Pattern 3: Parametrize for Equivalence Classes
`@pytest.mark.parametrize` is not just for DRY — it's for making explicit that a set of inputs
should produce equivalent behavior. Group inputs by equivalence class: valid inputs, invalid
inputs, boundary conditions, empty/null conditions.

```python
@pytest.mark.parametrize("dosage,expected_unit", [
    ("500mg", "mg"),
    ("1g", "g"),
    ("2.5 mcg", "mcg"),
    ("1000 IU", "IU"),
])
def test_parse_dosage_extracts_unit(dosage, expected_unit):
    assert parse_dosage(dosage).unit == expected_unit
```

---

## Section 3 — Standard Workflow

1. **Identify what to test first.** Apply the value hierarchy. If everything feels equally
   important, ask: what breaks in production if this is wrong?

2. **Choose the level.** Unit if pure logic, integration if it touches external systems.
   Do not mock what you're actually testing — mock only what is outside your control.

3. **Design fixtures before writing tests.** List what state each test needs. Identify
   shared state (session scope) vs. per-test state (function scope). Write fixtures first.

4. **Write the failing test first.** Run it to confirm it fails for the right reason.
   If it fails for a different reason than expected, your understanding of the code is wrong.

5. **Make it pass with the minimum implementation.**

6. **Add parametrize for equivalence classes** — don't write 5 nearly identical tests.

7. **Add hypothesis for pure transformation functions** — one `@given` test often replaces
   10 parametrize cases and finds edge cases you missed.

8. **Check the failure message.** A test that fails with `AssertionError` with no message
   is a bad test. Every assertion should have a message that makes the failure self-explanatory.

---

## Section 4 — Edge Cases

**Edge Case 1: Testing async FastAPI endpoints**
Use `httpx.AsyncClient` with the FastAPI `TestClient` or `ASGITransport`. Never `requests`.
`pytest-asyncio` with `asyncio_mode = "auto"` in `pyproject.toml` avoids decorator noise.

```python
@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
```

**Edge Case 2: Testing code that calls external APIs**
Intercept at the HTTP layer with `respx` (for httpx) or `responses` (for requests). Never
mock the client object directly — you lose the serialization layer where bugs live.

**Edge Case 3: Flaky tests caused by time**
Tests that depend on `datetime.now()` are time-bombs. Inject time as a dependency or use
`freezegun`. Never mock `datetime` directly in the module under test — it breaks across imports.

**Edge Case 4: Tests that pass locally but fail in CI**
The cause is almost always: test order dependency (shared mutable state), missing environment
variables, or timezone differences. Run tests with `pytest --randomly-seed=12345` locally
to catch ordering issues before CI.

---

## Section 5 — Anti-Patterns

**Anti-Pattern 1: Mocking the Database**
Mocking SQLAlchemy sessions or using `unittest.mock` to fake database calls. The tests pass,
the queries are wrong, the production deployment fails. The only thing this tests is that your
mock setup is correct. Use a real test database with the transaction-rollback pattern instead.

**Anti-Pattern 2: The God Fixture**
A single fixture that sets up 15 database records, 3 API mocks, and 2 environment variables
because "tests need all of this." Each test ends up depending on state it doesn't control,
so changing one test breaks unrelated tests. Fix: each fixture provides exactly what one test
needs. Compose small fixtures.

**Anti-Pattern 3: Asserting Implementation, Not Behavior**
```python
# Testing implementation (bad):
assert mock_session.add.call_count == 1  # So what?

# Testing behavior (good):
user = db_session.query(User).filter_by(email="test@test.com").first()
assert user is not None  # The user was actually saved
```
Mock-based tests that assert on call counts are testing that you wrote the code in a specific
way, not that it works correctly.

**Anti-Pattern 4: The 100% Coverage Cargo Cult**
Pursuing 100% line coverage at the expense of test quality. A line can be covered without
being tested meaningfully. A function that returns the wrong value 20% of the time has 100%
line coverage if you only test the happy path with a single assertion.
Fix: Target 80% coverage on critical paths with assertions that would catch real failures.
Untested code with no coverage is better than tests that create false confidence.

---

## Section 6 — Quality Gates

- [ ] Every critical path has at least one integration test against a real database
- [ ] No test uses `unittest.mock.patch` on SQLAlchemy session or database connection
- [ ] Fixtures use transaction-rollback pattern for database tests
- [ ] Async endpoint tests use `httpx.AsyncClient` with `ASGITransport`
- [ ] External HTTP calls are intercepted at transport layer, not mocked at client level
- [ ] All assertions have failure messages that make the cause self-evident
- [ ] Time-dependent code uses injected time or `freezegun`

---

## Section 7 — Failure Modes and Fallbacks

**Failure: Tests are slow (>30 seconds for unit test suite)**
Detection: `pytest --durations=10` shows which fixtures or tests dominate time.
Fallback: Check fixture scope — expensive setup should be `session`-scoped. Check for
synchronous database calls in `function`-scoped fixtures. Check for missing `anyio` or
`asyncio` mode causing sync-in-async overhead.

**Failure: Flaky tests in CI that pass locally**
Detection: Test passes locally consistently but fails in CI 1 in 5 runs.
Fallback: Run `pytest --randomly-seed=0` locally. Add `pytest-repeat` to run the test 10 times.
Check: shared mutable global state, timezone assumptions, file system path assumptions,
race conditions in async tests using `asyncio.sleep(0)` as a synchronization point.

---

## Section 8 — Composability

**Hands off to:**
- `database-design` — when tests reveal schema constraints need verification at the DB level
- `code-review` — when writing tests reveals that the code under test has a correctness issue

**Receives from:**
- `code-review` — when review identifies missing test coverage as a finding
- `biohacking-data-pipeline` — when pipeline code needs test strategy for ETL correctness

---

## Section 9 — Improvement Candidates

- A `references/conftest-patterns.md` file with reusable conftest.py patterns for
  session-scoped DB setup, factory fixtures, and async client setup
- Hypothesis strategy library for domain-specific types (supplement names, biomarker values,
  dosage strings) as `references/hypothesis-strategies.md`
- Coverage report interpretation guide: what a meaningful 80% looks like vs. gaming the metric
