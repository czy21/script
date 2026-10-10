#!/bin/bash
set -e

conf_file={{ param_role_out_path }}/conf

openssl_cnf=${conf_file}/openssl.cnf
openssl_ext=${conf_file}/openssl.ext

ca_key_path={{ param_role_tmp_path }}/ca/ca.key
ca_crt_path={{ param_role_tmp_path }}/ca/ca.crt

generate_path={{ param_role_build_path }}/generate
demo_ca_path={{ param_role_build_path }}/demoCA

mkdir -p ${generate_path}
mkdir -p ${demo_ca_path}/{certs,newcerts,crl,private}

touch ${demo_ca_path}/index.txt
echo "01" > ${demo_ca_path}/serial

if [ ! -f "${ca_key_path}" ];then
  mkdir -p {{ param_role_build_path }}/ca
  ca_key_path={{ param_role_build_path }}/ca/ca.key
  ca_crt_path={{ param_role_build_path }}/ca/ca.crt
  openssl req -new -x509 -newkey rsa:4096 -keyout ${ca_key_path} -out ${ca_crt_path} -config ${openssl_cnf} -days {{ param_ssl_generate_ca_days }} -nodes -subj "{{ param_ssl_generate_ca_subj }}"
fi

openssl genrsa -out ${generate_path}/{{ param_ssl_generate_domain }}.key 2048
openssl req -new -key ${generate_path}/{{ param_ssl_generate_domain }}.key -out ${generate_path}/{{ param_ssl_generate_domain }}.csr -config ${openssl_cnf} -nodes -subj "{{ param_ssl_generate_subject }}/CN={{ param_ssl_generate_domain }}"
openssl ca -batch -notext -in ${generate_path}/{{ param_ssl_generate_domain }}.csr -out ${generate_path}/{{ param_ssl_generate_domain }}.crt -cert ${ca_crt_path} -keyfile ${ca_key_path} -config ${openssl_cnf} -extfile ${openssl_ext}

cat ${generate_path}/{{ param_ssl_generate_domain }}.crt ${ca_crt_path} > ${generate_path}/{{ param_ssl_generate_domain }}.pem

openssl base64 -A -in ${generate_path}/{{ param_ssl_generate_domain }}.key -out ${generate_path}/{{ param_ssl_generate_domain }}.key.base64
openssl base64 -A -in ${generate_path}/{{ param_ssl_generate_domain }}.crt -out ${generate_path}/{{ param_ssl_generate_domain }}.crt.base64
openssl base64 -A -in ${generate_path}/{{ param_ssl_generate_domain }}.pem -out ${generate_path}/{{ param_ssl_generate_domain }}.pem.base64
