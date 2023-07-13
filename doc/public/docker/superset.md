# dockerfile

# docker-compose
```yaml
version: "3.9"
services:

  superset:
    image: apache/superset:latest-dev
    container_name: superset_app
    command: ["/app/docker/docker-bootstrap.sh", "app-gunicorn"]
    user: "root"
    restart: unless-stopped
    ports:
      - 8088:8088
    volumes: 
      - /volume1/storage/docker-data/superset/conf/docker/:/app/docker/
      - /volume1/storage/docker-data/superset/data/superset/:/app/superset_home
    environment:
      DATABASE_DB: superset
      DATABASE_HOST: <ip>
      DATABASE_PASSWORD: <password>
      DATABASE_USER: postgres
      DATABASE_PORT: 5432
      DATABASE_DIALECT: postgresql
      POSTGRES_DB: superset
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <password>
      PYTHONPATH: /app/pythonpath:/app/docker/pythonpath_dev
      REDIS_HOST: <ip>
      REDIS_PORT: 6379
      FLASK_ENV: production
      SUPERSET_ENV: production
      SUPERSET_LOAD_EXAMPLES: "yes"
      CYPRESS_CONFIG: "false"
      SUPERSET_PORT: 8088

  superset-init:
    image: apache/superset:latest-dev
    container_name: superset_init
    command: ["/app/docker/docker-init.sh"]
    user: "root"
    volumes:
      - /volume1/storage/docker-data/superset/conf/docker/:/app/docker/
      - /volume1/storage/docker-data/superset/data/superset/:/app/superset_home
    environment:
      DATABASE_DB: superset
      DATABASE_HOST: <ip>
      DATABASE_PASSWORD: <password>
      DATABASE_USER: postgres
      DATABASE_PORT: 5432
      DATABASE_DIALECT: postgresql
      POSTGRES_DB: superset
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <password>
      PYTHONPATH: /app/pythonpath:/app/docker/pythonpath_dev
      REDIS_HOST: <ip>
      REDIS_PORT: 6379
      FLASK_ENV: production
      SUPERSET_ENV: production
      SUPERSET_LOAD_EXAMPLES: "yes"
      CYPRESS_CONFIG: "false"
      SUPERSET_PORT: 8088

  superset-worker:
    image: apache/superset:latest-dev
    container_name: superset_worker
    command: ["/app/docker/docker-bootstrap.sh", "worker"]
    restart: unless-stopped
    user: "root"
    volumes:
      - /volume1/storage/docker-data/superset/conf/docker/:/app/docker/
      - /volume1/storage/docker-data/superset/data/superset/:/app/superset_home
    environment:
      DATABASE_DB: superset
      DATABASE_HOST: <ip>
      DATABASE_PASSWORD: <password>
      DATABASE_USER: postgres
      DATABASE_PORT: 5432
      DATABASE_DIALECT: postgresql
      POSTGRES_DB: superset
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <password>
      PYTHONPATH: /app/pythonpath:/app/docker/pythonpath_dev
      REDIS_HOST: <ip>
      REDIS_PORT: 6379
      FLASK_ENV: production
      SUPERSET_ENV: production
      SUPERSET_LOAD_EXAMPLES: "yes"
      CYPRESS_CONFIG: "false"
      SUPERSET_PORT: 8088

  superset-worker-beat:
    image: apache/superset:latest-dev
    container_name: superset_worker_beat
    command: ["/app/docker/docker-bootstrap.sh", "beat"]
    restart: unless-stopped
    user: "root"
    volumes:
      - /volume1/storage/docker-data/superset/conf/docker/:/app/docker/
      - /volume1/storage/docker-data/superset/data/superset/:/app/superset_home
    environment:
      DATABASE_DB: superset
      DATABASE_HOST: <ip>
      DATABASE_PASSWORD: <password>
      DATABASE_USER: postgres
      DATABASE_PORT: 5432
      DATABASE_DIALECT: postgresql
      POSTGRES_DB: superset
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <password>
      PYTHONPATH: /app/pythonpath:/app/docker/pythonpath_dev
      REDIS_HOST: <ip>
      REDIS_PORT: 6379
      FLASK_ENV: production
      SUPERSET_ENV: production
      SUPERSET_LOAD_EXAMPLES: "yes"
      CYPRESS_CONFIG: "false"
      SUPERSET_PORT: 8088


```