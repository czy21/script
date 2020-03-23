#!/usr/bin/env bash

# sh install-all.sh --init user@host --start --config
# sh install-all.sh --start --config

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
      ssh $host "rm -rf compose/" && scp -r ../compose $host:
      ssh $host '$HOME/compose/install-all.sh '$@';'
      break
			;;
		--start)
		  shift 1
      for t in `ls -ld $HOME/compose/* | grep "^d" | awk '{print $9}'`
        do
          config_file=${t}/config.sh
          if [[ -f ${config_file} ]] && [[ $1 == '--config' ]]; then
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