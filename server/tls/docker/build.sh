#!/bin/bash

tmp_ca={{ param_role_temp_path }}/ca

# server
for t in {{ param_docker_host_ips | join (" ")}};do
  pem_dir={{ param_role_temp_path }}/$t
  mkdir -p $pem_dir

  openssl genrsa -out $pem_dir/server-key.pem 4096
  openssl req -subj "/CN=server" -sha256 -new -key $pem_dir/server-key.pem -out $pem_dir/server.csr
  echo "subjectAltName = IP:$t,IP:127.0.0.1\nextendedKeyUsage = serverAuth" > $pem_dir/extfile.cnf
  openssl x509 -req -days 365 -sha256 -passin pass:{{ param_docker_host_ca_password }} \
    -in $pem_dir/server.csr -CA $tmp_ca/ca.pem -CAkey $tmp_ca/ca-key.pem -CAcreateserial \
    -out $pem_dir/server-cert.pem -extfile $pem_dir/extfile.cnf
done

# client
client_dir={{ param_role_temp_path }}/client
mkdir -p $client_dir
openssl genrsa -out $client_dir/client-key.pem 4096
openssl req -subj '/CN=client' -new -key $client_dir/client-key.pem -out $client_dir/client.csr
echo "extendedKeyUsage = clientAuth" > $client_dir/extfile.cnf
openssl x509 -req -days 365 -sha256 -passin pass:{{ param_docker_host_ca_password }} \
  -in $client_dir/client.csr -CA $tmp_ca/ca.pem -CAkey $tmp_ca/ca-key.pem -CAcreateserial \
  -out $client_dir/client-cert.pem -extfile $client_dir/extfile.cnf