#!/bin/bash

# bash toolchain.sh -h user@host -f [inventory_file] -t [tags]
# -f deploy.yml | general.yml
# -t [tags within inventory_file]
#    deploy: os | docker | k8s | k8s-master | k8s-worker
#    general: prune | machine

while getopts "h:" opt
do
	case $opt in
		h)
      source ../share.sh
      host=$2
      shift 2
      upload_exec_py $@
      break
			;;
	esac
done