# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  homeassistant:
    image: homeassistant/home-assistant:stable
    container_name: homeassistant
    privileged: true
    network_mode: host
    user: root
    expose:
      - "8123"
    volumes:
      - /volume1/storage/docker-data/homeassistant/data/:/config/
    restart: always
#    networks:
#      vlan2:
#        ipv4_address: 192.168.2.17
```