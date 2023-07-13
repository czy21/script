# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  nginx:
    image: nginx:1.23.3-alpine
    container_name: nginx
    privileged: true
    user: root
    volumes:
      - /volume1/storage/docker-data/nginx/conf/nginx.conf:/etc/nginx/nginx.conf
      - /volume1/storage/docker-data/nginx/conf/conf.d/:/etc/nginx/conf.d/
      - /volume1/storage/docker-data/nginx/conf/cert/:/etc/nginx/cert/
    restart: always
```