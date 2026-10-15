#!/usr/bin/env bash
# Audit orchestrator — runs Phase A-C in sequence, drops intermediates into AUDIT_DIR.
# Phase D (REPORT.md) and Phase E (approval) are handled by the skill (Claude), not this script.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORGANIZER_DIR="${ORGANIZER_DIR:-/root/homelab/docs/organizer}"
AUDIT_DATE="$(date +%Y-%m-%d)"
export AUDIT_DIR="$ORGANIZER_DIR/AUDIT-$AUDIT_DATE"

mkdir -p "$AUDIT_DIR"

PHASES="${1:-all}"

# A phase that crashes still leaves its output file behind; gate on rc AND parseable JSON
run_checked() {
  local label="$1" script="$2" out="$3" rc
  echo "[$label] → $out" >&2
  bash "$SCRIPT_DIR/$script" > "$out"
  rc=$?
  if (( rc != 0 )) || ! python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$out" 2>/dev/null; then
    echo "[$label] FAILED (rc=$rc, or $out is not valid JSON) — audit stopped" >&2
    exit 1
  fi
}

run_phase_a() { run_checked A inventory-containers.sh "$AUDIT_DIR/containers.json"; }
run_phase_b() { run_checked B scan-files.sh "$AUDIT_DIR/files.json"; }
run_phase_c() { run_checked C check-links.sh "$AUDIT_DIR/links.json"; }

case "$PHASES" in
  containers|--containers) run_phase_a ;;
  files|--files) run_phase_b ;;
  links|--links) run_phase_c ;;
  all|--all|"") run_phase_a; run_phase_b; run_phase_c ;;
  *) echo "Unknown phase: $PHASES" >&2; exit 2 ;;
esac

echo "Intermediates ready in: $AUDIT_DIR" >&2
echo "Next: skill renders REPORT.md, presents to user, awaits approval." >&2
