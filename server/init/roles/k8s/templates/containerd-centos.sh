#!/bin/bash
set -e

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo sed -i.bak -e "s,^baseurl=https://download.docker.com,baseurl=http://{{ param_mirror_apt }}/docker-ce,g" /etc/yum.repos.d/docker-ce.repo

sudo yum -y install containerd.io
sudo systemctl daemon-reload && sudo systemctl restart containerd && systemctl enable containerd

sudo wget -c https://github.com/kubernetes-sigs/cri-tools/releases/download/v{{ param_containerd_version }}/crictl-v{{ param_containerd_version }}-linux-amd64.tar.gz -O - | sudo tar -xz -C /usr/local/bin
sudo chown root:root /usr/local/bin/crictl
sudo chmod +x /usr/local/bin/crictl
sudo ln -s /usr/local/bin/crictl /usr/bin/crictl
sudo echo "
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 10
debug: false
" > /etc/crictl.yaml