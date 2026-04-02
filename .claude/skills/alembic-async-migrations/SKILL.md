---
name: alembic-async-migrations
description: Alembic migration patterns for async SQLAlchemy projects with asyncpg, covering autogenerate, batch ops, data migrations, branch management, and testing. Use when writing or reviewing Alembic migrations in Python async codebases.
---

# Alembic Async Migration Patterns

Production-grade Alembic migration patterns for async SQLAlchemy (asyncpg) projects. Covers the full migration lifecycle: env.py async configuration, autogenerate best practices, batch operations, data migrations, branch/merge workflows, rollback strategies, and migration testing. Complements the general `database-migration` skill (which covers zero-downtime strategies and ORM-agnostic concepts) by going deep on Alembic-specific mechanics.

## When to Apply

- Setting up Alembic in a project using `create_async_engine` / `AsyncSession`
- Running `alembic revision --autogenerate` and reviewing generated output
- Writing data migrations (backfills, seed data, bulk transformations)
- Resolving multiple migration heads in a team workflow
- Debugging migration failures or planning rollback procedures
- Configuring batch operations for SQLite compatibility
- Setting up CI migration testing (up/down cycle verification)

## Critical Rules

### Naming Conventions on MetaData (Non-Negotiable)

Without explicit naming conventions, Alembic cannot autogenerate constraint drops because the constraints have no deterministic names.

```python
# WRONG: implicit constraint names -- autogenerate cannot drop them
class Base(DeclarativeBase):
    pass

# RIGHT: explicit naming conventions on MetaData
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })
```

### Never Use Sync Engine in env.py for Async Projects

```python
# WRONG: using create_engine with asyncpg driver
from sqlalchemy import create_engine
engine = create_engine("postgresql+asyncpg://...")  # will fail

# RIGHT: use create_async_engine + run_async in env.py
from sqlalchemy.ext.asyncio import create_async_engine
```

### Always Define downgrade()

```python
# WRONG: empty downgrade
def downgrade() -> None:
    pass

# RIGHT: reverse every operation from upgrade
def downgrade() -> None:
    op.drop_column("users", "email_verified")
```

### Never Import Application Models in Migration Files

```python
# WRONG: importing live models (they change over time, breaking old migrations)
from myapp.models import User

# RIGHT: use ad-hoc table definitions scoped to the migration
from sqlalchemy.sql import table, column
import sqlalchemy as sa

users = table("users", column("id", sa.Integer), column("status", sa.String))
```

## Alembic Configuration for Async

### env.py with Async Engine (run_async Pattern)

The key pattern: Alembic's migration context is synchronous, so you run it inside `run_sync()` on an async connection.

```python
# env.py
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from myapp.db import Base  # your DeclarativeBase with naming_convention

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode -- generates SQL script."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # safe for all backends
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Configure context with a sync connection (called inside run_sync)."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
        compare_type=True,        # detect column type changes
        compare_server_default=True,  # detect server_default changes
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create async engine and run migrations via run_sync."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,  # no connection pooling for migrations
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Entrypoint for online migrations -- delegates to async."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### alembic.ini Key Settings

```ini
[alembic]
script_location = alembic
# async connection string -- note the +asyncpg driver
sqlalchemy.url = postgresql+asyncpg://user:pass@localhost:5432/mydb

# use file_template to enforce chronological ordering
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(slug)s-%%(rev)s

# truncate long revision hashes for readability
truncate_slug_length = 40

[post_write_hooks]
hooks = ruff
ruff.type = exec
ruff.executable = ruff
ruff.options = format REVISION_SCRIPT_FILENAME
```

### asyncpg Driver Specifics

asyncpg has behaviors that differ from psycopg2:

```python
# asyncpg does NOT support paramstyle="format" -- use "named" or default
# asyncpg returns native Python types (no string coercion needed)
# asyncpg requires explicit type casts in some raw SQL:

# WRONG with asyncpg
op.execute("UPDATE users SET count = count + '1'")

# RIGHT with asyncpg -- use proper types
op.execute("UPDATE users SET count = count + 1")

# Connection args specific to asyncpg (in env.py or alembic.ini)
connectable = create_async_engine(
    url,
    connect_args={
        "server_settings": {
            "jit": "off",              # disable JIT for faster short queries
            "statement_timeout": "60000",  # 60s timeout for migrations
        },
    },
)
```

## Autogenerate Patterns

### What Autogenerate Detects vs Misses

```
DETECTED AUTOMATICALLY:
  + Table creation / removal
  + Column addition / removal
  + Column type changes (with compare_type=True)
  + Nullable changes
  + Server default changes (with compare_server_default=True)
  + Index addition / removal
  + Named unique constraints
  + Foreign key changes

