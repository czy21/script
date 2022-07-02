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
  local is_debug=false
  local PYTHON_HOME="\$HOME/.python3-opsor"
  local PYTHON_EXEC="${PYTHON_HOME}/bin/python3"
  exec_cmd+="if [ ! -d ${PYTHON_HOME} ];then python3 -m venv ${PYTHON_HOME};fi && "
  for ((i=1;i<="$#";i++));do
    item=${!i}
    if [ "-r" == ${item} ]; then
        exec_cmd+="${PYTHON_EXEC} -m pip install -I -r \$HOME/${book_target}/requirements.txt && "
        shift 1
        continue
    fi
    if [ "--debug" == ${item} ]; then
      is_debug=true
    fi
    args+=" ${item}"
  done
  exec_cmd+="${PYTHON_EXEC} -B \$HOME/${book_target}/main.py ${args}"
  ${ssh_cmd} ${exec_cmd}
  if ${ssh_cmd} "[ -d ${book_target_temp_path} ]"; then
    ${scp_cmd} $host:${book_target_temp_path}/ ${book_source}/
  fi
  if [ ${is_debug} = false ]; then
    ${ssh_cmd} ${del_cmd}
  fi
}