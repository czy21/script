#!/bin/bash

set -e

sudo rm -rf /data/config/nginx/conf.d/
sudo mkdir -p /data/config/nginx/conf.d/

sudo tee /data/config/nginx/nginx.conf <<-'EOF'
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
EOF

sudo tee /data/config/nginx/conf.d/default.conf <<-'EOF'
server {
    listen       80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
EOF

sudo tee /data/config/nginx/conf.d/custom.conf <<-'EOF'
server {
		listen 80;
		server_name czy-home.cn;

    location /ray {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
    location /frp-dashboard {
        proxy_pass http://127.0.0.1:7500;
    }
}
EOF

sudo tee /data/config/nginx/conf.d/frp.conf <<-'EOF'
server {
		listen 80;
		server_name *.czy-home.cn;

		location / {
        proxy_pass http://127.0.0.1:6080;
        proxy_set_header Host $host:80;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
			}
}
EOF
