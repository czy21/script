#!/bin/bash

param_command="{{ param_command }}"
etc_app_path="{{ param_etc_app_path }}"
if [ "install" == "${param_command}" ];then
  echo ''
fi

if [ "backup" == "${param_command}" ];then
  find ${etc_app_path}/ -maxdepth 1 ! -path ${etc_app_path}/  -name "smb.conf.template" -o -name "smbpasswd" -exec cp -r {} {{ param_role_bak_path }} \;
fi

if [ "restore" == "${param_command}" ];then
  cp -r {{ param_role_bak_path }}/* ${etc_app_path}
fi