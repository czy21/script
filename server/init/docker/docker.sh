#!/bin/bash
set -e

dir=$(cd "$(dirname "$0")"; pwd)

sudo mkdir -p /volume1/
sudo mkdir -p /etc/docker/
sudo mkdir -p /etc/systemd/system/docker.service.d/
sudo tee /etc/systemd/system/docker.service.d/docker.conf <<-'EOF'
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd
EOF

os_type=$(awk -F= '/^ID=/{gsub("\"","",$2);print $2}' /etc/os-release)
if [ ${os_type} == 'centos' ]; then
    bash ${dir}/docker-centos.sh
elif [ ${os_type} == 'ubuntu' ]; then
    bash ${dir}/docker-ubuntu.sh
fi