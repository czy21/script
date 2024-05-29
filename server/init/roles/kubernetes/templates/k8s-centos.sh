#!/bin/bash
set -e

cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v{{ param_k8s_minor_version }}/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl kubernetes-cni
EOF

PROJECT_PATH=prerelease:/main
cat <<EOF | sudo tee /etc/yum.repos.d/cri-o.repo
[cri-o]
name=CRI-O
baseurl=https://pkgs.k8s.io/addons:/cri-o:/$PROJECT_PATH/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/addons:/cri-o:/$PROJECT_PATH/rpm/repodata/repomd.xml.key
EOF

sudo yum install -y cri-o cri-tools kubelet-{{ param_k8s_patch_version }} kubeadm-{{ param_k8s_patch_version }} kubectl-{{ param_k8s_patch_version }} --disableexcludes=kubernetes
sudo systemctl enable crio kubelet --now