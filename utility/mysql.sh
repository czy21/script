#!/bin/bash

wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-common-8.0.21-1.el8.x86_64.rpm
sudo rpm -ivh mysql-community-common-8.0.21-1.el8.x86_64.rpm

wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-libs-8.0.21-1.el8.x86_64.rpm
sudo rpm -ivh mysql-community-libs-8.0.21-1.el8.x86_64.rpm

wget https://cdn.mysql.com//Downloads/MySQL-8.0/mysql-community-client-8.0.21-1.el8.x86_64.rpm
sudo rpm -ivh mysql-community-client-8.0.21-1.el8.x86_64.rpm