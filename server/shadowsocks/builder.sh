#!/bin/bash

#!/usr/bin/env bash

# sh builder.sh --init user@host --tag <image_tag>
# sh builder.sh --tag <image_tag>

while [[ $# -ge 1 ]];
do
	case $1 in
		--init)
			if [[ ! $2 ]] || [[ "$2" =~ ^"--".* ]]; then
			  echo -e "\033[31m$1 value is null \033[0m"
			  shift 1
        continue
      fi
      host=$2
      shift 2
      ssh $host "rm -rf ./shadowsocks/" && scp -r ../shadowsocks/ $host:
      ssh $host '$HOME/shadowsocks/builder.sh '$@';'
      break
			;;
		--tag)
			if [[ ! $2 ]] || [[ "$2" =~ ^"--".* ]]; then
			  echo -e "\033[31m$1 value is null \033[0m"
			  shift 1
        continue
      fi
      sudo docker build --no-cache --force-rm --tag shadowsocks:$2 --file shadowsocks/Dockerfile shadowsocks/
      rm -rf shadowsocks/
      shift 2
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done