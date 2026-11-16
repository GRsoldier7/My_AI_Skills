---
name: homelab-decision-record
description: Use when diagnosing a home-lab fault (Proxmox host, LXC/VM, Prometheus/Alertmanager, Telegram alert routing, backups, SSH keys) or when a change sets a CPU quota, alert threshold, repeat interval, schedule, routing rule, credential path, or architecture choice. Enforces root-cause-first debugging and records the reason as an ADR.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# Home-Lab Decision Record

## 1. Search first
Before proposing any change, search existing ADRs for that host or service (`grep -ril <service> <adr-dir>`). Read matches. If an accepted ADR covers it, cite it; do not re-diagnose or silently contradict it.

## 2. Root-cause gate (no fix without evidence)
All diagnosis is read-only: status, logs, config reads, metrics queries.
1. Observe or reproduce. Record the exact trigger and time (CT).
2. Read the actual error or log line in full; note file:line.
3. Check recent changes: config diffs, package updates, ADRs, history lines.
4. State ONE hypothesis: "X is the cause because Y."
5. Test it with the smallest read-only check. Wrong: form a new hypothesis; do not stack guesses.
6. Evidence names the cause? Only then propose a fix.

## 3. Propose, then change
- Every state change (edit, restart, key change, quota, rule) is a proposal with exact command, backup/snapshot step, and undo. Run it only after Aaron approves that specific change.
- One change at a time. Verify after each: rerun the failing check, confirm metrics and logs.
- After 3 failed fixes, stop. Report what each fix showed and question the design (shared state, coupling, wrong layer) with Aaron before attempt 4.

## 4. Write an ADR when
A change sets or alters a limit, threshold, schedule, repeat interval, routing rule, credential path, or architecture choice. Skip it for pure restarts with no setting changed.

Path: `<runbook-or-vault-project>/adr/ADR-NNN-<slug>.md`, one file per decision, next sequential number.

```
# ADR-NNN: <title>
Date: <YYYY-MM-DD HH:MM CT>
Status: proposed | accepted | superseded by ADR-n
## Context
Symptom, evidence (commands + trimmed outputs, file:line), recent changes.
## Decision
Exact values (e.g. quota 200%, repeat_interval 4h, for: 10m).
## Alternatives considered
Each option and why not.
## Consequences and rollback
Effects, risks; exact undo command or backup path.
## Review trigger
Metric/threshold or date at which to revisit.
```

## 5. Maintain
- Status starts proposed; set accepted only after Aaron approves and the change is verified.
- Never rewrite an accepted ADR. Write a new one and mark the old "superseded by ADR-n".
- Link the ADR path in the task's history line.
- Close with `Shipped: ... · Verified: ... · Effect: ...`.

## Guardrails
- Drafts and read-only diagnosis only; no state change without Aaron's per-action approval.
- No secrets, IPs, or hostnames in ADRs that leave the box; use placeholders (<host-a>, <ct-id>) in any shared copy.
- Never invent evidence; mark unverified items [VERIFY].

_Adapted from: obra/superpowers (systematic-debugging), MIT; addyosmani/agent-skills (documentation-and-adrs), MIT; live homelab-runbook-generator._
