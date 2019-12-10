#!/usr/bin/env bash

# $1: user@host
# $2: --upload | --exec
# $3: --config

# ./install-all.sh user@host --upload --all

case "$2" in
        --upload)
        scp -r ././../compose/ $1:
        ssh $1 '$HOME/compose/install-all.sh cent_a --exec '$3';'
        ;;
        --exec)
        for t in `ls -ld $HOME/compose/* | grep "^d" | awk '{print $9}'`
        do
          config_file=${t}/config.sh
          if [[ -f ${config_file} ]] && [[ $3 == '--config' ]]; then
              echo -e "\033[32m executing => ${config_file}\n\033[0m"
              sudo ${config_file}
          fi
          compose_file=${t}/docker-compose.yml
          if [[ -f ${compose_file} ]];then
              echo -e "\033[32m starting => ${compose_file}\n\033[0m"
              sudo docker-compose -f ${compose_file} up -d
          fi
        done
        rm -rf compose
        ;;
        *)
        echo -e "\033[40;33m un_know input param \033[0m"
        ;;
esac