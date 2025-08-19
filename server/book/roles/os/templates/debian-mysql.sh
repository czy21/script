#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://repo.mysql.com/RPM-GPG-KEY-mysql-2023 -o /etc/apt/keyrings/mysql.asc
sudo chmod a+r /etc/apt/keyrings/mysql.asc

echo "deb [signed-by=/etc/apt/keyrings/mysql.asc] http://repo.mysql.com/apt/{{ param_ansible_distribution }} $(lsb_release -cs) mysql-8.0 mysql-tools" | sudo tee /etc/apt/sources.list.d/mysql.list

sudo apt-get -y update
sudo apt-get -y install mysql-server
sudo systemctl daemon-reload && sudo systemctl restart mysql-server && sudo systemctl enable mysql-server