#!/bin/bash
set -e

# install k8s
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet={{ param_k8s_version }}-00 kubeadm={{ param_k8s_version }}-00 kubectl={{ param_k8s_version }}-00 keepalived haproxy
sudo apt-mark hold kubelet kubeadm kubectl keepalived haproxy