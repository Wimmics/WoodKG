#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FOLDER_PATH="$SCRIPT_DIR/tools/transfer"
SCRIPT_PATH="$SCRIPT_DIR/tools/xr2rml"

IAWA_PROPERTIES_DIR="$SCRIPT_DIR/tools/iawa_thesaurus"
POWO_DIR="$SCRIPT_DIR/tools/powo"
OBSERVATION_DIR="$SCRIPT_DIR/tools/observation"
CEPAM_DIR="$SCRIPT_DIR/tools/cepam_observations"
INSIDEWOOD_DIR="$SCRIPT_DIR/tools/insidewood_observations"


# Fonction : retourne vrai si le dossier est vide ou inexistant
dossier_est_vide() {
    [[ ! -d "$1" || -z "$(ls -A "$1" 2>/dev/null)" ]]
}

while true; do
    echo
    echo "========= WoodKGL2 Menu ========="
    echo "1) Preprocess IAWA thesaurus"
    echo "2) Generate IAWA thesaurus as RDF"
    echo "3) Preprocess POWO taxonomy"
    echo "4) Generate POWO taxonomy as RDF"
    echo "5) Preprocess CEPAM observations"
    echo "6) Preprocess InsideWood observations"
    echo "7) Generate observations as RDF"
    echo "8) Quit"
    echo "================================="
    read -p "Select an option: " choice

    case $choice in
        1)
            echo "Generating IAWA Feature of Interest (FoI), Observable Properties (OP) and OP values..."
            echo "Invoking $IAWA_PROPERTIES_DIR/iawa_properties.py"
            mkdir -p "$IAWA_PROPERTIES_DIR/temp"
            python3 "$IAWA_PROPERTIES_DIR/iawa_properties.py"

            echo "Launching Thesaurus Processing..."
            echo "Invoking $IAWA_PROPERTIES_DIR/thesaurus.py"
            mkdir -p "$IAWA_PROPERTIES_DIR/temp"
            python3 "$IAWA_PROPERTIES_DIR/thesaurus.py"            
            ;;
        2)
            echo "Translating IAWA thesaurus to RDF..."
            echo "Invoking $SCRIPT_PATH/run_xr2rml.sh --thesaurus"
            bash "$SCRIPT_PATH/run_xr2rml.sh" --thesaurus
            ;;
        3)
            echo "Processing POWO taxonomy ..."
            echo "Invoking $POWO_DIR/powo_csvtojson.py"
            python3 "$POWO_DIR/powo_csvtojson.py"
            ;;
        4)
            echo "Translating POWO taxonomy to RDF..."
            echo "Invoking $SCRIPT_PATH/run_xr2rml.sh" --taxon
            bash "$SCRIPT_PATH/run_xr2rml.sh" --taxon
            ;;
        5)
            echo "Processing CEPAM observations..."
            echo "Invoking $CEPAM_DIR/cepam_csvtojson.py"
            mkdir -p "$CEPAM_DIR/temp"

            output_dir=input/cepam_observations/currated
            rm -rf $output_dir
            mkdir -p $output_dir

            python3 "$CEPAM_DIR/cepam_csvtojson.py"
            rm -rf "$CEPAM_DIR/temp"
            ;;
        6)
            echo "Processing InsideWood observations..."
            echo "Invoking $INSIDEWOOD_DIR/insidewood_csvtojson.py"
            python3 "$INSIDEWOOD_DIR/insidewood_csvtojson.py"
            ;;
        7)
            echo
            echo "Translating observations to RDF..."

            # Demande du chemin à l'utilisateur
            read -p "Please enter the path to the input file: " INPUT_FILE
            if [ ! -f "$INPUT_FILE" ]; then
                echo "❌ Error: '$INPUT_FILE' is not a valid file."
                read -p "Press Enter to continue..."
                break
            fi

            mkdir -p "$OBSERVATION_DIR/temp/output"
            INPUT_DIR="$OBSERVATION_DIR/temp/input"
            mkdir -p "$INPUT_DIR"
            cp "$INPUT_FILE" "$INPUT_DIR/"
            echo "Copied $INPUT_FILE to $INPUT_DIR"
            python3 "$OBSERVATION_DIR/observation.py"

            echo
            echo "Launching Morph-xR2RML for observations..."
            bash "$SCRIPT_PATH/run_xr2rml.sh" --observation
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
