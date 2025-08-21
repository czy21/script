#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://packages.redis.io/gpg -o /etc/apt/keyrings/redis.asc
sudo chmod a+r /etc/apt/keyrings/redis.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/redis.asc] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/apt/sources.list.d/redis.list /etc/apt/sources.list.d/redis.list.bak
  sed -e "s|https://packages.redis.io/deb|https://{{ param_mirror_raw }}/redis/deb|g" /etc/apt/sources.list.d/redis.list.bak | sudo tee /etc/apt/sources.list.d/redis.list
fi

sudo apt-get -y update
redis_version=`sudo apt-cache madison redis-server | awk '{ print $3 }' | grep "{{ param_db_redis_version }}" | head -n 1`
sudo apt-get -y install redis-server=${redis_version} redis-tools=${redis_version}
sudo systemctl daemon-reload && sudo systemctl enable redis-server && sudo systemctl restart redis-server