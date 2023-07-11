#!/bin/bash
set -e

# docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# override docker repo available mirror:https://mirrors.tuna.tsinghua.edu.cn
sudo sed -i.bak -e "s|https://download.docker.com|http://{{ param_mirror_raw }}/docker-ce|g" /etc/yum.repos.d/docker-ce.repo

sudo yum -y install docker-ce docker-ce-cli containerd.io
sudo systemctl daemon-reload && sudo systemctl restart docker && sudo systemctl enable docker

# docker compose
sudo -u root bash -c "echo \"alias docker-compose1='docker compose'\" > /etc/profile.d/99-docker-compose.sh"