#!/bin/bash
# upload sh_file and execute it

function upload_exec_py() {
  pwd_path=$(pwd)
  name_path=`basename ${pwd_path}`
  utility_dir=$(cd ${pwd_path}/../../utility; pwd)
  prune_cmd='rm -rf $HOME/'${name_path}';'
  ssh $host ${prune_cmd}

  scp -rqC ${pwd_path} $host:
  scp -rqC ${pwd_path}/../requirements.txt ${pwd_path}/../.env ${utility_dir}/share.py $host:${name_path}

  local args=""
  local exec_cmd=()
  for i in "$@" ; do
    if [ "-i" == $i ]; then
        exec_cmd+=('sudo pip3 install --requirement $HOME/'${name_path}/'requirements.txt;')
        shift 1
        continue
    fi
    args+=" $i"
  done
  exec_cmd+=('python3 -B $HOME/'${name_path}/'exec.py '${args}';')
  exec_cmd+=(${prune_cmd})
  echo -e '\033[32m command: \033[0m'${exec_cmd[@]}
  ssh $host ${exec_cmd[@]}
}

function upload_exec_sh() {
  pwd_path=$(pwd)
  name_path=`basename ${pwd_path}`
  ssh $host 'rm -rf $HOME/'${name_path}';'
  scp -rqC ${pwd_path} $host:
  ssh $host 'sh $HOME/'${name_path}/${sh_file}' '$@';'
  ssh $host 'rm -rf $HOME/'${name_path}';'
}