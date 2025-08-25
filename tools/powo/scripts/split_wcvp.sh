# Extraire l'en-tête


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

head -n 1 "$SCRIPT_DIR/../../../input/powo/raw/wcvp_taxon.csv" > header.csv

# Couper le fichier sans la première ligne (le header)
tail -n +2 "$SCRIPT_DIR/../../../input/powo/raw/wcvp_taxon.csv" | split -l 100000 -d --additional-suffix=.csv - "$SCRIPT_DIR/../../../input/powo/raw/wcvp_part_"

# Pour chaque fichier créé, remettre l'en-tête au début
for file in "$SCRIPT_DIR/../../../input/powo/raw/wcvp_part_"*.csv; do
  cat header.csv "$file" > temp && mv temp "$file"
done

# Supprimer le fichier temporaire
rm header.csv

# Supprimer le fichier CSV d'origine (optionnel)
rm "$SCRIPT_DIR/../../../input/powo/raw/wcvp_taxon.csv"
