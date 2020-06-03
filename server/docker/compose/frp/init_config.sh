#!/bin/bash

set -e

sudo mkdir -p /data/config/frp/conf/


sudo tee /data/config/frp/conf/frps.ini <<-'EOF'
[common]
bind_port = 7000
vhost_http_port = 6080
vhost_https_port = 6443
subdomain_host = czy-home.cn

token = cb5e0942-62b2-4578-a32f-3fd17444db26

dashboard_port = 7500
dashboard_user = admin
dashboard_pwd = czy.1106
EOF