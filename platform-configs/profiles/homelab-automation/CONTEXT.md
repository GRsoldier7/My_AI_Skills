# homelab-automation context contract

Public template, not a populated private profile or proof of native host discovery.

- Selection: `platform-configs/skill-sets/manifest.json` → `homelab-automation`.
- Review due: 2026-11-25; review state: structural draft.
- Behavioral test result: not run on any target host.

## Purpose

Design around the existing automation and agent services. This profile is blocked until n8n guidance is corrected.

## Context authority and boundaries

Keep skill procedures in Git; flow exports are versioned derivatives. Reuse n8n, self-hosted connector flows, existing agents and household automation according to their present owners. No new gateway is assumed.

The private overlay identifies its owner, project, approved data/tools and authoritative context path. If a Spec Kit constitution/plan or existing project context already owns these facts, link it; do not maintain a competing copy here. Select only the applicable context, not every profile.

## First acceptance task

Design a synthetic scheduled report with explicit inputs, idempotency, retry limit, failure notification and exported workflow; do not connect to or change live infrastructure.

Run on each claimed target tool using synthetic inputs first. Record tool/version, selected source revision, input fixture, observed result, correction effort and pass/fail. Compilation alone does not pass this task.
