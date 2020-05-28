#!/bin/bash

# sh install.sh -h user@host -i
# sh install.sh -i -c


function config_start() {
    config_file=${target_path}/config.sh
    if [[ -f ${config_file} ]]; then
        echo -e "\033[32m ${number} configing => ${config_file}\n\033[0m"
#        sudo sh ${config_file}
    fi
    compose_file=${target_path}/docker-compose.yml
    if [[ -f ${compose_file} ]];then
        echo -e "\033[32m ${number} starting => ${compose_file}\n\033[0m"
#        sudo docker-compose -f ${compose_file} up -d
    fi
}

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
      all_map=
      find_filter=(`find $HOME/compose/* -type d | cat -n | awk '{print $1","$2}'`)
      for (( i = 0; i < ${#find_filter[@]}; i++ )); do
        t=(${find_filter[i]/","/" "})
        id=${t[0]}
        name=${t[1]##*/}
        path=${t[1]}
        all_map[i]="${id} ${name} ${path}"
      done
      view_map=
      for (( i = 0; i < ${#all_map[@]}; i++ )); do
         internal_map=(${all_map[i]})
         view_map[i]="${internal_map[0]}"."${internal_map[1]}"
        if test `expr ${#view_map[@]} % 6` -eq 0; then
             echo ${view_map[@]}
             unset view_map
        fi
      done
      echo ${view_map[@]}
      echo -n "please select install number(default all)"
      read arg
      arg=($arg)
      if [ "${arg[0]}" = "all" ]; then
          for (( j = 0; j < ${#all_map[@]}; j++ )); do
               internal_map=(${all_map[j]})
                 target_path=${internal_map[2]}
                 number=${internal_map[0]}
                 config_start
          done
          exit
      fi
      for (( i = 0; i < ${#arg[@]}; i++ )); do
          for (( j = 0; j < ${#all_map[@]}; j++ )); do
               internal_map=(${all_map[j]})
               if test ${arg[i]} -eq ${internal_map[0]}; then
                 target_path=${internal_map[2]}
                 number=${internal_map[0]}
                 config_start
               fi
          done
      done
      shift 1
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done