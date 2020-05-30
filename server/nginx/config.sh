#!/bin/bash

# sh config.sh -h user@host -c
# sh config.sh -c

while [[ $# -ge 1 ]];
do
	case $1 in
		-h)
      source ../../utility/share.sh
      host=$2
      sh_file='nginx/config.sh'
      cp_path='../nginx/'
      rm_path='nginx/'
      shift 2
      upload_exec $@
      break
			;;
		-c)
		  dir=$(cd "$(dirname "$0")"; pwd)
		  sudo rm -rf /data/config/nginx/conf.d/
		  sudo cp -r $dir/cert/ /data/config/nginx/
      sudo cp -r $dir/conf.d/ /data/config/nginx/
      sudo docker restart nginx
      shift 1
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done