#!/bin/bash

set -e

sudo mkdir -p /etc/mongo
sudo mkdir -p /var/lib/mongo
sudo touch /var/lib/mongo/mongod.log

sudo tee /etc/mongo/mongod.conf <<-'EOF'
# mongod.conf

# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# Where and how to store data.
storage:
  dbPath: /data/db
  journal:
    enabled: true
#  engine:
#  mmapv1:
#  wiredTiger:

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /data/configdb/mongod.log

# network interfaces
net:
  port: 27017
  bindIp: 0.0.0.0

# how the process runs
processManagement:
  timeZoneInfo: /usr/share/zoneinfo

#security:

#operationProfiling:

#replication:

#sharding:

## Enterprise-Only Options:

#auditLog:

#snmp:
EOF

sudo docker run -d -p 27017:27017 --name mongo-master \
 -v /etc/mongo/mongod.conf:/data/configdb/mongod.conf \
 -v /var/lib/mongo:/data/db \
 -v /var/lib/mongo/mongod.log:/data/configdb/mongod.log mongo:4.0 \
 --config /data/configdb/mongod.conf
