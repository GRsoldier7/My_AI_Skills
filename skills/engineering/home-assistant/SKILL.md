---
name: home-assistant
description: |
  Operate Home Assistant (HAOS VM 100 @ 192.0.2.11) from Claude Code via the
  ha-mcp MCP server, hass-cli, or the HA REST/WebSocket API. Routes between
  tools by task: live device control + automation editing → ha-mcp; scripted
  ops + state dumps + bulk queries → hass-cli; backup/restore + Supervisor
  add-on lifecycle → REST `/api/hassio/`. Covers token rotation, ZHA pairing,
  add-on management, Lovelace dashboard edits, automation YAML idioms, and
  the backup pipeline.

  Trigger phrases: "home assistant", "HAOS", "HA automation", "Lovelace
  dashboard", "ZHA", "Zigbee2MQTT", "Mosquitto", "HACS", "ESPHome", "Matter",
  "Thread border router", "OTBR", "hass-cli", "ha-mcp", "smart home",
  "homeassistant.local", "192.0.2.11:8123", entity_id patterns
  (`light.`, `switch.`, `sensor.`, `binary_sensor.`, `climate.`, `media_player.`),
  service_id patterns (`light.turn_on`, `automation.trigger`, etc.).

  Auto-trigger when the user mentions: any of the above, configuring smart
  devices, smart-home automation design, pairing Zigbee/Matter/Thread devices,
  Home Assistant backup/restore, debugging an HA integration, or asking to
  control a specific device by name.

  Plugin overlap: this skill owns the OPERATOR layer for HA — running tools,
  validating tokens, walking add-on installs, drafting automation YAML. For
  the BACKEND-AS-A-SERVICE shape (LiveWello, Vaultwarden), do not route here.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: docker-infrastructure, mcp-server-builder, app-security-architect
  last-reviewed: "2026-05-16"
  review-trigger: "ha-mcp v8 release, HA Core major (every 4 months), Matter 1.4+ rollout"
---

# Home Assistant — Operator Skill

Drives HAOS VM 100 (`haos16.2` / Core 2025.9.3+) at `192.0.2.11:8123`. Tailscale-only off-LAN. Two long-lived tokens segregate blast radius: `homelab-backup` for backups, `claude-mcp` for AI/MCP traffic.

## Tool routing

| Goal | Tool | Why |
|---|---|---|
| Control a device / call a service / inspect state | **ha-mcp** MCP server | Structured tool surface (89 tools), reads exposed-entities allow-list |
| Bulk state dump, entity registry export, scripted ops | **hass-cli** (PyPI `homeassistant-cli`) | CSV/JSON output, easy pipes, low latency |
| Add-on install/restart/uninstall | **REST `/api/hassio/*`** with `claude-mcp` token | Supervisor endpoints, no CLI parity |
| Backup / restore | `/api/hassio/backups/*` via [haos-bundle.sh](/root/homelab/scripts/app-backups/haos-bundle.sh) | Native HA snapshot includes config + add-ons + history |
| Live event tail | **WebSocket** `/api/websocket` | hass-cli's `events watch` wraps this |
| One-off YAML edit | File Editor add-on **OR** SSH add-on | No API for raw YAML; Supervisor exposes via Web Terminal |

When in doubt: try ha-mcp first; fall back to hass-cli; only hit raw REST for endpoints neither covers.

## Secrets & credentials

- Operator break-glass admin login: `/root/homelab/infra/haos-admin.env` (mode 0600). NEVER read into chat, log, or commit. Only used for manual UI tasks (HACS GitHub OAuth, integration setup).
- Backup token (`homelab-backup`): `/root/homelab/infra/haos-backup.env`. Drives `haos-bundle.sh`.
- MCP token (`claude-mcp`): `/root/homelab/infra/haos-mcp.env`. Drives ha-mcp Add-on + check-ha-mcp.sh + Claude Code MCP client.
- Rotation: `/root/homelab/scripts/setup/rotate-haos-tokens.sh` walks the manual flow with atomic rewrite + validation.
- Leak response: revoke in HA Profile → Security → trash icon, then re-run rotate script. The Stop hook at `/root/.claude/hooks/security-audit.sh` flags `HAOS_ADMIN_PASSWORD=` and `HAOS_TOKEN=eyJ` patterns outside `.env` files.

## Common workflows

### 1. List entities (Claude Code with ha-mcp installed)
> Ask: "List all my light entities and their state."

ha-mcp will call its `get_entities` tool filtered by domain `light`.

