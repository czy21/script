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

name=$1
host=$2

shift 2

main_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

host_cmd="ssh ${ssh_opt} ${host}"

[ $host = "local" ] && host_cmd="eval"
os_name=$($host_cmd "uname -s")

PYTHON_HOME="\$HOME/.python3"
PYTHON_EXEC="${PYTHON_HOME}/bin/python3"

if [[ "$os_name" =~ "NT" ]];then
  PYTHON_EXEC="${PYTHON_HOME}/Scripts/python3"
fi

src_path=$main_dir/$name
if [ ! -d "$src_path" ];then
  echo "${name} not found"
  exit 1
fi

dst_name=script-$name
tmp_name=___temp
build_name=build
utility_path=$(realpath ${src_path}/../../utility)
del_cmd="rm -rf \$HOME/${dst_name}"
ssh_opt="-o StrictHostKeyChecking=no"

pypi="https://pypi.tuna.tsinghua.edu.cn/simple/"

cmd=$(cat <<EOF
if [ ! -f ${PYTHON_EXEC} ];then
  python3 -m venv ${PYTHON_HOME} --without-pip --system-site-packages && wget -nv -O - https://bootstrap.pypa.io/get-pip.py | ${PYTHON_EXEC} - -i ${pypi}
fi
if [ "${is_requirement}" = "true" ];then
  ${PYTHON_EXEC} -m pip config set global.index-url ${pypi}
  ${PYTHON_EXEC} -m pip install -r \$HOME/${dst_name}/server/requirements.txt
fi
${PYTHON_EXEC} -B \$HOME/${dst_name}/main.py $args
EOF
)

tar_args=
tar_args+="-C $(realpath ${utility_path}/../) ./$(basename ${utility_path}) "
tar_args+="-C $(realpath ${src_path}/../../) `cd ${src_path}/../;find . -maxdepth 1 -type f ! -name "main.sh" -and ! -name "README.md" -exec sh -c 'f={};echo ./server/$(basename $f)' \;` "
tar_args+="-C ${src_path} . "

if [ -d "$main_dir_ext" ];then
  src_path_ext=$main_dir_ext/$name
  tar_args+="-C $(realpath ${src_path_ext}/../../) `cd ${src_path_ext}/../;find . -maxdepth 1 -type f ! -name "main.sh" -and ! -name "README.md" -exec sh -c 'f={};echo ./server/$(basename $f)' \;` "
  [ -d "$src_path_ext" ] && tar_args+="-C ${src_path_ext} . "
fi

tar -zcf - --exclude="__pycache__" --exclude="${build_name}" ${tar_args} | ${host_cmd} "mkdir -p \$HOME/${dst_name};tar -zxf - -C \$HOME/${dst_name}"
${host_cmd} "${cmd}"
${host_cmd} "[ -d \$HOME/${dst_name} ]" && ${host_cmd} "tar -zcf - -C \$HOME/${dst_name} ${tmp_name} ${build_name}" | tar -zxf - -C ${src_path}

if [ ! $is_debug ];then
  ${host_cmd} "${del_cmd}"
fi