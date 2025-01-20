# WoodKG
WoodKG is a knowledge graph for African Wood charcoal studies. This repository contains the details of graph building and wood identification algorithm.
The graph is a merge of plant informations coming from: (1) Plant Of the World Online (POWO) which describe up to date taxonomic name, plants hierarchy and geolocation; (2) InsideWood wood charcoal description which use the International Association of Wood Anatomists (IAWA) features list and (3) the Southern African wood CHArcoal description using the IAWA features list.

# Requierement

All the implementation is contains in a Jupyter Notebook

# Usage

The identlib.py script take a csv of wood description and give the closest spicies based on their IAWA features. The list is order by number of mismatches.

# Example of identification
| Family | Taxa | Mismatchs |
|---|---|---|
| Olea |	Olea europaea subsp. cuspidata	| 7
| Olea	| Olea capensis subsp. enervis	| 8
| Oleaceae	| Olea schliebenii	| 8
| Asteraceae	| Brachylaena huillensis	| 9
| Loganiaceae	| Strychnos mitis	|9
| Olea	| Olea europaea subsp. cuspidata	| 9
| Ebenaceae	| Diospyros abyssinica	| 10
| Fabaceae	| Bauhinia tomentosa	| 10
| Malvaceae	| Dombeya rotundifolia	| 10
| Oleaceae	| Olea capensis	| 10
| Phyllanthaceae	|Cleistanthus capuronii	| 10
| Rhamnaceae	| Lasiodiscus mildbraedii	| 10
|Sapindaceae	| Dodonaea viscosa	|10
| Sapotaceae	| Synsepalum revolutum	| 10
| Apocynaceae	| Carissa spinarum	| 11
| Asteraceae	| Brachylaena discolor	| 11
| Asteraceae	| Brachylaena merana	| 11
| Capparaceae	| Cadaba glandulosa	| 11
| Capparaceae |	Cadaba rotundifolia	| 11
