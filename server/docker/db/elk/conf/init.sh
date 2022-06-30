#!/bin/bash

for ((i=1;i<={{ param_db_es_cluster_replicas }};i++));do
 data_node_dir=/usr/share/elasticsearch/data/${i}
 mkdir -p ${data_node_dir} && chown -R 1000:0 ${data_node_dir}
done

cert_dir=/usr/share/elasticsearch/config/cert

args="--silent --pem"
if [ -f ${cert_dir}/ca/ca.crt ] && [ -f ${cert_dir}/ca/ca.key ]; then
  args+=" --ca-cert ${cert_dir}/ca/ca.crt --ca-key ${cert_dir}/ca/ca.key"
else
  args+=" --keep-ca-key"
fi;
echo -e ${args}
rm -rf ${cert_dir}/bundle.zip
bin/elasticsearch-certutil cert ${args} --in config/instance.yml -out ${cert_dir}/bundle.zip && unzip -n ${cert_dir}/bundle.zip -d ${cert_dir}/
chown -R 1000:0 ${cert_dir}