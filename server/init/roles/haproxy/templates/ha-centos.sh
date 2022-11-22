#!/bin/bash
set -e

sudo yum install -y keepalived haproxy
sudo systemctl enable keepalived haproxy --now