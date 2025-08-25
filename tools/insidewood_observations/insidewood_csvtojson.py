from insidewood_csvtojson_functions import *
import os


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    transform_json_file(
        rewrite_taxa_with_genre(
            extract_taxa_and_numeric_keys(
                filter_json_by_key_number(
                    rename_json_keys(
                        remove_fossil_hardwood(convert_first_tsv_in_insidewood())
                    ),
                    max_number=163,
                )
            )
        )
    )

    delete_json_files()


if __name__ == "__main__":
    main()
