#!/usr/bin/env python
import docker
from docker import errors
from compose import config
import logging

client = docker.from_env()
app_network_name = "jenkins_default"


def test_network():
    try:
        client.api.remove_image(app_network_name)
    except errors.NotFound:
        print("创建", app_network_name)

    else:
        print("存在", app_network_name)


def test_compose():
    config.find(".",)

print("sss")
