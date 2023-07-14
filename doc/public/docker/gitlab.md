
## docker-compose
```bash
docker-compose --project-name gitlab --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.gitlab.service: gitlab
  traefik.http.services.gitlab.loadbalancer.server.port: 80

services:
  gitlab:
    image: gitlab/gitlab-ee:15.6.0-ee.0
    container_name: gitlab
    hostname: gitlab
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
      - "443"
      - "22"
    volumes:
      - /volume5/storage/docker-data/gitlab/data/conf/:/etc/gitlab/
      - /volume5/storage/docker-data/gitlab/data/data/:/var/opt/gitlab/
      - /volume5/storage/docker-data/gitlab/log/:/var/log/gitlab/
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://gitlab.czy21-internal.com'
      GITLAB_ROOT_PASSWORD: "<password>"
    shm_size: 256m
```