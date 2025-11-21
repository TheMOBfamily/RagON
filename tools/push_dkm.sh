#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment from .env (portable)
source "$SCRIPT_DIR/../load-env.sh"

# Source directory for DKM instructions
SOURCE_PROJECT="$RAGON_ROOT"
SOURCE_DIR="${SOURCE_PROJECT}/.fong/instructions/DKM"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
  echo "❌ Source directory not found: $SOURCE_DIR"
  exit 1
fi

echo "🚀 Starting push of DKM instructions from $SOURCE_DIR"

# Find all projects with .fong directory
PROJECTS_ROOT="$(dirname "$RAGON_ROOT")"
TARGETS=$(find "$PROJECTS_ROOT" -mindepth 2 -maxdepth 3 -name ".fong" -type d 2>/dev/null | sort -u)

COUNT=0
for FONG_DIR in $TARGETS; do
  PROJECT_ROOT=$(dirname "$FONG_DIR")
  TARGET_DKM_DIR="${FONG_DIR}/instructions/DKM"

  # Skip source project to avoid self-copying (though cp handles it, it's cleaner)
  if [[ "$PROJECT_ROOT" == "$SOURCE_PROJECT" ]]; then
    continue
  fi

  echo "👉 Processing: $PROJECT_ROOT"

  # Create destination directory if it doesn't exist
  if [ ! -d "$TARGET_DKM_DIR" ]; then
    mkdir -p "$TARGET_DKM_DIR"
    echo "   Created directory: $TARGET_DKM_DIR"
  fi

  # Copy files
  cp -r "$SOURCE_DIR"/* "$TARGET_DKM_DIR/"
  
  if [ $? -eq 0 ]; then
    echo "   ✅ Copied DKM files"
    ((COUNT++))
  else
    echo "   ❌ Failed to copy files"
  fi
done

echo ""
echo "🎉 Finished! Pushed to $COUNT projects."
