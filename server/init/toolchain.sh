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
      host=$OPTARG
			;;
	esac
done
shift "$((OPTIND-1))"

source ../share.sh
upload_exec_py $@