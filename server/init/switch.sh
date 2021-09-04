#!/bin/bash
# bash switch.sh -h user@host -t [target]
# -t os | docker | hosts | k8s-master | k8s-nodes | cp-certs | reboot | prune
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
    script_path=$(cd "$(dirname "$0")";pwd)
    script_name=$(basename ${script_path})
    private_key_file=${script_path}/___temp/private-key
    if [ -f "${private_key_file}" ]; then
      chmod 600 ${private_key_file}
    fi
    shift 1
    ansible_cmd="ansible-playbook \
    --extra-vars \"script_path=${script_path} script_name=${script_name}\" \
    --inventory ${script_path}/ansible_hosts ${script_path}/$1.yml \
    --step \
    --verbose"
    if [ $1 == 'os' ]; then
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
