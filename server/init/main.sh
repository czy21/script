#!/bin/bash

# bash main.sh -h user@host -f [inventory_file] -t [tags]
# -f deploy.yml | general.yml
# -t [tags within inventory_file]
#    deploy: os | docker | k8s | k8s-master | k8s-worker
#    general: prune | machine

../share.sh $@