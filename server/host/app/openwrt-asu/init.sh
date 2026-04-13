#!/bin/bash

mkdir -p /volume1/storage/docker-data/openwrt-asu/data/

cp -rv {{ param_role_output_path }}/key /volume1/storage/docker-data/openwrt-asu/data/

(
    cd {{ param_role_output_path }}
    podman-compose -p {{ param_role_name }} -f podman-deploy.yml up --detach --build --remove-orphans --force-recreate
) 