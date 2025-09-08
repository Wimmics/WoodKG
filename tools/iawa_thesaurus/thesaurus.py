from thesaurusFunctions import *

iawa_thesaurus_folder = "../../input/iawa_thesaurus"
raw_folder = f"{iawa_thesaurus_folder}/raw"
currated_folder = f"{iawa_thesaurus_folder}/currated"
output_file = "../../input/iawa_thesaurus/currated/iawa_thesaurus.json"


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    generate_full_combined_oneline_json(
        convert_iawa_tsv_to_json_three_dicts(raw_folder, currated_folder), output_file
    )

    delete_json_files()


if __name__ == "__main__":
    main()
