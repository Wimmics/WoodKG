# WoodKG
WoodKG is a knowledge graph for African Wood charcoal studies. This repository contains the details of graph building and wood identification algorithm.
The graph is a merge of plant informations coming from: (1) Plant Of the World Online (POWO) which describe up to date taxonomic name, plants hierarchy and geolocation; (2) InsideWood wood charcoal description which use the International Association of Wood Anatomists (IAWA) features list and (3) the Southern African wood CHArcoal description using the IAWA features list.

# Requierement

All the implementation is contains in a Jupyter Notebook

# Usage

The identlib.py script take a csv of wood description and give the closest spicies based on their IAWA features. The list is order by number of mismatches.
