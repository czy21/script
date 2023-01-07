#!/bin/bash

param_command="{{ param_command }}"
if [ "install" == "${param_command}" ];then
  echo ''
fi

if [ "backup" == "${param_command}" ];then
  find /etc/ -type f -name 'adguardhome.yaml' -exec sh -c 'f={}; cp $f {{ param_role_temp_path }}/$(basename $f).bak' \;
fi

if [ "restore" == "${param_command}" ];then
  find {{ param_role_temp_path }} -type f -name 'adguardhome.yaml.bak' -exec sh -c 'f={}; cp $f /etc/$(basename $f .bak)' \;
fi