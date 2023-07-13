# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  frp:
    build:
      context: /compose/frp/
      dockerfile: /compose/frp/Dockerfile
    image: frp:1.0.0
    container_name: frp
    privileged: true
    user: root
    ports:
      - 7000:7000
    volumes:
      - /frp/:/usr/local/frp/conf/


```