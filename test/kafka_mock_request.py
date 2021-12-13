#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests


def publish(max):
    for i in range(0, max):
        r = requests.get(url="https://callcenter-api.meditrusthealth.cn:8999/api/getCalllogData?key=5aekiETS5845215sdfasED&starttime=2021-10-06 17:08:23&endtime=2021-12-06 17:08:23&page_index={}&page_size=2000".format(i))
        print(r.__sizeof__())
        print(i + 1, "次")


if __name__ == '__main__':
    publish(100)
