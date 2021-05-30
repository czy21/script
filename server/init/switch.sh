#!/bin/bash
# bash switch.sh -h user@host -t
# -t centos | ubuntu | docker | k8s
set -e

while getopts ":h:t:" opt
do
	case $opt in
  h)
    source ../../utility/share.sh
    host=$2
    sh_file=$0
    shift 2
    upload_exec_sh $@
    break
    ;;
  t)
    parent_path=$(cd "$(dirname "$0")";pwd)
    private_key_file=${parent_path}/___temp/private-key
    if [ -f "${private_key_file}" ]; then
      chmod 600 ${private_key_file}
    fi
    shift 1
    ansible_cmd="ansible-playbook --inventory-file ${parent_path}/hosts ${parent_path}/$1.yml --verbose"
    if [ $1 == 'centos' ]; then
      bash -c "${ansible_cmd} --ask-pass"
    elif [ $1 == 'ubuntu' ]; then
      bash -c "${ansible_cmd} --ask-pass"
    elif [ $1 == 'docker' ]; then
      bash -c "${ansible_cmd} --private-key ${private_key_file}"
    fi
		;;
		?)
		echo -e "\033[31m$1 un_know input param \033[0m"
		break
		;;
	esac
done
