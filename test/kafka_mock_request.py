#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


def publish():
    r = requests.post(url="http://127.0.0.1:8075/user/publish",
                      data=json.dumps({'message': '1'}),
                      headers={'Content-Type': 'application/json'})
    print(r)


if __name__ == '__main__':
    publish()
