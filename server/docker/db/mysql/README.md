## Master Slave
```sql
-- create slave user on master
CREATE USER 'slave'@'192.168.2.%' IDENTIFIED BY '';
GRANT REPLICATION SLAVE ON *.* TO 'slave'@'192.168.2.%';
FLUSH PRIVILEGES;
show master status\G;
-- connect to master on slave
change master to master_host='192.168.2.12',master_user='slave',master_password='',master_log_file='mysql-bin.000003',master_log_pos=849;
```
## Backup
```shell
docker exec mysql sh -c 'exec mysqldump --databases <databases> -uroot -p<password>' > /volume1/storage/all-databases.sql
# show user databases
mysql -uroot -p<password> --skip-column-names -s -e 'SHOW DATABASES WHERE `Database` NOT IN ("mysql", "performance_schema", "sys")' | xargs
```
## Restore
```shell
docker exec -i mysql sh -c 'exec mysql -uroot -p<password>' < /volume1/storage/all-databases.sql
```