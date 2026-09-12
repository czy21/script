#!/bin/bash

# bash main.sh [name] [host] [command]
# -r           install requirements.txt

shopt -s expand_aliases

if [ -n "$(type -p gtar)" ];then
  alias tar='gtar'
fi

name=$1
host=$2
shift 2

main_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
util_dir=$(realpath ${main_dir}/../util)

setup=false
clean=false
debug=false
args=
while [ $# -gt 0 ];do
  case "$1" in
    -r)
      setup=true
      ;;
    --debug)
      debug=true
      ;;
    --clean)
      clean=true
      ;;
     *)
      args+="$1 "
      ;;
  esac
  shift
done

if [ "$debug" = true ];then
  args+="--debug "
  set -x
fi

src_path="$main_dir/$name"
src_plus="$([ -d "$plus_dir" ] && echo "$plus_dir/$name")"
src_plus_conf="$([[ -d "$plus_dir" && -d "$plus_dir/config" ]] && echo "$plus_dir/config")"

if [ ! -d "$src_path" ];then
  echo "${name} not found"
  exit 1
fi

if [ "$clean" = true ];then
  args+="--clean "
  find $src_path $([ -d "$src_plus" ] && echo $src_plus) \( -type d \( -name build \) -o -type f -name *.log \) -prune -exec sh -c 'rm -rf -- "$1" && [ "$2" = true ] && echo "removed $1"' _ {} "$debug" \;
  find $src_path $([ -d "$src_plus" ] && echo $src_plus) -depth -type d -empty -delete
fi

dst_path="\$HOME/script-${name}"
dst_exec=$([ $host = "local" ] && echo "eval" || echo "ssh -o StrictHostKeyChecking=no ${host}")

os_name=$($dst_exec "uname -s")

PYTHON_HOME="\$HOME/.python3"
PYTHON_EXEC="${PYTHON_HOME}/bin/python3"
[[ "$os_name" =~ "NT" ]] && PYTHON_EXEC="${PYTHON_HOME}/Scripts/python3"

pypi="https://pypi.tuna.tsinghua.edu.cn/simple/"

run_cmd=$(cat <<EOF
[ -f ${PYTHON_EXEC} ] || (python3 -m venv ${PYTHON_HOME} --without-pip --system-site-packages && wget -nv -O - https://bootstrap.pypa.io/get-pip.py | ${PYTHON_EXEC} - -i ${pypi})
[ "${setup}" = true ] && ${PYTHON_EXEC} -m pip config set global.index-url ${pypi} && ${PYTHON_EXEC} -m pip install -r ${dst_path}/server/requirements.txt

${PYTHON_EXEC} -B ${dst_path}/main.py $args
EOF
)

tar_args=
tar_args+="--exclude=build "
tar_args+="--exclude=*.log "
tar_args+="--exclude=__pycache__ "
tar_args+="--exclude=.DS_Store "

echo $args | grep -q 'target doc' || tar_args+="--exclude=*.md "

tar_args+="-C $(realpath ${util_dir}/../) ./$(basename ${util_dir}) "
tar_args+="-C $(realpath ${main_dir}/../) $(cd ${main_dir};find . -maxdepth 1 -type f \( ! -name "main.sh" -and ! -name "README.md" \) -exec sh -c 'f={};echo ./server/$(basename $f)' \;) "
tar_args+="-C ${src_path} . "

[ -d "$src_plus" ] && tar_args+="-C ${src_plus} . "
[ -d "$src_plus_conf" ] && tar_args+="-C $(realpath ${src_plus_conf}/../../) ./server/config "

tar -zcf - ${tar_args} | ${dst_exec} "mkdir -p ${dst_path};tar -zxf - -C ${dst_path}"

${dst_exec} "${run_cmd}"

${dst_exec} "[ -d ${dst_path} ]" && ${dst_exec} "cd ${dst_path} && find . \( -type d \( -name build \) -o -type f -name *.log \) | tar -zcf - -T -" | tar -zxf - -C $([ -d "$src_plus" ] && echo ${src_plus} || echo ${src_path})
[ "$debug" = true ] || ${dst_exec} "rm -rf ${dst_path}"

exit 0