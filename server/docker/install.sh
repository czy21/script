#!/bin/bash

# bash install.sh -h user@host -i
# bash install.sh -i -c
# -i exec init.sh and start compose.yaml
# -b exec build.sh
# -c exec post.sh
# -p param_cluster_env <env>

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