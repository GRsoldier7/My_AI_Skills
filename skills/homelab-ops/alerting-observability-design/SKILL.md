---
name: alerting-observability-design
description: >-
  Use when designing, reviewing, or de-noising alerting and observability for a
  home lab running Prometheus, Loki, Grafana, and Alertmanager.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Alerting & Observability Design

## Principles
- Alert on user-visible symptoms (service down, requests failing, disk full), not causes.
- Define 3-7 critical SLIs; every alert must be actionable. Home-lab SLOs (about 99.5-99.9%), not enterprise ones.
- Tiers: critical (page), warning (investigate soon), info (daily digest).
- RED for services (rate, errors, duration); USE for resources (utilization, saturation, errors).

## Workflow
1. **SLIs/SLOs:** list critical services, available exporters (node_exporter, cAdvisor, blackbox), pain points, channels, maintenance windows.
2. **Rules:** each has `for:` (2-10m), a `severity` label, a `summary`, and a `runbook_url`. Cover up/down, disk/memory, cert expiry (<7d), backup freshness (>48h), restart loops, and **staleness** (alert when a metric or textfile timestamp stops updating, not just on its value).
3. **Dead man's switch:** an always-firing `vector(1)` alert routed to an external heartbeat; also watch every independent watchdog's last-run time.
4. **Noise:** group by alertname+instance (group_wait 30s, group_interval 5m, repeat_interval 4h); inhibit dependents when a root cause fires (e.g., if all proxied hosts fail TLS, alert once on the proxy/cert); silence before planned work.
5. **Routing:** critical to pager (ntfy, Pushover, Telegram), warning to chat, info to digest. All URLs and tokens as `<PLACEHOLDER>`.
6. **Dashboards:** an overview (uptime, cert days, disk, backup freshness, recent alerts) drilling down to USE/RED views.
7. **Monthly hygiene:** fix alerts firing >5x/month, expire stale silences, check runbooks and thresholds, test each receiver, confirm the dead man's switch.

## Output
Draft `prometheus_rules.yml` and `alertmanager.yml` snippets plus a short table: alert, severity, why, runbook.

## Guardrails
- Drafts only; the user reviews and applies. No changes to live systems without explicit approval.
- Mark assumed metric names and thresholds `VERIFY`.
- No secrets in output; use `<PLACEHOLDER>`.
- No commands that modify production.

_Adapted from: alirezarezvani/claude-skills (observability-designer, slo-architect), MIT._
