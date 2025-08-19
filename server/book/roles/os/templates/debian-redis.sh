#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://packages.redis.io/gpg -o /etc/apt/keyrings/redis.asc
sudo chmod a+r /etc/apt/keyrings/redis.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/redis.asc] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get -y update
sudo apt-get -y install redis-server
sudo systemctl daemon-reload && sudo systemctl restart redis-server && sudo systemctl enable redis-server