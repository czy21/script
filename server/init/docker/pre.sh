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