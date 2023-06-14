#!/bin/bash

tmp_generate={{ param_role_path }}/___temp/generate
tmp_demo_ca={{ param_role_path }}/___temp/demoCA
tmp_ca={{ param_role_path }}/___temp/ca

mkdir -p \
${tmp_generate} \
${tmp_demo_ca}/certs \
${tmp_demo_ca}/newcerts \
${tmp_demo_ca}/crl \
${tmp_demo_ca}/private

touch ${tmp_demo_ca}/index.txt
echo "01" > ${tmp_demo_ca}/serial

conf_file={{ param_role_path }}/conf

openssl_cnf=${conf_file}/openssl.cnf
openssl_ext=${conf_file}/openssl.ext

openssl genrsa -out ${tmp_generate}/server.key 4096
openssl req -new -key ${tmp_generate}/server.key -out ${tmp_generate}/server.csr -config ${openssl_cnf} -nodes -subj "/C=CN/ST=SH/L=SH/O=Home/OU=IT/CN=server.czy21.com"
openssl ca -in ${tmp_generate}/server.csr -out ${tmp_generate}/server.crt -cert ${tmp_ca}/ca.crt -keyfile ${tmp_ca}/ca.key -config ${openssl_cnf} -extfile ${openssl_ext}