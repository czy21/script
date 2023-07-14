# dockerfile

# docker-compose
```shell
docker-compose --project-name nginx-unit --file docker-compose.yaml up --detach --build --remove-orphans
```
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