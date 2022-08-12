#!/bin/bash
set -e

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo sed -i.bak -e "s,^baseurl=https://download.docker.com,baseurl=http://{{ param_mirror_apt }}/docker-ce,g" /etc/yum.repos.d/docker-ce.repo

sudo yum -y install containerd.io
sudo systemctl daemon-reload && sudo systemctl restart containerd && systemctl enable containerd

sudo echo "
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 10
debug: false
" > /etc/crictl.yaml