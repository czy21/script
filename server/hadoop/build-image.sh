#!/bin/bash

#!/usr/bin/env bash

# $1: user@host
# $2: --upload <image_tag> | --tag <image_tag>

# ./build-image.sh user@host --upload --tag <image_tag>

#case "$2" in
#        --upload)
##        scp -r ../hadoop/ $1:
##        ssh $1 '$HOME/hadoop/build-image.sh --tag '$3';'
#        ;;
#        --tag)
#          sudo docker build --no-cache --force-rm --tag hadoop:$3 --file hadoop/Dockerfile ./hadoop
#        ;;
#        *)
#        echo -e "\033[40;33m un_know input param \033[0m"
#        ;;
#esac
while [[ $# -ge 1 ]];
do
	case $1 in
		--upload)
			if [[ ! $2 ]] || [[ "$2" =~ ^"--".* ]]; then
			  echo "\033[31m$1 value is null \033[0m"
			  shift 1
        continue
      fi
      shift 2
			;;
		--tag)
			if [[ ! $2 ]] || [[ "$2" =~ ^"--".* ]]; then
			  echo "\033[31m$1 value is null \033[0m"
			  shift 1
        continue
      fi
      shift 2
			;;
		*)
		  echo "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done