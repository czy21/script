# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  ubuntu-friendlywrt:
    image: registry.czy21-internal.com/library/ubuntu-friendlywrt
    pull_policy: always
    container_name: ubuntu-friendlywrt
    hostname: ubuntu-friendlywrt
    user: opsor
    tty: true
    volumes:
      - /volume1/storage/docker-data/ubuntu-friendlywrt/data/:/data/
    restart: always
```