#!/bin/bash

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
      all_map=
      for t in `find $HOME/compose/* -type d | cat -n | awk '{print $1","$2}'`; do
           t=(${t/","/" "})
           id=${t[0]}
           name=${t[1]##*/}
           path=${t[1]}
           all_map[$id]="${id} ${name} ${path}"
      done
      view_map=
      for (( i = 0; i < ${#all_map[@]}; i++ )); do
         index=`expr $i + 1`
         internal_map=(${all_map[index]})
         view_map[index]="${internal_map[0]}"."${internal_map[1]}"
      done
      echo ${view_map[@]}
      shift 1
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done