# dockerfile

# docker-compose
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.sonarqube.service: sonarqube
  traefik.http.services.sonarqube.loadbalancer.server.port: 9000

services:

  sonarqube:
    image: sonarqube:10.1-community
    container_name: sonarqube
    labels:
      <<: *traefik-label
    expose:
      - "9000"
    volumes:
      - /volume1/storage/docker-data/sonarqube/data/:/opt/sonarqube/data/
      - /volume1/storage/docker-data/sonarqube/extensions/:/opt/sonarqube/extensions/
      - /volume1/storage/docker-data/sonarqube/logs/:/opt/sonarqube/logs/
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://192.168.2.18:5432/sonarqube
      SONAR_JDBC_USERNAME: "postgres"
      SONAR_JDBC_PASSWORD: "***REMOVED***"
    restart: always
```