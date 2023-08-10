
## docker-compose
```bash
docker-compose --project-name mariadb --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  mariadb:
    image: mariadb:11.0.2
    container_name: mariadb
    privileged: true
    user: root
    ports:
      - "3406:3306"
    volumes:
      - /volume5/storage/docker-data/mariadb/data/:/var/lib/mysql/
    environment:
      TZ: Asia/Shanghai
      MARIADB_USER: "<username>"
      MARIADB_PASSWORD: "<password>"
      MARIADB_ROOT_PASSWORD: "<password>"
    restart: always
```