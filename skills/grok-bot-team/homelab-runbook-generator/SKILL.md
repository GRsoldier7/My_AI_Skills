---
name: homelab-runbook-generator
description: >-
  Use when a home-lab service (Proxmox VM/LXC, n8n, NPM proxy,
  Prometheus/Grafana/Loki, an agent stack) alerts or fails, before a risky
  change, or after an incident to write a runbook or post-incident note.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Home-Lab Runbook Generator

## Inputs
Service name, alert or symptom, host and VM/CT id, dependencies (DNS, proxy, storage, databases, APIs), recent changes, and access method.

## Workflow
1. **Scope:** service, purpose, type (VM/LXC/Docker/systemd/agent), host, ids.
2. **Dependencies:** host and storage pool, network/IP, DNS, reverse proxy (upstream, cert source), monitoring (scrape job, dashboard, log source), upstream and downstream services.
3. **Read-only health checks,** tagged [READ-ONLY]: `pct status`/`qm status`, `systemctl status`, `systemctl list-timers`, `journalctl -u <svc> --since ...`, `docker ps`/`docker logs --tail 50`, `df -h`, `ping`/`curl -I`/`dig`, `pvesm status`.
4. **Triage tree:** symptom, then likely causes, then a read-only check for each, then a fix tagged [CHANGES-STATE]. Include the escalation path.
5. **Before any change:** snapshot the VM or CT, back up the config file, and write exact rollback steps, all as proposals.
6. **Verify after the fix:** rerun the checks, confirm upstream and downstream, metrics back to normal, logs clean, a real user test passes.
7. **Escalate if stuck:** preserve state (don't restart impulsively), snapshot, collect logs, record what was tried.
8. **Post-incident note:** time, severity, duration, impact, timeline, root cause, fix, prevention items (including the monitoring gap that let it go unnoticed), lessons. Unknowns [VERIFY].

## Output
```
# Runbook: <service> | host <node> | id <ctid> | updated <date>
Dependencies | Health checks [READ-ONLY]
Triage: symptom -> cause -> check -> fix [CHANGES-STATE, needs approval]
Backup & rollback | Verification | Escalation
```

## Guardrails
- No [CHANGES-STATE] command runs without the owner's explicit approval for that specific change.
- Nothing is deleted or purged without a verified backup.
- No secrets in runbooks; use placeholders.
- Mark unknown values [VERIFY].

_Adapted from: alirezarezvani/claude-skills (runbook-generator, incident-commander), MIT._
