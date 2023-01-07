#!/bin/bash

param_command="{{ param_command }}"
acme_etc_path="{{ param_acme_etc_path }}"
if [ "install" == "${param_command}" ];then
  echo ''
fi

if [ "backup" == "${param_command}" ];then
  mkdir -p {{ param_role_temp_path }}/acme-bak/ && cp -r ${acme_etc_path}/* {{ param_role_temp_path }}/acme-bak/
fi

if [ "restore" == "${param_command}" ];then
  echo ''
fi