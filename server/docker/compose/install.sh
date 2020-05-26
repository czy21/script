#!/usr/bin/env bash

# sh install.sh -h user@host -i -c
# sh install.sh -i -c

while [[ $# -ge 1 ]];
do
	case $1 in
		-h)
      source ../../../utility/share.sh
      host=$2
      sh_file='compose/install.sh'
      cp_path='../compose'
      rm_path='compose/'
      shift 2
      upload_exec $@
      break
			;;
		-i)
		  shift 1
      for t in `ls -ld $HOME/compose/* | grep "^d" | awk '{print $9}'`
        do
          config_file=${t}/config.sh
          if [[ -f ${config_file} ]] && [[ $1 == '-c' ]]; then
              echo -e "\033[32m executing => ${config_file}\n\033[0m"
              sudo sh ${config_file}
          fi
          compose_file=${t}/docker-compose.yml
          if [[ -f ${compose_file} ]];then
              echo -e "\033[32m starting => ${compose_file}\n\033[0m"
              sudo docker-compose -f ${compose_file} up -d
          fi
        done
      shift 1
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done