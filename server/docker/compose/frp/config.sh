#!/bin/bash

set -e

sudo mkdir -p /data/config/frp/conf/


sudo tee /data/config/frp/conf/frps.ini <<-'EOF'
[common]
bind_addr = 0.0.0.0
bind_port = 7000
dashboard_addr = 0.0.0.0
dashboard_port = 7500
EOF