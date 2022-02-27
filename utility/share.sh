#!/bin/bash
# upload sh_file and execute it
# -r install requirement.txt
function upload_exec_py() {
  local pwd_path=$(pwd)
  local name_path=`basename ${pwd_path}`
  local utility_dir=$(cd ${pwd_path}/../../utility; pwd)
  local prune_cmd='rm -rf $HOME/'${name_path}';'
  ssh $host ${prune_cmd}

  scp -rqC ${pwd_path} $host:
  scp -rqC ${pwd_path}/../requirements.txt ${pwd_path}/../.env ${utility_dir}/share.py $host:${name_path}

  local args
  local exec_cmd
  for i in "$@" ; do
    if [ "-r" == ${i} ]; then
        exec_cmd+='sudo pip3 install --requirement $HOME/'${name_path}/'requirements.txt --ignore-installed;'
        shift 1
        continue
    fi
    args+=" ${i}"
  done
  exec_cmd+='python3 -B $HOME/'${name_path}/'exec.py '${args}';'
  exec_cmd+=${prune_cmd}
  echo -e '\033[32mcommand: \033[0m'${exec_cmd}
  ssh $host ${exec_cmd}
}