#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://www.mongodb.org/static/pgp/server-{{ param_db_mongo_minor_version }}.asc -o /etc/apt/keyrings/mongo.asc
sudo chmod a+r /etc/apt/keyrings/mongo.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/mongo.asc] https://repo.mongodb.org/apt/{{ param_ansible_distribution }} $(lsb_release -cs)/mongodb-org/{{ param_db_mongo_minor_version }} multiverse" | sudo tee /etc/apt/sources.list.d/mongo.list

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/apt/sources.list.d/mongo.list /etc/apt/sources.list.d/mongo.list.bak
  sed -e "s|https://repo.mongodb.org/apt|https://{{ param_mirror_raw }}/mongo/apt|g" /etc/apt/sources.list.d/mongo.list.bak | sudo tee /etc/apt/sources.list.d/mongo.list
fi

sudo apt-get -y update
mongo_version=`sudo apt-cache madison mongodb-org | awk '{ print $3 }' | grep "{{ param_db_mongo_patch_version }}" | head -n 1`
sudo apt-get -y install mongodb-org=${mongo_version}
sudo systemctl daemon-reload && sudo systemctl enable mongod && sudo systemctl restart mongod