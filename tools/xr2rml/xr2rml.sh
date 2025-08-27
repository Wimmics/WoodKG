#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ $1 =~ ^-([0-9]+)$ ]]; then
    TAXON_NUMBER="${BASH_REMATCH[1]}"
    echo "Translation of taxonomy to RDF with option (-$TAXON_NUMBER)"
    bash "$PROJECT_ROOT/xr2rml/run_mapping_taxon.sh" "-$TAXON_NUMBER"
    exit 0
else
    echo "Error : option --taxon requires an integer parameter (ex: -taxon -2)"
    exit 1
