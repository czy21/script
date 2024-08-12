#!/bin/bash

param_command="{{ param_command }}"
etc_app_path="{{ param_app_path }}"
if [ "install" = "${param_command}" ];then
  mkdir -p ${etc_app_path} && cp -r {{ param_role_output_path }}/conf/* ${etc_app_path}
  chmod +x ${etc_app_path}/*.sh
fi

if [ "backup" = "${param_command}" ];then
  find ${etc_app_path} -maxdepth 1 ! -path ${etc_app_path} -exec sh -c 'p={{ param_role_bak_path }};mkdir -p $p;cp -r {} $p' \;
fi

if [ "restore" = "${param_command}" ];then
  mkdir -p ${etc_app_path} && cp -r {{ param_role_bak_path }}/* ${etc_app_path}
  chmod +x ${etc_app_path}/*.sh
fi