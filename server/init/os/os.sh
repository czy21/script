#!/bin/bash
set -e

dir=$(cd "$(dirname "$0")"; pwd)

timedatectl set-timezone Asia/Shanghai
os_type=$(awk -F= '/^ID=/{gsub("\"","",$2);print $2}' /etc/os-release)
bash ${dir}/${os_type}.sh