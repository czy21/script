#!/bin/bash
set -e

sudo tee /etc/yum.repos.d/mongo.repo << EOF
[mongodb-org-8.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/8.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://pgp.mongodb.com/server-8.0.asc
EOF

sudo yum -y install mongodb-org
sudo systemctl daemon-reload && sudo systemctl restart mongod && sudo systemctl enable mongod