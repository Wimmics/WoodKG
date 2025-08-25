import os
import json
import re
from collections import defaultdict
import glob

temp_folder = "temp"
input_folder = f"{temp_folder}/observation_input"
output_folder = f"{temp_folder}/observation_output"


def extract_iawa_information(json_obj):
    """Extracts family, genre, usual name, and original string from the given JSON object.
    Args:
        json_obj (dict): The JSON object containing the 'Taxon' field.
    Returns:
        tuple: A tuple containing family, genre, usual name, and original string.
    """
    family = ""
    original_string = json_obj["Taxon"].replace("?", "")

    for x in original_string.split("|"):
        x = x.replace("Synonym:", "").strip()

        family_match = re.search(r"[A-Z][A-Z]+\s[A-Z][A-Z]+|[A-Z][A-Z]+", x)
        family = family_match.group(0) if family_match else ""

        genre_match = re.search(
            r"[A-Z][a-z]+\s(spp\.|sp\.|SPP\.|SP\.|sect\.)|"
            r"[A-Z][a-z]+\s[a-z]+\s(subsp\.|var\.)\s[a-z]+|"
            r"[A-Z][a-z]+\s(aff\.|cf\.)\s[a-z\-]+|"
            r"[A-Z][a-z]+\s[a-z\-]+|"
            r"[A-Z][a-z]+\.*",
            x,
        )
        genre = genre_match.group(0) if genre_match else ""

        usual_name_match = re.search(r"\([A-Z][A-Z,\s]+\)", x)
        usual_name = usual_name_match.group(0) if usual_name_match else ""

        return family, genre, usual_name, original_string


def rewrite_taxa():
    """Rewrites the taxa in the Observation_input folder to match the expected format for InsideWood.

    Args:
        None
    Returns:
        str: The path to the updated JSON file with taxa rewritten.
    """

    json_files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

    if len(json_files) == 0:
        print("❌ Aucun fichier JSON trouvé dans le dossier Observation_input.")
        return None
    elif len(json_files) > 1:
        print(
            "❌ Plus d'un fichier JSON trouvé dans Observation_input, merci de n'en laisser qu'un seul."
        )
        return None

    input_file = json_files[0]
    input_path = os.path.join(input_folder, input_file)

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}validNames.json"
    else:
        output_file = f"{temp_folder}/validNames.json"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_data = []

    for obj in data:
        try:
            _, genre, _, _ = extract_iawa_information(obj)
            new_obj = obj.copy()
            new_obj["Taxon"] = genre  # Remplacement du champ "Taxon"
            updated_data.append(new_obj)
        except Exception as e:
            print(f"Erreur lors du traitement de l'entrée : {obj}\n{e}")
            updated_data.append(obj)  # Si erreur, on garde l'objet d'origine

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)


    return output_file


