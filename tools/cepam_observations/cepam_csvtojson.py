from sys import argv
from cepam_csvtojson_functions import *


def main():
    csv_file = (
        argv[1]
        if len(argv) > 1
        else "../../input/cepam_observations/raw/CEPAM_feature_net.csv"
    )
    export_dir = "../../input/cepam_observations/currated"

    print(f"📂Input CSV file: {csv_file}")

    # CD to the path of current script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    json_file = csv_to_json(csv_file)
    extracted_file = extract_taxa_and_numeric_keys(json_file)
    transform_json_file(extracted_file, export_dir=export_dir)


if __name__ == "__main__":
    main()
