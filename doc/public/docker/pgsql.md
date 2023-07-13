# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  pgsql:
    image: postgres:14-alpine
    container_name: pgsql
    privileged: true
    user: root
    ports:
      - "5432:5432"
    volumes:
      - /volume1/storage/docker-data/pgsql/conf/postgresql.conf:/etc/postgresql/postgresql.conf
      - /volume1/storage/docker-data/pgsql/data/:/var/lib/postgresql/data/
    command: -c config_file=/etc/postgresql/postgresql.conf
    environment:
      TZ: Asia/Shanghai
      POSTGRES_PASSWORD: "<password>"
    restart: always
  pgsql-exporter-5432:
    image: prometheuscommunity/postgres-exporter
    container_name: pgsql-exporter-5432
    environment:
      DATA_SOURCE_NAME: "postgresql://postgres:<password>@pgsql:5432/postgres?sslmode=disable"
    restart: always
```