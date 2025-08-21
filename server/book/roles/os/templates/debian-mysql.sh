#!/bin/bash
set -e

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://repo.mysql.com/RPM-GPG-KEY-mysql-2023 -o /etc/apt/keyrings/mysql.asc
sudo chmod a+r /etc/apt/keyrings/mysql.asc

mysql_repo_version="{{ param_db_mysql_minor_version }}"

if [ "${mysql_repo_version}" = "8.4" ];then
  mysql_repo_version="${mysql_repo_version}-lts"
fi

echo "deb [signed-by=/etc/apt/keyrings/mysql.asc] http://repo.mysql.com/apt/{{ param_ansible_distribution }} $(lsb_release -cs) mysql-${mysql_repo_version} mysql-tools" | sudo tee /etc/apt/sources.list.d/mysql.list

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/apt/sources.list.d/mysql.list /etc/apt/sources.list.d/mysql.list.bak
  sed -e "s|http://repo.mysql.com/apt|https://{{ param_mirror_raw }}/mysql/apt|g" /etc/apt/sources.list.d/mysql.list.bak | sudo tee /etc/apt/sources.list.d/mysql.list
fi

sudo apt-get -y update
mysql_version=`sudo apt-cache madison mysql-server | awk '{ print $3 }' | grep "{{ param_db_mysql_patch_version }}" | head -n 1`
sudo apt-get -y install mysql-server=${mysql_version}
sudo systemctl daemon-reload && sudo systemctl enable mysql-server && sudo systemctl restart mysql-server