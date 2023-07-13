# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.jenkins.service: jenkins
  traefik.http.services.jenkins.loadbalancer.server.port: 8080

services:

  jenkins:
    image: registry.czy21-internal.com/library/jenkins
    pull_policy: always
    container_name: jenkins
    privileged: true
    working_dir: /var/jenkins_home/
    labels:
      <<: *traefik-label
    ports:
      - "50000:50000"
    volumes:
      - /volume1/storage/docker-data/jenkins/data/:/var/jenkins_home/
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      JENKINS_UC: https://mirrors.aliyun.com/jenkins/updates/update-center.json
      JENKINS_UC_EXPERIMENTAL: https://mirrors.aliyun.com/jenkins/updates/experimental/update-center.json
      # JAVA_OPS: "-Xms1024m -Xmx2048m -XX:PermSize=256m -XX:MaxPermSize=512m"
    deploy:
      resources:
        limits:
          memory: 8g
    restart: always
```