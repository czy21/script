#!/bin/bash

# bash switch.sh -h user@host -i [inventory_name] -t [tags]
# -i site | general
# -t [tags within inventory_file]
#    site: os | docker | hosts | k8s-master | k8s-node
#    general: prune | k8s-reset

while getopts ":h" opt
do
	case $opt in
		h)
      source ../../utility/share.sh
      host=$2
      shift 2
      upload_exec_py $@
      break
			;;
	esac
done