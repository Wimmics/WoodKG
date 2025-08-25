# WoodKG

WoodKG is a project to build a knowledge graph linking botanical taxonomy and wood anatomical features defined by IAWA.  
The data mainly comes from CEPAM samples and the InsideWood database.

- POWO for [Plants Of the World Online](https://powo.science.kew.org/)
- CEPAM for [Cultures – Environnements. Préhistoire, Antiquité, Moyen Âge](https://www.cepam.cnrs.fr/)
- IAWA for [International Association of Wood Anatomists](http://www.maderasenargentina.com.ar/archivos/IAWA_Committee1989.pdf)
- [InsideWood](https://insidewood.lib.ncsu.edu/search)

## Usage

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Example of use](#example-of-use)
- [Technologies used](#technologies-used)

## Installation

Before starting, you must download two important resources:

### 1. Morph-XR2RML

1. Go to the `xr2rml` folder.

2. Install XR2RML following the instructions here:  
   [morph-xr2rml Docker README](https://github.com/frmichel/morph-xr2rml/blob/master/docker/README.md)

3. Open the file `mongo_tools/import-tools.sh`.

4. Modify the following line:  
   ```bash 
   MONGO_IMPORT_MAXSIZE=16000000
   ```
   to increase the size 
   ```
   MONGO_IMPORT_MAXSIZE=160000000
   ```

### 2. WCVP - Plant taxonomy
From the project root, run:
```bash
mkdir -p input/powo/raw input/powo/currated
```

Download the WCVP taxonomic data from the following address:

https://sftp.kew.org/pub/data-repositories/WCVP/

Download the file `wccp_dwca.zip`, then extract the file `wcvp_taxon.csv`.
Place it in `input/powo/raw`.

Run the script `./tools/powo/scripts/split_wcvp.sh`

## Features

### input

This folder contains all the data sources:
- powo/: WCVP taxonomy,
- [insidewood_observations/](input/insidewood_observations/): InsideWood observations,
- [cepam_observations/](input/cepam_observations/): CEPAM observations.

Each subfolder contains:
- `raw/`: raw files,
- `currated/`: transformed versions ready to be used.

### output

Contains the generated RDF graphs:
- the POWO taxonomy (powo_taxonomy_*.ttl),
- the observations (InsideWood, CEPAM),
- the IAWA thesaurus.

A file [wrong_taxonid.json](output/wrong_taxonid/observations_output_unique_sans_taxonid.json) indicates the samples for which no taxonomic identifier was found in POWO.

### tools

Contains scripts:
- for transforming raw files to currated,
- for generating RDF files.

### xr2rml

Contains mapping and configuration files necessary to use XR2RML.

## Usage

Launch the main menu with:

## Table of contents
**./menu.sh**

The menu offers different options by calling .sh scripts located in `tools/<subfolder>/scripts`:

1. Generate IAWA thesaurus as JSON  
Transforms the IAWA thesaurus files from [raw](/input/iawa_thesaurus/raw/) to [currated](/input/iawa_thesaurus/currated/).  
Using `tools/iawa_thesaurus/scripts/thesaurus.sh`  
and `tools/iawa_thesaurus/scripts/iawa_properties.sh` 

2. Generate IAWA thesaurus as RDF  
Generates thesaurus.ttl in [output](/output/) from [JSON](/input/iawa_thesaurus/currated/) files.  
Must be executed after option 1.  
Using `tools/xr2rml/observation2xr2rml -thesaurus`

3. Generate POWO taxonomy as JSON  
Transforms WCVP taxonomic files from [raw](/input/powo/raw/) to [currated](/input/powo/currated/).  
Using `tools/powo/scripts/powo.sh`

4. Generate POWO taxonomy as RDF  
Generates RDF files [powo_taxonomy_*.ttl](/output/) from [JSON](/input/powo/currated/) files.  
Using `tools/xr2rml/observation2xr2rml -taxon`

5. Generate CEPAM observations as JSON  
Transforms CEPAM observations from [raw](/input/cepam_observations/raw/) to [currated](/input/cepam_observations/currated/).  
Using `tools/cepam_observations/scripts/cepam_csvtojson.sh`

6. Generate InsideWood observations as JSON  
Transforms InsideWood observations from [raw](/input/insidewood_observations/raw/) to [currated](/input/insidewood_observations/currated/).  
Using `tools/insidewood_observations/scripts/insidewood_observations.sh`

7. Generate observations as RDF  
Requires a .json file (currated type) and generates RDF observations in [output](/output/).

8. Quit  
Exit the menu.

## Example of use

Here is a complete execution example:
```bash
./menu.sh
```
Then in the menu:  
- 1 → to generate the IAWA JSON thesaurus  
- 3 → to generate the currated POWO files  
- 5 → to transform CEPAM observations  
- 7 → and enter this path:
```bash
input/cepam_observations/currated/CEPAM_feature_net_taxa_and_numbers_homogene.json
```

## Technologies used

- SPARQL, SOSA/SSN ontologies  
- Morph-xR2RML  
- Python 3.10.12
