#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DEST_DIR="$SCRIPT_DIR/../temp/observation_input"


if [ -n "$1" ]; then
    SOURCE_FILE="$1"

fi


rm -rf "$DEST_DIR/"*.json

    cp "$SOURCE_FILE" "$DEST_DIR/"
    echo "✅ Copied: $SOURCE_FILE to $DEST_DIR"


