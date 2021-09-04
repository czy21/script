#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

#sudo wget -O - https://get.helm.sh/helm-v3.6.0-linux-amd64.tar.gz | sudo tar -zxf - --strip-components 1 -C /usr/local/bin/ linux-amd64/helm
#sudo chmod +x /usr/local/bin/helm
#sudo ln -s /usr/local/bin/helm /usr/bin/helm