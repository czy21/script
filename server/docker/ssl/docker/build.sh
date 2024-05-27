#!/bin/bash

# server
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -passin pass:1121 -out ca.pem -subj "/C=CN/ST=SH/L=SH/O=Home/OU=IT/CN=server"
openssl genrsa -out server-key.pem 4096
openssl req -subj "/CN=server" -sha256 -new -key server-key.pem -out server.csr
echo subjectAltName = IP:192.168.2.12,IP:127.0.0.1 >> extfile.cnf
echo extendedKeyUsage = serverAuth >> extfile.cnf
openssl x509 -req -days 365 -sha256 -passin pass:1121 -in server.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -extfile extfile.cnf

# client
openssl genrsa -out client-key.pem 4096
openssl req -subj '/CN=client' -new -key client-key.pem -out client.csr
echo extendedKeyUsage = clientAuth > extfile-client.cnf
openssl x509 -req -days 365 -sha256 -passin pass:1121 -in client.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem -extfile extfile-client.cnf