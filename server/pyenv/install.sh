#!/bin/bash

# for machine version centos

# install to host machine
# sh install.sh --host user@host --install

# install to container
# sh install.sh --host user@host --install --container [container_name] --user [container_user]

set -e

root_dir="pyenv"

while [[ $# -ge 1 ]];
do
	case $1 in
		--host)
			if [[ ! $2 ]] || [[ "$2" =~ ^"--".* ]]; then
			  echo -e "\033[31m$1 host is null \033[0m"
			  shift 1
        continue
      fi
      host=$2
      shift 2
      ssh $host 'rm -rf $HOME/'"${root_dir}"'/' && scp -r ../${root_dir}/ $host:
      ssh $host '$HOME/'"${root_dir}"'/install.sh '$@';'
      ssh $host 'rm -rf $HOME/'"${root_dir}"'/'
      break
			;;
		--install)
		  if [[ ! $2 ]]; then
          curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
          echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
          source ${HOME}/.bashrc
          mkdir ${HOME}/.pyenv/cache

		      rm -rf ${HOME}/${root_dir}/
		      shift 1
		      continue
		  fi
      if [ $2 == "--container" ]; then
        container_name=$3
        shift 3
        user=""
        if [ $1 == "--user" ]; then
            user=$2
            shift 2
        fi
          sudo docker exec -i $container_name bash -c 'rm -rf $HOME/'"${root_dir}"'/'
          sudo docker cp $HOME/rpm/ $container_name:$user
          sudo docker exec -i $container_name bash -c 'sh $HOME/'"${root_dir}"'/install.sh --install'
      fi
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done