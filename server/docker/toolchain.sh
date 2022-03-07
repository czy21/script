#!/bin/bash

# bash toolchain.sh -h user@host -i
# -i exec init.sh and start compose.yaml
# -b exec build.sh
# -c exec post.sh
# -p param_cluster_name <env>
# --force-recreate  # recreate containers

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