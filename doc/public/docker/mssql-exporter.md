# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  mssql_exporter:
    image: awaragi/prometheus-mssql-exporter
    container_name: mssql_exporter
    ports:
      - "4000:4000"
    environment:
      SERVER: 192.168.2.18
      PORT: 1433
      USERNAME: sa
      PASSWORD: ***REMOVED***
      DEBUG: app

    user: root

```