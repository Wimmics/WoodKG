from observationFunctions import *
from taxon_currated_to_taxon_filtered import taxonomy_to_single_jsonl

iawa_folder = "../../input/iawa_thesaurus"
iawa_currated_folder = f"{iawa_folder}/currated"
iawa_values_file = f"{iawa_currated_folder}/values.json"
foi_op_mapping_file = f"{iawa_currated_folder}/foiAndOp.json"

output_folder = "../../output"
temp_folder = "temp"
temp_input = f"{temp_folder}/input"
temp_wcvp = f"{temp_folder}/wcvp"

# Codes couleur ANSI
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


if __name__ == "__main__":

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Rewrite the observations with taxon names formatted exactly as "genus species"
    obs_files = [f for f in os.listdir(temp_input) if f.endswith(".json")]
    if len(obs_files) == 0:
        print("❌ No JSON file found in $temp_input.")
        exit(-1)
    elif len(obs_files) > 1:
        print("❌ More than one JSON file found in $temp_input.")
        exit(-1)
    obs_with_reformatted_taxa = f"{temp_folder}/obs_1_reformatted_taxon_names.json"
    reformat_taxon_names(
        os.path.join(temp_input, obs_files[0]), obs_with_reformatted_taxa
    )
    print(f"Reformated taxon names in observations: {obs_with_reformatted_taxa}")

    # Reformat observations by concatenating the IAWA values by group (feature of interest, observable property)
    obs_merge_iawa_vals = f"{temp_folder}/obs_2_merged_values.json"
    merge_iawa_values(
        obs_with_reformatted_taxa,
        f"{iawa_currated_folder}/values.json",
        obs_merge_iawa_vals,
    )
    print(f"Reformated observations with aggregated IAWA values: {obs_merge_iawa_vals}")

    # Turn multi-measuremlent observations into single-measurement observations
    measurements_file = f"{temp_folder}/obs_3_individual.json"
    split_obs_to_measurements(obs_merge_iawa_vals, measurements_file)
    print(f"Turned observations into single measurements: {measurements_file}")

    # Enrich each observation with IAWA value, property and feature
    obs_with_iawa = f"{temp_folder}/obs_4_individual_with_iawa.json"
    enrich_obs_with_iawa_details(
        measurements_file, iawa_values_file, foi_op_mapping_file, obs_with_iawa
    )
    print(f"Enriched observations with IAWA property/feature: {obs_with_iawa}")

    # Generate a single file from the generated WCVP files and remove syntactically incorrect entries
    os.makedirs(temp_wcvp, exist_ok=True)
    taxonomy_to_single_jsonl(
        "../../input/wcvp/currated", f"{temp_wcvp}/wcvp_filtered.json"
    )
    print(f"Generated single-file taxonomy: {temp_wcvp}/wcvp_filtered.json")

    # Enrich each observation with the WCVP taxon ID based on the taxon name
    obs_with_taxa = f"{temp_folder}/obs_5_individual_with_iawa_taxa.json"
    enrich_obs_with_taxon_simple_match(obs_with_iawa, temp_wcvp, obs_with_taxa)
    print(f"Enriched observations with WCVP taxon id: {obs_with_taxa}")

    # Convert the JSON file into a "JSON-line" file ie. with 1 JSON document per line
    os.makedirs(output_folder, exist_ok=True)

    obs_file_jsonlines = os.path.abspath(os.path.join(output_folder, "observations.json"))
    json_to_jsonlines(obs_with_taxa, obs_file_jsonlines)
    print(f"{GREEN}Final file of observations: {obs_file_jsonlines}.{RESET}")

    output_file = os.path.join(output_folder, "unmatched_taxa.json")
    extract_obs_without_taxonid(obs_file_jsonlines, output_file)
    print(f"Observations not matched with a WCVP taxon id (if any): {output_file}")

    # delete_json_files("temp_folder")
