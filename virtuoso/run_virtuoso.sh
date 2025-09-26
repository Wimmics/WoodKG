#!/bin/bash

sudo docker run  \
    --name virtuoso \
    --detach \
    --restart always \
    --env DBA_PASSWORD=$VIRTUOSO_DBA_PWD \
    --publish 1111:1111 \
    --publish 8890:8890 \
    --volume `pwd`:/database \
    openlink/virtuoso-opensource-7:latest
