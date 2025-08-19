#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc -o /etc/apt/keyrings/mongo.asc
sudo chmod a+r /etc/apt/keyrings/mongo.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/mongo.asc] https://repo.mongodb.org/apt/{{ param_ansible_distribution }} $(lsb_release -cs)/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongo.list

sudo apt-get -y update
sudo apt-get -y install mongodb-org
sudo systemctl daemon-reload && sudo systemctl restart mongod && sudo systemctl enable mongod