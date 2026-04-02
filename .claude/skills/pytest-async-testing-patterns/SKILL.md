---
name: pytest-async-testing-patterns
description: pytest best practices with async testing, fixtures, parametrize, hypothesis property-based testing, and transaction rollback isolation for FastAPI/SQLAlchemy. Use when writing tests, designing test suites, or setting up test infrastructure.
---

# Pytest Async Testing Patterns

Production-grade pytest patterns with async support, hypothesis property-based testing, and database transaction isolation.

## When to Apply

- Writing tests for FastAPI async endpoints
- Designing fixture hierarchies with conftest.py
- Setting up database test isolation with transaction rollback
- Using hypothesis for property-based testing
- Configuring pytest-asyncio for async test suites

## Critical Rules

**Async Test Configuration**: Always configure pytest-asyncio mode and loop scope

```ini
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_test_loop_scope = "function"
markers = [
    "integration: marks tests requiring database",
    "slow: marks slow-running tests",
]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning",
]
```

**Never use sync fixtures in async tests**: Match fixture async-ness to test async-ness

```python
# WRONG - sync fixture for async test
@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()

# RIGHT - async fixture for async test
@pytest.fixture
async def db_session(async_engine):
    async with async_sessionmaker(async_engine)() as session:
        yield session
        await session.rollback()
```

## Key Patterns

### Transaction Rollback Isolation

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://test:test@localhost:5432/test_db",
        echo=False,
    )
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def setup_database(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(async_engine, setup_database):
    """Each test gets its own transaction that rolls back."""
    async with async_engine.connect() as conn:
        trans = await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        yield session
        await session.close()
        await trans.rollback()
```

### FastAPI Test Client with DB Override

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import get_session

@pytest.fixture
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

### Fixture Composition with conftest.py

```python
# conftest.py - hierarchical fixtures
import pytest
from app.models import User

@pytest.fixture
async def user_factory(db_session):
    """Factory fixture for creating test users."""
    created = []
    async def _create(email: str = "test@example.com", **kwargs):
        user = User(email=email, **kwargs)
        db_session.add(user)
        await db_session.flush()
        created.append(user)
        return user
    yield _create

@pytest.fixture
async def sample_user(user_factory):
    return await user_factory(email="user@test.com", name="Test User")
```

### Parametrize Patterns

```python
import pytest

# Basic parametrize with IDs
@pytest.mark.parametrize(
    "status_code, endpoint",
    [
        (200, "/api/health"),
        (200, "/api/users"),
        (401, "/api/admin"),
    ],
    ids=["health-check", "users-list", "admin-unauthorized"],
)
async def test_endpoint_status(client, endpoint, status_code):
    response = await client.get(endpoint)
    assert response.status_code == status_code

# Parametrize with marks
@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"email": "valid@test.com"}, 201),
        ({"email": ""}, 422),
        pytest.param({"email": "duplicate@test.com"}, 409, marks=pytest.mark.integration),
    ],
)
async def test_create_user(client, payload, expected):
    response = await client.post("/api/users", json=payload)
    assert response.status_code == expected
```

### Hypothesis Property-Based Testing

```python
from hypothesis import given, strategies as st, settings, HealthCheck
import pytest

# Basic property-based test
@given(
    email=st.emails(),
    name=st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=("L", "N", "Z"))),
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_user_creation_properties(email, name):
    """Any valid email and name should create a valid user."""
    user = UserCreate(email=email, name=name)
    assert user.email == email
    assert len(user.name) >= 1

# Strategy composition for domain objects
user_strategy = st.builds(
    UserCreate,
    email=st.emails(),
    name=st.text(min_size=1, max_size=100),
    age=st.integers(min_value=0, max_value=150),
)

@given(user_data=user_strategy)
@settings(max_examples=100)
def test_user_serialization_roundtrip(user_data):
    """Serialization should be lossless."""
    json_data = user_data.model_dump()
    restored = UserCreate(**json_data)
    assert restored == user_data
```

### Event Loop Scoping for Shared Fixtures

```python
import pytest

# Share expensive fixtures across a module
@pytest.fixture(scope="module")
async def seeded_database(async_engine):
    """Seed data once per module, share across tests."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Seed data
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Tests sharing the module-scoped fixture
@pytest.mark.asyncio(loop_scope="module")
async def test_query_users(seeded_database, db_session):
    result = await db_session.execute(select(User))
    assert result.scalars().all()

@pytest.mark.asyncio(loop_scope="module")
async def test_query_posts(seeded_database, db_session):
    result = await db_session.execute(select(Post))
    assert result.scalars().all()
```

## Common Mistakes

- **Mixing loop scopes**: Don't share async fixtures across different loop scopes — a session-scoped fixture can't be used with function-scoped tests without matching the loop scope
- **Missing rollback**: Always rollback in test fixtures — committed data leaks between tests and causes flaky failures
- **Blocking the event loop**: Don't call `time.sleep()` or sync I/O in async tests — use `asyncio.sleep()` and async libraries
- **Over-mocking the database**: Use transaction rollback isolation instead of mocks — mocks hide real query bugs and migration failures
- **Hypothesis with async**: hypothesis `@given` doesn't support async test functions directly — use sync wrappers or `hypothesis.extra.asyncio` when available