NOT DETECTED (must write manually):
  - Table or column renames (detected as drop + add)
  - Changes to CHECK constraints
  - Changes to triggers, functions, stored procedures
  - Data migrations / backfills
  - Row-level security policies
  - Enum value additions (use op.execute ALTER TYPE)
  - Partial index WHERE clauses (some cases)
  - Expression-based indexes
```

### Autogenerate Workflow

```bash
# 1. Modify your SQLAlchemy models

# 2. Generate migration
alembic revision --autogenerate -m "add email verified column to users"

# 3. ALWAYS review the generated file -- never blindly apply
#    Check for: incorrect drop+add instead of rename,
#    missing data backfills, enum changes, CHECK constraints

# 4. Apply
alembic upgrade head

# 5. Verify
alembic current
alembic check  # verify models match DB (Alembic 1.9+)
```

### Custom Autogenerate Filters

Exclude tables you don't want Alembic to manage (e.g., spatial_ref_sys, alembic_version):

```python
# In env.py
def include_name(name, type_, parent_names):
    if type_ == "table":
        return name not in {"spatial_ref_sys", "alembic_version"}
    return True

context.configure(
    connection=connection,
    target_metadata=target_metadata,
    include_name=include_name,
    # Exclude specific schemas
    include_schemas=False,
)
```

### Adding PostgreSQL Enums

Autogenerate does not handle adding values to existing enums. Write these manually:

```python
def upgrade() -> None:
    # Adding a value to an existing enum (PostgreSQL)
    # NOTE: ALTER TYPE ... ADD VALUE cannot run inside a transaction
    op.execute("COMMIT")  # end the current transaction
    op.execute("ALTER TYPE status_enum ADD VALUE IF NOT EXISTS 'archived'")


def downgrade() -> None:
    # PostgreSQL does not support removing enum values
    # Document this as a non-reversible migration
    pass
```

## Batch Operations

`op.batch_alter_table` is critical for SQLite (which lacks ALTER TABLE support for most operations) and safe to use on all backends.

### Enable Batch Mode Globally

```python
# In env.py -- makes autogenerate emit batch syntax
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_as_batch=True,  # all autogenerated ops use batch_alter_table
)
```

### Batch Operation Syntax

```python
def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("phone", sa.String(20), nullable=True))
        batch_op.alter_column(
            "email",
            existing_type=sa.String(255),
            nullable=False,
        )
        batch_op.create_index("ix_users_phone", ["phone"])
        batch_op.drop_column("legacy_field")


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("legacy_field", sa.String(), nullable=True))
        batch_op.drop_index("ix_users_phone")
        batch_op.alter_column(
            "email",
            existing_type=sa.String(255),
            nullable=True,
        )
        batch_op.drop_column("phone")
```

### Batch Mode with Naming Conventions (SQLite)

When using batch mode on SQLite with naming conventions, pass the convention explicitly:

```python
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

with op.batch_alter_table(
    "users",
    naming_convention=naming_convention,
    recreate="always",  # force table recreation on SQLite
) as batch_op:
    batch_op.drop_constraint("uq_users_email", type_="unique")
```

## Data Migrations

### Backfill Pattern (Schema + Data in Separate Steps)

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade() -> None:
    # Step 1: Add column as nullable with no default
    op.add_column("users", sa.Column("role", sa.String(50), nullable=True))

    # Step 2: Backfill existing rows
    users = table("users", column("id", sa.Integer), column("role", sa.String))
    op.execute(
        users.update().where(users.c.role.is_(None)).values(role="member")
    )

    # Step 3: Now make it non-nullable
    op.alter_column("users", "role", nullable=False, existing_type=sa.String(50))


def downgrade() -> None:
    op.drop_column("users", "role")
```

### Bulk Insert with Ad-Hoc Table

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import date


