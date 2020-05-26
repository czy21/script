#!/bin/bash

set -e

sudo mkdir -p /data/config/frp/conf/


sudo tee /data/config/frp/conf/frps.ini <<-'EOF'
[common]
bind_addr = 0.0.0.0
bind_port = 7000
kcp_bind_port = 7000
vhost_http_port = 80
vhost_https_port = 443
dashboard_addr = 0.0.0.0
dashboard_port = 7500
dashboard_user = admin
dashboard_pwd = admin
authentication_timeout = 0
subdomain_host = frp.thyiad.top
EOF