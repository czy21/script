#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)

sudo mkdir -p /data/volumes/kafka1/

sudo chown -R 1000:1000 /data/volumes/kafka1/