#!/bin/bash

set -e

sudo mkdir -p /etc/mysql/
sudo mkdir -p /var/lib/mysql

sudo tee /etc/mysql/mysql.cnf <<-'EOF'
[client]
default-character-set=utf8
[mysql]
default-character-set=utf8
EOF

sudo tee /etc/mysql/mysqld.cnf <<-'EOF'
[mysqld]
character-set-server=utf8
default-storage-engine=INNODB
lower_case_table_names=1
pid-file  = /var/run/mysqld/mysqld.pid
socket    = /var/run/mysqld/mysqld.sock
datadir   = /var/lib/mysql
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
log-output=FILE
general-log=1
general_log_file="general.log"
slow-query-log=1
slow_query_log_file="slow.log"
log-error="error.err"
long_query_time=10
symbolic-links=0
EOF

sudo docker run -d -p 3306:3306 --name mysql-master \
-v /var/lib/mysql:/var/lib/mysql \
-v /etc/mysql/mysql.cnf:/etc/mysql/conf.d/mysql.cnf \
-v /etc/mysql/mysqld.cnf:/etc/mysql/mysql.conf.d/mysqld.cnf \
-e MYSQL_ROOT_PASSWORD=Czy.101048 mysql:5.7