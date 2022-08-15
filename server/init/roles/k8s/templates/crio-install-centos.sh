#!/bin/bash
set -e

sudo curl -L -o /etc/yum.repos.d/cri-o-{{ param_k8s_version }}.repo \
https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/1.24:/{{ param_k8s_version }}/CentOS_8_Stream/devel:kubic:libcontainers:stable:cri-o:1.24:{{ param_k8s_version }}.repo
sudo sed -i.bak -e "s|https://download.opensuse.org|http://{{ param_mirror_raw }}/opensuse|g" /etc/yum.repos.d/cri-o-{{ param_k8s_version }}.repo
sudo yum -y install cri-o