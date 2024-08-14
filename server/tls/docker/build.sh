#!/bin/bash

tmp_ca={{ param_role_temp_path }}/ca

# server
for t in {{ param_docker_host_ips | join (" ")}};do
  pem_dir={{ param_role_temp_path }}/$t
  mkdir -p $pem_dir

  openssl genrsa -out $pem_dir/server.key 4096
  openssl req -subj "/CN=server" -new -key $pem_dir/server.key -out $pem_dir/server.csr
  echo "subjectAltName = IP:$t,IP:127.0.0.1\nextendedKeyUsage = serverAuth" > $pem_dir/extfile.cnf
  openssl x509 -req -days {{ param_docker_tls_days }} -in $pem_dir/server.csr -CA $tmp_ca/ca.crt -CAkey $tmp_ca/ca.key -CAcreateserial -out $pem_dir/server.crt -extfile $pem_dir/extfile.cnf
done

# client
client_dir={{ param_role_temp_path }}/client
mkdir -p $client_dir
openssl genrsa -out $client_dir/client.key 4096
openssl req -subj '/CN=client' -new -key $client_dir/client.key -out $client_dir/client.csr
echo "extendedKeyUsage = clientAuth" > $client_dir/extfile.cnf
openssl x509 -req -days {{ param_docker_tls_days }} -in $client_dir/client.csr -CA $tmp_ca/ca.crt -CAkey $tmp_ca/ca.key -CAcreateserial -out $client_dir/client.crt -extfile $client_dir/extfile.cnf