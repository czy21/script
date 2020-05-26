#!/bin/bash

# sh builder.sh -h user@host -t <image_tag>
# sh builder.sh -t <image_tag>

while [[ $# -ge 1 ]];
do
	case $1 in
		-h)
      source ../../utility/share.sh
      host=$2
      sh_file='frp/builder.sh'
      cp_path='../frp'
      rm_path='frp/'
      shift 2
      upload_exec $@
      break
			;;
		-t)
      sudo docker build --no-cache --force-rm --tag frp:$2 --file frp/Dockerfile frp/
      shift 2
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done