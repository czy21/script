# dockerfile

# docker-compose
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
      - /volume1/storage/docker-data/jms/data/core/data:/opt/jumpserver/data
      - /volume1/storage/docker-data/jms/data/core/logs:/opt/jumpserver/logs
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
      - /volume1/storage/docker-data/jms/data/core/data:/opt/jumpserver/data
      - /volume1/storage/docker-data/jms/data/core/logs:/opt/jumpserver/logs

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
      - /volume1/storage/docker-data/jms/data/koko/data:/opt/koko/data
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
      - /volume1/storage/docker-data/jms/data/lion/data:/opt/lion/data

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
      - /volume1/storage/docker-data/jms/data/magnus/data:/opt/magnus/data
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
      - /volume1/storage/docker-data/jms/conf/nginx.conf:/etc/nginx/nginx.conf
      - /volume1/storage/docker-data/jms/data/core/data:/opt/jumpserver/data
      - /volume1/storage/docker-data/jms/data/nginx/data/logs:/var/log/nginx
    labels:
      <<: *traefik-label
```