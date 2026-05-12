#!/bin/bash

help()
{
  exe=$(basename $0)
  echo "Usage: $exe --wcvp  | --thesaurus | --observation"
  exit 1
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

XR2RML_CONFIG="$PROJECT_ROOT/xr2rml/xr2rml_config"
XR2RML_OUTPUT="$PROJECT_ROOT/xr2rml/xr2rml_output"

rm -rf $XR2RML_CONFIG/mapping*.ttl
rm -rf $XR2RML_OUTPUT/*
rm -rf $PROJECT_ROOT/xr2rml/mongo_import/*

case "$1" in
    --wcvp)
        MAPPING_FILE="$PROJECT_ROOT/tools/wcvp/mapping/mapping_wcvp.ttl"
        echo "xR2RML mapping file: $MAPPING_FILE"
        cp $MAPPING_FILE $XR2RML_CONFIG
        
        INPUT_DIR="$PROJECT_ROOT/input/wcvp/currated/"
        FILES=($INPUT_DIR/*)
        NO_FILES=${#FILES[@]}
        echo "$NO_FILES files found in $INPUT_DIR"

        for ((FILE_NUMBER=0; FILE_NUMBER<NO_FILES; FILE_NUMBER++)); do
            echo "=========================================================================="
            FILE="${FILES[$FILE_NUMBER]}"
            echo "Processing file" $(basename "$FILE")
            rm -rf $PROJECT_ROOT/xr2rml/mongo_import/*
            cp $FILE $PROJECT_ROOT/xr2rml/mongo_import/

            bash $SCRIPT_DIR/run_xr2rml_wcvp.sh $(basename "$FILE")
            OUTPUT_FILE=($XR2RML_OUTPUT/*)
            echo "Output file: ${OUTPUT_FILE[0]}"
            mv $XR2RML_OUTPUT/* $PROJECT_ROOT/output/
            echo
        done
        ;;

    --thesaurus)
        MAPPING_FILE="$PROJECT_ROOT/tools/iawa_thesaurus/mapping/mapping_thesaurus_iawa.ttl"
        echo "xR2RML mapping file: $MAPPING_FILE"
        cp $MAPPING_FILE $XR2RML_CONFIG

        INPUT_FILE="$PROJECT_ROOT/input/iawa_thesaurus/currated/iawa_thesaurus.json"
        echo "Input data to translate to RDF: $INPUT_FILE"
        cp $INPUT_FILE $PROJECT_ROOT/xr2rml/mongo_import

        bash $SCRIPT_DIR/run_xr2rml_thesaurus.sh
        cp $XR2RML_OUTPUT/iawa_thesaurus.ttl $PROJECT_ROOT/output/
        echo "Output file: $PROJECT_ROOT/output/iawa_thesaurus.ttl"
        exit 0
        ;;

    --observation)
        MAPPING_FILE="$PROJECT_ROOT/tools/observation/mapping/mapping_observation.ttl"
        echo "xR2RML mapping file: $MAPPING_FILE"
        cp $MAPPING_FILE $XR2RML_CONFIG

        INPUT_FILE="$PROJECT_ROOT/output/observations.json"
        echo "Input data to translate to RDF: $INPUT_FILE"
        cp $INPUT_FILE $PROJECT_ROOT/xr2rml/mongo_import

        bash $SCRIPT_DIR/run_xr2rml_observation.sh
        cp $XR2RML_OUTPUT/observation.ttl $PROJECT_ROOT/output/
        echo "Output file: $PROJECT_ROOT/output/observation.ttl"
        exit 0
        ;;
    *)
        echo "❌ Unknown option: $1"
        exit 1
        ;;
esac
