#!/bin/bash
set -e

sudo apt-get update -y
sudo apt-get install -y keepalived haproxy
sudo systemctl enable keepalived haproxy --now