#!/bin/bash
set -e

sudo mkdir -p /etc/docker
sudo mkdir -p /etc/systemd/system/docker.service.d/
sudo tee /etc/systemd/system/docker.service.d/docker.conf <<-'EOF'
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd
EOF
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "hosts": ["fd://","tcp://0.0.0.0:2375"],
  "data-root": "/volume1/docker-root",
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum -y install docker-ce docker-ce-cli containerd.io
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl enable docker

# docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# kompose
sudo curl -L "https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-linux-amd64" -o /usr/local/bin/kompose
sudo chmod +x /usr/local/bin/kompose
sudo ln -s /usr/local/bin/kompose /usr/bin/kompose