def merge_species_by_ID(reference_folder, species_json_path):
    """Combine the IDs of values sharing the same observable property and feature of interest.

    This function groups measurement IDs that observe the same property on the same
    feature of interest. Useful for merging related observations in datasets where
    properties and targets overlap

        Args:
            reference_folder (str): Path to the folder containing the reference of the IDs.
            species_json_path (str): Path to the JSON file containing species data.
        Returns:
            str: Path to the output JSON file with merged species data.


    """

    reference_json_filename = "values.json"
    reference_json_path = os.path.join(reference_folder, reference_json_filename)

    if not os.path.isfile(reference_json_path):
        raise FileNotFoundError(
            f"❌ Le fichier '{reference_json_filename}' est introuvable dans le dossier '{reference_folder}'."
        )
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}mergedbyid.json"
    else:
        output_file = f"{temp_folder}/mergedbyid.json"
    # Charger le fichier de référence
    with open(reference_json_path, "r", encoding="utf-8") as f:
        reference_data = json.load(f)

    # Grouper les IDs par (feature, property)
    grouped_ids_dict = defaultdict(list)
    for id_, info in reference_data.items():
        key = (info.get("feature"), info.get("property"))
        grouped_ids_dict[key].append(id_)

    # Garder uniquement les groupes avec plus d'un ID
    list_of_lists = [ids for ids in grouped_ids_dict.values() if len(ids) > 1]

    # Charger la liste d'espèces
    with open(species_json_path, "r", encoding="utf-8") as f:
        species_list = json.load(f)

    # Traiter chaque espèce avec un sampleID incrémental
    new_species_list = []
    sample_id_counter = 1

    for main_data in species_list:
        new_data = {"Taxon": main_data["Taxon"], "sampleID": sample_id_counter}
        sample_id_counter += 1

        used_ids = set()

        for group in list_of_lists:
            present_ids = [id_ for id_ in group if id_ in main_data]
            if len(present_ids) > 1:
                merged_key = "".join(present_ids)
                merged_value = "".join([main_data[id_] for id_ in present_ids])
                new_data[merged_key] = merged_value
                used_ids.update(present_ids)

        # Ajouter les champs non fusionnés
        for key, value in main_data.items():
            if key not in used_ids and key != "Taxon":
                new_data[key] = value

        new_species_list.append(new_data)

    # Sauvegarder dans un fichier
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(new_species_list, f, indent=2, ensure_ascii=False)

   
    return output_file


def split_measurements_by_id(data):
    """Splits compound measurement records into individual observations.

    For each non-empty measurement in the input data, creates a new entry with a unique
    Observation ID, preserving the associated taxon and sample ID. Each new entry represents
    a single observed property linked to its taxon.

    Args:
        data (list): List of dictionaries. Each dictionary represents a grouped record,
        with keys like 'Taxon', 'sampleID', and measurement fields.

    Returns:
        list: A list of dictionaries, where each dictionary is a distinct observation
        with a unique Observation ID.
    """
    all_results = []
    current_id = 1
    last_taxa = None

    for obj in data:
        taxa = obj.get("Taxon", "")
        sample_id = obj.get("sampleID")

        if taxa != last_taxa:
            current_id = 1
            last_taxa = taxa

        for key, val in obj.items():
            if key in ["Taxon", "sampleID"]:
                continue

            if val:  # ignore vide ou None
                new_entry = {
                    "Observationid": current_id,
                    "Taxon": taxa,
                    "VALID": key,
                    key: val,
                }
                if sample_id is not None:
                    new_entry["sampleID"] = sample_id

                all_results.append(new_entry)
                current_id += 1

    return all_results


def split_measurements_from_file(input_file):
    """Processes a JSON file and splits grouped measurements into individual observations.

    Reads measurement data from a JSON file, applies the splitting process to
    generate individual observations, and writes the result to a new JSON file.

    Args:
        input_file (str): Path to the input JSON file containing grouped measurement records.

    Returns:
        str: Path to the generated output file.
    """
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}dico.json"
    else:
        output_file = f"{temp_folder}/dico.json"
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    splited_data = split_measurements_by_id(data)

    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(splited_data, f_out, ensure_ascii=False, indent=2)

    return output_file


def merge_taxa_with_details_by_valid_id(taxa_file, details_file):
    """
    Merges taxa entries with corresponding detail information based on the 'VAlID' field.

    Args:
        taxa_file (str): Path to the JSON file containing the main taxa data (list of entries).
        details_file (str): Path to the JSON file containing detail mappings keyed by 'VAlID'.

    Returns:
        str: Path to the generated merged JSON file.
    """
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}mergedTaxa.json"
    else:
        output_file = f"{temp_folder}/mergedTaxa.json"
    # Load main taxa data
    with open(taxa_file, "r", encoding="utf-8") as f1:
        taxa_data = json.load(f1)

    # Load details data
    with open(details_file, "r", encoding="utf-8") as f2:
        details_data = json.load(f2)

    result = []

    for entry in taxa_data:
        merged_entry = dict(entry)  # make a copy for modification

        valid = entry.get("VALID")

        if valid and valid in details_data:
            detail = details_data[valid]
            merged_entry["value"] = detail.get("value", "")
            merged_entry["property"] = detail.get("property", "")
            merged_entry["feature"] = detail.get("feature", "")

        result.append(merged_entry)

    # Save merged output to JSON
    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(result, f_out, ensure_ascii=False, indent=2)

    return output_file


