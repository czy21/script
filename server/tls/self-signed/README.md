```shell
# self-signed ca
rm -rf ~/ssl/demoCA ~/ssl/server.* && mkdir -p ~/ssl/demoCA/{certs,newcerts,crl,private} && cd ~/ssl/ && touch demoCA/index.txt && echo "01" > demoCA/serial && sudo cp /etc/ssl/openssl.cnf ~/ssl/openssl.cnf
# -nodes: no password
openssl req -new -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -config openssl.cnf -days 3650 -nodes -subj "/C=CN/ST=SH/L=SH/O=Home/OU=IT/CN=Home Root CA"

# client; expire in 365days otherwise NET::ERR_CERT_VALIDITY_TOO_LONG
openssl genrsa -out client.key 4096 && openssl req -new -key client.key -out client.csr -config openssl.cnf -nodes -subj "/C=CN/ST=SH/L=SH/O=Home/OU=IT/CN=domain.com"
openssl ca -in client.csr -out client.crt -cert ca.crt -keyfile ca.key -config openssl.cnf -extfile openssl.ext
# 
```