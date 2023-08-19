#!/bin/bash

# -h user@host    upload to remote and execute
# -r              install requirement.txt

shopt -s expand_aliases

if [ -n "$(type -p gtar)" ];then
  alias tar='gtar'
fi

unset -v host
unset -v requirement
unset -v args

while [ $# -gt 0 ];do
  case "$1" in
    -h)
      host=$2
      shift
      ;;
    -r)
      requirement=true
      ;;
     *)
      args+=" $1"
      ;;
  esac
  shift
done

PYTHON_HOME="\$HOME/.python3"
PYTHON_EXEC="${PYTHON_HOME}/bin/python3"
src_path=$(pwd)
dst_name=$(basename ${src_path})
tmp_name=___temp
build_name=build
utility_path=$(realpath ${src_path}/../../utility)
del_cmd="rm -rf \$HOME/${dst_name}"
ssh_opt="-o StrictHostKeyChecking=no"
ssh_cmd="ssh ${ssh_opt} ${host}"
src_path_parent_path=$(realpath ${src_path}/../)
src_path_parent_files=$(cd ${src_path_parent_path};find . -maxdepth 1 -name "env*.yaml" -o -name "requirements.txt")

tar -cf - --exclude="__pycache__" --exclude="${build_name}" \
-C ${src_path} . \
-C $(realpath ${utility_path}/../) ./$(basename ${utility_path}) \
-C $(realpath ${src_path}/../../) ./server/share.py \
-C ${src_path_parent_path} ${src_path_parent_files} \
 | ${ssh_cmd} "mkdir -p ${dst_name};tar -xf - -C ${dst_name}"

cmd=""
pypi="-i https://pypi.tuna.tsinghua.edu.cn/simple/"
cmd+="if [ ! -f ${PYTHON_EXEC} ];then "
cmd+="python3 -m venv ${PYTHON_HOME} --without-pip --system-site-packages && wget -nv -O - https://bootstrap.pypa.io/get-pip.py | ${PYTHON_EXEC} - ${pypi}"
cmd+=";fi &&"
if [ $requirement ];then
  cmd+="${PYTHON_EXEC} -m pip install ${pypi} -r \$HOME/${dst_name}/requirements.txt && "
fi
cmd+="${PYTHON_EXEC} -B \$HOME/${dst_name}/main.py $@"
${ssh_cmd} ${cmd}
${ssh_cmd} "[ -d ${dst_name} ]" && ${ssh_cmd} "tar -zcf - -C ${dst_name} ${tmp_name} ${build_name}" | tar -zxf - -C ${src_path}
${ssh_cmd} ${del_cmd}
