#!/bin/bash

for ((i=1;i<={{ param_mq_rocket_cluster_replicas }};i++));do
 node_conf_dir=/data/conf/${i}
 broker_conf=${node_conf_dir}/broker.conf
 mkdir -p ${node_conf_dir}
cat << EOF > ${broker_conf}
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