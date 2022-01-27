#!/bin/bash

# bash install.sh -h user@host
# -a push apply delete
# -n string # namespace for this request
# -t int    # yaml's dir deep
# -p param_cluster_env <env>

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