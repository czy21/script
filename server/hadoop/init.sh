#!/bin/bash
sudo docker rmi $(sudo docker images -f "dangling=true" -q)
sudo docker rm -f hadoop
sudo docker rmi hadoop:1.0.0
sudo docker build --no-cache --force-rm --tag hadoop:1.0.0 --file hadoop/Dockerfile ./hadoop
sudo docker run -d -p 6022:22 --name=hadoop --privileged=true hadoop:1.0.0