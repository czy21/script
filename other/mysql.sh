#!/bin/bash
# 备份数据库并压缩
mysqldump --databases erp --host=localhost --port=30572 --user=root --password=Czy.101048 | gzip -c > /d/Developer/JavaProject/erp/_temp/db_bak/mysql.gz



mysql --host=localhost --port=3306 --user=root --password=sasa -e "drop database if exists erp; create database if not exists erp default charset utf8 collate utf8_general_ci;"

gzip -c -d /d/Developer/JavaProject/erp/_temp/db_bak/mysql.gz | mysql --database=erp --default-character-set=utf8 --host=localhost --port=3306 --user=root --password=sasa