#!/bin/bash

param_command="{{ param_command }}"
script_path=$HOME/script

mkdir -p ${script_path}
if [ "install" = "${param_command}" ];then
  cp -rv {{ param_role_output_path }}/conf/* ${script_path}
  find ${script_path} -name "*.sh" -exec chmod +x {} \;
fi