#!/bin/bash

sudo docker exec virtuoso \
    isql -H localhost -U dba -P $VIRTUOSO_DBA_PWD exec="LOAD import_woodkg.isql"
