---
name: docker-compose-production
description: Docker Compose production patterns for Python FastAPI services with multi-stage Dockerfiles, health checks, networking, secrets, and volumes. Use when containerizing applications, writing Dockerfiles, or configuring docker-compose stacks.
---

# Docker Compose Production Patterns

Production-grade Docker patterns for Python FastAPI services with PostgreSQL, multi-stage builds, and security hardening.

## When to Apply

- Writing Dockerfiles for Python/FastAPI applications
- Configuring docker-compose for local dev and production
- Setting up health checks and dependency ordering
- Implementing secrets management in containers
- Optimizing image size with multi-stage builds

## Critical Rules

**Multi-stage builds are mandatory**: Never ship build tools in production images

```dockerfile
# WRONG - single stage with dev dependencies
FROM python:3.12
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app"]

# RIGHT - multi-stage with minimal runtime
FROM python:3.12-slim AS builder
WORKDIR /app
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/venv/bin:$PATH"
COPY --from=builder /app/venv /app/venv
COPY app/ ./app/
RUN adduser --disabled-password --no-create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Always use health checks**: Services must declare readiness

```yaml
# WRONG - no health check, depends_on without condition
services:
  api:
    depends_on:
      - postgres

# RIGHT - health checks with condition
services:
  api:
    depends_on:
      postgres:
        condition: service_healthy
```

## Key Patterns

### Production Compose Stack

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    restart: unless-stopped
    ports:
      - "${API_PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 15s
    networks:
      - app-network
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    user: postgres
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${POSTGRES_USER}", "-d", "${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - app-network

volumes:
  postgres-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

### Multi-Stage Dockerfile with Dev Target

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# --- Builder stage ---
FROM base AS builder
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

# --- Dev target ---
FROM base AS development
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements-dev.txt .
RUN /app/venv/bin/pip install -r requirements-dev.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# --- Production target ---
FROM base AS production
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .
RUN adduser --disabled-password --no-create-home --uid 1001 appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose Watch for Development

```yaml
services:
  api:
    build:
      context: .
      target: development
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app:ro
    develop:
      watch:
        - action: sync+restart
          path: ./app
          target: /app/app
        - action: rebuild
          path: requirements.txt
        - action: rebuild
          path: requirements-dev.txt
    depends_on:
      postgres:
        condition: service_healthy
```

### Secrets Management

```yaml
# Use Docker secrets (Swarm) or env_file patterns
services:
  api:
    env_file:
      - .env              # defaults
      - .env.local         # local overrides (gitignored)
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

## Common Mistakes

- **Running as root**: Always add a non-root user with `adduser` and switch with `USER` directive
- **No .dockerignore**: Always create `.dockerignore` excluding `.git`, `__pycache__`, `.venv`, `.env`, `node_modules`, `*.pyc`
- **Fat images**: Use `-slim` or `-alpine` base images; never use the full `python:3.12` image in production
- **No resource limits**: Always set `deploy.resources.limits` for memory and CPU to prevent container resource exhaustion
- **Bind mounts in production**: Use named volumes for data persistence, never bind mounts — they create host dependencies
