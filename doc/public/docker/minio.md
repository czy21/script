
## docker-compose
```bash
docker-compose --project-name minio --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-minio-common: &minio-common
  image: minio/minio:RELEASE.2023-03-09T23-16-13Z
  privileged: true
  user: root
  expose:
    - "9000"
    - "9001"
  environment:
    MINIO_ROOT_USER: <username>
    MINIO_ROOT_PASSWORD: <password>
    MINIO_PROMETHEUS_AUTH_TYPE: public
  restart: always

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.minio-api.service: minio-api
  traefik.http.services.minio-api.loadbalancer.server.port: 9000
  traefik.http.routers.minio-web.service: minio-web
  traefik.http.services.minio-web.loadbalancer.server.port: 9001

services:
  minio:
    <<: *minio-common
    container_name: minio
    labels:
      <<: *traefik-label
    volumes:
      - /volume5/storage/docker-data/minio/data/single:/data/
    command: server /data --console-address ":9001"

```