#!/bin/bash

# upload sh_file and execute it
# -r install requirement.txt

function upload_exec_py() {
  local pwd_path=$(pwd)
  local name_path=`basename ${pwd_path}`
  local temp_path=${name_path}/___temp/
  local utility_dir=$(cd ${pwd_path}/../../utility; pwd)
  local prune_cmd='rm -rf $HOME/'${name_path}';'
  local ssh_cmd="ssh -o StrictHostKeyChecking=no ${host}"
  local scp_cmd="scp -o StrictHostKeyChecking=no -rqC"

  ${scp_cmd} ${pwd_path} $host:
  ${scp_cmd} ${pwd_path}/../requirements.txt ${pwd_path}/../env.yaml ${utility_dir}/share.py $host:${name_path}

  local args
  local exec_cmd=()
  for ((i=1;i<="$#";i++));do
    item=${!i}
    if [ "-r" == ${item} ]; then
        pip_cmd='pip3 install -I -r $HOME/'${name_path}/'requirements.txt'
        exec_cmd+='type sudo && sudo '${pip_cmd}' || '${pip_cmd}' && '
        shift 1
        continue
    fi
    args+=" ${item}"
  done
  exec_cmd+='python3 -B $HOME/'${name_path}/'exec.py '${args}''
  echo -e '\033[32mcommand: \033[0m'${exec_cmd}
  ${ssh_cmd} ${exec_cmd}
  if ${ssh_cmd} "[ -d ${temp_path} ]"; then
    ${scp_cmd} $host:${temp_path}/ ${pwd_path}/
  fi
  ${ssh_cmd} ${prune_cmd}
}