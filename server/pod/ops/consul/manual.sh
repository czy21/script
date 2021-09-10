#!/bin/bash
set -e

dir=$(cd "$(dirname "$0")"; pwd)
own_name=$(basename $(dirname "${dir}"))
app_name="$(basename ${dir})"
values_yaml=${dir}/values.yaml

if test -z "$(helm repo list | grep 'hashicorp' | awk '{print $1}')"; then
  helm repo add hashicorp https://helm.releases.hashicorp.com
fi
helm template hashicorp/consul --namespace ${own_name} --values ${values_yaml} > ${dir}/___temp/deploy.yaml