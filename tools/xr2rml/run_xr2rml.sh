#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

rm -rf "$PROJECT_ROOT/xr2rml/mongo_import/*"
rm -rf "$PROJECT_ROOT/xr2rml/xr2rml_config/mapping*.ttl"
rm -rf "$PROJECT_ROOT/xr2rml/xr2rml_output/*.ttl"


while [[ $# -gt 0 ]]; do
    case "$1" in
        --taxon)
            mappingfile="$PROJECT_ROOT/tools/powo/mapping/mapping_powo.ttl"
            echo "xR2RML mapping file: $mappingfile"
            cp "$mappingfile" "$PROJECT_ROOT/xr2rml/xr2rml_config/"
            FILES=("$PROJECT_ROOT/input/powo/currated"/*)
            TOTAL_FILES=${#FILES[@]}
            echo "$TOTAL_FILES files found in powo/"

            for ((i=0; i<TOTAL_FILES; i++)); do
                FILE="${FILES[$i]}"
                FILE_NUMBER=$((i+1))

                rm -rf "$PROJECT_ROOT/xr2rml/mongo_import"/*
                echo "Processing file #$FILE_NUMBER: $(basename "$FILE")"
                cp "$FILE" "$PROJECT_ROOT/xr2rml/mongo_import/"

                bash "$SCRIPT_DIR/run_mapping_taxon.sh" "-$FILE_NUMBER"
                cp "$PROJECT_ROOT/xr2rml/xr2rml_output/powo_taxonomy_$FILE_NUMBER.ttl" "$PROJECT_ROOT/output/"
                echo "Output file: $PROJECT_ROOT/output/powo_taxonomy_$FILE_NUMBER.ttl"
                echo
            done
            ;;

        --thesaurus)
            mappingfile="$PROJECT_ROOT/tools/iawa_thesaurus/mapping/mapping_thesaurus_iawa.ttl"
            echo "xR2RML mapping file: $mappingfile"
            cp "$mappingfile" "$PROJECT_ROOT/xr2rml/xr2rml_config/"

            rm -rf "$PROJECT_ROOT/xr2rml/mongo_import"/*
            sourcefile="$PROJECT_ROOT/input/iawa_thesaurus/currated/iawa_thesaurus.json"
            echo "Source data to translate to RDF: $sourcefile"
            cp "$sourcefile" "$PROJECT_ROOT/xr2rml/mongo_import"

            bash "$SCRIPT_DIR/run_mapping_thesaurus.sh"
            cp "$PROJECT_ROOT/xr2rml/xr2rml_output/iawa_thesaurus.ttl" "$PROJECT_ROOT/output/"
            echo "Output file: $PROJECT_ROOT/output/iawa_thesaurus.ttl"
            exit 0
            ;;

        --observation)
            mappingfile="$PROJECT_ROOT/tools/observation/mapping/mapping_observation.ttl"
            echo "xR2RML mapping file: $mappingfile"
            cp "$mappingfile" "$PROJECT_ROOT/xr2rml/xr2rml_config/"

            sourcefile="$PROJECT_ROOT/output/observations.json"
            echo "Source data to translate to RDF: $sourcefile"
            rm -rf "$PROJECT_ROOT/xr2rml/mongo_import"/*
            cp "$sourcefile" "$PROJECT_ROOT/xr2rml/mongo_import"

            bash "$SCRIPT_DIR/run_mapping_observation.sh"
            cp "$PROJECT_ROOT/xr2rml/xr2rml_output/observation.ttl" "$PROJECT_ROOT/output/"
            echo "Output file: $PROJECT_ROOT/output/observation.ttl"
            exit 0
            ;;
        *)
            echo "Option inconnue : $1"
            exit 1
            ;;
    esac
done
