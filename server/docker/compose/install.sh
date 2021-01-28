#!/bin/bash

# sh install.sh -h user@host -i -c
# sh install.sh -i -c
# -i exec init_config.sh and start compose
# -c exec post_config.sh

function exec_init_config() {
    config_path=/data/config/${name}/
    sudo mkdir -p ${config_path}
    if [ -d ${target_path}/conf/ ]; then
      echo -e "${number}.\033[32m copy conf dir\033[0m"
      sudo cp -rv ${target_path}/conf/* ${config_path}
    else
      echo -e "${number}.\033[33m no exist conf dir \033[0m"
    fi
    config_file=${target_path}/init_config.sh
    if [[ -f ${config_file} ]]; then
        echo -e "${number}.\033[32m init_config => \033[0m ${config_file}"
        sudo sh ${config_file}
    else
        echo -e "${number}.\033[33m no such file \033[0m ${config_file}"
    fi
}

function exec_post_config() {
    config_file=${target_path}/post_config.sh
    if [[ -f ${config_file} ]]; then
        echo -e "${number}.\033[32m post_config => \033[0m ${config_file}"
        sudo sh ${config_file}
    else
        echo -e "${number}.\033[33m no such file \033[0m ${config_file}"
    fi
}

function start_compose() {
    compose_file=${target_path}/docker-compose.yml
    if [[ -f ${compose_file} ]];then
        echo -e "${number}.\033[32m start_compose => \033[0m ${compose_file}"
#        sudo docker-compose --file ${compose_file} --env-file $HOME/compose/.env.global up -d --build
    fi
}

function print_app_list() {
    all_map=
    find_filter=(`find $HOME/compose/* -maxdepth 0 -type d | awk -F'/' '{print $0"|"$NF}' | cat -n | awk '{print $1"|"$2}'`)
    for (( i = 0; i < ${#find_filter[@]}; i++ )); do
      t=(`echo ${find_filter[i]} | tr '|' ' '` )
      num=${t[0]};path=${t[1]};name=${t[2]}
      all_map[i]="${num} ${name} ${path}"
    done
    view_map=
    for (( i = 0; i < ${#all_map[@]}; i++ )); do
       internal_map=(${all_map[i]})
       view_map="$view_map ${internal_map[0]}.${internal_map[1]}"
       if test `expr $[i+1] % 5` -eq 0; then
           view_map=$view_map`echo "\n"`
       fi
    done
    echo -e ${view_map} | awk '{printf "%-16s%-16s%-16s%-16s%-16s\n",$1,$2,$3,$4,$5}'
    unset view_map
}

while getopts ":h:ic" opt
do
	case $opt in
		h)
      source ../../../utility/share.sh
      host=$2
      sh_file='compose/install.sh'
      cp_path='../compose'
      rm_path='compose/'
      shift 2
      upload_exec $@
      break
			;;
		i)
		  print_app_list
      echo -n "please select install app number(example:1 2 ... or all)"
      read arg
      echo -e '\n'
      if [ "${arg}" = "all" ]; then
          for (( j = 0; j < ${#all_map[@]}; j++ )); do
               internal_map=(${all_map[j]})
               number=${internal_map[0]}
               name=${internal_map[1]}
               target_path=${internal_map[2]}
               echo ${internal_map[@]}
               exec_init_config
               start_compose
               echo -e '\n'
          done
      else
        arg=($arg)
        for i in ${arg[@]} ; do
          for (( j = 0; j < ${#all_map[@]}; j++ )); do
               internal_map=(${all_map[j]})
               if test $i -eq ${internal_map[0]}; then
                 number=${internal_map[0]}
                 name=${internal_map[1]}
                 target_path=${internal_map[2]}
                 echo ${internal_map[@]}
                 exec_init_config
                 start_compose
                 echo -e '\n'
               fi
          done
        done
      fi
			;;
	  c)
	    print_app_list
      echo -n "please select post_config app number(example:1 2 ... or all)"
      read arg
      echo -e '\n'
      if [ "${arg}" = "all" ]; then
          for (( j = 0; j < ${#all_map[@]}; j++ )); do
                 internal_map=(${all_map[j]})
                 number=${internal_map[0]}
                 name=${internal_map[1]}
                 target_path=${internal_map[2]}
                 echo ${internal_map[@]}
                 exec_post_config
                 echo -e '\n'
          done
      else
        arg=($arg)
        for i in ${arg[@]} ; do
          for (( j = 0; j < ${#all_map[@]}; j++ )); do
               internal_map=(${all_map[j]})
               if test $i -eq ${internal_map[0]}; then
                 number=${internal_map[0]}
                 name=${internal_map[1]}
                 target_path=${internal_map[2]}
                 echo ${internal_map[@]}
                 exec_post_config
                 echo -e '\n'
               fi
          done
        done
      fi
			;;
		?)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done