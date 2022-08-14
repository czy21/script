#!/bin/bash
set -e

sudo curl -L -o /etc/yum.repos.d/cri-o-{{ param_k8s_version }}.repo \
https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/1.24:/{{ param_k8s_version }}/CentOS_8_Stream/devel:kubic:libcontainers:stable:cri-o:1.24:{{ param_k8s_version }}.repo
sudo yum -y install cri-o
sudo sed -i.bak -e 's|registry.k8s.io|{{ param_registry_proxy_url }}|g' -e 's|^# \(pause_image = \)|\1|g' /etc/crio/crio.conf
sudo systemctl daemon-reload && sudo systemctl restart crio && systemctl enable crio