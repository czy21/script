#!/bin/bash

sudo curl -L "https://github.com/docker/compose/releases/download/v{{ param_global_compose_version }}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/libexec/docker/cli-plugins/docker-compose
sudo chmod +x /usr/libexec/docker/cli-plugins/docker-compose
sudo ln -sf /usr/libexec/docker/cli-plugins/docker-compose /usr/bin/docker-compose