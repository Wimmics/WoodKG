import csv
import json
import os


def convert_value(value):
    """Converts some values from CSV to the wording they have in the target IRIs.
    This allows to build the IRIs just by appending the value to the namespace.

    This applies to taxonomic ranks and taxonomic status.

    # Taxonomic ranks
    Here are all the taxonomic ranks found in WCVP:
    Convariety, ecas., Form, Genus, grex, lusus, , microf., microgène, modif., monstr., nid,
    nothof., nothosubsp., nothovar., positio, proles, provar., psp., Species, stirps, , subap.,
    Subform, subproles, Subspecies, subspecioid, Subvariety, Variety

    Only the following ones are translated to IRIs:
    Form, Genus, Species, Subform, Subspecies, Subvariety, Variety

    Args:
        value (str): The original value from CSV.

    Returns:
        str: The converted value.
    """
    mapping = {
        # Taxonomic ranks
        "Form": "Forma",
        "Genus": "Genus",
        "Species": "Species",
        "Subform": "SubForma",
        "Subspecies": "SubSpecies",
        "Subvariety": "SubVarietas",
        "Variety": "Varietas",
        # Taxonomic status
        "Artificial Hybrid": "ArtificialHybrid",
        "Provisionally Accepted": "ProvisionallyAccepted",
    }
    # Return original if no mapping found
    return mapping.get(value, value)


def convert_csv_to_json_lines(csv_path, json_lines_path):
    """Converts a CSV file to JSON Lines format.
    Args:
        csv_path (str): Path to the input CSV file.
        json_lines_path (str): Path to the output JSON Lines file.
        encoding (str): Encoding of the CSV file (default is 'utf-8').
    Returns:
        None
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the file is not a CSV file.
    """
    with open(csv_path, encoding="utf-8") as f_in, open(
        json_lines_path, "w", encoding="utf-8"
    ) as f_out:
        reader = csv.DictReader(f_in, delimiter="|")
        for row in reader:
            # Convert taxonomic ranks
            if "taxonrank" in row:
                row["taxonrank"] = convert_value(row["taxonrank"])
            # Convert taxonomic statuses
            if "taxonomicstatus" in row:
                row["taxonomicstatus"] = convert_value(row["taxonomicstatus"])
            f_out.write(json.dumps(row, ensure_ascii=False) + "\n")


def wcvpJson(csv_folder, output_folder):
    """Convertit tous les fichiers CSV d'un dossier en fichiers JSON Lines.

    Args:
        csv_folder (str): Dossier contenant les CSV.
        output_folder (str): Dossier où sauvegarder les fichiers JSON Lines.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Liste triée des fichiers CSV commençant par "partie_" et finissant par ".csv"
    csv_files = sorted([f for f in os.listdir(csv_folder) if f.endswith(".csv")])

    if not csv_files:
        print("❌ Aucun fichier '*.csv' trouvé dans le dossier.")
        return

    for i, filename in enumerate(csv_files, start=0):
        csv_path = os.path.abspath(os.path.join(csv_folder, filename))
        json_output = os.path.abspath(
            os.path.join(output_folder, f"wcvp_taxonomy_{i:02d}.json")
        )
        print(f"✅ Converting {csv_path} -> {json_output}")
        convert_csv_to_json_lines(csv_path, json_output)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    folder_path = os.path.join(script_dir, "../../input/wcvp")
    raw = os.path.join(folder_path, "raw")
    currated = os.path.join(folder_path, "currated")
    wcvpJson(raw, currated)
