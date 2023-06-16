# guide
```bash
# https://docs.azure.cn/zh-cn/articles/azure-operations-guide/application-gateway/aog-application-gateway-howto-create-self-signed-cert-via-openssl
```

# openssl.ext
```ini
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName=@alt_names

[ alt_names ]
DNS.1=domain.com
DNS.2=*.domain.com
```

```shell
# self-signed ca
rm -rf ~/ssl/demoCA ~/ssl/server.* && mkdir -p ~/ssl/demoCA/{certs,newcerts,crl,private} && cd ~/ssl/ && touch demoCA/index.txt && echo "01" > demoCA/serial && sudo cp /etc/ssl/openssl.cnf ~/ssl/openssl.cnf
# -nodes: no password
openssl req -new -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -config openssl.cnf -days 365 -nodes -subj "/C=CN/ST=SH/L=SH/O=czy/OU=czy/CN=Home Root CA"

# client
openssl genrsa -out client.key 4096 && openssl req -new -key client.key -out client.csr -config openssl.cnf -nodes -subj "/C=CN/ST=SH/L=SH/O=Home/OU=IT/CN=domain.com"
openssl ca -in client.csr -out client.crt -cert ca.crt -keyfile ca.key -config openssl.cnf -extfile openssl.ext
# 
```