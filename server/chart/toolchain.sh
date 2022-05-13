#!/bin/bash

# bash toolchain.sh -h user@host
# -i # helm install
# -d # helm delete
# -b build_file
# -a push
# -n namespace
# -p param_cluster_name dev|ops
#    param_ks_role host|member
#    param_ks_jwt  str
# --ignore-namespace
# --create-namespace

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