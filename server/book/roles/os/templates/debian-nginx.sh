#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://nginx.org/keys/nginx_signing.key -o /etc/apt/keyrings/nginx.asc
sudo chmod a+r /etc/apt/keyrings/nginx.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/nginx.asc] http://nginx.org/packages/{{ param_ansible_distribution }} $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list

sudo apt-get -y update
sudo apt-get -y install nginx
sudo systemctl daemon-reload && sudo systemctl restart nginx && sudo systemctl enable nginx