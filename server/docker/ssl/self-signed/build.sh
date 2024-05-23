#!/bin/bash
set -e
tmp_generate={{ param_role_temp_path }}/generate
tmp_demo_ca={{ param_role_temp_path }}/demoCA
tmp_ca={{ param_role_temp_path }}/ca

mkdir -p \
${tmp_generate} \
${tmp_demo_ca}/certs \
${tmp_demo_ca}/newcerts \
${tmp_demo_ca}/crl \
${tmp_demo_ca}/private

touch ${tmp_demo_ca}/index.txt
echo "01" > ${tmp_demo_ca}/serial

conf_file={{ param_role_output_path }}/conf

openssl_cnf=${conf_file}/openssl.cnf
openssl_ext=${conf_file}/openssl.ext

openssl genrsa -out ${tmp_generate}/{{ param_ssl_generate_domain }}.key 2048
openssl req -new -key ${tmp_generate}/{{ param_ssl_generate_domain }}.key -out ${tmp_generate}/{{ param_ssl_generate_domain }}.csr -config ${openssl_cnf} -nodes -subj "/C=CN/ST=SH/L=SH/O=Home/OU=IT/CN={{ param_ssl_generate_domain }}"
openssl ca -batch -notext -in ${tmp_generate}/{{ param_ssl_generate_domain }}.csr -out ${tmp_generate}/{{ param_ssl_generate_domain }}.crt -cert ${tmp_ca}/ca.crt -keyfile ${tmp_ca}/ca.key -config ${openssl_cnf} -extfile ${openssl_ext}

openssl base64 -A -in ${tmp_generate}/{{ param_ssl_generate_domain }}.key -out ${tmp_generate}/{{ param_ssl_generate_domain }}.key.base64
openssl base64 -A -in ${tmp_generate}/{{ param_ssl_generate_domain }}.crt -out ${tmp_generate}/{{ param_ssl_generate_domain }}.crt.base64