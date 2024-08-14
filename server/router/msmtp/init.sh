#!/bin/bash

param_command="{{ param_command }}"
etc_app_conf=/etc/msmtprc

if [ "install" = "${param_command}" ];then
  cp -r {{ param_role_output_path }}/conf/msmtprc ${etc_app_conf}
fi

if [ "backup" = "${param_command}" ];then
  cp -r $etc_app_conf {{ param_role_bak_path }}
fi

if [ "restore" = "${param_command}" ];then
  cp -r {{ param_role_bak_path }}/msmtprc ${etc_app_conf}
fi