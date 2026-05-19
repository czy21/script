## Create User
```sql
drop user if exists 'admin'@'localhost';
drop user if exists 'admin'@'%';
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY '<password>';
GRANT ALL ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;

CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY '<password>';
GRANT ALL ON *.* TO 'admin'@'%' WITH GRANT OPTION;

-- 创建xx管理员账号
CREATE USER IF NOT EXISTS 'xxadmin'@'%' IDENTIFIED BY '<pasword>';
--- 分配xx管理员账号权限
GRANT all ON `xx\_%`.* TO 'xxadmin'@'%';
-- 创建xx开发账号
CREATE USER IF NOT EXISTS 'xxdev'@'%' IDENTIFIED BY '<pasword>';
--- 分配xx开发账号权限
GRANT Create Temporary Tables, Create View,Delete,Event, Execute, Grant Option, Index, Insert, Lock Tables, References, SELECT,Show View, Trigger, Update ON `xx\_%`.* TO 'xxdev'@'%';
--- 创建nacos账号
CREATE USER IF NOT EXISTS 'nacos'@'%' IDENTIFIED BY '<pasword>';
GRANT all on `nacos`.* TO 'nacos'@'%';
--- 创建xxl_job账号
CREATE USER IF NOT EXISTS 'xxl_job'@'%' IDENTIFIED BY '<pasword>';
GRANT all on `xxl_job`.* TO 'xxl_job'@'%';
```

## Master Slave
```sql
-- create slave user on master
CREATE USER 'slave'@'192.168.20.%' IDENTIFIED BY '';
GRANT REPLICATION SLAVE ON *.* TO 'slave'@'192.168.20.%';
FLUSH PRIVILEGES;
show master status\G;
-- connect to master on slave
change master to master_host='192.168.20.12',master_user='slave',master_password='',master_log_file='mysql-bin.000003',master_log_pos=849;
```
## Query
```shell
# show user databases
mysql -uroot -p<password> --skip-column-names -s -e 'SHOW DATABASES WHERE `Database` NOT IN ("mysql", "performance_schema","information_schema","sys")' | xargs
```
## Backup
```shell
# to sql file
docker run --rm -i mysql:8.0.43 mysqldump --default-character-set=utf8mb4 -h127.0.0.1 -uroot -p<password> --databases <databases> > xxx.sql
# to zip file
docker run --rm -i mysql:8.0.43 mysqldump --default-character-set=utf8mb4 -h127.0.0.1 -uroot -p<password> --databases <databases> | gzip > xxx.gz
```
## Restore
```shell
# from sql file
docker run --rm -i mysql:8.0.43 mysql --default-character-set=utf8mb4 -h127.0.0.1 -uroot -p<password> < xxx.sql
# from zip file
gunzip -c xxx.gz | docker run --rm -i mysql:8.0.43 mysql --default-character-set=utf8mb4 -h127.0.0.1 -uroot -p<password>
```