#!/bin/bash
# Link all skills (except deprecated/ and misc/) into local harness skill directories
# Run after adding, removing, or renaming a skill

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
AGENTS_SKILLS_DIR="$HOME/.agents/skills"

mkdir -p "$CLAUDE_SKILLS_DIR"
mkdir -p "$AGENTS_SKILLS_DIR"

link_bucket() {
    local bucket="$1"
    local bucket_path="$REPO_ROOT/skills/$bucket"

    if [ ! -d "$bucket_path" ]; then
        echo "Bucket $bucket not found, skipping"
        return
    fi

    for skill_dir in "$bucket_path"/*/; do
        [ -d "$skill_dir" ] || continue
        skill_name=$(basename "$skill_dir")
        target_name="$bucket-$skill_name"

        # Link to ~/.claude/skills
        ln -sfn "$skill_dir" "$CLAUDE_SKILLS_DIR/$target_name"

        # Link to ~/.agents/skills
        ln -sfn "$skill_dir" "$AGENTS_SKILLS_DIR/$target_name"

        echo "Linked: $target_name -> $skill_dir"
    done
}

echo "Linking engineering skills..."
link_bucket "engineering"

echo "Linking productivity skills..."
link_bucket "productivity"

echo "Done. Re-run after adding/removing/renaming skills."