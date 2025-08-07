from thesaurusFunctions import *

iawa_thesaurus_folder = "../../input/iawa_thesaurus"
raw_folder = f"{iawa_thesaurus_folder}/raw"
currated_folder = f"{iawa_thesaurus_folder}/currated"


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    generate_full_combined_oneline_json(
        convert_iawa_tsv_to_json_three_dicts(raw_folder)
    )

    delete_json_files()


if __name__ == "__main__":
    main()
