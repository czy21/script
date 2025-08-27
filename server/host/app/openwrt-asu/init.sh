#!/bin/bash

mkdir -p $HOME/{{ param_role_name }}
cp -rv {{ param_role_output_path }}/{podman-deploy.yml,.env} $HOME/{{ param_role_name }}
podman-compose -p {{ param_role_name }} -f $HOME/{{ param_role_name }}/podman-deploy.yml up --detach --build --remove-orphans --force-recreate