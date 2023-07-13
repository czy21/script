# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  ubuntu-openwrt:
    image: registry.czy21-internal.com/library/ubuntu-openwrt
    pull_policy: always
    container_name: ubuntu-openwrt
    hostname: ubuntu-openwrt
    user: opsor
    tty: true
    volumes:
      - /volume1/storage/docker-data/ubuntu-openwrt/data/:/data/
    restart: always
```