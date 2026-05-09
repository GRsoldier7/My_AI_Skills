#!/bin/bash
# Sync My_AI_Skills bundles to the NotebookLM "My_AI_Skills — Skill Library Reference" notebook.
#
# Behavior:
#   1. Builds fresh bundles via build-bundle.sh
#   2. Computes sha256 of each bundle
#   3. Compares to last-sync state at /root/My_AI_Skills/.notebooklm-sync-state.json
#   4. For each changed bundle: deletes old NotebookLM source, adds new one (sequential)
#   5. Updates state file
#   6. Preserves the GitHub URL source (818c3ab3...) — never touched
#
# Usage:
#   sync-notebooklm.sh            # real run
#   sync-notebooklm.sh --dry-run  # show what would change, no writes
#
# Exit non-zero on any error.

set -euo pipefail

# --- Config ---------------------------------------------------------------
REPO="/root/My_AI_Skills"
BUNDLE_DIR="$REPO/.bundle-cache"
STATE_FILE="$REPO/.notebooklm-sync-state.json"
NOTEBOOK_ID="651141c9-8bfa-4f1e-b3ae-08f7393f2513"
NOTEBOOKLM="/root/.notebooklm-venv/bin/notebooklm"
BUILD_SCRIPT="$REPO/scripts/build-bundle.sh"
PROTECTED_SOURCE_PREFIX="818c3ab3"  # GitHub URL — never delete

# Bundle filenames (must match build-bundle.sh output)
BUNDLES=(
    "01_skills_core_engineering_faith_homelab_legal.md"
    "02_skills_growth_microsoft_product_strategy.md"
    "03_skills_top_level_docs.md"
)

# --- Args -----------------------------------------------------------------
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        -h|--help)
            sed -n '2,18p' "$0"
            exit 0
            ;;
        *)
            echo "ERROR: unknown arg: $arg" >&2
            exit 2
            ;;
    esac
done

# --- Pre-flight -----------------------------------------------------------
[ -x "$NOTEBOOKLM" ] || { echo "ERROR: notebooklm CLI not found at $NOTEBOOKLM" >&2; exit 1; }
[ -x "$BUILD_SCRIPT" ] || { echo "ERROR: build script not executable: $BUILD_SCRIPT" >&2; exit 1; }
command -v jq >/dev/null || { echo "ERROR: jq required but not installed" >&2; exit 1; }
command -v sha256sum >/dev/null || { echo "ERROR: sha256sum required" >&2; exit 1; }

# Activate venv (for completeness — calling the binary directly works too)
# shellcheck disable=SC1091
source /root/.notebooklm-venv/bin/activate

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
log() { echo "[$(ts)] $*"; }

# --- Step 1: Refresh bundles ---------------------------------------------
log "Building bundles via $BUILD_SCRIPT"
if ! "$BUILD_SCRIPT" >/dev/null; then
    echo "ERROR: build-bundle.sh failed" >&2
    exit 1
fi

# --- Step 2: Compute new hashes ------------------------------------------
declare -A NEW_HASH
for f in "${BUNDLES[@]}"; do
    path="$BUNDLE_DIR/$f"
    [ -f "$path" ] || { echo "ERROR: missing bundle: $path" >&2; exit 1; }
    NEW_HASH[$f]=$(sha256sum "$path" | awk '{print $1}')
done

# --- Step 3: Load prior state --------------------------------------------
# State schema:
# {
#   "notebook_id": "...",
#   "last_sync_utc": "...",
#   "bundles": {
#     "<filename>": { "sha256": "...", "source_id": "..." }
#   }
# }
if [ -f "$STATE_FILE" ]; then
    if ! jq -e . "$STATE_FILE" >/dev/null 2>&1; then
        echo "ERROR: state file exists but is invalid JSON: $STATE_FILE" >&2
        exit 1
    fi
    log "Loaded state from $STATE_FILE"
else
    log "No state file — bootstrapping by reading current notebook sources"
    # Bootstrap: query the live notebook and seed entries for our bundles by exact title match.
    if ! src_json=$("$NOTEBOOKLM" source list --notebook "$NOTEBOOK_ID" --json 2>/dev/null); then
        echo "ERROR: failed to list sources for notebook $NOTEBOOK_ID" >&2
        exit 1
    fi
    bootstrap='{"notebook_id":"'"$NOTEBOOK_ID"'","last_sync_utc":"'"$(ts)"'","bundles":{}}'
    for f in "${BUNDLES[@]}"; do
        sid=$(echo "$src_json" | jq -r --arg t "$f" '.sources[] | select(.title == $t) | .id' | head -1)
        if [ -n "$sid" ] && [ "$sid" != "null" ]; then
            bootstrap=$(echo "$bootstrap" | jq --arg f "$f" --arg sid "$sid" --arg h "${NEW_HASH[$f]}" \
                '.bundles[$f] = {"sha256": $h, "source_id": $sid}')
            log "Bootstrap: $f -> source $sid (assuming current bundle == uploaded content)"
        else
            log "Bootstrap: $f has no matching source in notebook (will be added on this run)"
        fi
    done
    if [ "$DRY_RUN" -eq 1 ]; then
        log "[dry-run] would write bootstrap state to $STATE_FILE"
    else
        echo "$bootstrap" | jq . > "$STATE_FILE"
        chmod 600 "$STATE_FILE"
    fi
