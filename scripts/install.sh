#!/bin/bash
# Content OS Installer
# Creates symlinks from your workspace to Content OS skills

set -e

CONTENT_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$CONTENT_OS_DIR/skills"

# Default target is ~/.claude/skills, but can be overridden
TARGET_DIR="${1:-$HOME/.claude/skills}"

echo "Content OS Installer"
echo "===================="
echo "Source: $SKILLS_DIR"
echo "Target: $TARGET_DIR"
echo ""

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Function to create symlink for a skill
link_skill() {
    local category=$1
    local skill=$2
    local source="$SKILLS_DIR/$category/$skill"
    local target="$TARGET_DIR/$skill"

    if [ -L "$target" ]; then
        echo "  [skip] $skill (symlink exists)"
    elif [ -d "$target" ]; then
        echo "  [skip] $skill (directory exists - not overwriting)"
    else
        ln -s "$source" "$target"
        echo "  [link] $skill -> $source"
    fi
}

# Interactive mode - ask which categories to install
echo "Which skill categories would you like to install?"
echo ""

categories=("writing" "video" "social" "research" "content" "productivity")

for category in "${categories[@]}"; do
    read -p "Install $category skills? [Y/n] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "Installing $category skills..."
        for skill_dir in "$SKILLS_DIR/$category"/*; do
            if [ -d "$skill_dir" ]; then
                skill=$(basename "$skill_dir")
                link_skill "$category" "$skill"
            fi
        done
        echo ""
    fi
done

echo "Installation complete!"
echo ""
echo "Your skills are now available in: $TARGET_DIR"
echo ""
echo "To use in a specific workspace, run:"
echo "  ./install.sh /path/to/workspace/.claude/skills"
