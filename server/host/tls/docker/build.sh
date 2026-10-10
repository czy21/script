#!/bin/bash

ca_key_path={{ param_role_tmp_path }}/ca/ca.key
ca_crt_path={{ param_role_tmp_path }}/ca/ca.crt

# server
for t in {{ param_docker_host_ips | join (" ")}};do
  t_dir={{ param_role_build_path }}/$t
  mkdir -p $t_dir

  openssl genrsa -out $t_dir/server.key 4096
  openssl req -subj "/CN=server" -new -key $t_dir/server.key -out $t_dir/server.csr
  printf "subjectAltName = DNS:localhost,IP:127.0.0.1,IP:$t\nextendedKeyUsage = serverAuth\n" > $t_dir/extfile.cnf
  openssl x509 -req -days {{ param_docker_tls_days }} -in $t_dir/server.csr -CA ${ca_crt_path} -CAkey ${ca_key_path} -CAcreateserial -out $t_dir/server.crt -extfile $t_dir/extfile.cnf
done

# client
client_dir={{ param_role_build_path }}/client
mkdir -p $client_dir
openssl genrsa -out $client_dir/client.key 4096
openssl req -subj '/CN=client' -new -key $client_dir/client.key -out $client_dir/client.csr
printf "extendedKeyUsage = clientAuth\n" > $client_dir/extfile.cnf
openssl x509 -req -days {{ param_docker_tls_days }} -in $client_dir/client.csr -CA ${ca_crt_path} -CAkey ${ca_key_path} -CAcreateserial -out $client_dir/client.crt -extfile $client_dir/extfile.cnf