#!/bin/bash
# upload sh_file and execute it

function upload_exec() {
  if [[ ! $2 ]] || [[ "$2" =~ ^"-".* ]]; then
    echo -e "\033[31m$1 value is null \033[0m"
    shift 1
    continue
  fi

  host=$2
  shift 2

  ssh $host 'rm -rf $HOME/'$rm_path';'

  scp -r $cp_path $host:
  ssh $host 'sh -x $HOME/'$sh_file' '$@';'

  ssh $host 'rm -rf $HOME/'$rm_path';'
}
