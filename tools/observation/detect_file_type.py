import os
import sys


def detect_single_file_type(file_path):
    """Detects the file type based on its extension.
    Args:
        file_path (str): Path to the file.
    Returns:
        str: "json" if the file is a JSON file, "csv" if it is a CSV or TSV file,
             or an error message if the file type is not supported.
    """
    if not os.path.isfile(file_path):
        return "Error: The provided path is not a valid file."

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".json":
        return "json"
    elif ext in [".csv", ".tsv"]:
        return "csv"
    else:
        return "Error: File must be a .json, .csv, or .tsv."


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = detect_single_file_type(file_path)
    print(result)
