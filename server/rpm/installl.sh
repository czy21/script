#!/bin/bash

dir=$(cd "$(dirname "$0")"; pwd)/
dir=$dir/___temp

mysql_version="8.0.21-1.el8"
mssql_version="17.6.1.1-1"
mongo_version="rhel80-4.4.1"
neo4j_version="4.1.2-1"

# mysql
sudo rpm -ivh $dir/mysql/mysql-community-common-${mysql_version}.x86_64.rpm
sudo rpm -ivh $dir/mysql/mysql-community-libs-${mysql_version}.x86_64.rpm
sudo rpm -ivh $dir/mysql/mysql-community-client-${mysql_version}.x86_64.rpm

# mssql
sudo yum localinstall $dir/mssql/msodbcsql17-${mssql_version}.x86_64.rpm
sudo yum localinstall $dir/mssql/mssql-tools-${mssql_version}.x86_64.rpm

# mongo
sudo tar -zxvf $dir/mongo/mongodb-linux-x86_64-${mongo_version}.tgz -C /opt/

# cypher
sudo rpm -ivh $dir/neo4j/cypher-shell-${neo4j_version}.noarch.rpm

# must use root login and exec
# echo 'export PATH="$PATH:/opt/mssql-tools/bin:"' >> /etc/bashrc

# echo 'export PATH="$PATH:/opt/mongodb-linux-x86_64-rhel80-4.4.1/bin:"' >> /etc/bashrc