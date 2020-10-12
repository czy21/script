#!/bin/bash

set -e

yum -y install wget
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
yum clean all
yum makecache
yum -y install vim gcc epel-release zlib-devel bzip2-devel readline-devel sqlite-devel openssl-devel make sudo

# pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
mkdir ~/.pyenv/cache