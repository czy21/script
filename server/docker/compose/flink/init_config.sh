#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

sudo docker build --no-cache --force-rm --tag flink:1.0.0 --file $dir/image/Dockerfile $dir/image/