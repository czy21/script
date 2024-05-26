#!/bin/bash
set -e

# docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo sed -i.bak -e "s|https://download.docker.com|http://{{ param_mirror_raw }}/docker-ce|g" /etc/yum.repos.d/docker-ce.repo
fi

sudo yum -y install docker-ce-{{ param_docker_version }} docker-ce-cli-{{ param_docker_version }} containerd.io docker-buildx-plugin
sudo systemctl daemon-reload && sudo systemctl restart docker && sudo systemctl enable docker