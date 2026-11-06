#!/bin/bash
set -e

sudo apt-get -y update
sudo apt-get -y install dnsmasq

sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved