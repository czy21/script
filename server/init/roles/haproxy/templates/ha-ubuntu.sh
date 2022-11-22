#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y keepalived haproxy
sudo apt-mark hold keepalived haproxy