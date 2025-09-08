from sys import argv
from cepam_csvtojson_functions import *
import os


def main():
    csv_file = (
        argv[1]
        if len(argv) > 1
        else "../../input/cepam_observations/raw/CEPAM_feature_net.csv"
    )
    print(f"📂Input CSV file: {os.path.abspath(csv_file)}")

    export_dir = "../../input/cepam_observations/currated"
    # Supprimer tout le contenu du dossier s'il existe
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    os.makedirs(export_dir, exist_ok=True)

    # CD to the path of current script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    json_file = csv_to_json(csv_file)
    extracted_file = extract_taxa_and_numeric_keys(json_file)

    # Build output filename from source file name
    file_noext_nopath = os.path.splitext(os.path.basename(csv_file))[0]
    output_file = os.path.abspath(os.path.join(export_dir, f"{file_noext_nopath}.json"))

    transform_json_file(extracted_file, output_file)


if __name__ == "__main__":
    main()
