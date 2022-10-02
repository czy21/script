#!/bin/bash

service ssh start

chmod 777 /data

exec "$@"