#!/bin/bash
set -e

# docker
sudo apt-get update
sudo NEEDRESTART_SUSPEND=1 apt -y install apt-transport-https ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# override docker repo
sudo sed -i.bak -e "s,https://download.docker.com,http://{{ param_mirror_apt }}/docker-ce,g" /etc/apt/sources.list.d/docker.list

sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl enable docker

# docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/{{ param_compose_version }}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose