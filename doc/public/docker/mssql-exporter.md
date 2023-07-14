# dockerfile

# docker-compose
```shell
docker-compose --project-name mssql-exporter --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  mssql_exporter:
    image: awaragi/prometheus-mssql-exporter
    container_name: mssql_exporter
    ports:
      - "4000:4000"
    environment:
      SERVER: <ip>
      PORT: 1433
      USERNAME: sa
      PASSWORD: <password>
      DEBUG: app

    user: root

```