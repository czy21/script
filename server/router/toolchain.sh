#!/bin/bash

# bash toolchain.sh -h user@host install
# -h show help

while getopts "h:" opt
do
	case $opt in
		h)
      source ../share.sh
      host=$2
      shift 2;
      upload_exec_py $@;
      break;
			;;
	esac
done