# WoodKG

WoodKG is a knowledge graph for African Wood charcoal studies.
This repository contains the tools that are used to build the 3 graphs that are linked together and form WoodKG:
- a biological taxonomy providing IRIs for taxa and scientific names,
- a thesaurus of anatomical characteristics being observed,
- the observations of charcoal samples.

The data sources are the following:
- [Plants Of the World Online](https://powo.science.kew.org/) (POWO) describes up to date taxonomic name and geolocation. The [World Checklist of Vascular Plants](https://powo.science.kew.org/about-wcvp) (WCVP) is the taxonomic names backbone that POWO relies on;
- [International Association of Wood Anatomists's features list](http://www.maderasenargentina.com.ar/archivos/IAWA_Committee1989.pdf) (IAWA). From this list we have derived a representation centered around the concepts of Feature of Interest (FoI), Observable Property (OP) and values, available as a [shared document](https://docs.google.com/spreadsheets/d/1PUWlXuF0ph-XoZLRLSvAEFjLJwu-esHQfoGm06nKwRs/edit?usp=sharing);
- Charcoal observations coming from 2 sources:
    - [InsideWood](https://insidewood.lib.ncsu.edu/search)'s charcoal descriptions;
    - The Southern African wood CHArcoal description proided by research lab [Cultures – Environnements. Préhistoire, Antiquité, Moyen Âge](https://www.cepam.cnrs.fr/) (CEPAM).

Descriptions coming from InsideWood and CEPAM both use IAWA's features list.


## Table of Concent

- [Installation](#installation)
- [Repository Structure](#repository-structure)
- [Usage](#usage)
- [Requirements](#requirements)


## Installation

Before starting, you must download two resources:

### 1. [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml/)

1. Create folder `xr2rml`.
2. CD to `xr2rml` and install the necessary files and folders following the [Docker installation instructions](https://github.com/frmichel/morph-xr2rml/blob/master/docker/README.md).
3. Open file `xr2rml/mongo_tools/import-tools.sh`.
4. Modify the following line:  
   ```bash 
   MONGO_IMPORT_MAXSIZE=16000000
   ```
   to increase the size 
   ```
   MONGO_IMPORT_MAXSIZE=160000000
   ```

Start Morph-xR2RML containers with `docker-compose up -d`.


### 2. WCVP - Plant taxonomy
Run the commands below to download the WCVP taxonomic data `wccp_dwca.zip`, extract the file `wcvp_taxon.csv` and place it in `input/wcvp/raw`.

From the project root, run:
```bash
mkdir -p input/wcvp/raw input/wcvp/currated
cd input/wcvp/raw
wget https://sftp.kew.org/pub/data-repositories/WCVP/wcvp_dwca.zip
unzip wcvp_dwca.zip wcvp_taxon.csv
```

Then, return to the project root and run the script `./tools/wcvp/split_wcvp.sh`.
This will split the csv file into chunks of maximum 100000 lines each.


## Repository Structure

### input

This folder contains the data sources: [WCVP taxonomy](input/wcvp/), [IAWA thesaurus](input/iawa_thesaurus/), [InsideWood observations](input/insidewood_observations/), [CEPAM observations](input/cepam_observations/).

Each folder contains two subfolders:
- `raw/` for the raw files downloaded from their respective sources,
- `currated/`for the transformed versions ready to be used for RDF generation.

[More details.](input/README.md)

### output

Contains the generated RDF files:
- the WCVP taxonomy (wcvp_taxonomy_*.ttl)
- the IAWA thesaurus
- the InsideWood or CEPAM observations (observations_*.ttl)

File [unmatched_taxa.json](output/unmatched_taxa.json) gives the observations for which no taxonomic identifier was found in WCVP.


### tools

Contains the scripts for transforming raw files into currated files, and currated files into RDF files.


## Usage

Launch the main menu with: ``./menu.sh``

**Generation of RDF with Morph-xR2RML requires sudo rights to launch Docker.**

The menu offers different options by calling bash scripts located in `tools/<subfolder>/scripts`:

1. Generate IAWA thesaurus as JSON  
Transforms the IAWA thesaurus files from [raw](/input/iawa_thesaurus/raw/) to [currated](/input/iawa_thesaurus/currated/) using `tools/iawa_thesaurus/scripts/thesaurus.sh` and `tools/iawa_thesaurus/scripts/iawa_properties.sh`.

2. Generate IAWA thesaurus as RDF  
Generates iawa_thesaurus.ttl in [output](/output/) from [JSON](/input/iawa_thesaurus/currated/) files using `tools/xr2rml/observation2xr2rml --thesaurus`. Must be executed after option 1.  

3. Generate WCVP taxonomy as JSON  
Transforms WCVP taxonomic files from [raw](/input/wcvp/raw/) to [currated](/input/wcvp/currated/) using `tools/wcvp/scripts/wcvp.sh`.

4. Generate WCVP taxonomy as RDF  
Generates RDF files [wcvp_taxonomy_*.ttl](/output/) from [JSON](/input/wcvp/currated/) files using `tools/xr2rml/observation2xr2rml --taxon`.

5. Generate CEPAM observations as JSON  
Transforms CEPAM observations from [raw](/input/cepam_observations/raw/) to [currated](/input/cepam_observations/currated/) using `tools/cepam_observations/scripts/.cepam_csvtojson.sh`

6. Generate InsideWood observations as JSON  
Transforms InsideWood observations from [raw](/input/insidewood_observations/raw/) to [currated](/input/insidewood_observations/currated/) using `tools/insidewood_observations/scripts/insidewood_observations.sh`.

7. Generate observations as RDF  
Requires a .json file (currated type) and generates RDF observations in [output](/output/).

8. Quit  
Exit the menu.

### Example of use

Here is a complete execution example:
```bash
./menu.sh
```
Then in the menu:  
- 1 → to generate the IAWA JSON thesaurus  
- 3 → to generate the currated WCVP files  
- 5 → to transform CEPAM observations  
- 7 → and enter this path:
```bash
input/cepam_observations/currated/CEPAM_feature_net_taxa_and_numbers_homogene.json
```

## Requirements

- Morph-xR2RML  
- Python >3.10.12
