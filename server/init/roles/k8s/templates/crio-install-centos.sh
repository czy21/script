#!/bin/bash
set -e

sudo curl -L -o /etc/yum.repos.d/cri-o-{{ param_k8s_version }}.repo \
https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/1.24:/{{ param_k8s_version }}/CentOS_8_Stream/devel:kubic:libcontainers:stable:cri-o:1.24:{{ param_k8s_version }}.repo
sudo sed -i \
-e "s|^baseurl=https://download.opensuse.org|baseurl=http://{{ param_mirror_raw }}/opensuse|g" \
-e "s|^gpgkey=https://download.opensuse.org|gpgkey=http://{{ param_mirror_raw }}/opensuse|g" /etc/yum.repos.d/cri-o-{{ param_k8s_version }}.repo
sudo yum -y install cri-o