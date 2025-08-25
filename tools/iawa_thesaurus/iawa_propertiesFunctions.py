import csv
import json
import os
from collections import defaultdict
from itertools import combinations
import re

temp_folder = "temp"


def extract_iawa_features_from_tsv(input_folder, temp_folder=temp_folder):
    """
    Finds the first .tsv file in the IawaProperties_import directory,
    extracts the features of interest (FOI), operations (OP), and values (VAL),
    and writes the result to a JSON file in the current directory.
    Args:
        None
    Returns:
        str: Path to the generated JSON file.
    """
   
    # Trouve le premier fichier .tsv dans le dossier
    for file in os.listdir(input_folder):
        if file.endswith(".tsv"):
            input_csv = os.path.join(input_folder, file)
            base_name = os.path.splitext(file)[0]
            # Crée le nom du fichier JSON de sortie
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            if temp_folder.endswith("/"):
                output_file = f"{temp_folder}{base_name}.json"
            else:
                output_file = f"{temp_folder}/{base_name}.json"
            break
    else:
        print("❌ Aucun fichier .tsv trouvé dans IawaProperties_import.")
        return None

    # Structure : FOI > OP > [VAL...]
    features = defaultdict(lambda: defaultdict(list))

    # Lecture du fichier TSV
    with open(input_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        for row in reader:
            foi = row["FOI"].strip()
            op = row["OP"].strip()
            val = row["VAL"].strip()

            # Si val est TRUE ou FALSE, on combine avec l'op
            if val.upper() in ["TRUE", "FALSE"]:
                val_to_add = f"{op} {val}"
            else:
                val_to_add = val

            if val_to_add not in features[foi][op]:
                features[foi][op].append(val_to_add)

    final_json = {"featuresOfInterest": features}

    # Écriture du JSON dans le répertoire courant
    with open(output_file, "w", encoding="utf-8") as jsonfile:
        json.dump(final_json, jsonfile, indent=4, ensure_ascii=False)

    
    return output_file


def extract_iawa_numbers_mapping(input_folder, temp_folder=temp_folder):
    """
    finds the first .tsv file in the IawaProperties_import directory,
    extracts the iawaNumbers mapping from the file,
    We write only VAL if VAL is not TRUE or FALSE, else we write OP VAL.
    and writes the result to a JSON file in the current directory.
    Args:
        None
    Returns:
        str: Path to the generated JSON file.
    """

    tsv_file = None

    # Cherche le premier fichier TSV
    for f in os.listdir(input_folder):
        if f.endswith(".tsv"):
            tsv_file = f
            break

    if not tsv_file:
        raise FileNotFoundError(
            "❌ Aucun fichier .tsv trouvé dans 'IawaProperties_import'"
        )

    input_path = os.path.join(input_folder, tsv_file)
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}iawaNumbers.json"
    else:
        output_file = f"{temp_folder}/iawaNumbers.json"

    iawaNumbers = {}

    with open(input_path, newline="", encoding="utf-8") as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in reader:
            val = row["VAL"].strip()
            valid = row["VALID"].strip()
            op = row["OP"].strip()

            if val.upper() in ["TRUE", "FALSE"]:
                key = f"{op} {val}"
            else:
                key = val

            iawaNumbers[key] = valid

    with open(output_file, "w", encoding="utf-8") as jsonfile:
        json.dump({"iawaNumbers": iawaNumbers}, jsonfile, indent=4, ensure_ascii=False)

    
    return output_file


def map_features_to_iawa_ids(
    input_features_json,
    input_iawa_numbers_json,
    temp_folder=temp_folder,
):
    """
    Maps features from the input JSON file to their corresponding IAWA IDs based on the iawaNumbers mapping.

    Args:
        input_features_json (str): Path to the JSON file containing features to convert.
        input_iawa_numbers_json (str): Path to the JSON file containing the iawaNumbers mapping.
        output_file (str): Path where the output JSON file with numbered features will be saved.

    Returns:
        str: Path to the output JSON file containing the features mapped to their IAWA IDs.
    """
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}numbered_features.json"
    else:
        output_file = f"{temp_folder}/numbered_features.json"
    # Load features from input JSON
    with open(input_features_json, encoding="utf-8") as f:
        data = json.load(f)

    # Load IAWA ID mapping
    with open(input_iawa_numbers_json, "r", encoding="utf-8") as f:
        iawa_data = json.load(f)
    iawaNumbers = iawa_data.get("iawaNumbers", {})

    # Build the final numbered features dictionary
    numbered_features = {}

    for feature, properties in data["featuresOfInterest"].items():
        for prop, values in properties.items():
            for value in values:
                if value not in iawaNumbers:
                    print(f"⚠️ Unknown value in iawaNumbers: '{value}'")
                    continue

                iawa_id = iawaNumbers[value]
                numbered_features[iawa_id] = {
                    "value": value,
                    "property": prop,
                    "feature": feature,
                }

    # Save the output JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(numbered_features, f, indent=4, ensure_ascii=False)

   
    return output_file


