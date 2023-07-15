
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
    listen       80;
    listen      443 ssl http2;
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

services:

  nginx:
    image: nginx:1.23.3-alpine
    container_name: nginx
    privileged: true
    user: root
    volumes:
      - /volume5/storage/docker-data/nginx/conf/nginx.conf:/etc/nginx/nginx.conf
      - /volume5/storage/docker-data/nginx/conf/conf.d/:/etc/nginx/conf.d/
      - /volume5/storage/docker-data/nginx/conf/cert/:/etc/nginx/cert/
    restart: always
```