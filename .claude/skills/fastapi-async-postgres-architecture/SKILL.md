---
name: fastapi-async-postgres-architecture
description: FastAPI project structure with async SQLAlchemy ORM, Pydantic v2 models, and PostgreSQL. Use when building scalable APIs with dependency injection, CRUD operations, domain-driven architecture, or migrating from sync to async patterns.
---

# FastAPI Async PostgreSQL Architecture

Domain-driven FastAPI architecture with async SQLAlchemy ORM, Pydantic v2 models, and dependency injection patterns.

## When to Apply

- Building FastAPI APIs with PostgreSQL and async operations
- Implementing CRUD services with SQLAlchemy async ORM
- Setting up domain-based project structure for scalable applications
- Configuring Pydantic v2 models with SQLAlchemy integration

## Critical Rules

**Async Session Management**: Always use async context managers and proper session lifecycle

```python
# WRONG - sync session in async context
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# RIGHT - async session with proper context
async def get_user(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
```

**Domain Structure**: Organize by domain modules, not file types

```python
# WRONG - generic structure
src/
├── models/
├── schemas/
├── routers/
└── services/

# RIGHT - domain-based structure
src/
├── auth/
│   ├── models.py
│   ├── schemas.py
│   ├── router.py
│   ├── service.py
│   └── dependencies.py
├── posts/
│   ├── models.py
│   ├── schemas.py
│   └── router.py
└── database.py
```

## Key Patterns

### Database Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    pass

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### Model Definition

```python
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    posts: Mapped[List["Post"]] = relationship(back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    user: Mapped["User"] = relationship(back_populates="posts")
```

### Pydantic Schema Integration

```python
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    posts: list["PostResponse"] = []
```

### Service Layer with CRUD

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user_with_posts(self, user_id: int) -> User | None:
        stmt = select(User).options(selectinload(User.posts)).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
```

### Dependency Injection

```python
from fastapi import Depends, HTTPException

async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)

async def valid_user_id(
    user_id: int, 
    service: UserService = Depends(get_user_service)
) -> User:
    user = await service.get_user_with_posts(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Router Implementation

```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(user_data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user: User = Depends(valid_user_id)):
    return user

@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
):
    return await service.list_users(skip, limit)
```

## Common Mistakes

- **Mixing sync/async**: Don't use sync SQLAlchemy methods in async contexts — use `await session.execute()` not `session.query()`
- **Session leaks**: Always use async context managers (`async with session:`) to ensure proper cleanup
- **Missing selectinload**: Use `selectinload()` for related objects to avoid N+1 queries in async contexts
- **Generic dependencies**: Create domain-specific validation dependencies instead of generic database lookups