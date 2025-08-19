#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://packages.microsoft.com/keys/microsoft.asc -o /etc/apt/keyrings/microsoft.asc
sudo chmod a+r /etc/apt/keyrings/microsoft.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/microsoft.asc] https://packages.microsoft.com/{{ param_ansible_distribution }}/{{ param_ansible_distribution_version }}/prod $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/dotnet.list

sudo apt-get -y update
sudo apt-get -y install dotnet-sdk-9.0