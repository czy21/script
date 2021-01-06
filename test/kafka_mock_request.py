#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests


def publish(max):
    for i in range(0, max):
        r = requests.post(url="http://127.0.0.1:8075/user/publish",
                          data=json.dumps({'message': (i + 1).__str__()}),
                          headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    publish(10)
