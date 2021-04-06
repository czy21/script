#!/bin/bash
# upload sh_file and execute it

function upload_exec() {
  pwd_path=$(pwd)
  name_path=`basename ${pwd_path}`
  ssh $host 'rm -rf $HOME/'${name_path}';'&&

  scp -r ${pwd_path} $host:
  ssh $host 'python3 $HOME/'${name_path}/'exec.py '$@';'

  ssh $host 'rm -rf $HOME/'${name_path}';'
}
