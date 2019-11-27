#!/bin/bash

set -e

# mongo
sudo yum -y install mongodb-org

# nginx
sudo yum -y install nginx

# mysql
sudo yum -y install mysql-community-server
sudo bash -c 'echo -e "
[client]
default-character-set=utf8
[mysql]
default-character-set=utf8
[mysqld]
character-set-server=utf8
default-storage-engine=INNODB
lower_case_table_names=1
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-output=FILE
general-log=1
general_log_file=\"general.log\"
slow-query-log=1
slow_query_log_file=\"slow.log\"
long_query_time=10
log-error=\"error.err\"
symbolic-links=0
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
[mysqld_safe]
default-character-set=utf8
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
" > /etc/my.cnf'
sudo service mysqld start
# sudo grep 'temporary password' /var/lib/mysql/error.err
# mysql -uroot -p
# ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';

# redis
# stop service redis stop
# start service redis start
sudo wget http://download.redis.io/releases/redis-5.0.3.tar.gz -O - | tar -zxvf - -C /usr/local/
sudo make MALLOC=libc -C /usr/local/redis-5.0.3
sudo make install -C /usr/local/redis-5.0.3/src
sudo mkdir /etc/redis
sudo cp /usr/local/redis-5.0.3/redis.conf /etc/redis/6379.conf
sudo sed -i -r "s/^\s*daemonize\s+no/daemonize yes/;s/^\s*# requirepass\s+foobared/requirepass team3059/;" /etc/redis/6379.conf
sudo cp /usr/local/redis-5.0.3/utils/redis_init_script /etc/init.d/redis
sudo sed -i "5i\# chkconfig: 2345 90 10\n# description: Redis is a persistent key-value database" /etc/init.d/redis
sudo chmod +x /etc/init.d/redis
sudo chkconfig redis on
sudo service redis start

# node
curl --location https://rpm.nodesource.com/setup_8.x | sudo bash -
sudo yum -y install nodejs
sudo wget https://dl.yarnpkg.com/rpm/yarn.repo -O /etc/yum.repos.d/yarn.repo
sudo yum -y install yarn
sudo yarn config set registry 'https://registry.npm.taobao.org'

