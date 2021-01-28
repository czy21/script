#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../.env.global

sudo mkdir -p ${GLOBAL_VOLUMES_DIR}/jenkins/

sudo tee ${GLOBAL_VOLUMES_DIR}/jenkins/hudson.model.UpdateCenter.xml <<-'EOF'
<?xml version='1.0' encoding='UTF-8'?>
<sites>
  <site>
    <id>default</id>
    <url>https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json</url>
  </site>
</sites>
EOF