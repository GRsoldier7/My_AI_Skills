#!/usr/bin/env bash
# Phase A — Container audit
# Outputs JSON to stdout. Safe to run on Proxmox (uses pct/qm; falls back gracefully).
set -uo pipefail

AUDIT_DIR="${AUDIT_DIR:-/root/homelab/docs/organizer/AUDIT-$(date +%Y-%m-%d)}"
STATE_FILE="${STATE_FILE:-/root/homelab/docs/organizer/state.yaml}"
HOMELAB_LXC_DOC="${HOMELAB_LXC_DOC:-/root/homelab/lxc}"
HOMELAB_CT_DOC="${HOMELAB_CT_DOC:-/root/homelab/containers}"
HOMELAB_VM_DOC="${HOMELAB_VM_DOC:-/root/homelab/vms}"

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

# Build container list (track IDs by type as we go — avoids regex parsing later)
declare -a entries lxc_ids vm_ids
if have pct; then
  while read -r line; do
    [[ -z "$line" ]] && continue
    [[ "$line" == VMID* ]] && continue
    id=$(awk '{print $1}' <<<"$line")
    [[ "$id" =~ ^[0-9]+$ ]] || continue
    entries+=("$(emit_container_json "$id" lxc)")
    lxc_ids+=("$id")
  done < <(pct list 2>/dev/null)
fi
if have qm; then
  while read -r line; do
    [[ -z "$line" ]] && continue
    [[ "$line" == *VMID* ]] && continue
    id=$(awk '{print $1}' <<<"$line")
    [[ "$id" =~ ^[0-9]+$ ]] || continue
    entries+=("$(emit_container_json "$id" vm)")
    vm_ids+=("$id")
  done < <(qm list 2>/dev/null)
fi

# Drift detection — compare to docs
# Primary signal: folder-name convention `<id>-<name>` in /root/homelab/lxc/
# Secondary signal: explicit "CT N" / "VM N" mentions in doc content
declare -a undocumented_lxc undocumented_vm orphaned naming_mismatch
documented_ids=""
if [[ -d "$HOMELAB_LXC_DOC" || -d "$HOMELAB_VM_DOC" ]]; then
  # Folder convention — primary signal. Track LXC and VM separately for accurate drift.
  documented_lxc_ids=$(ls -d "$HOMELAB_LXC_DOC"/*/ 2>/dev/null | xargs -n1 -r basename | grep -oE '^[0-9]{2,3}' | sort -u)
  documented_vm_ids=$(ls -d "$HOMELAB_VM_DOC"/*/ 2>/dev/null | xargs -n1 -r basename | grep -oE '^[0-9]{2,3}' | sort -u)
  # Content grep — secondary; require explicit prefix to avoid matching "100MB" etc
  content_ids=$(find "$HOMELAB_LXC_DOC" "$HOMELAB_CT_DOC" "$HOMELAB_VM_DOC" -maxdepth 3 -type f \( -name '*.md' -o -name '*.yaml' \) 2>/dev/null \
    | xargs -r grep -hoE '(CT|VM|VMID)[[:space:]]+#?[0-9]{2,3}|^id:[[:space:]]*[0-9]{2,3}' 2>/dev/null \
    | grep -oE '[0-9]{2,3}' | sort -u)
  documented_ids=$(printf '%s\n%s\n%s\n' "$documented_lxc_ids" "$documented_vm_ids" "$content_ids" | sort -u)
fi
# Real IDs split by type
real_ids=$(printf '%s\n' "${lxc_ids[@]:-}" "${vm_ids[@]:-}" | grep -E '^[0-9]+$' | sort -u)

for id in "${lxc_ids[@]:-}"; do
  [[ -z "$id" ]] && continue
  # An LXC is documented if it has a folder in lxc/ OR a content reference (anywhere)
  if ! { grep -qx "$id" <<<"$documented_lxc_ids" 2>/dev/null || grep -qx "$id" <<<"$content_ids" 2>/dev/null; }; then
    undocumented_lxc+=("$id")
  fi
done
for id in "${vm_ids[@]:-}"; do
  [[ -z "$id" ]] && continue
  # A VM is documented if it has a folder in vms/ OR a content reference (anywhere)
  if ! { grep -qx "$id" <<<"$documented_vm_ids" 2>/dev/null || grep -qx "$id" <<<"$content_ids" 2>/dev/null; }; then
    undocumented_vm+=("$id")
  fi
done
# Orphaned docs: track by source location, not just ID — an LXC folder for an ID that's actually a VM is "misfiled", not orphaned
for id in $documented_lxc_ids; do
  [[ -z "$id" ]] && continue
  if grep -qx "$id" <<<"$(printf '%s\n' "${lxc_ids[@]:-}")" 2>/dev/null; then continue; fi
  # ID has an lxc/ folder doc but no matching LXC. Could be: (a) deleted CT, (b) misfiled VM doc.
  if grep -qx "$id" <<<"$(printf '%s\n' "${vm_ids[@]:-}")" 2>/dev/null; then
    naming_mismatch+=("lxc/${id}-* but ID is a VM (should be in vms/)")
  else
    orphaned+=("$id")
  fi
done
for id in $documented_vm_ids; do
  [[ -z "$id" ]] && continue
  if grep -qx "$id" <<<"$(printf '%s\n' "${vm_ids[@]:-}")" 2>/dev/null; then continue; fi
  if grep -qx "$id" <<<"$(printf '%s\n' "${lxc_ids[@]:-}")" 2>/dev/null; then
    naming_mismatch+=("vms/${id}-* but ID is an LXC (should be in lxc/)")
  else
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
  echo '    "undocumented_lxc": ['"$(printf '"%s",' "${undocumented_lxc[@]:-}" | sed 's/^,//;s/,$//')"'],'
  echo '    "undocumented_vm": ['"$(printf '"%s",' "${undocumented_vm[@]:-}" | sed 's/^,//;s/,$//')"'],'
  echo '    "orphaned_docs": ['"$(printf '"%s",' "${orphaned[@]:-}" | sed 's/^,//;s/,$//')"'],'
  echo '    "naming_mismatches": []'
  echo '  }'
  echo '}'
}
