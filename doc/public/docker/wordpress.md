
## docker-compose
```bash
docker-compose --project-name wordpress --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.wordpress.service: wordpress
  traefik.http.services.wordpress.loadbalancer.server.port: 80

services:
  wordpress:
    image: wordpress:php8.0-apache
    container_name: wordpress
    hostname: wordpress
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
    volumes:
      - /volume5/storage/docker-data/wordpress/data/:/var/www/html
    environment:
      WORDPRESS_DB_HOST: "<ip>"
      WORDPRESS_DB_USER: "<username>"
      WORDPRESS_DB_PASSWORD: "<password>"
      WORDPRESS_DB_NAME: wordpress
    restart: always
```