#!/usr/bin/env bash

set -e

sudo mkdir -p /data/volumes/shadowsocks/

sudo tee /data/volumes/shadowsocks/config.json <<-'EOF'
{
    "server":"0.0.0.0",
    "server_port":9000,
    "password":"czy20200325.",
    "timeout":300,
    "user":"nobody",
    "method":"aes-256-gcm",
    "fast_open":false,
    "nameserver":"8.8.8.8",
    "mode":"tcp_and_udp"
}
EOF