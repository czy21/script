#!/bin/bash

# bash toolchain.sh -h user@host -i
# -i # exec init.sh and start compose.yaml
# -d # docker-compose down
# -b build_file
# -a str
# -n namespace
# -p param_cluster_name test|nas|dsm

while getopts "h:" opt
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