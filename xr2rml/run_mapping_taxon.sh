#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

DB=database
COLLECTION=collection

# --- Gestion de l'argument pour sélectionner le numéro de taxon
if [[ $1 =~ ^-([0-9]+)$ ]]; then
    TAXON_NUMBER="${BASH_REMATCH[1]}"
    TAXON_FILE="powo_taxonomy_${TAXON_NUMBER}.ttl"
else
    echo "Usage: $0 -<number>    (ex: $0 -1)"
    exit 1
fi

MONGO_CONTAINER=$(docker ps --format='{{.Names}}' | grep "mongo-xr2rml")
XR2RML_CONTAINER=$(docker ps --format='{{.Names}}' | grep "morph-xr2rml")

# --- Import the JSON files of a directory into MongoDB
docker exec -w /mongo_tools "$MONGO_CONTAINER" \
   /bin/bash import-json-files.sh $DB $COLLECTION taxonid

# --- Run the translation to RDF
docker exec -w /xr2rml_config "$XR2RML_CONTAINER" \
   /bin/bash run_xr2rml_template.sh mapping_powo.ttl "$TAXON_FILE" dataset1.0 $COLLECTION
