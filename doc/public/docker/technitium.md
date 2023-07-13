# dockerfile

# docker-compose
```yaml
version: "3.9"

services:

  technitium-dns-server:
    image:  technitium/dns-server:latest
    container_name: technitium-dns-server
    hostname: technitium-dns-server
    privileged: true
    user: root
    ports:
      - "5380:5380"
      - "5302:53/tcp"
      - "5302:53/udp"
    volumes:
      - /volume1/storage/docker-data/technitium/data/:/etc/dns/config
    environment:
      DNS_SERVER_DOMAIN: dns-server
      DNS_SERVER_ADMIN_PASSWORD: "***REMOVED***"
```