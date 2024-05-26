#!/bin/bash

sudo mkdir -p /usr/local/lib/docker/cli-plugins/
sudo curl -L "https://github.com/docker/compose/releases/download/v{{ param_compose_version }}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
sudo ln -sf /usr/local/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose