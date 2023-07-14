
## docker-compose
```bash
docker-compose --project-name dm8 --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  dm8:
    image: dm8_single:v8.1.2.128_ent_x86_64_ctm_pack4
    container_name: dm8
    privileged: true
    user: root
    ports:
      - "5236:5236"
    volumes:
      - /volume5/storage/docker-data/dm8/data/:/opt/dmdbms/data/
    environment:
      PAGE_SIZE: 16
      LD_LIBRARY_PATH: /opt/dmdbms/bin
      INSTANCE_NAME: dm8_01
    restart: always

```