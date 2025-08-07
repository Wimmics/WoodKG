# tools

Le répertoire `tools` est organisé en plusieurs sous-dossiers, chacun pouvant contenir jusqu’à quatre types de sous-dossiers :

- `scripts/` : contient les scripts `.sh` utilisés pour exécuter les programmes Python correspondants.
- `temp/` : contient les fichiers temporaires nécessaires au bon fonctionnement des programmes.
- `mapping/` : contient les fichiers de mapping compatibles avec XR2RML.
- fichiers Python : chaque module Python est généralement constitué de deux fichiers :
  - un fichier se terminant par `functions.py` qui regroupe les fonctions utilitaires,
  - un fichier principal (sans `functions` dans son nom) qui lance le programme.

## Table des matières
- [xr2rml](#xr2rml)

---

### xr2rml

#### observation2xr2rml

Ce script effectue les opérations suivantes :
- Copie le fichier de mapping approprié dans le dossier `xr2rml_config`.
- Copie le fichier JSON dans `mongo_import`.
- Exécute `xr2rml.sh` avec l’option `--taxon`, `--iawa`, ou `--thesaurus` selon les besoins.
- Copie les résultats générés par XR2RML depuis `xr2rml_output` vers le dossier `output`.

#### xr2rml

Ce fichier exécute l’un des scripts `run_mapping` pour générer les fichiers RDF à l’aide de XR2RML.