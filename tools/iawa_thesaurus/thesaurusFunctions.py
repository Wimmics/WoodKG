import csv
import json
import os
import re
from itertools import combinations


output_file = "../../input/iawa_thesaurus/currated/iawa_thesaurus.json"


def normalize_id(identifier):
    """Normalize an ID to 3 digits, keeping any trailing letters."""
    match = re.match(r"(\d+)([a-zA-Z]*)", identifier)
    if match:
        number_part = match.group(1).zfill(3)
        letter_part = match.group(2)
        return number_part + letter_part
    return identifier  # Return as-is if no match


def convert_iawa_tsv_to_json_three_dicts(input_folder, currated_folder):
    """
    Convert IAWA TSV files to a structured JSON format with three dictionaries.
    The TSV file should be in the format:
    FOI, FOIFR, FOIID, OP, OPFR, OPID, VAL, VALFR, VALID
    The output JSON will have three dictionaries:
    - featuresOfInterest: {foiid: {"label_en": foi, "label_fr": foifr}}
    - observableProperties: {opid: {"label_en": op, "label_fr": opfr}}
    - values: {valid: {"label_en": val, "label_fr": valfr, "foi": foi, "op": op}}
    """
    # Find the first .tsv file
    for file in os.listdir(input_folder):
        if file.endswith(".tsv"):
            input_csv = os.path.join(input_folder, file)
            base_name = os.path.splitext(file)[0]
            output_file = os.path.join(currated_folder, f"{base_name}_structured.json")
            break
    else:
        print("❌ No .tsv file found in IawaProperties_import.")
        return None

    features_of_interest = {}
    observable_properties = {}
    values = {}

    with open(input_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        for row in reader:
            # Retrieve and clean fields
            foi = row["FOI"].strip()
            foifr = row["FOIFR"].strip()
            foiid = normalize_id(row["FOIID"].strip())

            op = row["OP"].strip()
            opfr = row["OPFR"].strip()
            opid = normalize_id(row["OPID"].strip())

            val = row["VAL"].strip()
            valfr = row["VALFR"].strip()
            valid = normalize_id(row["VALID"].strip())

            # Fill the FOI and OP dictionaries
            if foiid and foiid not in features_of_interest:
                features_of_interest[foiid] = {"label_en": foi, "label_fr": foifr}

            if opid and opid not in observable_properties:
                observable_properties[opid] = {"label_en": op, "label_fr": opfr}

            # Fill the VALUES dictionary
            if valid and valid not in values:
                values[valid] = {
                    "label_en": val,
                    "label_fr": valfr,
                    "foi": foi,
                    "op": op,
                }

    final_json = {
        "featuresOfInterest": features_of_interest,
        "observableProperties": observable_properties,
        "values": values,
    }

    # Write JSON
    with open(output_file, "w", encoding="utf-8") as jsonfile:
        json.dump(final_json, jsonfile, indent=4, ensure_ascii=False)

    print(f"Converted IAWA thesaurus from TSV to JSON in '{output_file}'")
    return output_file


def key_sort_key(k):
    """Generate a sort key for dictionary keys that may contain numbers and letters.
    This function ensures that numeric parts are sorted numerically,
    while letter parts are sorted lexicographically.
    """
    match = re.match(r"(\d+)([a-zA-Z]*)", k)
    if match:
        num_part = int(match.group(1))
        letter_part = match.group(2)
        return (num_part, letter_part)
    else:
        return (float("inf"), k)


def generate_value_combinations(values):
    """Generate all combinations of values based on their features of interest (foi) and observable properties (op).
    The result is a dictionary where keys are combinations of value IDs,
    and values are dictionaries with combined labels and associated foi and op.
    ARGS:
        values (dict): Dictionary of values where each key is a value ID and each value is
        a dictionary containing 'foi', 'op', 'label_en', and 'label_fr'.
    RETURNS:
        dict: A dictionary with combined value IDs as keys and dictionaries with combined labels and associated foi
    """
    grouped = {}

    for key, entry in values.items():
        foi = entry.get("foi")
        op = entry.get("op")
        en = entry.get("label_en")
        fr = entry.get("label_fr")

        group_key = (foi, op)
        grouped.setdefault(group_key, []).append((key, en, fr))

    result = {}

    for (foi, op), entries in grouped.items():
        entries.sort(key=lambda x: key_sort_key(x[0]))

        n = len(entries)
        for r in range(1, n + 1):
            for combo in combinations(entries, r):
                keys = [c[0] for c in combo]
                combined_key = "".join(keys)
                combined_en = " or ".join(c[1] for c in combo)
                combined_fr = " ou ".join(c[2] for c in combo)

                result[combined_key] = {
                    "label_en": combined_en,
                    "label_fr": combined_fr,
                    "foi": foi,
                    "op": op,
                }

    return result


def generate_full_combined_oneline_json(input_file: str):
    """
    Génère un fichier JSONL (une document JSON par ligne) à partir du fichier structuré,
    avec les valeurs combinées produites par `generate_value_combinations`.

    Chaque ligne contient un champ "type" : "featuresOfInterest", "observableProperties", ou "values".
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        full_data = json.load(f)

    # Récupère les données
    features = full_data.get("featuresOfInterest", {})
    properties = full_data.get("observableProperties", {})
    original_values = full_data.get("values", {})

    # Combine les valeurs (fonction fournie ailleurs)
    combined_values = generate_value_combinations(original_values)

    with open(output_file, "w", encoding="utf-8") as f_out:
        # Écrit chaque feature
        for id_, content in features.items():
            entry = {"id": id_, "type": "featuresOfInterest", **content}
            f_out.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # Écrit chaque propriété observable
        for id_, content in properties.items():
            entry = {"id": id_, "type": "observableProperties", **content}
            f_out.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # Écrit chaque valeur combinée
        for id_, content in combined_values.items():
            entry = {"id": id_, "type": "values", **content}
            f_out.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"JSONL file (one document per line) with combined values saved in: '{output_file}'")
    return output_file


def convert_to_onelinejson(data: dict, output_file: str):
    with open(output_file, "w", encoding="utf-8") as f:
        for parent_key, entries in data.items():
            for entry_id, entry_content in entries.items():
                # Ajoute l'ID et le type à l'entrée
                entry = {"id": entry_id, "type": parent_key, **entry_content}
                json_line = json.dumps(entry, ensure_ascii=False)
                f.write(json_line + "\n")


def delete_json_files():
    for file in os.listdir("."):
        if file.endswith(".json") and os.path.isfile(file):
            os.remove(file)
