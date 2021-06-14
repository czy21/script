#!/bin/bash

# bash install.sh -h user@host

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