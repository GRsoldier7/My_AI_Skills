#!/usr/bin/env bash
# Phase A — Container audit
# Outputs JSON to stdout. Safe to run on Proxmox (uses pct/qm; falls back gracefully).
set -uo pipefail

AUDIT_DIR="${AUDIT_DIR:-/root/homelab/docs/organizer/AUDIT-$(date +%Y-%m-%d)}"
STATE_FILE="${STATE_FILE:-/root/homelab/docs/organizer/state.yaml}"
HOMELAB_LXC_DOC="${HOMELAB_LXC_DOC:-/root/homelab/lxc}"
HOMELAB_CT_DOC="${HOMELAB_CT_DOC:-/root/homelab/containers}"

have() { command -v "$1" >/dev/null 2>&1; }

if ! have pct && ! have qm; then
  echo '{"audit_date":"'"$(date +%Y-%m-%d)"'","error":"pct/qm not available — not on a Proxmox host","containers":[],"drift_summary":{}}'
  exit 0
fi

# In-container probe — read-only, single round-trip per container
PROBE='cat <<EOF
{
  "uptime": "$(uptime -p 2>/dev/null | sed "s/\"/\\\\\"/g")",
  "disk_root_pct": "$(df -h / 2>/dev/null | awk "NR==2 {print \$5}")",
  "log_files_24h": $(find /var/log -mtime -1 -type f 2>/dev/null | wc -l),
  "services_up": "$(systemctl list-units --type=service --state=running --no-legend --no-pager 2>/dev/null | awk "{print \$1}" | head -20 | tr "\n" "," | sed "s/,\$//")",
  "pkgs_outdated": $(apt list --upgradable 2>/dev/null | grep -c upgradable || echo 0)
}
EOF'

emit_container_json() {
  local id="$1" type="$2"
  local status config probe_out
  if [[ "$type" == "lxc" ]]; then
    status=$(pct status "$id" 2>/dev/null | awk "{print \$2}")
    config=$(pct config "$id" 2>/dev/null | head -40)
    if [[ "$status" == "running" ]]; then
      probe_out=$(pct exec "$id" -- bash -c "$PROBE" 2>/dev/null || echo '{}')
    else
      probe_out='{}'
    fi
  else
    status=$(qm status "$id" 2>/dev/null | awk "{print \$2}")
    config=$(qm config "$id" 2>/dev/null | head -40)
    probe_out='{}'
  fi
  # Minimal config extract
  local ram disk hostname
  ram=$(grep -oE '^memory:\s*[0-9]+' <<<"$config" | awk '{print $2}')
  disk=$(grep -oE 'rootfs:.*size=[0-9]+G' <<<"$config" | grep -oE '[0-9]+G' | head -1)
  hostname=$(grep -oE '^hostname:\s*\S+' <<<"$config" | awk '{print $2}')
  cat <<JSON
{
  "id": "$id",
  "type": "$type",
  "status": "${status:-unknown}",
  "hostname": "${hostname:-}",
  "ram_mb": ${ram:-0},
  "disk_alloc": "${disk:-}",
  "probe": $probe_out
}
JSON
}

# Build container list
declare -a entries
if have pct; then
  while read -r line; do
    [[ -z "$line" ]] && continue
    [[ "$line" == VMID* ]] && continue
    id=$(awk '{print $1}' <<<"$line")
    [[ -z "$id" ]] && continue
    entries+=("$(emit_container_json "$id" lxc)")
  done < <(pct list 2>/dev/null)
fi
if have qm; then
  while read -r line; do
    [[ -z "$line" ]] && continue
    [[ "$line" == *VMID* ]] && continue
    id=$(awk '{print $1}' <<<"$line")
    [[ -z "$id" ]] && continue
    entries+=("$(emit_container_json "$id" vm)")
  done < <(qm list 2>/dev/null)
fi

# Drift detection — compare to docs
declare -a undocumented orphaned naming_mismatch
if [[ -d "$HOMELAB_LXC_DOC" ]]; then
  documented_ids=$(find "$HOMELAB_LXC_DOC" "$HOMELAB_CT_DOC" -maxdepth 2 -type f \( -name '*.md' -o -name '*.yaml' \) 2>/dev/null \
    | xargs -r grep -hoE '(CT|VM)[[:space:]]?#?[0-9]{2,3}|^id:[[:space:]]*[0-9]{2,3}' 2>/dev/null \
    | grep -oE '[0-9]{2,3}' | sort -u)
fi
real_ids=$(echo "${entries[*]}" | grep -oE '"id": "[0-9]+"' | grep -oE '[0-9]+' | sort -u)

for id in $real_ids; do
  if ! grep -qx "$id" <<<"$documented_ids" 2>/dev/null; then
    undocumented+=("$id")
  fi
done
for id in $documented_ids; do
  if ! grep -qx "$id" <<<"$real_ids" 2>/dev/null; then
    orphaned+=("$id")
  fi
done

# Emit final JSON
{
  echo '{'
  echo '  "audit_date": "'"$(date +%Y-%m-%d)"'",'
  echo '  "containers": ['
  for i in "${!entries[@]}"; do
    printf '%s' "${entries[$i]}"
    [[ $i -lt $((${#entries[@]} - 1)) ]] && echo ',' || echo ''
  done
  echo '  ],'
  echo '  "drift_summary": {'
  echo '    "undocumented": ['"$(printf '"%s",' "${undocumented[@]}" | sed 's/,$//')"'],'
  echo '    "orphaned_docs": ['"$(printf '"%s",' "${orphaned[@]}" | sed 's/,$//')"'],'
  echo '    "naming_mismatches": []'
  echo '  }'
  echo '}'
}
