## conf
- /volume5/storage/docker-data/homeassistant/conf/automations.yaml
```text

```
- /volume5/storage/docker-data/homeassistant/conf/configuration.yaml
```text

# Loads default set of integrations. Do not remove.
default_config:

homeassistant:
  name: Home
  latitude: 45.80
  longitude: 126.54
  time_zone: Asia/Shanghai

http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 0.0.0.0/0

recorder:
  db_url: postgresql://postgres:<password>@<ip>:5432/homeassistant
  purge_keep_days: 180

# Text to speech
tts:
  - platform: google_translate

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```
- /volume5/storage/docker-data/homeassistant/conf/scenes.yaml
```text

```
- /volume5/storage/docker-data/homeassistant/conf/scripts.yaml
```text

```
## docker-compose
```bash
docker-compose --project-name homeassistant --file docker-compose.yaml up --detach --build --remove-orphans
```
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
      - /volume5/storage/docker-data/homeassistant/data/:/config/
    restart: always
#    networks:
#      vlan2:
#        ipv4_address: 192.168.2.17
```