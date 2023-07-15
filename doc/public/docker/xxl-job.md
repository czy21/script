
## docker-compose
```bash
docker-compose --project-name xxl-job --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.xxl-job.service: xxl-job
  traefik.http.services.xxl-job.loadbalancer.server.port: 8080

services:

  xxl-job:
    image: xuxueli/xxl-job-admin:2.4.0
    container_name: xxl-job
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "8080"
    user: root
    volumes:
      - /volume5/storage/docker-data/xxl-job/log/:/data/applogs
    environment:
      PARAMS: "
        --spring.datasource.url=jdbc:mysql://<ip>:3306/xxl_job?useUnicode=true&characterEncoding=UTF-8&autoReconnect=true&serverTimezone=Asia/Shanghai 
        --spring.datasource.username=<username>
        --spring.datasource.password=<password>
        --server.servlet.context-path=/
      "
    restart: always
```