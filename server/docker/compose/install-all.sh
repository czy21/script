#!/usr/bin/env bash

# ./install-all.sh user@host -upload

case "$2" in
        -upload)
        scp -r ././../compose/ $1:
        ssh $1 ' ./compose/install-all.sh cent_a -exec;'
        ;;
        -exec)
        for tar_dir in `ls compose`
        do
          if [ -d compose/${tar_dir} ]
          then
          sudo ./compose/${tar_dir}/config.sh
          sudo docker-compose -f compose/${tar_dir}/docker-compose.yml up -d
          fi
        done
        rm -rf compose
        ;;
        *)
        echo -e "\033[40;33m unknow input param \033[0m"
        ;;
esac