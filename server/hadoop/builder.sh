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
#      ssh $2 "rm -rf ./hadoop/"
      scp -r ../hadoop/ $2:
      ssh $2 '$HOME/hadoop/builder.sh --tag '$4';'
      break
			;;
		--tag)
			if [[ ! $2 ]] || [[ "$2" =~ ^"--".* ]]; then
			  echo -e "\033[31m$1 value is null \033[0m"
			  shift 1
        continue
      fi
      sudo docker build --no-cache --force-rm --tag hadoop:$2 --file hadoop/Dockerfile hadoop/
      rm -rf hadoop/
      shift 2
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done