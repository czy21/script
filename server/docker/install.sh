#!/bin/bash

# bash install.sh -h user@host -i -c
# bash install.sh -i -c
# -i exec init_config.sh and start compose
# -c exec post_config.sh

while getopts ":h" opt
do
	case $opt in
		h)
      source ../../utility/share.sh
      host=$2
      shift 2
      upload_exec $@
      break
			;;
	esac
done