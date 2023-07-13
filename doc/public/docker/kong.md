# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  kong:
    image: kong/kong-gateway:2.8-alpine
    pull_policy: always
    container_name: kong
    privileged: true
    user: root
    expose: ["8000","8001","8002","8003","8004","8443","8444","8445"]
    ports:
      - "8002:8002"
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: "<ip>"
      KONG_PG_USER: "postgres"
      KONG_PG_PASSWORD: "<password>"
      KONG_CASSANDRA_CONTACT_POINTS: kong
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
      KONG_ADMIN_GUI_URL: http://localhost:8002


  konga:
    image: pantsel/konga
    pull_policy: always
    container_name: konga
    privileged: true
    user: root
    expose: ["1337"]
    environment:
      DB_ADAPTER: mysql
      DB_URI: "mysql://<username>:<password>@<ip>:3306/konga"
      NODE_ENV: production



```