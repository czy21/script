#!/usr/bin/env python
import docker

client = docker.from_env()

print("sss")
for item in client.networks.list():
    print(item)
