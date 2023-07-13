# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.web.service: web
  traefik.http.services.web.loadbalancer.server.port: 80

  # dynamic config proxy for docker labels
#  traefik.http.routers.web.priority: 1
#  traefik.http.routers.web.rule: Host(`nginx-.czy21-internal.com`)
#  traefik.http.routers.web.middlewares: https-redirect@file
#  traefik.http.routers.web-https.tls: true
#  traefik.http.routers.web-https.rule: Host(`nginx-.czy21-internal.com`)

services:
  
  
  web1:
    image: nginx:1.21-alpine
    labels:
      <<: *traefik-label
    container_name: web1
    pull_policy: always
    privileged: true
    volumes:
      - /volume1/storage/docker-data/web/conf/templates/:/etc/nginx/templates/
    environment:
      WEB_NODE_NAME: web1

  
  
  web2:
    image: nginx:1.21-alpine
    labels:
      <<: *traefik-label
    container_name: web2
    pull_policy: always
    privileged: true
    volumes:
      - /volume1/storage/docker-data/web/conf/templates/:/etc/nginx/templates/
    environment:
      WEB_NODE_NAME: web2

  
  
  web3:
    image: nginx:1.21-alpine
    labels:
      <<: *traefik-label
    container_name: web3
    pull_policy: always
    privileged: true
    volumes:
      - /volume1/storage/docker-data/web/conf/templates/:/etc/nginx/templates/
    environment:
      WEB_NODE_NAME: web3

  
```