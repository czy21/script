# dockerfile
# conf
- /volume5/storage/docker-data/phpldapadmin/conf/config.yaml
```text
# Apache
PHPLDAPADMIN_SERVER_ADMIN: webmaster@example.org
PHPLDAPADMIN_SERVER_PATH: /phpldapadmin

# Self signed certificat will be generated
# if PHPLDAPADMIN_HTTPS is set to true and no certificat and key are provided.

# To use your custom certificat and key 2 options :
# - add them in service/phpldapadmin/assets/apache2/certs and build the image
# - or during docker run mount a data volume with those files to /container/service/phpldapadmin/assets/apache2/certs
PHPLDAPADMIN_HTTPS: false
PHPLDAPADMIN_HTTPS_CRT_FILENAME: phpldapadmin.crt
PHPLDAPADMIN_HTTPS_KEY_FILENAME: phpldapadmin.key
PHPLDAPADMIN_HTTPS_CA_CRT_FILENAME: ca.crt

PHPLDAPADMIN_TRUST_PROXY_SSL: false

# ssl-helper environment variables prefix
PHPLDAPADMIN_SSL_HELPER_PREFIX: phpldapadmin # ssl-helper first search config from PHPLDAPADMIN_SSL_HELPER_* variables, before SSL_HELPER_* variables.

PHPLDAPADMIN_LDAP_HOSTS:
  - 192.168.2.2:
      - server:
          - tls: false
      - login:
          - bind_id: cn=admin,dc=example,dc=com
  - 192.168.2.12:
      - server:
          - tls: false
      - login:
          - bind_id: cn=admin,dc=nodomain
  - 192.168.2.16:
      - server:
          - tls: false
      - login:
          - bind_id: cn=admin,dc=example,dc=com
```

# docker-compose
```shell
docker-compose --project-name phpldapadmin --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-label: &traefik-label
  traefik.enable: true
  traefik.http.routers.phpldapadmin.service: phpldapadmin
  traefik.http.services.phpldapadmin.loadbalancer.server.port: 80

services:

  phpldapadmin:
    image: osixia/phpldapadmin:0.9.0
    pull_policy: always
    container_name: phpldapadmin
    labels:
      <<: *traefik-label
    privileged: true
    user: root
    expose:
      - "80"
    volumes:
      - "/volume1/storage/docker-data/phpldapadmin/conf/config.yaml:/container/environment/01-custom/env.yaml"
      - "/volume1/storage/docker-data/phpldapadmin/data/:/var/www/phpldapadmin/"
    restart: always
```