def pad_json_keys_to_3_digits(input_file, temp_folder=temp_folder):
    """
    read a JSON file, format its keys to be 3 digits padded,
    and save the result to a new JSON file.
    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file.
    Returns:
        str: Path to the output JSON file.
    """
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}nh.json"
    else:
        output_file = f"{temp_folder}/nh.json"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Formater les clés
    new_data = {}
    for key, value in data.items():
        match = re.match(r"^(\d+)([a-zA-Z]*)$", key)
        if match:
            number_part, letter_part = match.groups()
            padded_key = f"{int(number_part):03d}{letter_part}"
            new_data[padded_key] = value
        else:
            new_data[key] = value

    # Créer le dossier s'il n'existe pas

    output_path = os.path.join(output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

  
    return output_path


def extract_sort_key(k):
    """Extracts the numeric and letter parts from a key,
    returning a tuple for sorting purposes.
    Args:
        k (str): The key to be sorted.
    Returns:
        tuple: A tuple containing the numeric part as an integer and the letter part as a string
    """
    match = re.match(r"(\d+)([a-zA-Z]*)", k)
    if match:
        num_part = int(match.group(1))
        letter_part = match.group(2)
        return (num_part, letter_part)
    else:
        return (float("inf"), k)


def generate_all_combinations(data):
    """
    Generates all combinations of keys grouped by property and feature,
    and returns a new dictionary with combined keys and values.
    Args:
        data (dict): The input dictionary with keys to be combined.
    Returns:
        dict: A new dictionary with combined keys and values.
    """
    grouped = {}
    for key, entry in data.items():
        prop = entry.get("property")
        feat = entry.get("feature")
        val = entry.get("value")

        group_key = (prop, feat)
        grouped.setdefault(group_key, []).append((key, val))

    result = {}

    for (prop, feat), entries in grouped.items():
        entries.sort(key=lambda x: extract_sort_key(x[0]))

        n = len(entries)
        for r in range(1, n + 1):
            for combo in combinations(entries, r):
                keys = [c[0] for c in combo]
                combined_key = "".join(keys)
                combined_value = " or ".join(c[1] for c in combo)

                result[combined_key] = {
                    "value": combined_value,
                    "property": prop,
                    "feature": feat,
                }
    return result


def generate_combinations_from_json(
    input_file, output_file_dir="../../input/iawa_thesaurus/currated"
):
    """
    Reads a JSON file, generates all combinations of keys grouped by property and feature,
    and saves the result to a new JSON file in the specified directory.
    Args:
        input_file (str): Path to the input JSON file.
        output_file_dir (str): Directory where the output JSON file will be saved.
    Returns:
        None
    """

    # Création du dossier de sortie s'il n'existe pas
    os.makedirs(output_file_dir, exist_ok=True)

    # Nom complet du fichier de sortie
    output_file = os.path.join(output_file_dir, "values.json")

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    new_data = generate_all_combinations(data)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

    print(
        f"\033[0;32m✅ Combinaisons générées et sauvegardées dans '{output_file}'\033[0m"
    )


def extract_foi_op_from_tsv(export_folder, folder_path):
    """
    Reads a .tsv file in the specified folder, extracts FOI and OP mappings,
    and saves the result to a JSON file in a subfolder named 'IawaProperties_export'.
    Args:
        folder_path (str): Path to the folder containing the .tsv file.
    Returns:
        None
    """

    # Trouve le seul fichier .tsv dans le dossier
    for file in os.listdir(folder_path):
        if file.lower().endswith(".tsv"):
            tsv_path = os.path.join(folder_path, file)
            break
    else:
        raise FileNotFoundError(f"❌ Aucun fichier .tsv trouvé dans : {folder_path}")

    # Lecture du TSV et création des dictionnaires
    foi_dict = {}
    op_dict = {}

    with open(tsv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            foi = row["FOI"].strip()
            foi_id = row["FOIID"].strip().zfill(3)
            if foi and foi_id:
                foi_dict[foi] = foi_id

            op = row["OP"].strip()
            op_id = row["OPID"].strip().zfill(3)
            if op and op_id:
                op_dict[op] = op_id

    result = {"FOI": foi_dict, "OP": op_dict}

    # Création du sous-dossier si besoin
    export_folder = os.path.join(folder_path, "../currated")
    os.makedirs(export_folder, exist_ok=True)

    # Écriture du JSON
    output_file = os.path.join(export_folder, "foiAndOp.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON écrit dans : {output_file}")


def delete_json_files(temp_folder=temp_folder):
    """
    Deletes all JSON files in the given directory.

    Args:
        temp_folder (str): Path to the temporary directory.
    """
    for file in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, file)
        if file.endswith(".json") and os.path.isfile(file_path):
            os.remove(file_path)
