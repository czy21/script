#!/usr/bin/env python
import docker
from docker import errors

client = docker.from_env()
app_network_name = "jenkins_default"
try:
    app_network = client.api.inspect_network(app_network_name)
except errors.NotFound:
    print("创建", app_network_name)

else:
    print("存在", app_network_name)

app_network_containers = [c["Name"] for c in app_network["Containers"].values()]

print("sss")
# for item in client.networks.list():
#     print(item)
