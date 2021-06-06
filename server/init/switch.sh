#!/bin/bash
# bash switch.sh -h user@host -t [target]
# -t centos | ubuntu | docker | set-hosts | k8s-master | k8s-nodes
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
    root_path=$(cd "$(dirname "$0")";pwd)
    private_key_file=${root_path}/___temp/private-key
    if [ -f "${private_key_file}" ]; then
      chmod 600 ${private_key_file}
    fi
    shift 1
    ansible_cmd="ansible-playbook --extra-vars root_path=${root_path} --inventory-file ${root_path}/ansible_hosts ${root_path}/$1.yml --step --verbose"
    if [ $1 == 'centos' ]; then
      bash -c "${ansible_cmd} --ask-pass"
    elif [ $1 == 'ubuntu' ]; then
      bash -c "${ansible_cmd} --ask-pass"
    else
      bash -c "${ansible_cmd} --private-key ${private_key_file}"
    fi
		;;
		?)
		echo -e "\033[31m$1 un_know input param \033[0m"
		break
		;;
	esac
done
