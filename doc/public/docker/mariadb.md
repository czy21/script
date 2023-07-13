# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  mariadb:
    image: mariadb:10.9.4
    container_name: mariadb
    privileged: true
    user: root
    ports:
      - "3406:3306"
    volumes:
      - /volume1/storage/docker-data/mariadb/data/:/var/lib/mysql/
    environment:
      TZ: Asia/Shanghai
      MARIADB_USER: "admin"
      MARIADB_PASSWORD: "***REMOVED***"
      MARIADB_ROOT_PASSWORD: "***REMOVED***"
    restart: always
```