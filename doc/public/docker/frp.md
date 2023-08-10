
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/frp --file Dockerfile . --pull
```
```dockerfile
FROM alpine:3.11
ARG FRP_VERSION=0.34.2
WORKDIR /root/
COPY ./___temp/ .

RUN mkdir -p /usr/local/frp/conf/
RUN tar -zxvf frp_${FRP_VERSION}_linux_amd64.tar.gz --strip-components 1 -C /usr/local/frp/

VOLUME /usr/local/frp/conf/
ENTRYPOINT /usr/local/frp/frps -c /usr/local/frp/conf/frps.ini
```
## conf
- /volume5/storage/docker-data/frp/conf/frps.ini
```text
[common]
bind_port = 7000
vhost_http_port = 80
subdomain_host = frp.czy-app.com

token = cb5e0942-62b2-4578-a32f-3fd17444db26

dashboard_port = 7500
dashboard_user = admin
dashboard_pwd = czy.1106
```
## docker-compose
```bash
docker-compose --project-name frp --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  frp:
    build:
      context: /compose/frp/
      dockerfile: /compose/frp/Dockerfile
    image: frp:1.0.0
    container_name: frp
    privileged: true
    user: root
    ports:
      - 7000:7000
    volumes:
      - /frp/:/usr/local/frp/conf/


```