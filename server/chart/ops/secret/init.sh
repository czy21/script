#!/bin/bash

cert_dir={{ param_role_path }}/cert

certs=$(find "$cert_dir" -mindepth 1 -maxdepth 1 -type d)

for t in $certs;do

  t_name=$(basename $t)

  t_crt=$t/${t_name}.cer
  t_key=$t/${t_name}.key

  t_crt_base64=$(openssl base64 -A -in $t_crt)
  t_key_base64=$(openssl base64 -A -in $t_key)
  
  kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
type: kubernetes.io/tls
metadata:
  name: ${t_name}-secret
  namespace: {{ param_namespace }}
data:
  tls.crt: ${t_crt_base64}
  tls.key: ${t_key_base64}
EOF
done