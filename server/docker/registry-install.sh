#!/bin/bash

set -e

docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e  REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  registry:2.7

sudo docker exec -i registry sh -c 'htpasswd -Bcb /auth/htpasswd chenzhaoyu chenzhaoyu'