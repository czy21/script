#!/bin/bash

for t in $(find "{{ param_role_path }}/cert" -mindepth 1 -maxdepth 1 -type d);do
  t_name=$(basename $t)

  t_crt=$t/${t_name}.crt
  t_key=$t/${t_name}.key

  kubectl create secret tls "${t_name}-secret" --cert="${t_crt}" --key="${t_key}" -n "{{ param_namespace }}" --dry-run=client -o yaml | kubectl apply -f -
done