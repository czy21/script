#!/bin/bash

tmp_generate={{ param_role_path }}/___temp/generate
tmp_ca={{ param_role_path }}/___temp/demoCA

mkdir -p ${tmp_generate} ${tmp_ca}/{certs,newcerts,crl,private}

touch ${tmp_ca}/index.txt
echo "01" > ${tmp_ca}/serial

conf_file={{ param_role_path }}/conf

openssl_cnf=${conf_file}/openssl.cnf
openssl_ext=${conf_file}/openssl.ext

ca_crt_file=${conf_file}/ca.crt
ca_key_file=${conf_file}/ca.key

openssl genrsa -out ${tmp_generate}/server.key 4096 && openssl req -new -key ${tmp_generate}/server.key -out ${tmp_generate}/server.csr -config ${openssl_cnf} -nodes -subj "/C=CN/ST=SH/L=SH/O=czy/OU=czy/CN=server.cluster.com"

openssl ca -in ${tmp_generate}/server.csr -out ${tmp_generate}/server.crt -cert ${ca_crt_file} -keyfile ${ca_key_file} -config ${openssl_cnf} -extfile ${openssl_ext}