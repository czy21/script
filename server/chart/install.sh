#!/bin/bash

# bash install.sh -h user@host
# -a [install|delete|template|push|]
# -n string # namespace for this request
# -t int    # yaml's dir deep
# -p param_cluster_name < dev|ops >
#    param_ks_role < host | member >
#    param_ks_jwt <>
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