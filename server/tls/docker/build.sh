#!/bin/bash

tmp_ca={{ param_role_temp_path }}/ca

# server
for t in {{ param_docker_host_ips | join (" ")}};do
  t_dir={{ param_role_temp_path }}/$t
  mkdir -p $t_dir

  openssl genrsa -out $t_dir/server.key 4096
  openssl req -subj "/CN=server" -new -key $t_dir/server.key -out $t_dir/server.csr
  echo "subjectAltName = IP:$t,IP:127.0.0.1\nextendedKeyUsage = serverAuth" > $t_dir/extfile.cnf
  openssl x509 -req -days {{ param_docker_tls_days }} -in $t_dir/server.csr -CA $tmp_ca/ca.crt -CAkey $tmp_ca/ca.key -CAcreateserial -out $t_dir/server.crt -extfile $t_dir/extfile.cnf
done

# client
client_dir={{ param_role_temp_path }}/client
mkdir -p $client_dir
openssl genrsa -out $client_dir/client.key 4096
openssl req -subj '/CN=client' -new -key $client_dir/client.key -out $client_dir/client.csr
echo "extendedKeyUsage = clientAuth" > $client_dir/extfile.cnf
openssl x509 -req -days {{ param_docker_tls_days }} -in $client_dir/client.csr -CA $tmp_ca/ca.crt -CAkey $tmp_ca/ca.key -CAcreateserial -out $client_dir/client.crt -extfile $client_dir/extfile.cnf