#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Lancer le script Python IAWA.py
python3 "$SCRIPT_DIR/../insidewood_csvtojson.py"