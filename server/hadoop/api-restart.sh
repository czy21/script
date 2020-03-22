#!/bin/bash
sudo docker rmi $(sudo docker images -f "dangling=true" -q)
sudo docker build --no-cache --force-rm --tag hadoop:1.0.0 --file hadoop/Dockerfile .
sudo docker rm -f hadoop && sudo docker rmi hadoop:1.0.0
sudo docker rm -f hadoop&&sudo docker run -d -p 6022:22 --name=hadoop --privileged=true hadoop:1.0.0

ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key
ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key