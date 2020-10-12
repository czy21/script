#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
container_name="jenkins"
sudo docker exec -i ${container_name} bash -c "
  yum -y install wget
  sudo mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
  wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
  sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
  yum clean all
  yum makecache
  yum -y install vim gcc epel-release zlib-devel bzip2-devel readline-devel sqlite-devel openssl-devel sudo

  wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-common-8.0.21-1.el8.x86_64.rpm
  rpm -ivh mysql-community-common-8.0.21-1.el8.x86_64.rpm

  wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-libs-8.0.21-1.el8.x86_64.rpm
  rpm -ivh mysql-community-libs-8.0.21-1.el8.x86_64.rpm

  wget https://cdn.mysql.com//Downloads/MySQL-8.0/mysql-community-client-8.0.21-1.el8.x86_64.rpm
  rpm -ivh mysql-community-client-8.0.21-1.el8.x86_64.rpm
"