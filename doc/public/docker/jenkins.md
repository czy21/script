
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/jenkins --file Dockerfile . --pull
```
```dockerfile
FROM jenkins/jenkins:2.418-jdk11

LABEL org.opencontainers.image.url='https://github.com/czy21/container'
LABEL org.opencontainers.image.source='https://github.com/czy21/container/tree/main/jenkins'
LABEL org.opencontainers.image.title='base on jenkins/jenkins:2.418-jdk11'
LABEL org.opencontainers.image.authors='a805899926@gmail.com>'

USER root
RUN apt update && apt install sudo -y
RUN curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins
USER jenkins
```
## docker-compose
```bash
docker-compose --project-name jenkins --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.jenkins.service: jenkins
  traefik.http.services.jenkins.loadbalancer.server.port: 8080

services:

  jenkins:
    image: docker.io/czy21/jenkins
    pull_policy: always
    container_name: jenkins
    privileged: true
    working_dir: /var/jenkins_home/
    labels:
      <<: *traefik-label
    ports:
      - "50000:50000"
    volumes:
      - /volume5/storage/docker-data/jenkins/data/:/var/jenkins_home/
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      JENKINS_UC: https://mirrors.aliyun.com/jenkins/updates/update-center.json
      JENKINS_UC_EXPERIMENTAL: https://mirrors.aliyun.com/jenkins/updates/experimental/update-center.json
      #JAVA_OPS: "-Xms1024m -Xmx2048m -XX:PermSize=256m -XX:MaxPermSize=512m"
    deploy:
      resources:
        limits:
          memory: 8g
    restart: always
```