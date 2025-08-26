#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FOLDER_PATH="$SCRIPT_DIR/tools/transfer"
SCRIPT_PATH="$SCRIPT_DIR/tools/xr2rml"



OBSERVATION_DIR="$SCRIPT_DIR/tools/observation"
IAWA_PROPERTIES_DIR="$SCRIPT_DIR/tools/iawa_thesaurus"
CEPAM_DIR="$SCRIPT_DIR/tools/CEPAM"
POWO_DIR="$SCRIPT_DIR/tools/powo"
CEPAM_DIR="$SCRIPT_DIR/tools/cepam_observations"
INSIDEWOOD_DIR="$SCRIPT_DIR/tools/insidewood_observations"



# Fonction : retourne vrai si le dossier est vide ou inexistant
dossier_est_vide() {
    [[ ! -d "$1" || -z "$(ls -A "$1" 2>/dev/null)" ]]
}

while true; do
    echo
    echo "========= WoodKGL2 Menu ========="
    echo "1) Generate IAWA thesaurus as JSON"
    echo "2) Generate IAWA thesaurus as RDF"
    echo "3) Generate POWO taxonomy as JSON"
    echo "4) Generate POWO taxonomy as RDF"
    echo "5) Generate CEPAM observations as JSON"
    echo "6) Generate InsideWood observations as JSON"
    echo "7) Generate observations as RDF"
    echo "8) Quit"
    echo "================================="
    read -p "Select an option: " choice

    case $choice in
        1)
            echo "Generating IAWA Feature of Interest (FoI), Observable Properties (OP) and OP values..."
            bash "$IAWA_PROPERTIES_DIR/scripts/iawa_properties.sh"
            echo "Launching Thesaurus Processing..."
            bash "$IAWA_PROPERTIES_DIR/scripts/thesaurus.sh"
            read -p "Press Enter to continue..."
            ;;
        2)
            echo "Launching XR2RML for thesaurus..."
            bash "$SCRIPT_PATH/observation2xr2rml.sh" -thesaurus
            read -p "Press Enter to continue..."
            ;;
        3)
            echo "Launching POWO taxonomy processing..."
            bash "$POWO_DIR/scripts/powo.sh"
            read -p "Press Enter to continue..."
            ;;
       
        4)

            echo "Launching XR2RML for taxon..."
            bash "$SCRIPT_PATH/observation2xr2rml.sh" -taxon
            read -p "Press Enter to continue..."
            ;;
        5)
            echo "Launching CEPAM observations processing..."
            bash "$CEPAM_DIR/scripts/cepam_csvtojson.sh"
            read -p "Press Enter to continue..."
            ;;
        6)
            echo "Launching InsideWood observations processing..."
            bash "$INSIDEWOOD_DIR/scripts/insidewood_observations.sh"
            read -p "Press Enter to continue..."
            ;;
        7)
            echo "Launching Observation Processing..."

            # Demande du chemin à l'utilisateur
            read -p "Please enter the path to the input file: " inputFILE

            # Vérification : est-ce un fichier ?
            if [ ! -f "$inputFILE" ]; then
                echo "❌ Error: '$inputFILE' is not a valid file."
                read -p "Press Enter to continue..."
                break
            fi

            # Détection du type de fichier
            bash "$OBSERVATION_DIR/scripts/detect_file_type.sh" "$inputFILE"

            # Si succès, on enchaîne avec observation.sh en lui passant le chemin du fichier
            if [ $? -eq 0 ]; then
                bash "$OBSERVATION_DIR/scripts/observation.sh" "$inputFILE"
            fi


            echo "Launching XR2RML for iawa properties..."
            bash "$SCRIPT_PATH/observation2xr2rml.sh" -iawa

            read -p "Press Enter to continue..."
            ;;

        8)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid option."
            read -p "Press Enter to continue..."
            ;;
    esac
done
