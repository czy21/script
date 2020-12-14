#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kafka import KafkaConsumer

bootstrap_servers = ['192.168.110.140:19092']
topic_name = 'person'

consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers)
for msg in consumer:
    print(msg)
