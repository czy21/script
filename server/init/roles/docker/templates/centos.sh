#!/bin/bash
set -e

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo sed -i.bak -e "s,^baseurl=https://download.docker.com/linux,baseurl=http://{{ param_mirror_yum }},g" /etc/yum.repos.d/docker-ce.repo
sudo yum -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl enable docker