# input

Chaque dossier présent dans le répertoire `input` est structuré en deux sous-dossiers :

- `raw/` : contient les fichiers bruts, tels que téléchargés depuis leurs sources respectives sur Internet.
- `currated/` : contient les fichiers transformés à l’aide de mes scripts, adaptés à la génération de graphes RDF.

## Table des matières

- [cepam_observations](#cepam_observations)
- [iawa_thesaurus](#iawa_thesaurus)
- [insidewood_observations](#insidewood_observations)
- [powo](#powo)

---

### cepam_observations

- `raw/` : contient un fichier CSV téléchargeable des observations issues du CEPAM.
- `currated/` : contient une version transformée de ce fichier au format JSON, utilisable directement par mon code.

Exemple de structure JSON :

    {
      "Taxon": "Sclerocarya birrea subsp caffra",
      "sampleID": "BRS18-2-31",
      "001": "1",
      "005": "5"
    }

Les identifiants des propriétés sont normalisés sur trois chiffres.

---

### iawa_thesaurus

- `raw/` : contient un fichier TSV représentant la modélisation du thésaurus IAWA, développée avec l’équipe WIMMICS.
- `currated/` : contient trois fichiers JSON :

  - `foiAndOP.json` : deux dictionnaires référençant les *features of interest* et les *observable properties*, avec leurs identifiants respectifs.
  - `values.json` : contient les valeurs observées selon le format suivant :

        "001002": {
          "value": "boundaries distinct or indistinct or absent",
          "property": "boundary marks",
          "feature": "growth ring"
        }

    Certaines valeurs correspondent à des unions. Les liens vers `foiAndOP.json` se font via les champs `property` et `feature`.

  - `iawa_thesaurus.json` : fichier utilisé par XR2RML pour générer le RDF du thésaurus.

---

### insidewood_observations

- `raw/` : contient un fichier CSV téléchargeable depuis le site InsideWood :  
  https://insidewood.lib.ncsu.edu/search

- `currated/` : contient une version transformée de ce fichier, au même format que celui du CEPAM.

---

### powo

- `raw/` : contient la version brute du fichier CSV téléchargé depuis POWO (WCVP).
- `currated/` : contient sa version transformée en JSON, exploitable par XR2RML.