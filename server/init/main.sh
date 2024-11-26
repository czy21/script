#!/bin/bash

# bash main.sh user@host 
# --ansible-host [ansible host file]
# -f [inventory_file]
# -t [tags within inventory_file]
#    deploy: os | docker | k8s | k8s-master | k8s-worker
#    general: prune | machine

../share.sh $@