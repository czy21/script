#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kafka import KafkaProducer

bootstrap_servers = ['192.168.110.140:19092']
topic_name = 'person'

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
producer.send(topic_name, b'')
producer.flush()
