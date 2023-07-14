
## conf
- /volume5/storage/docker-data/mysql/conf/mysql.cnf
```text
[client]
default-character-set=utf8mb4
[mysql]
default-character-set=utf8mb4
```
## docker-compose
```bash
docker-compose --project-name mysql --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  mysql:
    image: mysql:8.0.31
    container_name: mysql
    privileged: true
    user: root
    ports:
      - "3306:3306"
    volumes:
      - /volume5/storage/docker-data/mysql/data/:/var/lib/mysql/
      - /volume5/storage/docker-data/mysql/conf/conf.d/:/etc/mysql/conf.d/
    command: --default-authentication-plugin=mysql_native_password 
             --character-set-server=utf8mb4
             --collation-server=utf8mb4_unicode_ci
             --max_connections=10000
             --transaction-isolation=READ-COMMITTED
             --skip-log-bin
    environment:
      TZ: Asia/Shanghai
      MYSQL_ALLOW_EMPTY_PASSWORD: 0
      MYSQL_ROOT_PASSWORD: "<password>"
    restart: always

  mysql-exporter-3306:
    image: prom/mysqld-exporter
    container_name: mysql-exporter-3306
    environment:
      DATA_SOURCE_NAME: "<username>:<password>@(mysql:3306)/"
    restart: always

```