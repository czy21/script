#!/bin/bash
set -e

sudo cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF
sudo yum install -y kubelet-{{ param_k8s_patch_version }} kubeadm-{{ param_k8s_patch_version }} kubectl-{{ param_k8s_patch_version }} --disableexcludes=kubernetes
sudo systemctl enable kubelet --now