
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

    log_format  main  '$remote_addr $host $remote_user [$time_local] '
                      '"$request" $status $body_bytes_sent '
                      '"$http_referer" "$http_user_agent" "$http_x_forwarded_for" '
                      '$request_time $upstream_response_time';

    access_log  /dev/stdout main;

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
- /volume5/storage/docker-data/nginx/conf/conf.d/default.conf
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
    logging:
      driver: "fluentd"
      options:
        fluentd-address: localhost:24224
        tag: "docker.{{.Name}}"


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