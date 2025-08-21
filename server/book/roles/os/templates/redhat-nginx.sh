#!/bin/bash
set -e

sudo tee /etc/yum.repos.d/nginx.repo << EOF
[nginx-stable]
name=nginx stable repo
baseurl=https://nginx.org/packages/centos/\$releasever/\$basearch/
enabled=1
gpgcheck=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true

[nginx-mainline]
name=nginx mainline repo
baseurl=https://nginx.org/packages/mainline/centos/\$releasever/\$basearch/
enabled=0
gpgcheck=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
EOF

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/yum.repos.d/nginx.repo /etc/yum.repos.d/nginx.repo.bak
  sed -e "s|https://nginx.org/packages|https://{{ param_mirror_raw }}/nginx|g" /etc/yum.repos.d/nginx.repo.bak | sudo tee /etc/yum.repos.d/nginx.repo
fi

sudo yum -y install nginx-{{ param_app_nginx_version }}
sudo systemctl daemon-reload && sudo systemctl enable nginx && sudo systemctl restart nginx