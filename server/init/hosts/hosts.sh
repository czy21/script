#!/bin/bash
set -e

dir=$(cd "$(dirname "$0")"; pwd)

os_type=$(awk -F= '/^ID=/{gsub("\"","",$2);print $2}' /etc/os-release)

cat ${dir}/${os_type} > /etc/hosts

echo "
192.168.2.21 k8s-node-11
192.168.2.22 k8s-node-12
" >>/etc/hosts
nmcli d reapply ens192