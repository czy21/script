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
sudo kubeadm init phase certs etcd-ca --kubernetes-version {{ param_k8s_version }}

for i in "${!HOSTS[@]}"; do
  HOST=${HOSTS[$i]}
  NAME=${NAMES[$i]}
  HOST_DIR=${DIR}/${HOST}
  KUBEADM_CFG=${HOST_DIR}/kubeadm-config.yaml
  mkdir -p ${HOST_DIR}
  cat << EOF > ${KUBEADM_CFG}
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
   sudo kubeadm init phase certs etcd-server --config=${KUBEADM_CFG}
   sudo kubeadm init phase certs etcd-peer --config=${KUBEADM_CFG}
   sudo kubeadm init phase certs etcd-healthcheck-client --config=${KUBEADM_CFG}
   sudo kubeadm init phase certs apiserver-etcd-client --config=${KUBEADM_CFG}
   sudo cp -R /etc/kubernetes/pki ${HOST_DIR}
   sudo find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete
   if [ $i == 0 ]; then
     sudo cp -R ${HOST_DIR}/pki ${DIR}
   else
     sudo find ${HOST_DIR}/pki -name ca.key -type f -delete
   fi
   uid=$(id -u)
   sudo chown -R ${uid}:${uid} ${DIR}
done

sh -c 'cd {{ param_remote_role_path }} && tar -pzcvf {{ param_k8s_etcd_cluster_name }}.tar.gz {{ param_k8s_etcd_cluster_name }}'
rm -rf ${DIR}