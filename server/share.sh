#!/bin/bash

# -r              install requirements.txt

shopt -s expand_aliases

if [ -n "$(type -p gtar)" ];then
  alias tar='gtar'
fi

unset -v host
unset -v args
unset -v is_requirement
unset -v is_debug

host=$1
shift

while [ $# -gt 0 ];do
  case "$1" in
    -r)
      is_requirement=true
      ;;
    --debug)
      is_debug=true
      ;;
     *)
      args+=" $1"
      ;;
  esac
  shift
done

if [ $is_debug ];then
  args+=" --debug"
  set -x
fi

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
src_path_server_files=$(cd ${src_path_parent_path};find . -maxdepth 1 -type f -not -name "share.sh" -not -name "README.md" -exec sh -c 'f={};echo ./server/$(basename $f)' \;)

cmd=""
pypi="-i https://pypi.tuna.tsinghua.edu.cn/simple/"
cmd+="if [ ! -f ${PYTHON_EXEC} ];then "
cmd+="python3 -m venv ${PYTHON_HOME} --without-pip --system-site-packages && wget -nv -O - https://bootstrap.pypa.io/get-pip.py | ${PYTHON_EXEC} - ${pypi}"
cmd+=";fi &&"
if [ ${is_requirement} ];then
  cmd+="${PYTHON_EXEC} -m pip install ${pypi} -r \$HOME/${dst_name}/server/requirements.txt && "
fi
cmd+="${PYTHON_EXEC} -B \$HOME/${dst_name}/main.py $args"

[ $host == "local" ] && ssh_cmd="sh -c"

tar -zcf - --exclude="__pycache__" --exclude="${build_name}" \
-C ${src_path} . \
-C $(realpath ${utility_path}/../) ./$(basename ${utility_path}) \
-C $(realpath ${src_path}/../../) ${src_path_server_files} \
| ${ssh_cmd} "mkdir -p \$HOME/${dst_name};tar -zxf - -C \$HOME/${dst_name}"
${ssh_cmd} "${cmd}"
${ssh_cmd} "[ -d $HOME/${dst_name} ]" && ${ssh_cmd} "tar -zcf - -C \$HOME/${dst_name} ${tmp_name} ${build_name}" | tar -zxf - -C ${src_path}
${ssh_cmd} "${del_cmd}"