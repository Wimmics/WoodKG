#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Go two levels up to get the root of the project
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
# Check if a file path is provided as an argument
if [ -n "$1" ]; then
    FILE_PATH="$1"

fi

mkdir -p "$SCRIPT_DIR/../temp/observation_input"
mkdir -p "$SCRIPT_DIR/../temp/observation_output"
# Run the Python script to detect the file type (json or csv)
result=$(python3 "$SCRIPT_DIR/../detect_file_type.py" "$FILE_PATH")

# Print the detected file type
echo "Detection result: $result"

# If the detected type is JSON, call the json.sh script
if [ "$result" = "json" ]; then
    echo "Calling json.sh..."
    bash "$SCRIPT_DIR/json.sh" "$FILE_PATH"
    exit 0

# If the detected type is CSV, call the csv.sh script
elif [ "$result" = "csv" ]; then
    echo "Calling csv.sh..."
    bash "$SCRIPT_DIR/csv.sh" "$FILE_PATH"
    exit 0

# If the result is unknown, exit with error
else
    exit 1   # Signals failure
fi
