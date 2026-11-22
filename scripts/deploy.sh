#!/usr/bin/env bash
# Compatibility entrypoint for project instructions. Full packages use install-skills.sh.
set -euo pipefail
for arg in "$@"; do
    case "$arg" in
        --skills|--skills=*|--category|--category=*)
            echo 'Choose a full package or set with scripts/install-skills.sh --help.' >&2
            exit 2 ;;
        --force|--force=*)
            echo 'Review and merge existing project instructions manually.' >&2
            exit 2 ;;
    esac
done
script_dir="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
    exec python3 "$script_dir/project-guidance.py" deploy "$@"
fi
exec python "$script_dir/project-guidance.py" deploy "$@"
