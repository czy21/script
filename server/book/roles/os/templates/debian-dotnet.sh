#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://packages.microsoft.com/keys/microsoft.asc -o /etc/apt/keyrings/microsoft.asc
sudo chmod a+r /etc/apt/keyrings/microsoft.asc

curl -fsSL https://packages.microsoft.com/config/{{ param_ansible_distribution }}/{{ param_ansible_distribution_version }}/prod.list \
  | sed -e 's|\(signed-by=\)[^]]*|\1/etc/apt/keyrings/microsoft.asc|' \
  | sudo tee /etc/apt/sources.list.d/dotnet.list

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/apt/sources.list.d/dotnet.list /etc/apt/sources.list.d/dotnet.list.bak
  sed -e "s|https://\(packages.microsoft.com\)|https://{{ param_mirror_raw }}/\1|g" /etc/apt/sources.list.d/dotnet.list.bak | sudo tee /etc/apt/sources.list.d/dotnet.list
fi

sudo apt-get -y update
sudo apt-get -y install dotnet-sdk-9.0