## Generate CA
```shell
rm -rf ~/ssl/demoCA ~/ssl/server.* && mkdir -p ~/ssl/demoCA/{certs,newcerts,crl,private} && cd ~/ssl/ && touch demoCA/index.txt && echo "01" > demoCA/serial && sudo cp /etc/ssl/openssl.cnf ~/ssl/openssl.cnf
# -nodes: no password
openssl req -new -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -config openssl.cnf -days 3650 -nodes -subj "/C=CN/ST=SH/L=SH/O=Home/OU=IT/CN=Home Root CA"
```
## Expire in 365days otherwise NET::ERR_CERT_VALIDITY_TOO_LONG for broswer