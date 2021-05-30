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
"data-root": "/volume1/docker-root",
"hosts": ["fd://","tcp://0.0.0.0:2375"]
}
EOF

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum -y install docker-ce docker-ce-cli containerd.io
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl enable docker
sudo docker network create local_default

# docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# docker machine
sudo curl -L "https://github.com/docker/machine/releases/download/v0.16.0/docker-machine-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-machine
sudo chmod +x /usr/local/bin/docker-machine
sudo ln -sf /usr/local/bin/docker-machine /usr/bin/docker-machine