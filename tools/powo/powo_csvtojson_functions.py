import csv
import json
import os


def convert_csv_to_json_lines(csv_path, json_lines_path):
    """Converts a CSV file to JSON Lines format.
    Args:
        csv_path (str): Path to the input CSV file.
        json_lines_path (str): Path to the output JSON Lines file.
    Returns:
        None
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the file is not a CSV file.
    """
    with open(csv_path, encoding="utf-8") as f_in, open(
        json_lines_path, "w", encoding="utf-8"
    ) as f_out:
        reader = csv.DictReader(f_in, delimiter="|")
        for row in reader:
            f_out.write(json.dumps(row, ensure_ascii=False) + "\n")


def wcvpJson(csv_folder, output_folder):
    """Convertit tous les fichiers CSV d'un dossier en fichiers JSON Lines.

    Args:
        csv_folder (str): Dossier contenant les CSV.
        output_folder (str): Dossier où sauvegarder les fichiers JSON Lines.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Liste triée des fichiers CSV commençant par "partie_" et finissant par ".csv"
    csv_files = sorted([f for f in os.listdir(csv_folder) if f.endswith(".csv")])

    if not csv_files:
        print("❌ Aucun fichier '*.csv' trouvé dans le dossier.")
        return

    for i, filename in enumerate(csv_files, start=1):
        csv_path = os.path.join(csv_folder, filename)
        json_output = os.path.join(output_folder, f"powo_taxonomy_{i}.json")

        print(f"✅ Converting {csv_path} -> {json_output}")
        convert_csv_to_json_lines(csv_path, json_output)
