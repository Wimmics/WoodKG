#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Extraire l'en-tête
head -n 1 "$SCRIPT_DIR/../../input/powo/raw/wcvp_taxon.csv" > header.csv

# Enlever la 1ère ligne et couper le fichier en parties de max 100000 lignes
echo "Spliting wcvp_taxon.csv into chunks of 100000 lines..."
tail -n +2 "$SCRIPT_DIR/../../input/powo/raw/wcvp_taxon.csv" | split -l 100000 -d --additional-suffix=.csv - "$SCRIPT_DIR/../../input/powo/raw/wcvp_part_"

# Pour chaque fichier créé, remettre l'en-tête au début
for file in "$SCRIPT_DIR/../../input/powo/raw/wcvp_part_"*.csv; do
  cat header.csv "$file" > temp && mv temp "$file"
done

# Supprimer le fichier temporaire
rm -f header.csv

# Supprimer le fichier CSV d'origine (optionnel)
rm -f "$SCRIPT_DIR/../../input/powo/raw/wcvp_taxon.csv"
