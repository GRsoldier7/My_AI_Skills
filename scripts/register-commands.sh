#!/usr/bin/env bash
# Register skills as Claude Code slash commands via symlinks.
#
# Usage:
#   ./scripts/register-commands.sh                     # Register all skills globally
#   ./scripts/register-commands.sh --category core     # Register only core skills
#   ./scripts/register-commands.sh --project /path      # Register into a specific project
#   ./scripts/register-commands.sh --list               # List registered commands
#   ./scripts/register-commands.sh --clean              # Remove all symlinks

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

COMMANDS_DIR="$HOME/.claude/commands"
CATEGORY=""
ACTION="register"

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --project PATH    Register into project-level .claude/commands/ instead of global"
    echo "  --category NAME   Only register skills from a specific category (core, strategy, product, microsoft)"
    echo "  --list            List currently registered commands"
    echo "  --clean           Remove all skill symlinks from commands directory"
    echo "  -h, --help        Show this help message"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --project)
            COMMANDS_DIR="$2/.claude/commands"
            shift 2
            ;;
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        --list)
            ACTION="list"
            shift
            ;;
        --clean)
            ACTION="clean"
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

list_commands() {
    if [[ ! -d "$COMMANDS_DIR" ]]; then
        echo "No commands directory found at $COMMANDS_DIR"
        return
    fi
    echo "Registered commands in $COMMANDS_DIR:"
    echo ""
    for link in "$COMMANDS_DIR"/*.md; do
        [[ -e "$link" ]] || continue
        name="$(basename "$link" .md)"
        if [[ -L "$link" ]]; then
            target="$(readlink "$link")"
            echo "  /$name -> $target"
        else
            echo "  /$name (file, not symlink)"
        fi
    done
}

clean_commands() {
    if [[ ! -d "$COMMANDS_DIR" ]]; then
        echo "No commands directory found at $COMMANDS_DIR"
        return
    fi
    local count=0
    for link in "$COMMANDS_DIR"/*.md; do
        [[ -L "$link" ]] || continue
        target="$(readlink "$link")"
        if [[ "$target" == "$SKILLS_DIR"* ]]; then
            rm "$link"
            count=$((count + 1))
        fi
    done
    echo "Removed $count skill symlinks from $COMMANDS_DIR"
}

register_commands() {
    mkdir -p "$COMMANDS_DIR"

    local search_dir="$SKILLS_DIR"
    if [[ -n "$CATEGORY" ]]; then
        search_dir="$SKILLS_DIR/$CATEGORY"
        if [[ ! -d "$search_dir" ]]; then
            echo "Category not found: $CATEGORY"
            echo "Available categories: $(ls "$SKILLS_DIR" | tr '\n' ', ' | sed 's/,$//')"
            exit 1
        fi
    fi

    local count=0
    while IFS= read -r skill_file; do
        # Extract the skill directory name (parent of SKILL.md)
        skill_dir="$(dirname "$skill_file")"
        skill_name="$(basename "$skill_dir")"
        link_path="$COMMANDS_DIR/$skill_name.md"

        if [[ -L "$link_path" ]]; then
            # Update existing symlink
            rm "$link_path"
        fi

        ln -s "$skill_file" "$link_path"
        echo "  /$skill_name -> $skill_file"
        count=$((count + 1))
    done < <(find "$search_dir" -name "SKILL.md" -type f | sort)

    echo ""
    echo "Registered $count skills as Claude Code slash commands in $COMMANDS_DIR"
}

case "$ACTION" in
    register)
        echo "Registering skills from $SKILLS_DIR..."
        [[ -n "$CATEGORY" ]] && echo "Filtering by category: $CATEGORY"
        echo ""
        register_commands
        ;;
    list)
        list_commands
        ;;
    clean)
        clean_commands
        ;;
esac
