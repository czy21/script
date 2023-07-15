
## docker-compose
```bash
docker-compose --project-name adguard --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  adguardhome:
    image: adguard/adguardhome
    container_name: adguardhome
    hostname: adguardhome
    privileged: true
    user: root
    ports:
      - "3002:3000"
      - "5335:53/tcp"
      - "5335:53/udp"
    volumes:
      - /volume5/storage/docker-data/adguard/data/:/opt/adguardhome/work/
```