#!/bin/bash
set -e

sudo apt-get update -y
podman_version=`sudo apt-cache madison podman | awk '{ print $3 }' | grep "{{ param_podman_version }}" | head -n 1`
podman_compose_version=`sudo apt-cache madison podman-compose | awk '{ print $3 }' | grep "{{ param_podman_compose_version }}" | head -n 1`
sudo apt-get -y install podman=${podman_version} podman-compose=${podman_compose_version} 