#!/bin/bash
set -e

IPV4S=({{ param_ansible_host_ipv4s | join(' ') }})
NAMES=({{ param_ansbile_host_names | join(' ') }})
CLUSTER="{{ param_ansible_host_ipv4s|zip(param_ansbile_host_names)|map('reverse')|map('format','{0}=https://{1}:2380')|join(',') }}"

DIR=${HOME}/{{ param_remote_role_path }}/{{ param_k8s_etcd_cluster_name }}
PKI=${DIR}/pki
mkdir -p ${PKI}
kubeadm init phase certs etcd-ca --kubernetes-version {{ param_k8s_version }} --cert-dir ${PKI}

for i in "${!IPV4S[@]}"; do
  IPV4=${IPV4S[$i]}
  NAME=${NAMES[$i]}
  IPV4_DIR=${DIR}/${IPV4}
  KUBE_CFG=${IPV4_DIR}/kubeadm-config.yaml
  mkdir -p ${IPV4_DIR}
  cat << EOF > ${KUBE_CFG}
---
apiVersion: "kubeadm.k8s.io/v1beta3"
kind: InitConfiguration
nodeRegistration:
  name: ${NAME}
  criSocket: "{{ param_cri_socket }}"
localAPIEndpoint:
  advertiseAddress: ${IPV4}
---
apiVersion: "kubeadm.k8s.io/v1beta3"
kind: ClusterConfiguration
kubernetesVersion: "v{{ param_k8s_version }}"
imageRepository: "{{ param_registry_proxy_url }}"
certificatesDir: "${PKI}"
etcd:
  local:
    serverCertSANs:
      - "${IPV4}"
    peerCertSANs:
      - "${IPV4}"
    extraArgs:
      initial-cluster: "${CLUSTER}"
      initial-cluster-state: new
      name: ${NAME}
      listen-peer-urls: https://${IPV4}:2380
      listen-client-urls: https://${IPV4}:2379
      advertise-client-urls: https://${IPV4}:2379
      initial-advertise-peer-urls: https://${IPV4}:2380
EOF
   kubeadm init phase certs etcd-server --config=${KUBE_CFG}
   kubeadm init phase certs etcd-peer --config=${KUBE_CFG}
   kubeadm init phase certs etcd-healthcheck-client --config=${KUBE_CFG}
   kubeadm init phase certs apiserver-etcd-client --config=${KUBE_CFG}
   find ${DIR} -name kubeadm-config.yaml -type f -exec sed -i '/certificatesDir/d' {} \;
   cp -R ${PKI} ${IPV4_DIR}
   find ${PKI} -not -name ca.crt -not -name ca.key -type f -delete
   if [ ${IPV4} != ${IPV4S[0]} ]; then
     find ${IPV4_DIR}/pki -name ca.key -type f -delete
   fi
done
cp -R ${DIR}/${IPV4S[0]}/pki ${DIR}