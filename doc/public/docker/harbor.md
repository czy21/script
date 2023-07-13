# dockerfile

# docker-compose
```yaml
version: "3.9"

x-common: &common
  privileged: true
  user: root
  restart: always

x-traefik-portal-label: &traefik-portal-label
  traefik.enable: true
  traefik.http.routers.harbor-portal.rule: Host(`harbor.czy21-internal.com`)
  traefik.http.routers.harbor-portal.service: harbor-portal
  traefik.http.services.harbor-portal.loadbalancer.server.port: 8080

x-traefik-core-label: &traefik-core-label
  traefik.enable: true
  traefik.http.routers.harbor-core.rule: Host(`harbor.czy21-internal.com`) && PathPrefix(`/{target:c|api|chartrepo|service}/`)
  traefik.http.routers.harbor-core.service: harbor-core
  traefik.http.services.harbor-core.loadbalancer.server.port: 8080
  traefik.http.middlewares.header-proto-https.headers.customrequestheaders.X-Forwarded-Proto: https
  traefik.http.routers.harbor-v2.rule: Host(`harbor.czy21-internal.com`) && PathPrefix(`/v2/`)
  traefik.http.routers.harbor-v2.service: harbor-v2
  traefik.http.services.harbor-v2.loadbalancer.server.port: 8080
  traefik.http.routers.harbor-v2.middlewares: header-proto-https

services:
  log:
    image: goharbor/harbor-log:v2.5.3
    container_name: harbor-log
    <<: *common
    volumes:
      - /volume1/storage/docker-data/harbor/log/harbor/:/var/log/docker/
      - /volume1/storage/docker-data/harbor/data/common/config/log/logrotate.conf:/etc/logrotate.d/logrotate.conf
      - /volume1/storage/docker-data/harbor/data/common/config/log/rsyslog_docker.conf:/etc/rsyslog.d/rsyslog_docker.conf
    ports:
      - "127.0.0.1:1514:10514"
  registry:
    image: goharbor/registry-photon:v2.5.3
    container_name: registry
    <<: *common
    expose:
      - "5000"
    volumes:
      - /volume1/storage/docker-data/harbor/data/registry/:/storage/
      - /volume1/storage/docker-data/harbor/data/common/config/registry/:/etc/registry/
      - /volume1/storage/docker-data/harbor/data/secret/registry/root.crt:/etc/registry/root.crt
      - /volume1/storage/docker-data/harbor/data/common/config/shared/trust-certificates:/harbor_cust_cert
    depends_on:
      - log
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://localhost:1514"
        tag: "registry"
  registryctl:
    image: goharbor/harbor-registryctl:v2.5.3
    container_name: registryctl
    <<: *common
    env_file:
      - /volume1/storage/docker-data/harbor/data/common/config/registryctl/env
    volumes:
      - /volume1/storage/docker-data/harbor/data/registry/:/storage/
      - /volume1/storage/docker-data/harbor/data/common/config/registry/:/etc/registry/
      - /volume1/storage/docker-data/harbor/data/common/config/registryctl/config.yml:/etc/registryctl/config.yml
      - /volume1/storage/docker-data/harbor/data/common/config/shared/trust-certificates:/harbor_cust_cert
    depends_on:
      - log
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://localhost:1514"
        tag: "registryctl"
  core:
    image: goharbor/harbor-core:v2.5.3
    container_name: harbor-core
    <<: *common
    labels:
      <<: *traefik-core-label
    expose:
      - "8080"
    env_file:
      - /volume1/storage/docker-data/harbor/data/common/config/core/env
    volumes:
      - /volume1/storage/docker-data/harbor/data/ca_download/:/etc/core/ca/
      - /volume1/storage/docker-data/harbor/data/:/data/
      - /volume1/storage/docker-data/harbor/data/common/config/core/certificates/:/etc/core/certificates/
      - /volume1/storage/docker-data/harbor/data/common/config/core/app.conf:/etc/core/app.conf
      - /volume1/storage/docker-data/harbor/data/secret/core/private_key.pem:/etc/core/private_key.pem
      - /volume1/storage/docker-data/harbor/data/secret/keys/secretkey:/etc/core/key
      - /volume1/storage/docker-data/harbor/data/common/config/shared/trust-certificates:/harbor_cust_cert
    depends_on:
      - log
      - registry
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://localhost:1514"
        tag: "core"
  portal:
    image: goharbor/harbor-portal:v2.5.3
    container_name: harbor-portal
    <<: *common
    labels:
      <<: *traefik-portal-label
    expose:
      - "8080"
    volumes:
      - /volume1/storage/docker-data/harbor/data/common/config/portal/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - log
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://localhost:1514"
        tag: "portal"

  jobservice:
    image: goharbor/harbor-jobservice:v2.5.3
    container_name: harbor-jobservice
    <<: *common
    env_file:
      - /volume1/storage/docker-data/harbor/data/common/config/jobservice/env
    volumes:
      - /volume1/storage/docker-data/harbor/data/job_logs/:/var/log/jobs/
      - /volume1/storage/docker-data/harbor/data/common/config/jobservice/config.yml:/etc/jobservice/config.yml
      - /volume1/storage/docker-data/harbor/data/common/config/shared/trust-certificates:/harbor_cust_cert
    depends_on:
      - core
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://localhost:1514"
        tag: "jobservice"
```