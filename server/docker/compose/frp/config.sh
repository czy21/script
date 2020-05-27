#!/bin/bash

set -e

sudo mkdir -p /data/config/frp/conf/


sudo tee /data/config/frp/conf/frps.ini <<-'EOF'
[common]
bind_port = 7000
vhost_http_port = 80
vhost_https_port = 443
token = 12345678

dashboard_addr = 0.0.0.0
dashboard_port = 7500
EOF