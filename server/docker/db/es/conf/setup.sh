#!/bin/bash

for ((i=1;i<={{ param_db_es_cluster_replicas }};i++));do
 data_node_dir=/usr/share/elasticsearch/data/${i}
 mkdir -p ${data_node_dir} && chown -R 1000:0 ${data_node_dir}
done

cert_path={{ param_db_es_target_cert_path }}

echo "Creating CA";
bin/elasticsearch-certutil ca --silent --pem -out ${cert_path}/ca.zip;
unzip -n ${cert_path}/ca.zip -d ${cert_path};

echo "Creating cert";
bin/elasticsearch-certutil cert --ca-cert ${cert_path}/ca/ca.crt --ca-key ${cert_path}/ca/ca.key --silent --pem --in config/instance.yml -out ${cert_path}/cert.zip;
unzip -n ${cert_path}/cert.zip -d ${cert_path}/

rm -rf ${cert_path}/ca.zip ${cert_path}/cert.zip
chown -R root:root ${cert_path}

echo "Waiting for Elasticsearch availability";
until curl -s http://{{ param_db_es_first_node_name }}:9200 | grep -q "missing authentication credentials"; do sleep 30; done;

echo "All done!";