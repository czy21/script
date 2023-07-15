
## conf
- /volume5/storage/docker-data/jms/conf/nginx.conf
```text
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for" "$upstream_addr"';

    # access_log  /var/log/nginx/access.log  main;
    access_log off;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;
    # include /etc/nginx/conf.d/*.conf;

    server {
        listen 80;
        server_name  _;

        client_max_body_size 4096m;  # 录像及文件上传大小限制

        location /player/ {
            try_files $uri / /index.html;
            alias /opt/player/;
        }
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
        location /media/ {
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
            proxy_ignore_client_abort on;
            proxy_connect_timeout 600;
            proxy_send_timeout 600;
            proxy_read_timeout 600;
            send_timeout 6000;
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
            proxy_ignore_client_abort on;
            proxy_connect_timeout 600;
            proxy_send_timeout 600;
            proxy_read_timeout 600;
            send_timeout 6000;
        }
        location /ws/ {
            proxy_pass http://jms-core:8070;
            proxy_buffering off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location /api/ {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://jms-core:8080;
        }
        location /core/ {
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
    image: jumpserver/core:v2.28.5
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
    image: jumpserver/core:v2.28.5
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
    image: jumpserver/koko:v2.28.5
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
    image: jumpserver/lion:v2.28.5
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
    image: jumpserver/magnus:v2.28.5
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
    image: jumpserver/web:v2.28.5
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