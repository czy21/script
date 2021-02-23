#!/bin/bash

set -e

dir=$(cd "$(dirname "$0")"; pwd)

container_names=("flink_jobmanager" "flink_taskmanager_1")

function cpLib() {
  for i in ${container_names[@]}
  do
    sudo docker exec -i ${i} bash -c "cp -r /opt/flink/usrlib/. /opt/flink/lib/"
  done
}

cpLib
sudo docker restart ${container_names[@]}