import os
import json
import re
from collections import defaultdict
import glob


def extract_taxonomic_information(taxon_name):
    """
    Extracts family, "genus species", usual name, and original string from the given JSON object.

    Args:
        taxon_name (string): value of the 'Taxon' field in an observation

    Returns:
        tuple: (family, "genus species", usual name, original string)
    """
    family = ""
    original_string = taxon_name
    taxon_name = taxon_name.replace("?", "")

    for x in taxon_name.split("|"):
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
        genus_species = genre_match.group(0) if genre_match else ""

        usual_name_match = re.search(r"\([A-Z][A-Z,\s]+\)", x)
        usual_name = usual_name_match.group(0) if usual_name_match else ""

        # print((family, genus_species, usual_name, original_string))
        return family, genus_species, usual_name, original_string


def reformat_taxon_names(input_file: str, output_file: str):
    """
    Rewrites an observation file after reformating the taxon name as "genus species"

    Args:
        input_file (str): JSON observations file.
        output_file (str): output JSON file where the rewritten taxa will be saved.
    """

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    updated_data = []

    for obj in data:
        try:
            _, genus_species, _, _ = extract_taxonomic_information(obj["Taxon"])
            new_obj = obj.copy()
            new_obj["Taxon"] = genus_species  # Remplacement du champ "Taxon"
            updated_data.append(new_obj)
        except Exception as e:
            print(f"Erreur lors du traitement de l'entrée : {obj}\n{e}")
            updated_data.append(obj)  # Si erreur, on garde l'objet d'origine

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)
    return


def merge_iawa_values(obs_file, iawa_values_file, output_file):
    """
    Combine the IAWA values sharing the same observable property and feature of interest.

    This function groups measurement IDs that observe the same property of the same
    feature of interest. Useful for merging related observations in datasets where
    properties and targets overlap

    Args:
        obs_file (str): file with observations containing modified taxon names.
        iawa_values_file (str): file containing the pre-computed IAWA values.
        output_file (str): path to the output JSON file with merged species data.
    """

    # Charger le fichier des valeurs IAWA
    if not os.path.isfile(iawa_values_file):
        raise FileNotFoundError(f"❌ File '{iawa_values_file}' does not exist.")
    with open(iawa_values_file, "r", encoding="utf-8") as f:
        iawa_values = json.load(f)

    # Grouper les valeurs IAWA par (feature, property)
    # Input: has documents like:
    #  { "nnn": { "value": "...", "property": "...", "feature": "..." }}
    #  { "ppp": { "value": "...", "property": "...", "feature": "..." }}
    # Output dictionnary is like
    #  { (property, feature): [nnn, ppp, ...] }
    grouped_vals = defaultdict(list)
    for id_, info in iawa_values.items():
        key = (info.get("feature"), info.get("property"))
        grouped_vals[key].append(id_)
    # Garder uniquement les groupes avec plus d'un ID
    grouped_vals_multi = [ids for ids in grouped_vals.values() if len(ids) > 1]

    # Charger les observations
    with open(obs_file, "r", encoding="utf-8") as f:
        obs_list = json.load(f)

    new_obs_list = []
    sample_id_counter = 0
    for obs in obs_list:

        # Si une observation a un sampleID le garder, sinon attribuer un nouveau sampleID incrémental
        if hasattr(obs, "sampleID"):
            new_data = {"Taxon": obs["Taxon"], "sampleID": obs["sampleID"]}
        else:
            new_data = {"Taxon": obs["Taxon"], "sampleID": sample_id_counter}
            sample_id_counter += 1

        # Grouper les valeurs IAWA par (feature, property)
        used_vals = set()
        for group in grouped_vals_multi:
            present_vals = [_val for _val in group if _val in obs]
            if len(present_vals) > 1:
                merged_key = "".join(present_vals)
                merged_value = "".join([obs[_val] for _val in present_vals])
                new_data[merged_key] = merged_value
                used_vals.update(present_vals)

        # Ajouter les champs non fusionnés
        for key, value in obs.items():
            if key not in used_vals and key != "Taxon":
                new_data[key] = value

        new_obs_list.append(new_data)

    # Sauvegarder dans un fichier
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(new_obs_list, f, indent=2, ensure_ascii=False)


def split_obs_to_measurements(input_file, output_file):
    """
    Transforms an observation file where an observation contains multiple measurements done at once,
    into observation with an individual measurement that are assigned a unique Observation ID,
    preserving the associated taxon and sample ID.
    The format of each measurement is as follows:
    ```
    {   "Observationid": 1,
        "Taxon": "Sclerocarya birrea",
        "iawa_val_key": "031033",
        "031033": "3133",
        "sampleID": "BRS18-2-31"
    }
    ```
    Args:
        input_file (str): file with observations containing aggregated IAWA values,
                with keys like 'Taxon', 'sampleID', and measurement fields.
        output_file (str): output JSON file for individual measturements.
    """

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

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
                    "iawa_val_key": key,
                    key: val,
                }
                if sample_id is not None:
                    new_entry["sampleID"] = sample_id

                all_results.append(new_entry)
                current_id += 1

    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(all_results, f_out, ensure_ascii=False, indent=2)


