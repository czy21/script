#!/bin/bash
set -e

sudo tee /etc/yum.repos.d/mysql.repo << EOF
[mysql-{{ param_db_mysql_minor_version }}-community]
name=MySQL {{ param_db_mysql_minor_version }} Community Server
baseurl=http://repo.mysql.com/yum/mysql-{{ param_db_mysql_minor_version }}-community/el/\$releasever/\$basearch/
enabled=1
gpgcheck=1
gpgkey=https://repo.mysql.com/RPM-GPG-KEY-mysql-2023
EOF

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/yum.repos.d/mysql.repo /etc/yum.repos.d/mysql.repo.bak
  sed -e "s|http://repo.mysql.com/yum|https://{{ param_mirror_raw }}/mysql/yum|g" /etc/yum.repos.d/mysql.repo.bak | sudo tee /etc/yum.repos.d/mysql.repo
fi

sudo yum -y install mysql-community-server-{{ param_db_mysql_patch_version }}
sudo systemctl daemon-reload && sudo systemctl enable mysqld && sudo systemctl restart mysqld