from iawa_propertiesFunctions import *

iawa_thesaurus_folder = "../../input/iawa_thesaurus"
raw_folder = f"{iawa_thesaurus_folder}/raw"
currated_folder = f"{iawa_thesaurus_folder}/currated"
temp_folder = "temp"


def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Ce code génère les combinaisons à partir des fichiers JSON et les sauvegarde dans un fichier JSON.
    generate_combinations_from_json(
        pad_json_keys_to_3_digits(
            map_features_to_iawa_ids(
                extract_iawa_features_from_tsv(raw_folder),
                extract_iawa_numbers_mapping(raw_folder),
            ),
        )
    )
    extract_foi_op_from_tsv(currated_folder, raw_folder)


if __name__ == "__main__":
    main()
    delete_json_files()
