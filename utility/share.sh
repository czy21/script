#!/bin/bash
# upload sh_file and execute it

function upload_exec_py() {
  pwd_path=$(pwd)
  name_path=`basename ${pwd_path}`
  ssh $host 'rm -rf $HOME/'${name_path}';'
  scp -r ${pwd_path} $host:
  ssh $host 'python3 $HOME/'${name_path}/'exec.py '$@';'

  ssh $host 'rm -rf $HOME/'${name_path}';'
}



function upload_exec_sh() {
  pwd_path=$(pwd)
  name_path=`basename ${pwd_path}`
  ssh $host 'rm -rf $HOME/'${name_path}';'
  scp -r ${pwd_path} $host:
  ssh $host 'bash $HOME/'${name_path}/${sh_file}' '$@';'
}