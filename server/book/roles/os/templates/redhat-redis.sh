#!/bin/bash
set -e

sudo yum -y install redis
sudo systemctl daemon-reload && sudo systemctl restart redis && sudo systemctl enable redis