fi

# Re-load (or use bootstrap) — for dry-run with no prior file, fall back to in-memory bootstrap.
if [ -f "$STATE_FILE" ]; then
    STATE=$(cat "$STATE_FILE")
else
    STATE="$bootstrap"
fi

# --- Step 4: Diff and apply ----------------------------------------------
changed=0
unchanged=0
errors=0
new_state="$STATE"

for f in "${BUNDLES[@]}"; do
    new_h="${NEW_HASH[$f]}"
    old_h=$(echo "$STATE" | jq -r --arg f "$f" '.bundles[$f].sha256 // ""')
    old_sid=$(echo "$STATE" | jq -r --arg f "$f" '.bundles[$f].source_id // ""')

    if [ "$new_h" = "$old_h" ] && [ -n "$old_sid" ]; then
        log "UNCHANGED: $f (sha256 ${new_h:0:12}…, source $old_sid)"
        unchanged=$((unchanged + 1))
        continue
    fi

    log "CHANGED:   $f (old=${old_h:0:12}… -> new=${new_h:0:12}…)"
    changed=$((changed + 1))

    if [ "$DRY_RUN" -eq 1 ]; then
        log "  [dry-run] would delete source $old_sid and re-upload $BUNDLE_DIR/$f"
        continue
    fi

    # Guardrail: never touch the protected source
    if [ -n "$old_sid" ] && [[ "$old_sid" == "$PROTECTED_SOURCE_PREFIX"* ]]; then
        echo "ERROR: refusing to touch protected source $old_sid for $f" >&2
        errors=$((errors + 1))
        continue
    fi

    # Delete old source if we have one
    if [ -n "$old_sid" ]; then
        if ! "$NOTEBOOKLM" source delete --notebook "$NOTEBOOK_ID" -y "$old_sid" >/dev/null 2>&1; then
            echo "ERROR: failed to delete source $old_sid for $f" >&2
            errors=$((errors + 1))
            continue
        fi
        log "  deleted old source $old_sid"
    fi

    # Add new source (sequential — one at a time, never parallel)
    add_out=$("$NOTEBOOKLM" source add "$BUNDLE_DIR/$f" --notebook "$NOTEBOOK_ID" --type file --mime-type "text/markdown" --json 2>&1) || {
        echo "ERROR: source add failed for $f: $add_out" >&2
        errors=$((errors + 1))
        continue
    }
    new_sid=$(echo "$add_out" | jq -r '.id // .source_id // empty' 2>/dev/null || true)
    if [ -z "$new_sid" ]; then
        # Fallback: re-list and find by title
        sleep 2
        new_sid=$("$NOTEBOOKLM" source list --notebook "$NOTEBOOK_ID" --json | jq -r --arg t "$f" '.sources[] | select(.title == $t) | .id' | head -1)
    fi
    if [ -z "$new_sid" ] || [ "$new_sid" = "null" ]; then
        echo "ERROR: could not determine new source ID for $f" >&2
        errors=$((errors + 1))
        continue
    fi
    log "  added new source $new_sid"

    new_state=$(echo "$new_state" | jq --arg f "$f" --arg h "$new_h" --arg sid "$new_sid" \
        '.bundles[$f] = {"sha256": $h, "source_id": $sid}')
done

# --- Step 5: Persist state -----------------------------------------------
if [ "$DRY_RUN" -eq 0 ] && [ "$changed" -gt 0 ] && [ "$errors" -eq 0 ]; then
    new_state=$(echo "$new_state" | jq --arg ts "$(ts)" --arg nb "$NOTEBOOK_ID" \
        '.last_sync_utc = $ts | .notebook_id = $nb')
    echo "$new_state" | jq . > "$STATE_FILE"
    chmod 600 "$STATE_FILE"
    log "Wrote updated state to $STATE_FILE"
fi

# --- Summary --------------------------------------------------------------
echo ""
echo "=== Sync summary ==="
echo "  notebook:  $NOTEBOOK_ID"
echo "  changed:   $changed"
echo "  unchanged: $unchanged"
echo "  errors:    $errors"
echo "  dry-run:   $DRY_RUN"

if [ "$errors" -gt 0 ]; then
    exit 1
fi
exit 0
