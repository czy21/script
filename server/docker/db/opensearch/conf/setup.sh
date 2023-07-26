#!/bin/bash

for ((i=1;i<={{ param_db_opensearch_cluster_replicas }};i++));do
 data_node_dir=/usr/share/opensearch/data/${i}
 mkdir -p ${data_node_dir} && chown -R 1000:0 ${data_node_dir}
done

echo "Waiting for Opensearch availability";
until curl -s http://{{ param_db_opensearch_first_node_name }}:9200 | grep -q "{{ param_db_opensearch_first_node_name }}"; do sleep 30; done;

echo "All done!";