#!/bin/bash
set -e

sudo tee /etc/yum.repos.d/mongo.repo << EOF
[mongodb-org-{{ param_db_mongo_minor_version }}]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/{{ param_db_mongo_minor_version }}/x86_64/
enabled=1
gpgcheck=1
gpgkey=https://pgp.mongodb.com/server-{{ param_db_mongo_minor_version }}.asc
EOF

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/yum.repos.d/mongo.repo /etc/yum.repos.d/mongo.repo.bak
  sed -e "s|https://repo.mongodb.org/yum|https://{{ param_mirror_raw }}/mongo/yum|g" /etc/yum.repos.d/mongo.repo.bak | sudo tee /etc/yum.repos.d/mongo.repo
fi

sudo yum -y install mongodb-org-{{ param_db_mongo_patch_version }}
sudo systemctl daemon-reload && sudo systemctl enable mongod && sudo systemctl restart mongod