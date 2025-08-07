#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

rm -rf "$PROJECT_ROOT/xr2rml/mongo_import"/*
rm -rf "$PROJECT_ROOT"/xr2rml/xr2rml_config/mapping*.ttl

rm -rf "$PROJECT_ROOT/xr2rml/xr2rml_output"/*.ttl


while [[ $# -gt 0 ]]; do
    case "$1" in
        -taxon)
            cp "$PROJECT_ROOT/tools/powo/mapping/mapping_powo.ttl" "$PROJECT_ROOT/xr2rml/xr2rml_config/"

            FILES=("$PROJECT_ROOT/input/powo/currated"/*)
            TOTAL_FILES=${#FILES[@]}

            echo "$TOTAL_FILES fichiers trouvés dans Powo/"

            for ((i=0; i<TOTAL_FILES; i++)); do
                FILE="${FILES[$i]}"
                FILE_NUMBER=$((i+1))

                echo "Traitement du fichier $FILE_NUMBER : $(basename "$FILE")"

                # Nettoyer mongo_import et copier le fichier courant
                rm -rf "$PROJECT_ROOT/xr2rml/mongo_import"/*
                cp "$FILE" "$PROJECT_ROOT/xr2rml/mongo_import/"

                # Appel du script avec -taxon -<numéro>
                bash "$SCRIPT_DIR/xr2rml.sh" -taxon "-$FILE_NUMBER"

                # Copier le résultat généré
                cp "$PROJECT_ROOT/xr2rml/xr2rml_output/powo_taxonomy_$FILE_NUMBER.ttl" "$PROJECT_ROOT/output/"
            done

            exit 0
            ;;
        -thesaurus)
            cp "$PROJECT_ROOT/tools/iawa_thesaurus/mapping/mapping_thesaurus_iawa.ttl" "$PROJECT_ROOT/xr2rml/xr2rml_config/"
            cp "$PROJECT_ROOT/input/iawa_thesaurus/currated/iawa_thesaurus.json" "$PROJECT_ROOT/xr2rml/mongo_import"

            bash "$SCRIPT_DIR/xr2rml.sh" -thesaurus
            cp "$PROJECT_ROOT/xr2rml/xr2rml_output/thesaurus.ttl" "$PROJECT_ROOT/output/"
            exit 0
            ;;
        -iawa)
            cp "$PROJECT_ROOT/tools/observation/mapping/mapping_observation.ttl" "$PROJECT_ROOT/xr2rml/xr2rml_config/"
            cp "$PROJECT_ROOT/tools/observation/temp/observation_output/observations_output.json" "$PROJECT_ROOT/xr2rml/mongo_import"

            bash "$SCRIPT_DIR/xr2rml.sh" -iawa
            cp "$PROJECT_ROOT/xr2rml/xr2rml_output/observation.ttl" "$PROJECT_ROOT/output/"
            exit 0
            ;;
        *)
            echo "Option inconnue : $1"
            show_help
            exit 1
            ;;
    esac
done
