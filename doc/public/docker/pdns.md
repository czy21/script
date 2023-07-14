# dockerfile

# docker-compose
```shell
docker-compose --project-name pdns --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  pdns-auth:
    image: powerdns/pdns-auth-master
    container_name: pdns-auth
    privileged: true
    user: root
    environment:
      PDNS_AUTH_API_KEY: ***REMOVED***
  pdns-web:
    image: ngoduykhanh/powerdns-admin
    container_name: pdns-web
    privileged: true
    user: root
    ports:
      - "9191:80"
    volumes:
      - /volume1/storage/docker-data/pdns/data/web/:/data/
    environment:
      SECRET_KEY: ***REMOVED***
```