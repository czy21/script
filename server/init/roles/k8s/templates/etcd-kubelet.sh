#!/bin/bash
set -e

# {%- set initial_nodes=[] %}
# {% for t in vars['param_hosts'] %}
#  {{- initial_nodes.append('{0}=https://{1}:2380'.format(t.name,t.ip)) or '' }}
# {% endfor %}

HOSTS=({{ param_hosts | join(' ', attribute='ip') }})
NAMES=({{ param_hosts | join(' ', attribute='name') }})
CLUSTER="{{ initial_nodes | join(',') }}"

DIR=${HOME}/{{ param_remote_role_path }}/{{ param_k8s_etcd_cluster_name }}
PKI=${DIR}/pki
mkdir -p ${PKI}
kubeadm init phase certs etcd-ca --kubernetes-version {{ param_k8s_version }} --cert-dir ${PKI}

for i in "${!HOSTS[@]}"; do
  HOST=${HOSTS[$i]}
  NAME=${NAMES[$i]}
  HOST_DIR=${DIR}/${HOST}
  KUBE_CFG=${HOST_DIR}/kubeadm-config.yaml
  mkdir -p ${HOST_DIR}
  cat << EOF > ${KUBE_CFG}
---
apiVersion: "kubeadm.k8s.io/v1beta3"
kind: InitConfiguration
nodeRegistration:
  name: ${NAME}
  criSocket: "{{ param_cri_socket }}"
localAPIEndpoint:
  advertiseAddress: ${HOST}
---
apiVersion: "kubeadm.k8s.io/v1beta3"
kind: ClusterConfiguration
kubernetesVersion: "v{{ param_k8s_version }}"
imageRepository: "{{ param_registry_proxy_url }}"
certificatesDir: "${PKI}"
etcd:
  local:
    serverCertSANs:
      - "${HOST}"
    peerCertSANs:
      - "${HOST}"
    extraArgs:
      initial-cluster: {{ initial_nodes | join(',') }}
      initial-cluster-state: new
      name: ${NAME}
      listen-peer-urls: https://${HOST}:2380
      listen-client-urls: https://${HOST}:2379
      advertise-client-urls: https://${HOST}:2379
      initial-advertise-peer-urls: https://${HOST}:2380
EOF
   kubeadm init phase certs etcd-server --config=${KUBE_CFG}
   kubeadm init phase certs etcd-peer --config=${KUBE_CFG}
   kubeadm init phase certs etcd-healthcheck-client --config=${KUBE_CFG}
   kubeadm init phase certs apiserver-etcd-client --config=${KUBE_CFG}
   find ${DIR} -name kubeadm-config.yaml -type f -exec sed -i '/certificatesDir/d' {} \;
   cp -R ${PKI} ${HOST_DIR}
   find ${PKI} -not -name ca.crt -not -name ca.key -type f -delete
   if [ ${HOST} != ${HOSTS[0]} ]; then
     find ${HOST_DIR}/pki -name ca.key -type f -delete
   fi
done
cp -R ${DIR}/${HOSTS[0]}/pki ${DIR}