#!/usr/bin/env bash

set -e

sudo mkdir -p /data/config/mysql/conf.d/

sudo tee /data/config/mysql/conf.d/mysql.cnf <<-'EOF'
[client]
default-character-set=utf8mb4
[mysql]
default-character-set=utf8mb4
EOF

sudo tee /data/config/mysql/my.cnf <<-'EOF'
[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
default-time-zone = '+8:00'
secure-file-priv= NULL
symbolic-links=0
# Custom config should go here
!includedir /etc/mysql/conf.d/
EOF