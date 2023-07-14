# dockerfile

# docker-compose
```shell
docker-compose --project-name mssql --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  mssql:
    image: "mssql/server:2022-latest" # mcr.microsoft.com/mssql/server:2022-latest
    container_name: mssql
    privileged: true
    user: root
    ports:
      - "1433:1433"
    volumes:
      - /volume5/storage/docker-data/mssql/data/:/var/opt/mssql/
    environment:
      TZ: Asia/Shanghai
      ACCEPT_EULA: Y
      MSSQL_SA_PASSWORD: <password>
      MSSQL_COLLATION: Chinese_PRC_CI_AS
    restart: always
    deploy:
      resources:
        limits:
          memory: 8G

```