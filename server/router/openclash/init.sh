#!/bin/bash

param_command="{{ param_command }}"
etc_app_path="{{ param_app_path }}"
if [ "install" = "${param_command}" ];then
  echo ''
fi

if [ "backup" = "${param_command}" ];then
  find ${etc_app_path}/custom -maxdepth 1 ! -path ${etc_app_path}/custom -name "openclash_custom_rules.list" -exec sh -c 'p={{ param_role_bak_path }}/custom;mkdir -p $p;cp -r {} $p' \;
fi

if [ "restore" = "${param_command}" ];then
  cp -r {{ param_role_bak_path }}/custom/* ${etc_app_path}/custom
fi