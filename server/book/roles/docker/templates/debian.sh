#!/bin/bash
set -e

os_distribution="{{ param_ansible_distribution }}"
os_codename=$(lsb_release -cs)

if [ "kali" = "${os_distribution}" ]; then
  os_distribution=debian
  os_codename=trixie
fi

if [ "{{ param_docker_add_repo | lower }}" = true ];then
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/${os_distribution}/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc

  sudo rm -rf /etc/apt/sources.list.d/docker.list*

  sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/${os_distribution}
Suites: ${os_codename}
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

  if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
    sudo cp -rv /etc/apt/sources.list.d/docker.sources /etc/apt/sources.list.d/docker.sources.bak
    sed -e "s|https://download.docker.com|https://{{ param_mirror_docker_ce }}|g" /etc/apt/sources.list.d/docker.sources.bak | sudo tee /etc/apt/sources.list.d/docker.sources
  fi
fi

sudo apt-get update -y
docker_version=`sudo apt-cache madison docker-ce | awk '{ print $3 }' | grep "{{ param_docker_version }}" | head -n 1`
sudo apt-get install -y docker-ce=${docker_version} docker-ce-cli=${docker_version} containerd.io docker-buildx-plugin
sudo systemctl daemon-reload && sudo systemctl restart docker && sudo systemctl enable docker