def upgrade() -> None:
    roles_table = table(
        "roles",
        column("id", sa.Integer),
        column("name", sa.String),
        column("created_at", sa.Date),
    )

    op.bulk_insert(
        roles_table,
        [
            {"id": 1, "name": "admin", "created_at": date(2025, 1, 1)},
            {"id": 2, "name": "member", "created_at": date(2025, 1, 1)},
            {"id": 3, "name": "viewer", "created_at": date(2025, 1, 1)},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE id IN (1, 2, 3)")
```

### Separating Schema vs Data Migrations

Use Alembic's `-x` argument to conditionally run data migrations:

```python
from alembic import context


def upgrade() -> None:
    schema_upgrade()
    if context.get_x_argument(as_dictionary=True).get("data"):
        data_upgrade()


def downgrade() -> None:
    if context.get_x_argument(as_dictionary=True).get("data"):
        data_downgrade()
    schema_downgrade()


def schema_upgrade() -> None:
    op.add_column("orders", sa.Column("total_cents", sa.BigInteger, nullable=True))


def schema_downgrade() -> None:
    op.drop_column("orders", "total_cents")


def data_upgrade() -> None:
    op.execute(
        "UPDATE orders SET total_cents = CAST(total_dollars * 100 AS BIGINT)"
    )


def data_downgrade() -> None:
    op.execute("UPDATE orders SET total_cents = NULL")
```

```bash
# Schema only
alembic upgrade head

# Schema + data
alembic -x data=true upgrade head
```

### Large Table Backfill (Batched)

For tables with millions of rows, backfill in batches to avoid lock escalation and WAL bloat:

```python
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    op.add_column("events", sa.Column("processed", sa.Boolean, nullable=True))

    conn = op.get_bind()
    batch_size = 10_000
    while True:
        result = conn.execute(
            sa.text(
                "UPDATE events SET processed = false "
                "WHERE id IN ("
                "  SELECT id FROM events WHERE processed IS NULL LIMIT :batch"
                ")"
            ),
            {"batch": batch_size},
        )
        if result.rowcount == 0:
            break

    op.alter_column("events", "processed", nullable=False, existing_type=sa.Boolean)
```

## Migration Naming & Organization

### File Template Convention

```ini
# alembic.ini -- chronological ordering with descriptive slugs
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(slug)s-%%(rev)s

# Produces: 2025_03_15_1430-add_user_email_verified-a1b2c3d4e5f6.py
```

### Branch Labels for Feature Work

When multiple developers create migrations concurrently, use branch labels:

```bash
# Developer A creates a migration on their feature branch
alembic revision --autogenerate -m "add billing tables" --branch-label=billing

# Developer B creates a migration on their feature branch
alembic revision --autogenerate -m "add notification prefs" --branch-label=notifications
```

### depends_on for Ordering Guarantees

When one migration must run after another (even across branches):

```python
# In the migration file header
revision = "abc123"
down_revision = "def456"
branch_labels = None
depends_on = ("xyz789",)  # this migration runs after xyz789
```

### Merge Migrations for Resolving Multiple Heads

When two branches merge and Alembic detects multiple heads:

```bash
# Check for multiple heads
alembic heads

# If multiple heads exist, create a merge migration
alembic merge -m "merge billing and notifications" abc123 def456

# This creates a migration with two down_revisions
# revision = "merge_rev"
# down_revision = ("abc123", "def456")
```

```python
# The generated merge migration file
revision = "a1b2c3"
down_revision = ("abc123", "def456")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass  # merge point -- no operations needed


def downgrade() -> None:
    pass
```

### Stamping (Skip Migrations Without Running Them)

When the database is already at a certain state (e.g., created from models directly):

```bash
# Mark the database as being at a specific revision without running migrations
alembic stamp head

# Stamp to a specific revision
alembic stamp abc123

# Useful after initial setup or when adopting Alembic on an existing DB
```

## Rollback Strategies

### Downgrade to Specific Revision

```bash
# Downgrade one step
alembic downgrade -1

# Downgrade to a specific revision
alembic downgrade abc123

# Downgrade to base (all the way back)
alembic downgrade base

# Show what SQL would run without executing
alembic downgrade -1 --sql
```

### Testing Downgrades Before Deploying

```python
# In your CI pipeline or test suite
import subprocess

def test_migration_roundtrip():
    """Verify every migration can go up and back down cleanly."""
    # Upgrade to head
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    # Downgrade to base
    subprocess.run(["alembic", "downgrade", "base"], check=True)
    # Upgrade again (proves reversibility)
    subprocess.run(["alembic", "upgrade", "head"], check=True)
```

### Non-Reversible Migrations

Some operations genuinely cannot be reversed. Document them clearly:

```python
def upgrade() -> None:
    # Drop column containing data we no longer need
    op.drop_column("users", "legacy_hash")


def downgrade() -> None:
    # DATA LOSS: the original legacy_hash values cannot be recovered.
    # This downgrade re-creates the column but data is gone.
    op.add_column(
        "users",
        sa.Column("legacy_hash", sa.String(128), nullable=True),
    )
```

## Testing Migrations

### pytest Fixture for Migration Testing

```python
# tests/test_migrations.py
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import create_async_engine


@pytest.fixture
def alembic_config():
    config = Config("alembic.ini")
    config.set_main_option(
        "sqlalchemy.url",
        "postgresql+asyncpg://test:test@localhost:5432/test_migrations",
    )
    return config


def test_upgrade_to_head(alembic_config):
    """All migrations apply cleanly from base to head."""
    command.upgrade(alembic_config, "head")


def test_downgrade_to_base(alembic_config):
    """All migrations reverse cleanly from head to base."""
    command.upgrade(alembic_config, "head")
    command.downgrade(alembic_config, "base")


def test_up_down_consistency(alembic_config):
    """Upgrade then downgrade every migration individually."""
    from alembic.script import ScriptDirectory

    script = ScriptDirectory.from_config(alembic_config)
    revisions = [r.revision for r in script.walk_revisions()]
    revisions.reverse()  # oldest first

    for rev in revisions:
        command.upgrade(alembic_config, rev)
        command.downgrade(alembic_config, "-1")
        command.upgrade(alembic_config, rev)  # re-apply


def test_model_and_migration_in_sync(alembic_config):
    """Verify no pending model changes exist (Alembic 1.9+ check)."""
    # alembic check exits non-zero if models differ from migrations
    command.check(alembic_config)
```

### CI Pipeline Integration

```yaml
# .github/workflows/migrations.yml
name: Migration Tests
on: [pull_request]

jobs:
  test-migrations:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_migrations
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[test]"
      - run: alembic upgrade head
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_migrations
      - run: alembic downgrade base
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_migrations
      - run: alembic upgrade head  # re-apply proves reversibility
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_migrations
      - run: alembic check  # verify models match DB
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_migrations
```

## Common Mistakes

### 1. Forgetting compare_type in env.py

Without `compare_type=True`, autogenerate silently ignores column type changes.

```python
# WRONG
context.configure(connection=connection, target_metadata=target_metadata)

# RIGHT
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    compare_type=True,
    compare_server_default=True,
)
```

### 2. Using ORM Session in Migrations

Migrations use the `op` module and raw SQL, not the ORM session.

```python
# WRONG: ORM session in migration
from myapp.db import async_session
async with async_session() as session:
    session.add(User(name="admin"))

# RIGHT: use op.execute or op.bulk_insert
op.execute("INSERT INTO users (name) VALUES ('admin')")
```

### 3. Multiple Heads in Production

Never deploy with multiple heads. Always merge before deploying:

```bash
# Check before deploy
alembic heads --verbose

# If more than one head, merge first
alembic merge -m "merge heads" rev1 rev2
alembic upgrade head
```

### 4. Modifying Already-Applied Migrations

Never edit a migration that has been applied to any database. Create a new migration instead.

```bash
# WRONG: editing 2025_01_15-add_users-abc123.py after it ran in staging

# RIGHT: create a correction migration
alembic revision -m "fix users table column type"
```

### 5. Missing server_default When Adding Non-Nullable Columns

```python
# WRONG: fails on tables with existing rows
op.add_column("users", sa.Column("role", sa.String(50), nullable=False))

# RIGHT: provide server_default for existing rows, optionally drop it after
op.add_column(
    "users",
    sa.Column("role", sa.String(50), nullable=False, server_default="member"),
)
# Optionally remove the default after backfill:
op.alter_column("users", "role", server_default=None, existing_type=sa.String(50))
```

### 6. Running Migrations Without NullPool

In migration scripts, connection pooling causes stale connections and timeout issues:

```python
# WRONG: default pool in migration context
connectable = create_async_engine(url)

# RIGHT: NullPool for migrations
from sqlalchemy import pool
connectable = create_async_engine(url, poolclass=pool.NullPool)
```

### 7. Enum Changes Without COMMIT

PostgreSQL's `ALTER TYPE ... ADD VALUE` cannot run inside a transaction:

```python
# WRONG: will fail with "cannot be executed inside a transaction block"
def upgrade() -> None:
    op.execute("ALTER TYPE status_enum ADD VALUE 'archived'")

# RIGHT: commit the current transaction first
def upgrade() -> None:
    op.execute("COMMIT")
    op.execute("ALTER TYPE status_enum ADD VALUE IF NOT EXISTS 'archived'")
```
