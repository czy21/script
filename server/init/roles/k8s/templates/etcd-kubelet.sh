#!/bin/bash
set -e

CLUSTER=${HOME}/{{ param_remote_role_path }}/cluster
PKI=${CLUSTER}/pki
NODE=${CLUSTER}/node
mkdir -p ${PKI} ${NODE}
sudo kubeadm init phase certs etcd-ca --kubernetes-version {{ param_k8s_version }}
{% for t in vars['param_hosts'] %}
  IP={{ t.ip }}
  NAME={{ t.name }}
  IP_DIR=${NODE}/${IP}
  KUBEADM_CFG=${IP_DIR}/kubeadm-config.yaml
  mkdir -p ${IP_DIR}
  {%- set initial_nodes=[] %}
  {% for t in vars['param_hosts'] %}
     {{- initial_nodes.append('{0}=https://{1}:2380'.format(t.name,t.ip)) or '' }}
  {% endfor %}
  cat << EOF > ${KUBEADM_CFG}
---
apiVersion: "kubeadm.k8s.io/v1beta3"
kind: InitConfiguration
nodeRegistration:
    name: ${NAME}
localAPIEndpoint:
    advertiseAddress: ${IP}
nodeRegistration:
  criSocket: ""
---
apiVersion: "kubeadm.k8s.io/v1beta3"
kind: ClusterConfiguration
kubernetesVersion: "v{{ param_k8s_version }}"
etcd:
    local:
        serverCertSANs:
        - "${IP}"
        peerCertSANs:
        - "${IP}"
        extraArgs:
            initial-cluster: {{ initial_nodes | join(',') }}
            initial-cluster-state: new
            name: ${NAME}
            listen-peer-urls: https://${IP}:2380
            listen-client-urls: https://${IP}:2379
            advertise-client-urls: https://${IP}:2379
            initial-advertise-peer-urls: https://${IP}:2380
EOF
   sudo kubeadm init phase certs etcd-server --config=${KUBEADM_CFG}
   sudo kubeadm init phase certs etcd-peer --config=${KUBEADM_CFG}
   sudo kubeadm init phase certs etcd-healthcheck-client --config=${KUBEADM_CFG}
   sudo kubeadm init phase certs apiserver-etcd-client --config=${KUBEADM_CFG}
   sudo cp -R /etc/kubernetes/pki ${IP_DIR}
   sudo find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete
{% endfor %}

sh -c 'cd {{ param_remote_role_path }} && sudo tar -pzcvf cluster.tar.gz cluster'
sudo rm -rf ${CLUSTER}