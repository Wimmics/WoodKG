import csv
import json
import os
import re
import json
import shutil


def csv_to_json(csv_filepath):
    """
    Converts a CSV file to a JSON file.
    Args:
        csv_filepath (str): Path to the CSV file.
    Returns:
        str: Path to the created JSON file.
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the file is not a CSV file.
    """
    if not os.path.isfile(csv_filepath):
        raise FileNotFoundError(f"❌ Fichier introuvable : {csv_filepath}")

    if not csv_filepath.lower().endswith(".csv"):
        raise ValueError("❌ Le fichier doit être au format .csv")

    csv_filename = os.path.splitext(os.path.basename(csv_filepath))[0]
    output_file = f"{csv_filename}.json"

    # Lire le CSV et écrire le JSON
    data = []
    with open(csv_filepath, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    with open(output_file, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

    
    return output_file


def extract_taxa_and_numeric_keys(input_file, output_file=None):
    """
    Extracts only the 'Taxa' key and all keys that start with a number.

    Args:
        input_file (str): path to the input JSON file
        output_file (str, optional): path to the output JSON file.
                                     If None, creates one with suffix '_taxa_and_numbers.json'

    Returns:
        str: path to the output JSON file
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = []
    for entry in data:
        new_entry = {}

        taxon_keys = {"taxaname", "taxa name", "taxa", "taxon", "taxaname", "taxa_name"}
        sample_id_keys = {
            "sampleid",
            "sample id",
            "sample_id",
            "id sample",
            "id_sample",
            "idsample",
        }

        # Find the value for 'Taxa'
        taxon_value = ""
        for key in entry:
            normalized_key = key.replace(" ", "").lower()
            if normalized_key in taxon_keys:
                taxon_value = entry[key]
                break

        # Find the value for 'Sample ID'
        sample_id_value = ""
        for key in entry:
            normalized_key = key.replace(" ", "").lower()
            if normalized_key in sample_id_keys:
                sample_id_value = entry[key]
                break
        new_entry["Taxon"] = taxon_value
        new_entry["sampleID"] = sample_id_value
        # Keep keys that start with a number
        for key, value in entry.items():
            if re.match(r"^\d+", key):
                new_entry[key] = value

        result.append(new_entry)

    if output_file is None:
        base_filename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_filename}_taxa_and_numbers.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


    return output_file


def transform_single_taxa_dict(input_dict):
    """Transforms a single dictionary by renaming 'Taxa' to 'Taxon' and formatting numeric keys.
    Args:
        input_dict (dict): The input dictionary to transform.
    Returns:
        dict: The transformed dictionary with 'Taxa' renamed to 'Taxon' and numeric"""
    result = {}

    for key, value in input_dict.items():
        # Ignorer les valeurs vides (str vides ou contenant que des espaces)
        if isinstance(value, str) and value.strip() == "":
            continue

        # Extraction du nombre au début de la clé
        match = re.match(r"^(\d+)", key)
        if match:
            num = match.group(1)
            # clé devient le nombre sur 3 chiffres uniquement
            new_key = num.zfill(3)
            result[new_key] = value
        else:
            # on garde la clé telle quelle si pas de nombre au début
            result[key] = value

    return result


def transform_json_file(input_json_path, export_dir):
    """Transforms a JSON file by applying specific transformations to each dictionary.
    Args:
        input_json_path (str): Path to the input JSON file.
        export_dir (str): Directory where the transformed JSON file will be saved.
    Returns:
        str: Path to the transformed JSON file.
    """

    # Supprimer tout le contenu du dossier s'il existe
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    os.makedirs(export_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_json_path))[0]
    output_file = os.path.join(export_dir, f"{base_name}_homogene.json")

    with open(input_json_path, "r", encoding="utf-8") as f:
        input_list = json.load(f)

    transformed_list = [transform_single_taxa_dict(taxa) for taxa in input_list]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(transformed_list, f, ensure_ascii=False, indent=4)

    print(
        f"\033[0;32m✅ Transformation terminée, fichier sauvegardé sous : {output_file}\033[0m"
    )

    return output_file


def delete_json_files():
    for file in os.listdir("."):
        if file.endswith(".json") and os.path.isfile(file):
            os.remove(file)
