#!/usr/bin/env bash

set -e

sudo mkdir -p /data/volumes/jenkins/

sudo tee /data/volumes/jenkins/hudson.model.UpdateCenter.xml <<-'EOF'
<?xml version='1.1' encoding='UTF-8'?>
<sites>
  <site>
    <id>default</id>
    <url>https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json</url>
  </site>
</sites>
EOF