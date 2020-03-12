#!/bin/bash
# 备份数据库并压缩
mongodump.exe --host 127.0.0.1 --port 30701 --db erp --gzip --archive=/d/Developer/JavaProject/erp/_temp/db_bak/mongo.gz

# 还原数据库
mongorestore.exe --host 127.0.0.1 --port 30701 --db erp --gzip --archive=/d/Developer/JavaProject/erp/_temp/db_bak/mongo.gz

#ss