#!/bin/bash
set -e

cat {{ param_remote_role_path }}/k8s.repo | sudo tee /etc/yum.repos.d/kubernetes.repo
cat <<EOF | sudo tee /etc/yum.repos.d/cri-o.repo
[cri-o]
name=CRI-O
baseurl=https://pkgs.k8s.io/addons:/cri-o:/stable:/v{{ param_k8s_minor_version }}/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/addons:/cri-o:/stable:/v{{ param_k8s_minor_version }}/rpm/repodata/repomd.xml.key
EOF

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/yum.repos.d/kubernetes.repo /etc/yum.repos.d/kubernetes.repo.bak
  sed -e "s|https://pkgs.k8s.io|http://{{ param_mirror_k8s }}|g" /etc/yum.repos.d/kubernetes.repo.bak | sudo tee /etc/yum.repos.d/kubernetes.repo > /dev/null
  sudo cp -rv /etc/yum.repos.d/cri-o.repo /etc/yum.repos.d/cri-o.repo.bak
  sed -e "s|https://pkgs.k8s.io|http://{{ param_mirror_k8s }}|g" /etc/yum.repos.d/cri-o.repo.bak | sudo tee /etc/yum.repos.d/cri-o.repo > /dev/null
fi

sudo yum install -y cri-o cri-tools kubelet-{{ param_k8s_patch_version }} kubeadm-{{ param_k8s_patch_version }} kubectl-{{ param_k8s_patch_version }}
sudo systemctl enable crio kubelet --now