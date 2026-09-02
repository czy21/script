#!/bin/bash
set -e

os_distribution="{{ param_ansible_distribution }}"

[ "rocky" = "${os_distribution}" ] && os_distribution=rhel

sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/${os_distribution}/docker-ce.repo

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/yum.repos.d/docker-ce.repo /etc/yum.repos.d/docker-ce.repo.bak
  sed -e "s|https://download.docker.com|https://{{ param_mirror_docker_ce }}|g" /etc/yum.repos.d/docker-ce.repo.bak | sudo tee /etc/yum.repos.d/docker-ce.repo > /dev/null
fi

sudo yum update -y
sudo yum install -y docker-ce-{{ param_docker_version }} docker-ce-cli-{{ param_docker_version }} containerd.io docker-buildx-plugin docker-compose-plugin
[ -f /usr/libexec/docker/cli-plugins/docker-compose ] && sudo ln -sf /usr/libexec/docker/cli-plugins/docker-compose /usr/bin/docker-compose

sudo systemctl daemon-reload && sudo systemctl restart docker && sudo systemctl enable docker