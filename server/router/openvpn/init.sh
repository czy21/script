#!/bin/bash

param_command="{{ param_command }}"
openvpn_etc_path="{{ param_openvpn_etc_path }}"
if [ "install" == "${param_command}" ];then
  echo ''
fi

if [ "backup" == "${param_command}" ];then
  find ${openvpn_etc_path} -regex '.*\.\(auth\|ovpn\)' -exec sh -c 'f={}; cp $f {{ param_role_temp_path }}/$(basename $f).bak' \;
fi

if [ "restore" == "${param_command}" ];then
  find ${param_role_temp_path} -regex '.*\.\(auth\|ovpn\).bak' -exec sh -c 'f={}; cp $f {{ openvpn_etc_path }}/$(basename $f .bak)' \;
fi