def enrich_obs_with_iawa_details(
    input_file, iawa_values_file, iawa_foi_op_file, output_file
):
    """
    Adds to observation entries the corresponding IAWA information
    about the value ('iawa_val_key' field), and the ids of the feature of interest (FOI)
    and observable property (OP)

    Args:
        input_file (str): file containing the observation data
        iawa_values_file (str): file containing the detail of IAWA values
        iawa_foi_op_file (str): file containing IAWA FOIs and OPs
        output_file (str): output JSON file for individual measturements.
    """

    # Load observation data
    with open(input_file, "r", encoding="utf-8") as f1:
        obs_data = json.load(f1)

    # Load IAWA values
    with open(iawa_values_file, "r", encoding="utf-8") as f2:
        iawa_values = json.load(f2)

    # Load IAWA FOIs and OPs
    with open(iawa_foi_op_file, "r", encoding="utf-8") as f3:
        iawa_foi_ops = json.load(f3)

    result = []
    for entry in obs_data:
        merged_entry = dict(entry)  # make a copy for modification
        iawa_key = entry.get("iawa_val_key")

        if iawa_key and iawa_key in iawa_values:
            iawa_value = iawa_values[iawa_key]
            merged_entry["value"] = iawa_value.get("value", "")

            iawa_property = iawa_value.get("property", "")
            merged_entry["property"] = iawa_property
            op_id = iawa_foi_ops.get("OP", {}).get(iawa_property, "000")
            merged_entry["property_id"] = op_id

            iawa_feature = iawa_value.get("feature", "")
            merged_entry["feature"] = iawa_feature
            foi_id = iawa_foi_ops.get("FOI", {}).get(iawa_feature, "000")
            merged_entry["feature_id"] = foi_id

        result.append(merged_entry)

    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(result, f_out, ensure_ascii=False, indent=2)


def enrich_obs_with_taxon_simple_match(
    input_file: str, taxo_folder: str, output_file: str
):
    """
    Enriches observation entries by adding the POWO/WCVP taxon IDs.
    Matching scientific names is simple case-insensitive.
    If the "genus species" name is not found, then try to match with the genus name only.

    Args:
        input_file (str): file containing the observation data
        taxo_folder (str): folder containing JSON-Line files with taxonomic info formatted like:
            ```
                {
                    "taxonid": "3152367",
                    "family": "Polypodiaceae",
                    "genus": "Elaphoglossum",
                    "scientfiicname": "Elaphoglossum pygmaeum"
                }
            ```
            Note: the double 'i' typo in 'scientfiicname' is how it comes from in WCVP.
        output_file (str): output JSON file for individual measurements.
    """

    # Load observation data
    with open(input_file, "r", encoding="utf-8") as f:
        obs_data = json.load(f)

    # Build dictionary mapping lowercase scientific name -> taxonid
    scientific_name_to_taxonid = {}

    # Read taxonomy files from the folder
    for filename in glob.glob(os.path.join(taxo_folder, "*.json")):
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
    for item in obs_data:
        taxon_name = item.get("Taxon")
        if taxon_name:
            taxonid = scientific_name_to_taxonid.get(taxon_name.lower().strip())
            if taxonid:
                item["taxonid"] = taxonid
            else:
                # If 'taxonid' not found, then match the genus name
                genus = taxon_name.strip().split()[0].lower()
                if genus:
                    taxonid = scientific_name_to_taxonid.get(genus)
                    if taxonid:
                        item["taxonid"] = taxonid

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(obs_data, f, indent=2, ensure_ascii=False)


def json_to_jsonlines(input_file, output_file):
    """
    Converts a JSON file to JSON Lines format and saves it in the 'Observation_output' directory.
    Args:
        input_file (str): JSON file containing the observation data
        output_file (str): output file in JSON-line format
    """

    with open(input_file, "r", encoding="utf-8") as f:
        obs_data = json.load(f)

    with open(output_file, "w", encoding="utf-8") as f_out:
        for obj in obs_data:
            line = json.dumps(obj, ensure_ascii=False)
            f_out.write(line + "\n")


def extract_obs_without_taxonid(input_file: str, output_file: str) -> int:
    """
    Reads observations in JSON-line format and extracts those with a 'Taxon' but no 'taxonid'.
    Writes these observations unmatched with a taxon id in the output file.

    Args:
        input_file (str): JSON file containing the observation data in JSON-line format
        output_file (str): output file in JSON-line format containing the taxa without taxon id
    """

    seen_taxa = set()
    count = 0

    with open(input_file, "r", encoding="utf-8") as f_in, open(
        output_file, "w", encoding="utf-8"
    ) as f_out:
        for line in f_in:
            try:
                obs_data = json.loads(line)
                if "taxonid" not in obs_data and "Taxon" in obs_data:
                    taxon = obs_data["Taxon"].strip()
                    if taxon and taxon not in seen_taxa:
                        seen_taxa.add(taxon)
                        f_out.write(json.dumps(obs_data, ensure_ascii=False) + "\n")
                        count += 1
            except json.JSONDecodeError as e:
                print(f"Ligne invalide ignorée : {e}")

    # Codes couleur ANSI
    RED = "\033[31m"
    GREEN = "\033[32m"
    RESET = "\033[0m"

    if count == 0:
        print(f"{GREEN}All observations were matched with a taxon id in POWO{RESET}")
    else:
        print(
            f"{RED}{count} observations could not be matched with a taxon in POWOZ{RESET}"
        )


def delete_json_files(file_path):
    """Deletes all JSON files in the specified directory."""
    for file in os.listdir(file_path):
        if file.endswith(".json") and os.path.isfile(os.path.join(file_path, file)):
            os.remove(os.path.join(file_path, file))
