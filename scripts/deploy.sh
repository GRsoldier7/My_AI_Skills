#!/usr/bin/env bash
# Deploy platform config files and/or skills to a target project.
#
# Usage:
#   ./scripts/deploy.sh --target /path/to/project --platforms claude,codex,gemini,cursor
#   ./scripts/deploy.sh --target /path/to/project --skills polychronos-team,biohacking-data-pipeline
#   ./scripts/deploy.sh --target /path/to/project --platforms claude --category microsoft

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TARGET=""
PLATFORMS=""
SKILLS=""
CATEGORY=""
FORCE=false

usage() {
    echo "Usage: $0 --target PATH [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --target PATH        Target project directory (required)"
    echo "  --platforms LIST     Comma-separated platforms: claude,codex,gemini,cursor"
    echo "  --skills LIST        Comma-separated skill names to register as project commands"
    echo "  --category NAME      Register all skills from a category (core, strategy, product, microsoft)"
    echo "  --force              Overwrite existing files"
    echo "  -h, --help           Show this help message"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target)
            TARGET="$2"
            shift 2
            ;;
        --platforms)
            PLATFORMS="$2"
            shift 2
            ;;
        --skills)
            SKILLS="$2"
            shift 2
            ;;
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if [[ -z "$TARGET" ]]; then
    echo "Error: --target is required"
    usage
    exit 1
fi

if [[ ! -d "$TARGET" ]]; then
    echo "Error: Target directory does not exist: $TARGET"
    exit 1
fi

TARGET="$(cd "$TARGET" && pwd)"

deploy_file() {
    local src="$1"
    local dest="$2"

    if [[ -f "$dest" && "$FORCE" != true ]]; then
        echo "  SKIP $dest (already exists, use --force to overwrite)"
        return
    fi
    cp "$src" "$dest"
    echo "  CREATED $dest"
}

# Deploy platform config files
if [[ -n "$PLATFORMS" ]]; then
    echo "Deploying platform configs to $TARGET..."
    echo ""

    IFS=',' read -ra PLATFORM_LIST <<< "$PLATFORMS"
    for platform in "${PLATFORM_LIST[@]}"; do
        case "$platform" in
            claude)
                deploy_file "$REPO_DIR/platform-configs/claude/CLAUDE.md.template" "$TARGET/CLAUDE.md"
                ;;
            codex)
                deploy_file "$REPO_DIR/platform-configs/codex/AGENTS.md.template" "$TARGET/AGENTS.md"
                ;;
            gemini)
                deploy_file "$REPO_DIR/platform-configs/gemini/GEMINI.md.template" "$TARGET/GEMINI.md"
                ;;
            cursor)
                deploy_file "$REPO_DIR/platform-configs/cursor/cursorrules.template" "$TARGET/.cursorrules"
                ;;
            *)
                echo "  WARNING: Unknown platform '$platform' (supported: claude, codex, gemini, cursor)"
                ;;
        esac
    done
    echo ""
fi

# Deploy skills as project-level commands
register_skill() {
    local skill_name="$1"
    local skill_file=""

    # Search for the skill across all categories
    skill_file="$(find "$REPO_DIR/skills" -path "*/$skill_name/SKILL.md" -type f | head -1)"

    if [[ -z "$skill_file" ]]; then
        echo "  WARNING: Skill not found: $skill_name"
        return
    fi

    mkdir -p "$TARGET/.claude/commands"
    local link_path="$TARGET/.claude/commands/$skill_name.md"

    if [[ -L "$link_path" || -f "$link_path" ]] && [[ "$FORCE" != true ]]; then
        echo "  SKIP /$skill_name (already exists)"
        return
    fi

    ln -sf "$skill_file" "$link_path"
    echo "  /$skill_name -> $skill_file"
}

if [[ -n "$SKILLS" ]]; then
    echo "Registering skills as project commands in $TARGET..."
    echo ""
    IFS=',' read -ra SKILL_LIST <<< "$SKILLS"
    for skill in "${SKILL_LIST[@]}"; do
        register_skill "$skill"
    done
    echo ""
fi

if [[ -n "$CATEGORY" ]]; then
    echo "Registering all $CATEGORY skills as project commands in $TARGET..."
    echo ""
    category_dir="$REPO_DIR/skills/$CATEGORY"
    if [[ ! -d "$category_dir" ]]; then
        echo "  ERROR: Category not found: $CATEGORY"
        exit 1
    fi
    while IFS= read -r skill_file; do
        skill_name="$(basename "$(dirname "$skill_file")")"
        register_skill "$skill_name"
    done < <(find "$category_dir" -name "SKILL.md" -type f | sort)
    echo ""
fi

echo "Done."
