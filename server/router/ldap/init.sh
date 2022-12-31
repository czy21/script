#!/bin/bash

param_command="{{ param_command }}"

if [ "install" == "${param_command}" ];then
  echo "这是安装哦"
fi

if [ "backup" == "${param_command}" ];then
  echo "这是备份哦"
fi