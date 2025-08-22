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