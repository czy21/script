#!/bin/bash

param_command="{{ param_command }}"
if [ "install" == "${param_command}" ];then
  echo ''
fi

if [ "backup" == "${param_command}" ];then
  find /etc/docker/ -type f -name 'daemon.json' -exec sh -c 'f={}; cp $f {{ param_role_temp_path }}/$(basename $f).bak' \;
fi

if [ "restore" == "${param_command}" ];then
  find {{ param_role_temp_path }} -type f -name 'daemon.json.bak' -exec sh -c 'f={}; cp $f /etc/docker/$(basename $f .bak)' \;
fi