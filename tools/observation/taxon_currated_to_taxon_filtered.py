import os
import json

def extract_fields_to_jsonl(input_dir, output_file):
    """
    Extrait les champs 'taxonid', 'family', 'genus', 'scientificname' de chaque ligne JSON dans chaque fichier
    du dossier input_dir (chaque ligne est un JSON), et écrit un JSON par ligne dans output_file.
    """
    with open(output_file, 'w', encoding='utf-8') as out:
        for filename in os.listdir(input_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(input_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            filtered = {
                                "taxonid": data.get("taxonid"),
                                "family": data.get("family"),
                                "genus": data.get("genus"),
                                "scientfiicname": data.get("scientfiicname")
                            }
                            out.write(json.dumps(filtered, ensure_ascii=False) + "\n")
                        except json.JSONDecodeError:
                            print(f"Erreur JSON dans {filename} : {line[:30]}...")
