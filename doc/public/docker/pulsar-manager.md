# dockerfile
# conf
- /volume5/storage/docker-data/pulsar-manager/conf/manager.properties
```text
spring.cloud.refresh.refreshable=none
server.port=7750

# configuration log
logging.path=
logging.file=/log/pulsar-manager.log

# DEBUG print execute sql
logging.level.org.apache=INFO

mybatis.type-aliases-package=org.apache.pulsar.manager

# postgresql configuration
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://192.168.2.18:5432/pulsar_manager?user=postgres&password=***REMOVED***

# zuul config
# https://cloud.spring.io/spring-cloud-static/Dalston.SR5/multi/multi__router_and_filter_zuul.html
# By Default Zuul adds  Authorization to be dropped headers list. Below we are manually setting it
zuul.sensitive-headers=Cookie,Set-Cookie
zuul.routes.admin.path=/admin/**
zuul.routes.admin.url=http://pulsar-broker1:8080/admin/
zuul.routes.lookup.path=/lookup/**
zuul.routes.lookup.url=http://pulsar-broker1:8080/lookup/

# pagehelper plugin
#pagehelper.helperDialect=sqlite
# force 'mysql' for HerdDB, comment out for postgresql
pagehelper.helperDialect=postgresql

backend.directRequestBroker=true
backend.directRequestHost=http://pulsar-broker1:8080
backend.jwt.token=
backend.broker.pulsarAdmin.authPlugin=
backend.broker.pulsarAdmin.authParams=
backend.broker.pulsarAdmin.tlsAllowInsecureConnection=false
backend.broker.pulsarAdmin.tlsTrustCertsFilePath=
backend.broker.pulsarAdmin.tlsEnableHostnameVerification=false

jwt.secret=dab1c8ba-b01b-11e9-b384-186590e06885
jwt.sessionTime=2592000
# If user.management.enable is true, the following account and password will no longer be valid.
pulsar-manager.account=pulsar
pulsar-manager.password=pulsar
# If true, the database is used for user management
user.management.enable=true

# Optional -> SECRET, PRIVATE, default -> PRIVATE, empty -> disable auth
# SECRET mode -> bin/pulsar tokens create --secret-key file:///path/to/my-secret.key --subject test-user
# PRIVATE mode -> bin/pulsar tokens create --private-key file:///path/to/my-private.key --subject test-user
# Detail information: http://pulsar.apache.org/docs/en/security-token-admin/
jwt.broker.token.mode=
jwt.broker.secret.key=file:///path/broker-secret.key
jwt.broker.public.key=file:///path/pulsar/broker-public.key
jwt.broker.private.key=file:///path/broker-private.key

# bookie
bookie.host=http://localhost:8050
bookie.enable=false

redirect.scheme=http
redirect.host=localhost
redirect.port=9527

# Stats interval
# millisecond
insert.stats.interval=30000
# millisecond
clear.stats.interval=300000
init.delay.interval=0

# cluster data reload
cluster.cache.reload.interval.ms=60000

# Third party login options
third.party.login.option=

# Github login configuration
github.client.id=your-client-id
github.client.secret=your-client-secret
github.oauth.host=https://github.com/login/oauth/access_token
github.user.info=https://api.github.com/user
github.login.host=https://github.com/login/oauth/authorize
github.redirect.host=http://localhost:9527

user.access.token.expire=604800

# thymeleaf configuration for third login.
spring.thymeleaf.cache=false
spring.thymeleaf.prefix=classpath:/templates/
spring.thymeleaf.check-template-location=true
spring.thymeleaf.suffix=.html
spring.thymeleaf.encoding=UTF-8
spring.thymeleaf.servlet.content-type=text/html
spring.thymeleaf.mode=HTML5

# default environment configuration
default.environment.name=
default.environment.service_url=

# enable tls encryption
# keytool -import -alias test-keystore -keystore ca-certs -file certs/ca.cert.pem
tls.enabled=false
tls.keystore=keystore-file-path
tls.keystore.password=keystore-password
tls.hostname.verifier=false
tls.pulsar.admin.ca-certs=ca-client-path

# support peek message, default false
pulsar.peek.message=false
```
- /volume5/storage/docker-data/pulsar-manager/conf/nginx.conf
```text
server {
    listen       9527;
    server_name  0.0.0.0;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    location /admin {
      proxy_pass http://localhost:7750;
    }

    location /pulsar-manager {
      proxy_pass http://localhost:7750;
    }

    location /lookup {
      proxy_pass http://localhost:7750;
    }

    location /bkvm {
      proxy_pass http://localhost:7750;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

# docker-compose
```shell
docker-compose --project-name pulsar-manager --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.pulsar-manager.service: pulsar-manager
  traefik.http.services.pulsar-manager.loadbalancer.server.port: 9527

services:

  pulsar-manager:
    image: registry.czy21-internal.com/library/pulsar-manager
    container_name: pulsar-manager
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "9527"
    volumes:
      - /volume1/storage/docker-data/pulsar-manager/log/web/:/var/log/nginx/
      - /volume1/storage/docker-data/pulsar-manager/log/api/:/log/
    environment:
      SPRING_CONFIGURATION_FILE: /opt/pulsar-manager/application.properties
      JAVA_ARGS: "
      --spring.datasource.driver-class-name=org.postgresql.Driver
      --spring.datasource.url=jdbc:postgresql://192.168.2.18:5432/pulsar_manager?user=postgres&password=***REMOVED***
      --spring.datasource.initialization-mode=NEVER
      "



```