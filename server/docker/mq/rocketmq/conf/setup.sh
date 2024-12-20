#!/bin/bash

for i in $(seq 1 {{ param_mq_rocket_cluster_replicas }});do
 broker_data_dir=/data/${i}
 broker_conf=${broker_data_dir}/broker.conf
 mkdir -p ${broker_data_dir}
 tee ${broker_conf} << EOF
brokerClusterName = {{ param_mq_rocket_cluster_name }}
brokerName = rocketmq-broker-${i}
brokerId = 0
deleteWhen = 04
fileReservedTime = 48
brokerRole = ASYNC_MASTER
flushDiskType = ASYNC_FLUSH
EOF
done
echo "All done!";