#!/bin/bash
# upload sh_file and execute it

function upload_exec_py() {
  pwd_path=$(pwd)
  name_path=`basename ${pwd_path}`
  utility_dir=$(cd ${pwd_path}/../../utility; pwd)
  ssh $host 'rm -rf $HOME/'${name_path}';'

  scp -rqC ${pwd_path} $host:
  scp -rqC ${pwd_path}/../requirements.txt ${utility_dir}/share.py $host:${name_path}
  
  ssh $host 'sudo pip3 install -r $HOME/'${name_path}/'requirements.txt && python3 -B $HOME/'${name_path}/'exec.py '$@';'

  ssh $host 'rm -rf $HOME/'${name_path}';'
}

function upload_exec_sh() {
  pwd_path=$(pwd)
  name_path=`basename ${pwd_path}`
  ssh $host 'rm -rf $HOME/'${name_path}';'
  scp -rqC ${pwd_path} $host:
  ssh $host 'sh $HOME/'${name_path}/${sh_file}' '$@';'
  ssh $host 'rm -rf $HOME/'${name_path}';'
}