#!/bin/bash
set -e

if [ "{{ param_docker_add_repo | lower }}" = true ];then
  # Add Docker's official GPG key:
  sudo apt-get update
  sudo apt-get install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/{{ param_ansible_distribution }}/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc

  # Add the repository to Apt sources:
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/{{ param_ansible_distribution }} $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
    [ ! -f "/etc/apt/sources.list.d/docker.list.bak" ] && sudo cp -rv /etc/apt/sources.list.d/docker.list /etc/apt/sources.list.d/docker.list.bak
    sed -e "s|https://download.docker.com|http://{{ param_mirror_raw }}/docker-ce|g" /etc/apt/sources.list.d/docker.list.bak | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  fi

fi

sudo apt-get update
docker_version=`sudo apt-cache madison docker-ce | awk '{ print $3 }' | grep "{{ param_docker_version }}" | head -n 1`
sudo apt-get -y install docker-ce=${docker_version} docker-ce-cli=${docker_version} containerd.io docker-buildx-plugin
sudo systemctl daemon-reload && sudo systemctl restart docker && sudo systemctl enable docker