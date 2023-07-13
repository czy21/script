# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  ubuntu-lede:
    image: registry.czy21-internal.com/library/ubuntu-lede
    pull_policy: always
    container_name: ubuntu-lede
    hostname: ubuntu-lede
    user: opsor
    tty: true
    volumes:
      - /volume1/storage/docker-data/ubuntu-lede/data/:/data/
    restart: always
```