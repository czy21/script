#!/bin/bash

param_command="{{ param_command }}"
if [ "install" == "${param_command}" ];then
  echo ''
fi

if [ "backup" == "${param_command}" ];then
  find /etc/docker/ -type f -name 'daemon.json' -exec sh -c 'f={}; cp $f {{ param_role_bak_path }}/$(basename $f)' \;
fi

if [ "restore" == "${param_command}" ];then
  find {{ param_role_bak_path }} -type f -name 'daemon.json' -exec sh -c 'f={};mkdir -p /etc/docker/;cp $f /etc/docker/$(basename $f )' \;
fi