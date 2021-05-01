#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)
source ${dir}/../../.env.global
container_name="jenkins"

sudo docker exec -i ${container_name} bash -c "
yum -y install wget
yum -y install vim sudo
dnf -y install python38
"