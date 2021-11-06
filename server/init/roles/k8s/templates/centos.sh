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
sudo yum install -y kubelet-{{param_k8s_version}} kubeadm-{{param_k8s_version}} kubectl-{{param_k8s_version}} --disableexcludes=kubernetes
sudo systemctl enable --now kubelet

sudo wget -O - https://get.helm.sh/helm-v3.6.3-linux-amd64.tar.gz | sudo tar -zxf - --strip-components 1 -C /usr/local/bin/ linux-amd64/helm
sudo chmod +x /usr/local/bin/helm
sudo ln -s /usr/local/bin/helm /usr/bin/helm