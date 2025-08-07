#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
if [ -n "$1" ]; then
    FILE_PATH="$1"

fi

# Lancer le script Python IAWA.py

python3 "$SCRIPT_DIR/../observations_csvtojson.py" "$FILE_PATH"