### 2. Bulk state dump (shell)
```sh
hass-cli state list -o table | head -30
hass-cli entity get sensor.living_room_temperature
hass-cli service call light.turn_off --arguments entity_id=light.living_room
```
`HASS_SERVER` and `HASS_TOKEN` should be exported in `/root/.bashrc` from `haos-backup.env`.

### 3. Trigger a one-off backup
```sh
/root/homelab/scripts/app-backups/haos-bundle.sh
```
Bundles land at `/mnt/pve/synology-backups/dump/`. Daily run is already wired into `app-backups.timer`.

### 4. Restart an add-on (e.g., ha-mcp)
```sh
. /root/homelab/infra/haos-mcp.env
curl -fsS -X POST -H "Authorization: Bearer $HAOS_MCP_TOKEN" \
  "$HAOS_URL/api/hassio/addons/homeassistant_ai_ha_mcp/restart"
```
Slug is the add-on's Supervisor slug — find via `GET /api/hassio/addons`.

### 5. Pair a new Zigbee device (ZHA)
1. HA UI → Settings → Devices & Services → ZHA → Configure → Add Devices.
2. Put device into pairing mode (manufacturer-specific).
3. Wait ~60 s. Device appears with auto-derived entity ids.
4. Rename via UI to match your naming convention (area + function, e.g., `light.kitchen_under_cabinet`).

### 6. Draft an automation
Automations live at `/config/automations.yaml` (mounted in HAOS). Pattern:
```yaml
- id: morning_lights_on
  alias: Morning lights on at sunrise
  trigger:
    - platform: sun
      event: sunrise
      offset: '-00:30:00'
  condition:
    - condition: state
      entity_id: input_boolean.away_mode
      state: 'off'
  action:
    - service: light.turn_on
      target:
        area_id: kitchen
      data:
        brightness_pct: 40
  mode: single
```
Validate via `ha core check` (in the Supervisor SSH add-on) before reload.

## Architecture & where things live

- **VM 100** (`haos16.2`, 4 GB RAM, 32 GB disk, 2 cores, vmbr0 bridge, `onboot=1 startup=order=4`)
- **Backup bundle**: [haos-bundle.sh](/root/homelab/scripts/app-backups/haos-bundle.sh)
- **PVE-level snapshot**: VMID 100 in `/etc/pve/jobs.cfg` `backup-stateful-daily`
- **DNS**: AdGuard CT 204 — local rewrites for `ha.lab`
- **Reverse proxy**: NPM CT 206 — public Cloudflare DNS exists but not wired (Tailscale only)
- **Tailscale**: HAOS Add-on `core_tailscale` adds VM 100 as a tailnet node
- **Healthcheck**: `/root/homelab/scripts/checks/check-ha-mcp.sh` + systemd timer (every 5 min)

## What NOT to do

- **Do NOT** auto-update the ha-mcp Add-on — it's a third-party component; pin a version and review release notes before bumping.
- **Do NOT** delete `homelab-backup` token while leaving `claude-mcp` in place (or vice versa) — they're separate by design. Rotate both via the script.
- **Do NOT** install Mosquitto unless adding a Zigbee2MQTT/Tasmota/ESPHome device. ZHA path needs no broker.
- **Do NOT** expose `homeassistant.deeznutz.com` publicly without an Authelia/Authentik in front. Cloudflare DNS exists but no proxy host configured.
- **Do NOT** echo `HAOS_ADMIN_PASSWORD` or `HAOS_TOKEN` values into any chat output, log, or committed file. Hooks will flag and noise the session.

## Future-proof tripwires (review every quarter)

- `homeassistant-ai/ha-mcp` release notes — breaking tool-surface changes
- HA Core major version (every 4 months) — recorder schema migration, Lovelace YAML deprecations
- Matter 1.4+ rollout — when first Thread device arrives, install OTBR add-on AND disable multicast snooping on `vmbr0` (Proxmox bridge) — documented community issue
- ZHA → Zigbee2MQTT migration only if a specific device requires Z2M extensions
- HACS auth model — token rotation is GitHub OAuth; refresh on GitHub Personal-Access-Token expiry

## Quick verification

```sh
# Backup token alive
curl -fsS -H "Authorization: Bearer $HAOS_TOKEN" http://192.0.2.11:8123/api/

# MCP add-on alive
curl -sS -o /dev/null -w '%{http_code}\n' http://192.0.2.11:8099/

# hass-cli wired
hass-cli info

# Claude MCP registered
claude mcp list | grep home-assistant
```
