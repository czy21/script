#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# k8s
curl -fsSL https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/deb/Release.key | sudo gpg -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list > /dev/null

# cri-o
curl -fsSL https://pkgs.k8s.io/addons:/cri-o:/stable:/v{{ param_k8s_minor_version }}/deb/Release.key | sudo gpg -o /etc/apt/keyrings/cri-o-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/cri-o-apt-keyring.gpg] https://pkgs.k8s.io/addons:/cri-o:/stable:/v{{ param_k8s_minor_version }}/deb/ /" | sudo tee /etc/apt/sources.list.d/cri-o.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y cri-o cri-tools kubelet={{ param_k8s_patch_version }}-1.1 kubeadm={{ param_k8s_patch_version }}-1.1 kubectl={{ param_k8s_patch_version }}-1.1
sudo systemctl enable crio kubelet --now