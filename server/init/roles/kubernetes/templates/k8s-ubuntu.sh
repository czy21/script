#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

curl -fsSL https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list > /dev/null

PROJECT_PATH=prerelease:/main
curl -fsSL https://pkgs.k8s.io/addons:/cri-o:/$PROJECT_PATH/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/cri-o-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/cri-o-apt-keyring.gpg] https://pkgs.k8s.io/addons:/cri-o:/$PROJECT_PATH/deb/ /" | sudo tee /etc/apt/sources.list.d/cri-o.list

sudo apt-get update
sudo apt-get install -y cri-o kubelet={{ param_k8s_patch_version }}-00 kubeadm={{ param_k8s_patch_version }}-00 kubectl={{ param_k8s_patch_version }}-00
sudo systemctl enable crio kubelet --now