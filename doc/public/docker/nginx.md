
## conf
- /volume5/storage/docker-data/nginx/conf/nginx.conf
```text
user  nginx;
worker_processes  auto;

error_log  /dev/stdout;
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

    access_log  /dev/stdout;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;
    resolver 127.0.0.11; # docker container internal dns
    server {
        listen 8080;
        server_name  localhost;
        location /stub_status {
           stub_status on;
           access_log off;
        }
    }
    include /etc/nginx/conf.d/*.conf;
}

stream {
     include /etc/nginx/conf.d/stream/*.conf;
}
```
- /volume5/storage/docker-data/nginx/conf/app.conf
```text
proxy_request_buffering off;
proxy_buffering off;
tcp_nodelay on;
server {
    http2 on;
    listen       80;
    listen      443 ssl;
    server_name  *.czy21-internal.com *.cluster.com;

    client_max_body_size 0;
    chunked_transfer_encoding off;

    ssl_certificate     /etc/nginx/cert/czy21-internal.com.crt;
    ssl_certificate_key /etc/nginx/cert/czy21-internal.com.key;

    location / {

        proxy_set_header Host                $host;
        proxy_set_header X-Real-IP           $remote_addr;
        proxy_set_header X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto   $scheme;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass http://traefik:80;
    }
}
```
- /volume5/storage/docker-data/nginx/conf/default.conf
```text
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

```
## docker-compose
```bash
docker-compose --project-name nginx --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-exporter-label: &traefik-exporter-label
  traefik.enable: true
  traefik.http.routers.nginx-exporter.service: nginx-exporter
  traefik.http.services.nginx-exporter.loadbalancer.server.port: 9113

services:

  nginx:
    image: nginx:1.25.1-alpine
    container_name: nginx
    privileged: true
    user: root
    volumes:
      - /volume5/storage/docker-data/nginx/conf/nginx.conf:/etc/nginx/nginx.conf
      - /volume5/storage/docker-data/nginx/conf/conf.d/:/etc/nginx/conf.d/
      - /volume5/storage/docker-data/nginx/conf/cert/:/etc/nginx/cert/
    restart: always

  nginx-exporter:
    image: nginx/nginx-prometheus-exporter:0.11.0
    container_name: nginx-exporter
    labels:
      <<: *traefik-exporter-label
    expose:
      - "9113"
    command: -nginx.scrape-uri=http://nginx:8080/stub_status
    restart: always
```