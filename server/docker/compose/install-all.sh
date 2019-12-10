#!/usr/bin/env bash

# ./install-all.sh user@host -upload

case "$2" in
        -upload)
        scp -r ././../compose/ $1:
        ssh $1 '$HOME/compose/install-all.sh cent_a -exec;'
        ;;
        -exec)
        for t in `ls -ld $HOME/compose/* | grep "^d" | awk '{print $9}'`
        do
          config_file=${t}/config.sh
          if [ -f ${config_file} ]; then
              echo -e "\033[32mexecuting => ${config_file}\n\033[0m"
              sudo ${config_file}
          fi
          compose_file=${t}/docker-compose.yml
          if [ -f ${compose_file} ];then
              echo -e "\033[32mstarting => ${compose_file}\n\033[0m"
              sudo docker-compose -f ${compose_file} up -d
          fi
        done
        rm -rf compose
        ;;
        *)
        echo -e "\033[40;33m un_know input param \033[0m"
        ;;
esac