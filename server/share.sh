#!/bin/bash

# upload sh_file and execute it
# -r install requirement.txt

function upload_exec_py() {
  local book_source=$(pwd)
  local book_target=$(basename ${book_source})
  local book_target_temp_path=${book_target}/___temp
  local utility=$(cd ${book_source}/../../utility; pwd)
  local del_cmd="rm -rf \$HOME/${book_target}"
  local ssh_opt="-o StrictHostKeyChecking=no"
  local ssh_cmd="ssh ${ssh_opt} ${host}"
  local scp_cmd="scp ${ssh_opt} -rqC"

  ${scp_cmd} ${book_source} $host:
  ${scp_cmd} ${book_source}/../requirements.txt ${book_source}/../env.yaml ${book_source}/../share.py ${utility} $host:${book_target}

  local args
  local exec_cmd=()
  for ((i=1;i<="$#";i++));do
    item=${!i}
    if [ "-r" == ${item} ]; then
        pip_cmd="python3 -m pip install -I -r \$HOME/${book_target}/requirements.txt"
        exec_cmd+="type sudo && sudo ${pip_cmd} || ${pip_cmd} && "
        shift 1
        continue
    fi
    args+=" ${item}"
  done
  exec_cmd+="python3 -B \$HOME/${book_target}/main.py ${args}"
  ${ssh_cmd} ${exec_cmd}
  if ${ssh_cmd} "[ -d ${book_target_temp_path} ]"; then
    ${scp_cmd} $host:${book_target_temp_path}/ ${book_source}/
  fi
#  ${ssh_cmd} ${del_cmd}
}