def enrich_taxa_with_taxonid_simple_match(input_file, jsonlines_folder):
    """
    Enriches taxa entries in the input JSON file by adding taxon IDs based on simple case-insensitive
    matching of scientific names found in multiple JSON Lines files within a folder.

    Args:
        input_file (str): Path to the input JSON file containing taxa data.
        jsonlines_folder (str): Path to the folder containing JSON Lines (.json) files with taxon info.

    Returns:
        str: Path to the enriched output JSON file.
    """
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}enrichedTaxa.json"
    else:
        output_file = f"{temp_folder}/enrichedTaxa.json"

    # Load main JSON data
    with open(input_file, "r", encoding="utf-8") as f:
        data_a = json.load(f)

    # Build dictionary mapping lowercase scientific name -> taxonid
    scientific_name_to_taxonid = {}

    # Read JSON Lines files in the folder
    pattern = os.path.join(jsonlines_folder, "*.json")
    for filename in glob.glob(pattern):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        name = entry.get("scientfiicname")  # typo preserved
                        taxonid = entry.get("taxonid")
                        if name and taxonid:
                            scientific_name_to_taxonid[name.lower().strip()] = taxonid
                    except json.JSONDecodeError as e:
                        print(f"JSON error in {filename}: {e}")
        except Exception as e:
            print(f"Read error in {filename}: {e}")

    # Enrich data with taxonid using simple lowercase match
    for item in data_a:
        taxon_name = item.get("Taxon")
        if taxon_name:
            key = taxon_name.lower().strip()
            taxonid = scientific_name_to_taxonid.get(key)
            if taxonid:
                item["taxonid"] = taxonid

    # Save enriched JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data_a, f, indent=2, ensure_ascii=False)

    return output_file


