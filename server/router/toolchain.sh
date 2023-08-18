#!/bin/bash

# bash toolchain.sh -h user@host install
# -h show help

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