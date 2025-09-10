# input

This directory contains the input data used to generate the WoodKG knowledge graph.

### iawa_thesaurus

- `raw/`: contains a TSV file representing the IAWA thesaurus modeling, developed by the WIMMICS team. This is an export from this [Google Sheet](https://docs.google.com/spreadsheets/d/1PUWlXuF0ph-XoZLRLSvAEFjLJwu-esHQfoGm06nKwRs/edit?usp=sharing)
- `currated/`: contains three JSON files:
    - `foiAndOP.json`: two dictionaries referencing the *features of interest* and *observable properties* with their respective identifiers.
    - `values.json`: contains the values of the observable properties, in the following format:

                "001002": {
                    "value": "boundaries distinct or indistinct or absent",
                    "property": "boundary marks",
                    "feature": "growth ring"
                }

        Some values correspond to unions. Links to `foiAndOP.json` are made via the `property` and `feature` fields.

    - `iawa_thesaurus.json`: file used by Morph-xR2RML to generate the thesaurus RDF.

---

### cepam_observations

- `raw/`: contains a downloadable CSV file of observations provided by researchers of the CEPAM.
- `currated/`: contains a transformed version of this file in JSON format.

JSON structure example:

        {
            "Taxon": "Sclerocarya birrea subsp caffra",
            "sampleID": "BRS18-2-31",
            "001": "1",
            "005": "5"
        }

Property identifiers are normalized to three digits.

---

### insidewood_observations

- `raw/`: contains a CSV file downloadable from the InsideWood website: https://insidewood.lib.ncsu.edu/search. 
  Do get it you must do a search by IAWA code (e.g. '1p') or keyword.
  Then, on the Search Results page, click the "Select All Description Results" checkbox and "Export nnn Selected Results" link.
- `currated/`: contains a transformed version of this file, in the same format as CEPAM.

---

### powo

- `raw/`: contains the raw version of the CSV file downloaded from POWO (WCVP).
- `currated/`: contains its transformed JSON version, usable by Morph-xR2RML.
