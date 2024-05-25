#!/bin/bash

curl -L "https://github.com/docker/compose/releases/download/v{{ param_global_compose_version }}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/lib/docker/cli-plugins/docker-compose
chmod +x /usr/lib/docker/cli-plugins/docker-compose
ln -sf /usr/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose