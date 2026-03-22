---
name: docker-infrastructure
description: |
  Docker and container infrastructure architect for self-hosted environments. Use when
  building, debugging, optimizing, or managing Docker containers, docker-compose stacks,
  container networking, volumes, or self-hosted services.

  EXPLICIT TRIGGER on: "Docker", "docker-compose", "container", "Dockerfile", "image",
  "volume", "network", "port mapping", "self-hosted", "home server", "home lab",
  "container orchestration", "Docker Hub", "registry", "build image", "multi-stage build",
  "Docker health check", "restart policy", "container logs", "Docker networking",
  "bridge network", "reverse proxy", "Traefik", "nginx proxy", "Portainer",
  "Docker security", "resource limits", "Docker backup".

  Also trigger when discussing infrastructure on Aaron's home server (192.168.1.240)
  or any self-hosted service deployment.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: app-security-architect, n8n-workflow-architect, cloud-migration-playbook
  last-reviewed: "2026-03-21"
  review-trigger: "Docker major version, Compose spec changes, new self-hosted service added"
  capability-assumptions:
    - "Docker Engine and Docker Compose v2 on Linux host"
    - "Home server at 192.168.1.240 running multiple services"
    - "Bash tool for running Docker commands"
  fallback-patterns:
    - "If no Docker access: provide compose files and Dockerfiles as text"
    - "If cloud-only: recommend Cloud Run patterns from cloud-migration-playbook"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: service deployment need, Docker issue, or infrastructure design question
- Output produces: Dockerfile, docker-compose.yml, troubleshooting guide, or architecture plan
- Can chain from: n8n-workflow-architect (deploy n8n stack), app-security-architect (harden containers)
- Can chain into: cloud-migration-playbook (containerized → cloud deployment)
- Orchestrator notes: always verify host OS and Docker version before generating configs

---

## Dockerfile Best Practices

### Multi-Stage Builds (Always Default)
```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
USER 1000:1000
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Key Rules
- **Never run as root** — always set `USER` to non-root
- **Pin base image versions** — `python:3.12.4-slim` not `python:latest`
- **Order layers by change frequency** — dependencies before code (cache efficiency)
- **Use `.dockerignore`** — exclude .git, __pycache__, .env, node_modules
- **No secrets in images** — use runtime env vars or Docker secrets
- **HEALTHCHECK always** — enables orchestrator health monitoring

---

## Docker Compose Patterns

### Standard Service Template
```yaml
services:
  app:
    build: .
    container_name: myapp
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    env_file:
      - .env
    volumes:
      - app-data:/app/data
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

volumes:
  app-data:
  db-data:

networks:
  backend:
    driver: bridge
```

### Service Dependencies
- Always use `depends_on` with `condition: service_healthy`
- Never rely on startup order alone — use health checks
- For services that need warm-up: add `start_period` to healthcheck

### Environment Variables
- **Development:** `env_file: .env` (gitignored)
- **Production:** Docker secrets or external secret manager
- **Never:** hardcode in docker-compose.yml or Dockerfile

---

## Networking

### Network Isolation Pattern
```yaml
networks:
  frontend:   # Public-facing services (reverse proxy)
  backend:    # App servers + databases (internal only)
  monitoring: # Metrics + logging (isolated)
```
- Reverse proxy (Traefik/Nginx) connects to frontend
- App services connect to frontend + backend
- Databases connect to backend only — never exposed to frontend
- Monitoring tools on their own network

### Reverse Proxy with Traefik
```yaml
services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik-certs:/certs
    command:
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443

  myapp:
    labels:
      - traefik.enable=true
      - traefik.http.routers.myapp.rule=Host(`app.mydomain.com`)
      - traefik.http.routers.myapp.entrypoints=websecure
      - traefik.http.services.myapp.loadbalancer.server.port=8080
```

---

## Volume and Data Management

### Backup Strategy
```bash
# Backup a named volume
docker run --rm -v myapp-db-data:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/db-data-$(date +%Y%m%d).tar.gz -C /data .

# Database-specific backup (preferred for databases)
docker exec myapp-db pg_dump -U user mydb | gzip > backups/mydb-$(date +%Y%m%d).sql.gz
```
- **Databases:** Always use the database's native dump tool, not volume snapshots
- **Application data:** Volume tar backup is fine
- **Schedule backups** via cron or n8n workflow
- **Test restores** quarterly — a backup you can't restore is not a backup

### Volume Best Practices
- Named volumes over bind mounts for service data
- Bind mounts only for config files and development hot-reload
- Never store critical data in anonymous volumes
- Label volumes: `docker volume create --label project=myapp db-data`

---

## Container Management

### Restart Policies
| Policy | Use When |
|--------|----------|
| `no` | Development, one-shot containers |
| `unless-stopped` | Production services (default choice) |
| `always` | Critical services that must survive reboot |
| `on-failure:5` | Services that should retry but not loop forever |

### Resource Limits
Always set memory limits in production — a runaway container shouldn't kill your host:
```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: "0.5"
    reservations:
      memory: 256M
```

### Logging
```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```
Without limits, Docker logs can fill your disk. Always configure log rotation.

---

## Monitoring and Troubleshooting

### Quick Diagnostics
```bash
docker ps -a                    # All containers, including stopped
docker logs --tail 100 <name>   # Last 100 log lines
docker stats                    # Live resource usage
docker inspect <name>           # Full container config
docker exec -it <name> sh       # Shell into running container
docker system df                # Disk usage by Docker
```

### Common Issues
| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Container restart loop | App crash on startup | Check logs, verify env vars |
| Port already in use | Another container/process on same port | `docker ps` or `lsof -i :PORT` |
| Volume permission denied | Container user vs host file ownership | Match UID/GID in Dockerfile |
| Out of disk space | Old images/volumes accumulating | `docker system prune -a` (careful) |
| DNS resolution fails between containers | Not on same network | Put services on shared network |

### Cleanup (with caution)
```bash
docker system prune              # Remove stopped containers, unused networks, dangling images
docker image prune -a            # Remove all unused images (careful — rebuilds take time)
docker volume prune              # Remove unused volumes (DANGER — verify no data loss)
```

---

## Security Hardening

- **Read-only root filesystem** where possible: `read_only: true` + tmpfs for /tmp
- **No privileged mode** unless absolutely required (and document why)
- **Drop all capabilities** then add back only what's needed
- **Docker socket access** is root access — limit to Traefik/Portainer only, mount read-only
- **Scan images** with `docker scout` or Trivy before deploying
- **Update base images** monthly — stale images accumulate CVEs

---

## Self-Evaluation (run before presenting output)

Before presenting Docker guidance, silently check:
[ ] Does every Dockerfile use a non-root user?
[ ] Does every compose service have a restart policy and health check?
[ ] Are secrets handled via env_file or Docker secrets, never hardcoded?
[ ] Are resource limits set for production services?
[ ] Is networking isolated (databases not exposed publicly)?
If any check fails, revise before presenting.
