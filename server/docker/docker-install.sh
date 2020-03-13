#!/bin/bash

set -e

sudo mkdir -p /etc/docker
sudo mkdir -p /data/config/ /data/volumes/
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://idyylogn.mirror.aliyuncs.com"]
}
EOF
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo yum makecache timer
sudo yum -y install docker-ce --nobest
sudo systemctl daemon-reload
sudo systemctl restart docker

 # docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# docker machine
sudo curl -L "https://github.com/docker/machine/releases/download/v0.16.0/docker-machine-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-machine
sudo chmod +x /usr/local/bin/docker-machine
sudo ln -sf /usr/local/bin/docker-machine /usr/bin/docker-machine