def enrich_taxa_with_taxonid_by_genus(input_json_path: str) -> str:
    """
    Enriches taxa entries in the input JSON file by adding taxon IDs based on matching the genus name
    (the first word of the taxon name) to scientific names found in multiple JSON Lines files in the 'wcvpJson' folder.

    Args:
        input_json_path (str): Path to the input JSON file containing taxa data.


    Returns:
        str: Path to the enriched output JSON file.
    """
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}enriched_by_genus.json"
    else:
        output_file = f"{temp_folder}/enriched_by_genus.json"
    # Load data to enrich
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build scientific name -> taxonid dictionary from JSON Lines files
    scientific_name_to_taxonid = {}
    for filename in glob.glob("wcvpJson/*.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f_part:
                for line in f_part:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        name = entry.get("scientfiicname")  # typo preserved
                        taxonid = entry.get("taxonid")
                        if name and taxonid:
                            scientific_name_to_taxonid[name.lower().strip()] = taxonid
                    except json.JSONDecodeError:
                        continue
        except Exception:
            continue

    # Helper function: get genus name (first word of taxon name, lowercased)
    def get_genus(taxa_name):
        if not taxa_name:
            return None
        return taxa_name.strip().split()[0].lower()

    # Enrich items missing 'taxonid' by matching the genus name
    updated_count = 0
    for item in data:
        if "taxonid" not in item:
            taxa_name = item.get("Taxon")
            genus = get_genus(taxa_name)
            if genus:
                taxonid = scientific_name_to_taxonid.get(genus)
                if taxonid:
                    item["taxonid"] = taxonid
                    updated_count += 1

    # Save enriched JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return output_file


def enrich_json_with_ids(observations_path, mapping_path):
    """Enriches the observations JSON file with FOIID and OPID based on a mapping file.
    Args:
        observations_path (str): Path to the observations JSON file.
        mapping_path (str): Path to the mapping JSON file containing FOI and OP mappings.

        Returns:
            str: Path to the enriched output JSON file.
    """
    if temp_folder.endswith("/"):
        output_file = f"{temp_folder}enriched_observations.json"
    else:
        output_file = f"{temp_folder}/enriched_observations.json"
    # Charger les fichiers JSON
    with open(observations_path, "r", encoding="utf-8") as f:
        observations = json.load(f)

    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    # Ajouter FOIID et OPID à chaque observation
    for obs in observations:
        feature = obs.get("feature")
        property_ = obs.get("property")
        foi_id = mapping.get("FOI", {}).get(feature, "000")
        op_id = mapping.get("OP", {}).get(property_, "000")

        obs["FOIID"] = foi_id
        obs["OPID"] = op_id

    # Définir le chemin du fichier de sortie si non spécifié
    if output_file is None:
        base, ext = os.path.splitext(observations_path)
        output_file = base + "_enriched.json"

    # Sauvegarder le JSON enrichi
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(observations, f, indent=2)

    return output_file


def json_to_jsonlines(input_json_path):
    """
    Converts a JSON file to JSON Lines format and saves it in the 'Observation_output' directory.
    Args:
        input_json_path (str): Path to the input JSON file.

    Returns:
        None"""
    # S'assurer que le dossier Observation_output existe

    os.makedirs(output_folder, exist_ok=True)

    if temp_folder.endswith("/"):
        output_file = f"{output_folder}observations_output.json"
    else:
        output_file = f"{output_folder}/observations_output.json"

    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(output_file, "w", encoding="utf-8") as f_out:
        for obj in data:
            line = json.dumps(obj, ensure_ascii=False)
            f_out.write(line + "\n")

    return output_file


def delete_json_files(file_path):
    """Deletes all JSON files in the specified directory."""
    for file in os.listdir(file_path):
        if file.endswith(".json") and os.path.isfile(os.path.join(file_path, file)):
            os.remove(os.path.join(file_path, file))


def extract_unique_taxon_without_taxonid(json_input_path: str) -> int:
    """
    Reads a JSON lines file, extracts objects without 'taxonid' but with a unique 'Taxon',
    writes these objects in a fixed output folder, and returns the number of extracted items.

    Args:
        json_input_path (str): Path to the input JSON lines file.

    Returns:
        int: Number of extracted items.
    """
    output_folder = "../../output/wrong_taxonid"
    os.makedirs(output_folder, exist_ok=True)

    basename = os.path.splitext(os.path.basename(json_input_path))[0]
    output_file = os.path.join(output_folder, "wrong_taxon_id.json")

    seen_taxa = set()
    count = 0

    with open(json_input_path, "r", encoding="utf-8") as f_in, open(
        output_file, "w", encoding="utf-8"
    ) as f_out:
        for line in f_in:
            try:
                data = json.loads(line)
                if "taxonid" not in data and "Taxon" in data:
                    taxon = data["Taxon"].strip()
                    if taxon and taxon not in seen_taxa:
                        seen_taxa.add(taxon)
                        f_out.write(json.dumps(data, ensure_ascii=False) + "\n")
                        count += 1
            except json.JSONDecodeError as e:
                print(f"Ligne invalide ignorée : {e}")

    # Codes couleur ANSI
    RED = "\033[31m"
    GREEN = "\033[32m"
    RESET = "\033[0m"

    if count == 0:
        print(
            f"{GREEN}For all your taxa we find a valid taxon ID in the powo database{RESET}"
        )
    else:
        print(
            f"{RED}{count} taxa we couldn't find a valid taxon ID for in the POWO database{RESET}"
        )
    print(
        f"{GREEN}You can see which taxa are invalid in the file: {output_file}{RESET}"
    )
