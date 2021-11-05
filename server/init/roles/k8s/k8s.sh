#!/bin/bash
set -e

dir=$(cd "$(dirname "$0")"; pwd)

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

os_type=$(awk -F= '/^ID=/{gsub("\"","",$2);print $2}' /etc/os-release)
echo $os_type
if [ ${os_type} == 'centos' ]; then
    bash ${dir}/k8s-centos.sh
elif [ ${os_type} == 'ubuntu' ]; then
    bash ${dir}/k8s-ubuntu.sh
fi