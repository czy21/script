#!/bin/bash
set -e

# install k8s
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

curl -fsSL https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list > /dev/null

sudo apt-get update
sudo apt-get install -y kubelet={{ param_k8s_patch_version }}-00 kubeadm={{ param_k8s_patch_version }}-00 kubectl={{ param_k8s_patch_version }}-00
sudo apt-mark hold kubelet kubeadm kubectl