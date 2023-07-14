# dockerfile

# docker-compose
```shell
docker-compose --project-name odoo --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.odoo.service: odoo
  traefik.http.services.odoo.loadbalancer.server.port: 8069

services:
  odoo:
    image: odoo:15.0
    container_name: odoo
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "8069"
    volumes:
      - /volume1/storage/docker-data/odoo/data/:/var/lib/odoo/
      - /volume1/storage/docker-data/odoo/addon/:/mnt/extra-addons/
    environment:
     HOST: '192.168.2.18'
     PORT: '5432'
     USER: 'odoo'
     PASSWORD: '***REMOVED***'
```