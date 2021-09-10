#!/bin/bash
set -e

dir=$(cd "$(dirname "$0")"; pwd)
app_name="$(basename ${dir})"
values_yaml=${dir}/values.yaml

if test -z "$(helm repo list | grep 'hashicorp' | awk '{print $1}')"; then
  helm repo add hashicorp https://helm.releases.hashicorp.com
fi
helm install ${app_name} hashicorp/consul --namespace ops --values ${values_yaml}