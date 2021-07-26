#!/bin/bash

set -e
dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global

sudo mkdir -p ${GLOBAL_VOLUMES_DIR}/hadoop/sys/fs/cgroup/