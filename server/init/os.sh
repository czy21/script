#!/bin/bash
set -e

dir=$(cd "$(dirname "$0")"; pwd)

timedatectl set-timezone Asia/Shanghai

os_type=$(awk -F= '/^ID=/{gsub("\"","",$2);print $2}' /etc/os-release)
echo $os_type
if [ ${os_type} == 'centos' ]; then
    bash ${dir}/os-centos.sh
elif [ ${os_type} == 'ubuntu' ]; then
    bash ${dir}/os-ubuntu.sh
fi