#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
mkdir -p "$SCRIPT_DIR/../temp"

# Lancer le script Python IAWA.py
python3 "$SCRIPT_DIR/../cepam_csvtojson.py"