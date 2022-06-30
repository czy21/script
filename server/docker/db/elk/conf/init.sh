#!/bin/bash

for ((i=1;i<={{ param_db_es_cluster_replicas }};i++));do
 data_node_dir=/usr/share/elasticsearch/data/${i}
 mkdir -p ${data_node_dir} && chown -R 1000:0 ${data_node_dir}
done

cert_path={{ param_db_es_target_cert_path }}

args="--silent --pem"
if [ -f ${cert_path}/ca/ca.crt ] && [ -f ${cert_path}/ca/ca.key ]; then
  args+=" --ca-cert ${cert_path}/ca/ca.crt --ca-key ${cert_path}/ca/ca.key"
else
  args+=" --keep-ca-key"
fi;
echo -e ${args}
rm -rf ${cert_path}/bundle.zip
bin/elasticsearch-certutil cert ${args} --in config/instance.yml -out ${cert_path}/bundle.zip && unzip -n ${cert_path}/bundle.zip -d ${cert_path}/
chown -R 1000:0 ${cert_path}