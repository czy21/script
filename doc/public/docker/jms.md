
## conf
- /volume5/storage/docker-data/jms/conf/nginx.conf
```text
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
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
    proxy_cache_path /var/cache/nginx/proxy_cache levels=1:1:1 keys_zone=cache:10m max_size=2g;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    gzip  on;
    server_tokens off;

    server {
        listen 80;
        server_name  _;

        proxy_cache cache;
        proxy_cache_key $host$request_uri;
        proxy_cache_methods GET HEAD;
        proxy_cache_valid 200 302 720m;
        proxy_cache_valid 404      1m;
        proxy_cache_use_stale http_502;
        proxy_set_header X-Real-IP $remote_addr;
        add_header X-Via $server_addr;

        client_max_body_size 4096m;  # 录像及文件上传大小限制

        location /download/ {
            alias /opt/download/;
        }
        location /ui/ {
            try_files $uri / /index.html;
            alias /opt/lina/;
        }
        location /luna/ {
            try_files $uri / /index.html;
            alias /opt/luna/;
        }
        location /media/replay/ {
            add_header Content-Encoding gzip;
            root /opt/jumpserver/data/;
        }
        location /static/ {
            root /opt/jumpserver/data/;
        }
        location /koko/ {
            proxy_pass http://jms-koko:5000;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_request_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location /lion/ {
            proxy_pass http://jms-lion:8081;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_request_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location /ws/ {
            proxy_pass http://jms-core:8080;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location ~ ^/(core|api|media)/ {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://jms-core:8080;
        }
        location / {
            rewrite ^/(.*)$ /ui/$1 last;
        }
    }
}
```
## docker-compose
```bash
docker-compose --project-name jms --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.jms.service: jms
  traefik.http.services.jms.loadbalancer.server.port: 80

services:
  jms-core:
    image: jumpserver/core:v3.5.0
    container_name: jms-core
    hostname: jms-core
    restart: always
    tty: true
    command: start web
    environment:
      SECRET_KEY: "B3f2w8P2PfxIAS7s4URrD9YmSbtqX4vXdPUL217kL9XPUOWrmy"
      BOOTSTRAP_TOKEN: "7Q11Vz6R2J6BLAdO"
      DEBUG: "FALSE"
      LOG_LEVEL: "ERROR"
      DB_HOST: "<ip>"
      DB_PORT: "3306"
      DB_USER: "<username>"
      DB_PASSWORD: "<password>"
      DB_NAME: "jms"
      REDIS_HOST: "<ip>"
      REDIS_PORT: "6379"
      REDIS_PASSWORD: "<password>"
    healthcheck:
      test: "curl -fsL http://localhost:8080/api/health/ > /dev/null"
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 90s
    volumes:
      - /volume5/storage/docker-data/jms/data/core/data:/opt/jumpserver/data
      - /volume5/storage/docker-data/jms/data/core/logs:/opt/jumpserver/logs
    expose:
      - "8080"

  jms-celery:
    image: jumpserver/core:v3.5.0
    container_name: jms-celery
    hostname: jms-celery
    restart: always
    tty: true
    command: start task
    environment:
      SECRET_KEY: "B3f2w8P2PfxIAS7s4URrD9YmSbtqX4vXdPUL217kL9XPUOWrmy"
      BOOTSTRAP_TOKEN: "7Q11Vz6R2J6BLAdO"
      DEBUG: "FALSE"
      LOG_LEVEL: "ERROR"
      DB_HOST: "<ip>"
      DB_PORT: "3306"
      DB_USER: "<username>"
      DB_PASSWORD: "<password>"
      DB_NAME: "jms"
      REDIS_HOST: "<ip>"
      REDIS_PORT: "6379"
      REDIS_PASSWORD: "<password>"
    depends_on:
      jms-core:
        condition: service_healthy
    healthcheck:
      test: "bash /opt/jumpserver/utils/check_celery.sh"
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
    volumes:
      - /volume5/storage/docker-data/jms/data/core/data:/opt/jumpserver/data
      - /volume5/storage/docker-data/jms/data/core/logs:/opt/jumpserver/logs

  jms-koko:
    image: jumpserver/koko:v3.5.0
    container_name: jms-koko
    hostname: jms-koko
    restart: always
    privileged: true
    tty: true
    environment:
      CORE_HOST: http://jms-core:8080
      BOOTSTRAP_TOKEN: "7Q11Vz6R2J6BLAdO"
      LOG_LEVEL: "ERROR"
      SSHD_PORT: "22"
    depends_on:
      jms-core:
        condition: service_healthy
    healthcheck:
      test: "curl -fsL http://localhost:5000/koko/health/ > /dev/null"
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    volumes:
      - /volume5/storage/docker-data/jms/data/koko/data:/opt/koko/data
    expose:
      - "22"
    ports:
      - 2222:22

  jms-lion:
    image: jumpserver/lion:v3.5.0
    container_name: jms-lion
    hostname: jms-lion
    restart: always
    tty: true
    environment:
      CORE_HOST: http://jms-core:8080
      BOOTSTRAP_TOKEN: "7Q11Vz6R2J6BLAdO"
      LOG_LEVEL: "ERROR"
    depends_on:
      jms-core:
        condition: service_healthy
    healthcheck:
      test: "curl -fsL http://localhost:8081/lion/health/ > /dev/null"
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    volumes:
      - /volume5/storage/docker-data/jms/data/lion/data:/opt/lion/data

  jms-magnus:
    image: jumpserver/magnus:v3.5.0
    container_name: jms-magnus
    hostname: jms-magnus
    restart: always
    tty: true
    environment:
      CORE_HOST: http://jms-core:8080
      BOOTSTRAP_TOKEN: "7Q11Vz6R2J6BLAdO"
      LOG_LEVEL: "ERROR"
    depends_on:
      jms-core:
        condition: service_healthy
    healthcheck:
      test: "ps axu | grep -v 'grep' | grep magnus"
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    volumes:
      - /volume5/storage/docker-data/jms/data/magnus/data:/opt/magnus/data
    ports:
      - 30000-30100:30000-30100

  jms-web:
    image: jumpserver/web:v3.5.0
    container_name: jms-web
    hostname: jms-web
    restart: always
    tty: true
    environment:
      HTTP_PORT: "80"
    depends_on:
      jms-core:
        condition: service_healthy
    healthcheck:
      test: "curl -fsL http://localhost/ > /dev/null"
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    volumes:
      - /volume5/storage/docker-data/jms/conf/nginx.conf:/etc/nginx/nginx.conf
      - /volume5/storage/docker-data/jms/data/core/data:/opt/jumpserver/data
      - /volume5/storage/docker-data/jms/data/nginx/data/logs:/var/log/nginx
    labels:
      <<: *traefik-label
```