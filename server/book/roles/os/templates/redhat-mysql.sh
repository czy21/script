#!/bin/bash
set -e

sudo tee /etc/yum.repos.d/mysql.repo << EOF
[mysql80-community]
name=MySQL 8.0 Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/\$releasever/\$basearch/
enabled=1
gpgcheck=1
gpgkey=https://repo.mysql.com/RPM-GPG-KEY-mysql-2023
EOF

sudo yum -y install mysql-community-server
sudo systemctl daemon-reload && sudo systemctl restart mysqld && sudo systemctl enable mysqld