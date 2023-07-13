# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  nginx-unit:
    image: unit:1.30.0-minimal
    container_name: nginx-unit
    privileged: true
    user: root
    restart: always
```