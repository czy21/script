
## generate key
```shell
ssh-keygen -t rsa -b 4096 -m PEM -f ./keys/session_signing_key
ssh-keygen -t rsa -b 4096 -m PEM -f ./keys/tsa_host_key
ssh-keygen -t rsa -b 4096 -m PEM -f ./keys/worker_key
```