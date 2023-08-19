#!/bin/bash

# upload sh_file and execute it
# -r install requirement.txt

shopt -s expand_aliases

if [ -n "$(type -p gtar)" ];then
  alias tar='gtar'
fi

function upload_exec_py() {
  local PYTHON_HOME="\$HOME/.python3"
  local PYTHON_EXEC="${PYTHON_HOME}/bin/python3"
  local src_path=$(pwd)
  local dst_name=$(basename ${src_path})
  local tmp_name=___temp
  local build_name=build
  local utility_path=$(realpath ${src_path}/../../utility)
  local del_cmd="rm -rf \$HOME/${dst_name}"
  local ssh_opt="-o StrictHostKeyChecking=no"
  local ssh_cmd="ssh ${ssh_opt} ${host}"
  local src_path_parent_path=$(realpath ${src_path}/../)
  local src_path_parent_files=$(cd ${src_path_parent_path};find . -maxdepth 1 -name "env*.yaml" -o -name "requirements.txt")

  tar -cf - --exclude="__pycache__" --exclude="${build_name}" \
  -C ${src_path} . \
  -C $(realpath ${utility_path}/../) ./$(basename ${utility_path}) \
  -C $(realpath ${src_path}/../../) ./server/share.py \
  -C ${src_path_parent_path} ${src_path_parent_files} \
   | ${ssh_cmd} "mkdir -p ${dst_name};tar -xf - -C ${dst_name}"

  local args=""
  local cmd=""
  pypi="-i https://pypi.tuna.tsinghua.edu.cn/simple/"
  cmd+="if [ ! -f ${PYTHON_EXEC} ];then "
  cmd+="python3 -m venv ${PYTHON_HOME} --without-pip --system-site-packages && wget -nv -O - https://bootstrap.pypa.io/get-pip.py | ${PYTHON_EXEC} - ${pypi}"
  cmd+=";fi &&"
  for ((i=1;i<="$#";i++));do
    item=${!i}
    if [ "-r" == ${item} ]; then
        cmd+="${PYTHON_EXEC} -m pip install ${pypi} -r \$HOME/${dst_name}/requirements.txt && "
        shift 1
        continue
    fi
    args+=" ${item}"
  done
  cmd+="${PYTHON_EXEC} -B \$HOME/${dst_name}/main.py ${args}"
  ${ssh_cmd} ${cmd}
  ${ssh_cmd} "[ -d ${dst_name} ]" && ${ssh_cmd} "tar -zcf - -C ${dst_name} ${tmp_name} ${build_name}" | tar -zxf - -C ${src_path}
  ${ssh_cmd} ${del_cmd}
}