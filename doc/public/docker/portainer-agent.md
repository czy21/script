# dockerfile

# docker-compose
```yaml
version: "3.9"

services:
  portainer-agent:
    image: portainer/agent:2.15.1-alpine
    container_name: portainer-agent
    privileged: true
    expose:
      - "9001"
    ports:
      - "9001:9001"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: always
    deploy:
      mode: global
      placement:
        constraints:
          - 'node.platform.os == linux'
```