---
name: homelab-life-stack
description: |
  Expert architect for the self-hosted MiniPC homelab stack that powers a life OS — Docker containers, n8n automation, data storage, APIs, and service orchestration running on local hardware. Specializes in: Docker Compose service design, n8n workflow architecture, local API design, service networking, backup strategies, and connecting homelab services to Obsidian and external tools. Use when designing homelab services, Docker Compose setup, n8n installation/configuration, local API design, service dependencies, or asking how to self-host something for your life system. Trigger phrases: "homelab", "docker compose", "n8n setup", "self-host", "minipc", "local server", "container setup", "n8n workflow", "homelab service", "docker stack".
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: obsidian-automation-architect, ai-business-optimizer, biohacking-data-pipeline
  source-repo: GRsoldier7/My_AI_Skills
---

# Homelab Life Stack — Expert Skill

## Stack Architecture (MiniPC Docker)

```
┌─────────────────────────────────────────────────────┐
│                   MiniPC Homelab                    │
├─────────────────────────────────────────────────────┤
│  Reverse Proxy: Traefik / Nginx Proxy Manager       │
├──────────────┬──────────────┬───────────────────────┤
│   Automation │   Data       │   AI / Inference      │
│   n8n        │   PostgreSQL │   Ollama (local LLM)  │
│   Cron jobs  │   Redis      │   Open WebUI          │
├──────────────┼──────────────┼───────────────────────┤
│   Monitoring │   Vault      │   Utilities           │
│   Uptime Kuma│   Obsidian   │   Portainer           │
│   Grafana    │   (sync'd)   │   Watchtower          │
└──────────────┴──────────────┴───────────────────────┘
```

## Core Docker Compose Structure

```yaml
# docker-compose.yml — Life Stack Foundation
version: "3.9"

services:
  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - WEBHOOK_URL=http://YOUR_LOCAL_IP:5678
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=homelab
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

  portainer:
    image: portainer/portainer-ce:latest
    restart: unless-stopped
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data

  uptime-kuma:
    image: louislam/uptime-kuma:latest
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - kuma_data:/app/data

volumes:
  n8n_data:
  postgres_data:
  redis_data:
  portainer_data:
  kuma_data:
```

## n8n Workflow Categories for Life OS

```
📁 n8n Workflows/
├── 00_Daily/
│   ├── Daily Note Creator (6am)
│   ├── Overdue Task Alert (8am)
│   └── End-of-Day Summary (9pm)
├── 01_Work/
│   ├── Calendar → Obsidian Sync
│   └── Email Priority Tagger
├── 02_Consulting/
│   ├── Time Log Webhook
│   ├── Invoice Reminder
│   └── Client Check-in Scheduler
├── 03_Business/
│   ├── Revenue Tracker
│   └── Lead Pipeline Updater
├── 04_Health/
│   ├── Health API Ingestion (daily)
│   └── Supplement Reminder
└── 05_Vault/
    ├── Inbox Processor (weekly)
    └── Vault Backup Verifier
```

## Service Networking Rules

- All services communicate on internal Docker network (`homelab_network`)
- Only n8n, Portainer, Uptime Kuma exposed to host (via ports)
- PostgreSQL and Redis NEVER exposed to external network
- Webhook endpoints use n8n's built-in HTTPS with basic auth
- Traefik handles SSL termination if exposing to internet

## Backup Strategy

```
BACKUP TIERS:
Tier 1 (Daily, automated):
  - PostgreSQL: pg_dump → compressed .sql.gz → NAS share
  - n8n workflows: export via n8n API → JSON → git commit
  - Obsidian vault: Remotely-Save → cloud (OneDrive/S3)

Tier 2 (Weekly):
  - Full Docker volume backup → NAS
  - Configuration files (.env, docker-compose.yml) → git

Tier 3 (Monthly):
  - Full system image → external drive
  - Test restore from Tier 1 backup (critical — backup untested = no backup)
```

## Environment Variable Management

```bash
# .env file structure (NEVER commit to git)
# PostgreSQL
POSTGRES_USER=homelab
POSTGRES_PASSWORD=[strong-random-password]

# n8n
N8N_USER=admin
N8N_PASSWORD=[strong-random-password]
N8N_ENCRYPTION_KEY=[32-char-random-key]

# APIs (populated as services are added)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Paths
OBSIDIAN_VAULT_PATH=C:/Users/Admin/Desktop/Desktop Folders/Obsidian/Homelab
```

## Service Addition Protocol

When adding a new service to the homelab:
1. Find official Docker image (prefer slim/alpine variants)
2. Add to `docker-compose.yml` with restart policy and volume
3. Add any required env vars to `.env` and `.env.example`
4. Add health check to Uptime Kuma
5. Document in `docs/services.md` — what it does, port, credentials location
6. Test backup/restore for any stateful service

## Anti-Patterns

1. **Exposing PostgreSQL to internet** — Never. Use SSH tunnel or VPN for remote access.
2. **Credentials in docker-compose.yml** — Always use `${VAR}` from `.env`.
3. **No health monitoring** — Every service in Uptime Kuma before trusting it.
4. **Single point of storage** — If n8n data is only in Docker volume with no backup, a disk failure kills all workflows.
5. **Latest tags in production** — Pin image versions (`postgres:16-alpine` not `postgres:latest`) to avoid surprise breaking changes.

## Quality Gates
- [ ] All services in docker-compose.yml have `restart: unless-stopped`
- [ ] PostgreSQL and Redis not exposed on host ports in production
- [ ] `.env` in `.gitignore`, `.env.example` committed
- [ ] Daily backup automation running and verified
- [ ] All services monitored in Uptime Kuma
- [ ] n8n workflow exports committed to git weekly
- [ ] Service docs updated whenever new container added
