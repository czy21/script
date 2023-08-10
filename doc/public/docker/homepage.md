
## conf
- /volume5/storage/docker-data/homepage/conf/bookmarks.yaml
```yaml
---
# For configuration options and examples, please see:
# https://gethomepage.dev/en/configs/bookmarks

#- dev:
#    - Github:
#        - abbr: GH
#          href: https://github.com/
#
#- Social:
#    - Reddit:
#        - abbr: RE
#          href: https://reddit.com/
#
#- Entertainment:
#    - YouTube:
#        - abbr: YT
#          href: https://youtube.com/
```
- /volume5/storage/docker-data/homepage/conf/docker.yaml
```yaml

```
- /volume5/storage/docker-data/homepage/conf/kubernetes.yaml
```yaml
---
# sample kubernetes config
```
- /volume5/storage/docker-data/homepage/conf/services.yaml
```yaml
- devops:
    - grafana:
        icon: grafana.svg
        href: http://grafana.czy21-internal.com
        widget:
          type: grafana
          url: http://grafana.czy21-internal.com
          username: <username>
          password: <password>
    - traefik-base:
        icon: traefik.svg
        href: http://traefik-base.czy21-internal.com
        widget:
          type: traefik
          url: http://traefik-base.czy21-internal.com
    - traefik-nas:
        icon: traefik.svg
        href: http://traefik-nas.czy21-internal.com
        widget:
          type: traefik
          url: http://traefik-nas.czy21-internal.com
    - prometheus-nas:
        icon: prometheus.svg
        href: http://prom-nas.czy21-internal.com
        widget:
          type: prometheus
          url: http://prom-nas.czy21-internal.com
    - portainer-nas:
        icon: portainer.svg
        href: http://portainer.czy21-internal.com
        widget:
          type: portainer
          url: http://portainer.czy21-internal.com
          env: 2
          key: ptr_V8YZL+4evqMYaJBysM4nwBm2ZQjHAtKAjJSwz1dK0pc=
    - portainer-test:
        icon: portainer.svg
        href: http://portainer.czy21-internal.com
        widget:
          type: portainer
          url: http://portainer.czy21-internal.com
          env: 3
          key: ptr_V8YZL+4evqMYaJBysM4nwBm2ZQjHAtKAjJSwz1dK0pc=

- media:
    - emby:
        icon: emby.svg
        href: http://emby.czy21-internal.com
        widget:
          type: emby
          url: http://emby.czy21-internal.com
          key: 56203aaf7539480db7e938b9a0357fbe
    - qbittorrent:
        icon: qbittorrent.svg
        href: http://qb.czy21-internal.com
        widget:
          type: qbittorrent
          url: http://qb.czy21-internal.com
          username: <username>
          password: <password>
    - sonarr:
        icon: sonarr.svg
        href: http://sonarr.czy21-internal.com
        widget:
          type: sonarr
          url: http://sonarr.czy21-internal.com
          key: 59ba45380d2649d087d3acdabf043af6
    - radarr:
        icon: radarr.svg
        href: http://radarr.czy21-internal.com
        widget:
          type: radarr
          url: http://radarr.czy21-internal.com
          key: c9db24d66ccf4e77959d7eb1384e519b
    - prowlarr:
        icon: prowlarr.svg
        href: http://prowlarr.czy21-internal.com
        widget:
          type: prowlarr
          url: http://prowlarr.czy21-internal.com
          key: e66d2f0f671d4a9999f27b274aa2a633
    - jackett:
        icon: jackett.svg
        href: http://jackett.czy21-internal.com
        widget:
          type: jackett
          url: http://jackett.czy21-internal.com
```
- /volume5/storage/docker-data/homepage/conf/settings.yaml
```yaml
---
# For configuration options and examples, please see:
# https://gethomepage.dev/en/configs/settings

providers:
  openweathermap: openweathermapapikey
  weatherapi: weatherapiapikey
```
- /volume5/storage/docker-data/homepage/conf/widgets.yaml
```yaml
---
# For configuration options and examples, please see:
# https://gethomepage.dev/en/configs/widgets

- resources:
    cpu: true
    memory: true
    disk: /

- search:
    provider: google
    focus: true
    target: _blank
```
## docker-compose
```bash
docker-compose --project-name homepage --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.homepage.service: homepage
  traefik.http.services.homepage.loadbalancer.server.port: 3000

services:

  homepage:
    image: "registry-proxy.czy21-public.com/benphelps/homepage:v0.6.22" # ghcr.io/benphelps/homepage:latest
    container_name: homepage
    hostname: homepage
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    volumes:
      - /volume5/storage/docker-data/homepage/conf/:/app/config/
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
    restart: always
```