#!/bin/bash

DB=database
COLLECTION=collection

FILE=$1

MONGO_CONTAINER=$(docker ps --format='{{.Names}}' | grep "mongo-xr2rml")
XR2RML_CONTAINER=$(docker ps --format='{{.Names}}' | grep "morph-xr2rml")

# --- Import the JSON files of a directory into MongoDB
docker exec -w /mongo_tools "$MONGO_CONTAINER" \
   /bin/bash import-json-files.sh $DB $COLLECTION taxonid

# --- Run the translation to RDF
docker exec -w /xr2rml_config "$XR2RML_CONTAINER" \
   /bin/bash run_xr2rml_template.sh mapping_wcvp.ttl $(basename "$FILE" .json).ttl dataset1 $COLLECTION
