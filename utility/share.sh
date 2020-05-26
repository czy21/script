#!/bin/bash
# upload sh_file and execute it

function upload_exec() {

  ssh $host 'rm -rf $HOME/'$rm_path';'

  scp -r $cp_path $host:
  ssh $host 'sh -x $HOME/'$sh_file' '$@';'

  ssh $host 'rm -rf $HOME/'$rm_path';'
}
