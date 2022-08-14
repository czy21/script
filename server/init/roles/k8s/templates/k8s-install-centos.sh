#!/bin/bash
set -e

sudo cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF
sudo sed -i \
-e "s|https://packages.cloud.google.com|http://{{ param_mirror_raw }}/kubernetes|g" \
-e "s|^gpgcheck=1|gpgcheck=0|g" \
-e "s|^repo_gpgcheck=1|repo_gpgcheck=0|g" /etc/yum.repos.d/kubernetes.repo
sudo yum install -y kubelet-{{ param_k8s_version }} kubeadm-{{ param_k8s_version }} kubectl-{{ param_k8s_version }} --disableexcludes=kubernetes
sudo systemctl enable --now kubelet