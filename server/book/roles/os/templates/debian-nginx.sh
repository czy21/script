#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://nginx.org/keys/nginx_signing.key -o /etc/apt/keyrings/nginx.asc
sudo chmod a+r /etc/apt/keyrings/nginx.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/nginx.asc] https://nginx.org/packages/{{ param_ansible_distribution }} $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/apt/sources.list.d/nginx.list /etc/apt/sources.list.d/nginx.list.bak
  sed -e "s|https://nginx.org/packages|https://{{ param_mirror_raw }}/nginx|g" /etc/apt/sources.list.d/nginx.list.bak | sudo tee /etc/apt/sources.list.d/nginx.list
fi

sudo apt-get -y update
nginx_version=`sudo apt-cache madison nginx | awk '{ print $3 }' | grep "{{ param_app_nginx_version }}" | head -n 1`
sudo apt-get -y install nginx=${nginx_version}
sudo systemctl daemon-reload && sudo systemctl enable nginx && sudo systemctl restart nginx