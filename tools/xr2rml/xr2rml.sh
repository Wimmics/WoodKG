#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ $# -eq 0 ]]; then
    echo "Aucune option fournie."
    exit 1
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        -taxon)
            shift
            if [[ $1 =~ ^-([0-9]+)$ ]]; then
                TAXON_NUMBER="${BASH_REMATCH[1]}"
                echo "Option -taxon détectée : lancement avec option spéciale (-$TAXON_NUMBER)"
                bash "$PROJECT_ROOT/xr2rml/run_mapping_taxon.sh" "-$TAXON_NUMBER"
                exit 0
            else
                echo "Erreur : après -taxon, tu dois mettre -<chiffre> (ex: -taxon -2)"
                exit 1
            fi
            ;;
        -iawa)
            echo "Option --iawa détectée : lancement avec option spéciale"
            bash "$PROJECT_ROOT/xr2rml/run_mapping_iawa.sh"
            exit 0
            ;;
        -thesaurus)
            echo "Option --thesaurus détectée : lancement avec option spéciale"
            bash "$PROJECT_ROOT/xr2rml/run_mapping_thesaurus.sh"
            exit 0
            ;;
        *)
            echo "Option inconnue : $1"
            exit 1
            ;;
    esac
done
