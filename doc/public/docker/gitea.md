# dockerfile

# docker-compose
```shell
docker-compose --project-name gitea --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.gitea.service: gitea
  traefik.http.services.gitea.loadbalancer.server.port: 3000

services:

  gitea:
    image: gitea/gitea:1.19.3
    container_name: gitea
    labels:
      <<: *traefik-label
    privileged: true
    expose:
      - "3000"
      - "22"
    user: root
    volumes:
      - /volume5/storage/docker-data/gitea/data/:/data/
    environment:
      TZ: Asia/Shanghai
      GITEA__server__DOMAIN: "gitea.czy21-internal.com"
      GITEA__server__SSH_DOMAIN: "gitea.czy21-internal.com"
      GITEA__server__ROOT_URL: "http://gitea.czy21-internal.com/"
      GITEA__server__HTTP_PORT: "3000"
      GITEA__server__LANDING_PAGE: explore
      GITEA__security__INSTALL_LOCK: true
      GITEA__database__DB_TYPE: sqlite3
      GITEA__service__DISABLE_REGISTRATION: true
      GITEA__packages__ENABLED: "true"
      GITEA__repository__DEFAULT_REPO_UNITS: repo.code,repo.releases
      GITEA__repository__DISABLED_REPO_UNITS: repo.issues, repo.ext_issues, repo.pulls, repo.wiki, repo.ext_wiki
      GITEA__attachment__MAX_SIZE: 1024
      GITEA__attachment__MAX_FILES: 20
    restart: always
```