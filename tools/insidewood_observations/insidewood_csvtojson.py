from insidewood_csvtojson_functions import *
import os

currated_folder = "../../input/insidewood_observations/currated"


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    json_file = convert_first_tsv_in_insidewood()

    # Build output filename from source file name
    file_nopath = os.path.basename(json_file)
    output_file = os.path.join(currated_folder, f"{file_nopath}")

    transform_json_file(
        rewrite_taxa_with_genre(
            extract_taxa_and_numeric_keys(
                filter_json_by_key_number(
                    rename_json_keys(remove_fossil_hardwood(json_file)),
                    max_number=163,
                )
            )
        ),
        output_file,
    )

    delete_json_files()


if __name__ == "__main__":
    main()
