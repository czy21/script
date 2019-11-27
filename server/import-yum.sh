#!/bin/bash

set -e

# mysql
sudo bash -c 'echo -e "
[mysql57-community]
name=MySQL 5.7 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/\$releasever/\$basearch/
enabled=1
gpgcheck=0
" > /etc/yum.repos.d/mysql57.repo'

# mongo
sudo bash -c 'echo -e "
[mongodb-org-4.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
" > /etc/yum.repos.d/mongodb-org-4.0.repo'

# nginx
sudo bash -c 'echo -e "
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/rhel/\$releasever/\$basearch/
gpgcheck=0
enabled=1" > /etc/yum.repos.d/nginx.repo'
