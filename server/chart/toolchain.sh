#!/bin/bash

# bash toolchain.sh -h user@host install
# -h show help
# -p param_cluster_name [dev | ops]
#    param_ks_role [host | member]
#    param_ks_jwt  str
# --ignore-namespace
# --create-namespace

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