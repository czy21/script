# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-qbittorrent-label: &traefik-qbittorrent-label
  traefik.enable: true
  traefik.http.routers.qbittorrent.service: qbittorrent
  traefik.http.services.qbittorrent.loadbalancer.server.port: 8080

x-traefik-jackett-label: &traefik-jackett-label
  traefik.enable: true
  traefik.http.routers.jackett.service: jackett
  traefik.http.services.jackett.loadbalancer.server.port: 9117

x-traefik-radarr-label: &traefik-radarr-label
  traefik.enable: true
  traefik.http.routers.radarr.service: radarr
  traefik.http.services.radarr.loadbalancer.server.port: 7878

x-traefik-sonarr-label: &traefik-sonarr-label
  traefik.enable: true
  traefik.http.routers.sonarr.service: sonarr
  traefik.http.services.sonarr.loadbalancer.server.port: 8989

x-traefik-prowlarr-label: &traefik-prowlarr-label
  traefik.enable: true
  traefik.http.routers.prowlarr.service: prowlarr
  traefik.http.services.prowlarr.loadbalancer.server.port: 9696

x-traefik-bazarr-label: &traefik-bazarr-label
  traefik.enable: true
  traefik.http.routers.bazarr.service: bazarr
  traefik.http.services.bazarr.loadbalancer.server.port: 6767

x-traefik-chinesesubfinder-label: &traefik-chinesesubfinder-label
  traefik.enable: true
  traefik.http.routers.chinesesubfinder.service: chinesesubfinder
  traefik.http.services.chinesesubfinder.loadbalancer.server.port: 19035

services:
  qbittorrent:
    image: linuxserver/qbittorrent:4.5.4
    container_name: qbittorrent
    labels:
      <<: *traefik-qbittorrent-label
    ports:
      - "6881:6881" # bt port
    volumes:
      - /volume1/storage/docker-data/streaming/data/qbittorrent/:/config/
      - /volume1/public/media/:/volume1/public/media/
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
      WEBUI_PORT: 8080
    restart: always

  jackett:
    image: linuxserver/jackett:0.21.361
    container_name: jackett
    labels:
      <<: *traefik-jackett-label
    volumes:
      - /volume1/storage/docker-data/streaming/data/jackett/:/config/
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
      AUTO_UPDATE: "true"
    restart: always

  radarr:
    image: linuxserver/radarr:4.6.4
    container_name: radarr
    labels:
      <<: *traefik-radarr-label
    volumes:
      - /volume1/storage/docker-data/streaming/data/radarr/:/config/
      - /volume1/public/media/:/volume1/public/media/
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
    restart: always

  sonarr:
    image: linuxserver/sonarr:3.0.10
    container_name: sonarr
    labels:
      <<: *traefik-sonarr-label
    volumes:
      - /volume1/storage/docker-data/streaming/data/sonarr/:/config/
      - /volume1/public/media/:/volume1/public/media/
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
    restart: always

  prowlarr:
    image: linuxserver/prowlarr:1.6.3
    container_name: prowlarr
    labels:
      <<: *traefik-prowlarr-label
    volumes:
      - /volume1/storage/docker-data/streaming/data/prowlarr/:/config/
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
    restart: always

  bazarr:
    image: linuxserver/bazarr:1.2.2
    container_name: bazarr
    labels:
      <<: *traefik-bazarr-label
    volumes:
      - /volume1/storage/docker-data/streaming/data/bazarr/:/config/
      - /volume1/public/media/:/volume1/public/media/
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
    restart: always

  chinesesubfinder:
    image: allanpk716/chinesesubfinder:v0.53.3
    container_name: chinesesubfinder
    labels:
      <<: *traefik-chinesesubfinder-label
    volumes:
      - /volume1/storage/docker-data/streaming/data/chinesesubfinder/:/config/
      - /volume1/public/media/:/media/
    environment:
      PUID: 1000    
      PGID: 1000        
      TZ: Asia/Shanghai
    restart: always
```