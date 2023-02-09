```sql
-- create slave user on master
CREATE USER 'slave'@'192.168.2.%' IDENTIFIED BY '';
GRANT REPLICATION SLAVE ON *.* TO 'slave'@'192.168.2.%';
FLUSH PRIVILEGES;
show master status\G;
-- connect to master on slave
change master to master_host='192.168.2.12',master_user='slave',master_password='',master_log_file='mysql-bin.000003',master_log_pos=849;
```