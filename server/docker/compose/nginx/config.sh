#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)

sudo rm -rf /data/config/nginx/conf.d/
sudo mkdir -p /data/config/nginx/conf.d/

sudo cp -r $dir/cert/ /data/config/nginx/

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
    server_name  czy-home.cn;

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
      listen 443 ssl;
      listen [::]:443 ssl;
      server_name czy-home.cn;

      ssl_certificate       /etc/nginx/cert/cert.pem;
      ssl_certificate_key   /etc/nginx/cert/key.pem;
      ssl_session_timeout 1d;
      ssl_session_cache shared:MozSSL:10m;
      ssl_session_tickets off;

      ssl_protocols         TLSv1.2 TLSv1.3;
      ssl_ciphers           ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
      ssl_prefer_server_ciphers off;

      location /ray {
        if ($http_upgrade != "websocket") {
            return 404;
        }
        proxy_redirect off;
        proxy_pass http://127.0.0.1:9000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      }
}
EOF

#sudo tee /data/config/nginx/conf.d/frp.conf <<-'EOF'
#server {
#		listen 80;
#		server_name *.czy-home.cn;
#
#		location / {
#        proxy_pass http://127.0.0.1:6080;
#        proxy_set_header Host $host:80;
#        proxy_set_header X-Real-IP $remote_addr;
#        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#
#        proxy_set_header Upgrade $http_upgrade;
#        proxy_set_header Connection "upgrade";
#			}
#}
#EOF
