from observationFunctions import *

iawa_thesaurus_folder = "../../input/iawa_thesaurus"
currated_folder = f"{iawa_thesaurus_folder}/currated"
iawa_values_path = f"{currated_folder}/values.json"
foi_op_mapping_path = f"{currated_folder}/foiAndOp.json"
observation_output_folder = "temp/observation_output"


def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Génère le fichier JSON utilisé par MongoDB pour mapper les propriétés IAWA
    cleaned_taxa_path = rewrite_taxa()
    taxa_grouped_by_id = merge_species_by_ID(currated_folder, cleaned_taxa_path)
    observation_dict = split_measurements_from_file(taxa_grouped_by_id)
    taxa_with_properties = merge_taxa_with_details_by_valid_id(
        observation_dict, iawa_values_path
    )
    taxa_with_ids = enrich_taxa_with_taxonid_simple_match(
        taxa_with_properties, jsonlines_folder="wcvpJson"
    )
    taxa_enriched_by_genus = enrich_taxa_with_taxonid_by_genus(taxa_with_ids)
    final_observation_json = enrich_json_with_ids(
        observations_path=taxa_enriched_by_genus, mapping_path=foi_op_mapping_path
    )
    jsonlines_output_path = json_to_jsonlines(final_observation_json)
    extract_unique_taxon_without_taxonid(jsonlines_output_path)

    print("\033[32mScript executed successfully!\033[0m")
    print(
        "\033[32mOutput files are located in the 'Observation_output' directory.\033[0m"
    )


if __name__ == "__main__":
    main()
    delete_json_files("temp")
